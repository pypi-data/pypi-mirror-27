# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_nsg.py
@time: 2017/2/13 10:07
"""

from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.network.models import NetworkSecurityGroup
from azure.mgmt.network.models import SecurityRule
from msrestazure.azure_exceptions import CloudError

from op_resource_group import OPResourceGroup
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST, AZURE_STATUS_RES_EXIST, AZURE_INFO_NSG_EXIST, \
    AZURE_INFO_NSG_NOT_EXIST


class OPNSG(object):
    """azure nsg sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.network_client = NetworkManagementClient(credentials, subscription_id)
        self.nsg_client = self.network_client.network_security_groups

    def list_all(self):
        """list all nsgs"""
        try:
            result = self.nsg_client.list_all()
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_by_resource_group(self, resource_group_name):
        """list all nsgs in a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.nsg_client.list(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, nsg_name):
        """check a nsg if exits"""
        if param_is_null([resource_group_name, nsg_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_by_resource_group(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == nsg_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, nsg_name):
        """get a nsg object"""
        if param_is_null([resource_group_name, nsg_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, nsg_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_NSG_NOT_EXIST

        try:
            result = self.nsg_client.get(resource_group_name, nsg_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def create(self, create_configs):
        """create a nsg object"""
        resource_group_name = create_configs.get("resource_group_name", None)
        location = create_configs.get("location", None)
        nsg_name = create_configs.get("nsg_name", None)
        if param_is_null([resource_group_name, nsg_name, location]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # create resource group
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            status_code, result = op_resource_group.create(resource_group_name, location)
            if status_code != AZURE_STATUS_OK:
                return status_code, result

        # check existence
        status_code, result = self.check_existence(resource_group_name, nsg_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_NSG_EXIST

        # create nsg
        parameters = NetworkSecurityGroup(location=location)

        try:
            result = self.nsg_client.create_or_update(resource_group_name, nsg_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def add_inbound_rule(self, create_configs):
        """add a inbound rule into a nsg"""
        resource_group_name = create_configs.get("resource_group_name", None)
        nsg_name = create_configs.get("nsg_name", None)
        if param_is_null([resource_group_name, nsg_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # create resource group
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        # get nsg
        status_code, nsg_obj = self.get(resource_group_name, nsg_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, nsg_obj

        # new security rule
        name = create_configs.get("name", None)
        priority = create_configs.get("priority", None)
        source_address_prefix = create_configs.get("source_address_prefix", None)
        protocol = create_configs.get("protocol", None)
        destination_port_range = create_configs.get("destination_port_range", None)
        access = create_configs.get("access", None)
        if param_is_null([name, priority, source_address_prefix, protocol, destination_port_range, access]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        new_security_rule = SecurityRule(name=name,
                                         priority=priority,
                                         direction="Inbound",
                                         source_address_prefix=source_address_prefix,
                                         protocol=protocol,
                                         destination_port_range=destination_port_range,
                                         access=access,
                                         source_port_range="*",
                                         destination_address_prefix="*")

        # new nsg
        nsg_obj.security_rules.append(new_security_rule)

        try:
            result = self.nsg_client.create_or_update(resource_group_name, nsg_name, nsg_obj)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete_inbound_rule(self, create_configs):
        """delete a inbound rule from nsg"""
        resource_group_name = create_configs.get("resource_group_name", None)
        nsg_name = create_configs.get("nsg_name", None)
        inbound_rule_name = create_configs.get("inbound_rule_name", None)
        if param_is_null([resource_group_name, nsg_name, inbound_rule_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # create resource group
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        # get nsg
        status_code, nsg_obj = self.get(resource_group_name, nsg_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, nsg_obj

        # new security rule

        # new nsg
        new_security_rules = []
        if nsg_obj.security_rules is not None:
            for security_rule in nsg_obj.security_rules:
                if security_rule.name != inbound_rule_name:
                    new_security_rules.append(security_rule)
        nsg_obj.security_rules = new_security_rules

        try:
            result = self.nsg_client.create_or_update(resource_group_name, nsg_name, nsg_obj)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def create_with_nsg(self, create_configs):
        """create nsg with inbound rules"""
        resource_group_name = create_configs.get("resource_group_name", None)
        location = create_configs.get("location", None)
        nsg_name = create_configs.get("nsg_name", None)
        if param_is_null([resource_group_name, nsg_name, location]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # create resource group
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            status_code, result = op_resource_group.create(resource_group_name, location)
            if status_code != AZURE_STATUS_OK:
                return status_code, result

        # check existence
        status_code, result = self.check_existence(resource_group_name, nsg_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_NSG_EXIST

        # inbound nsg rule
        nsg_inbound_rules = create_configs.get("nsg_inbound_rules", None)
        if nsg_inbound_rules is None:
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
        else:
            security_rules = []
            for nsg_inbound_rule in nsg_inbound_rules:
                name = nsg_inbound_rule.get("name", None)
                priority = nsg_inbound_rule.get("priority", None)
                source_address_prefix = nsg_inbound_rule.get("source_address_prefix", None)
                protocol = nsg_inbound_rule.get("protocol", None)
                destination_port_range = nsg_inbound_rule.get("destination_port_range", None)
                access = nsg_inbound_rule.get("access", None)

                if param_is_null([name, priority, source_address_prefix, protocol, destination_port_range, access]):
                    return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

                security_rule = SecurityRule(name=name,
                                             priority=priority,
                                             direction="Inbound",
                                             source_address_prefix=source_address_prefix,
                                             protocol=protocol,
                                             destination_port_range=destination_port_range,
                                             access=access,
                                             source_port_range="*",
                                             destination_address_prefix="*")
                security_rules.append(security_rule)

        # create nsg
        parameters = NetworkSecurityGroup(location=location,
                                          security_rules=security_rules)

        try:
            result = self.nsg_client.create_or_update(resource_group_name, nsg_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    # based on azure-mgmt-network 1.5+
    def create_with_rules(self, create_configs):
        """create nsg with inbound rules"""
        resource_group_name = create_configs.get("resource_group_name", None)
        location = create_configs.get("location", None)
        nsg_name = create_configs.get("nsg_name", None)
        if param_is_null([resource_group_name, nsg_name, location]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # create resource group
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            status_code, result = op_resource_group.create(resource_group_name, location)
            if status_code != AZURE_STATUS_OK:
                return status_code, result

        # check existence
        #status_code, result = self.check_existence(resource_group_name, nsg_name)
        #if status_code != AZURE_STATUS_OK:
        #    return status_code, result

        #if result is True:
        #    return AZURE_STATUS_RES_EXIST, AZURE_INFO_NSG_EXIST

        # inbound nsg rule
        nsg_inbound_rules = create_configs.get("nsg_inbound_rules", None)
        if nsg_inbound_rules is None:
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
        else:
            security_rules = []
            for nsg_inbound_rule in nsg_inbound_rules:
                name = nsg_inbound_rule.get("name", None)
                priority = nsg_inbound_rule.get("priority", None)
                source_address_prefix = nsg_inbound_rule.get("source_address_prefix", None)
                protocol = nsg_inbound_rule.get("protocol", None)
                destination_port_ranges = nsg_inbound_rule.get("destination_port_ranges", [])
                destination_port_range = nsg_inbound_rule.get("destination_port_range", None)
                access = nsg_inbound_rule.get("access", None)
                description = nsg_inbound_rule.get("description", None)
                
                if param_is_null([name, priority, source_address_prefix, protocol, access]):
                    return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
                    
                # destination_port_range or destination_port_ranges are not empty both
                if not destination_port_range and not destination_port_ranges:
                    return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL    
                
                destination_port_already_set_flag = False
                
                if not destination_port_already_set_flag and destination_port_ranges:
                    destination_port_already_set_flag = True
                    security_rule = SecurityRule(name=name,
                                                 priority=priority,
                                                 direction="Inbound",
                                                 source_address_prefix=source_address_prefix,
                                                 protocol=protocol,
                                                 destination_port_ranges=destination_port_ranges,
                                                 access=access,
                                                 description=description,
                                                 source_port_range="*",
                                                 destination_address_prefix="*")
                                                 
                if not destination_port_already_set_flag and destination_port_range:
                    destination_port_already_set_flag = True
                    security_rule = SecurityRule(name=name,
                             priority=priority,
                             direction="Inbound",
                             source_address_prefix=source_address_prefix,
                             protocol=protocol,
                             destination_port_range=destination_port_range,
                             access=access,
                             description=description,
                             source_port_range="*",
                             destination_address_prefix="*")
                             
                security_rules.append(security_rule)

        # create nsg
        parameters = NetworkSecurityGroup(location=location,
                                          security_rules=security_rules)

        try:
            result = self.nsg_client.create_or_update(resource_group_name, nsg_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result     
        
    # async
    def delete(self, resource_group_name, nsg_name):
        """delete a nsg"""
        if param_is_null([resource_group_name, nsg_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, nsg_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_NSG_NOT_EXIST

        try:
            result = self.nsg_client.delete(resource_group_name, nsg_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result
