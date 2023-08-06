# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_public_ip.py
@time: 2016/12/14 18:02
"""

from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.network.models import PublicIPAddress
from azure.mgmt.network.models import PublicIPAddressDnsSettings
from msrestazure.azure_exceptions import CloudError

from op_resource_group import OPResourceGroup
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST, AZURE_INFO_PUBLIC_IP_NOT_EXIST, AZURE_STATUS_PARAM_INVALID, \
    AZURE_INFO_PARAM_INVALID, AZURE_STATUS_RES_EXIST, AZURE_INFO_NIC_EXIST


class OPPublicIP(object):
    """azure public ip sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.network_client = NetworkManagementClient(credentials, subscription_id)
        self.public_ip_client = self.network_client.public_ip_addresses

    def list_all(self):
        """list all public ips"""
        try:
            result = self.public_ip_client.list_all()
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_by_resource_group(self, resource_group_name):
        """list all public ips in a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.public_ip_client.list(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, public_ip_address_name):
        """check a public ip if exits"""
        if param_is_null([resource_group_name, public_ip_address_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_by_resource_group(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == public_ip_address_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, public_ip_address_name):
        """get a public ip"""
        if param_is_null([resource_group_name, public_ip_address_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, public_ip_address_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_PUBLIC_IP_NOT_EXIST

        try:
            result = self.public_ip_client.get(resource_group_name, public_ip_address_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete(self, resource_group_name, public_ip_address_name):
        """delete a public ip"""
        if param_is_null([resource_group_name, public_ip_address_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, public_ip_address_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_PUBLIC_IP_NOT_EXIST

        try:
            result = self.public_ip_client.delete(resource_group_name, public_ip_address_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def create(self, create_configs):
        """create a public ip object"""
        resource_group_name = create_configs.get("resource_group_name", None)
        location = create_configs.get("location", None)
        public_ip_address_name = create_configs.get("public_ip_address_name", None)
        public_ip_allocation_method = create_configs.get("public_ip_allocation_method", None)
        domain_name_label = create_configs.get("domain_name_label", None)
        if param_is_null([resource_group_name, location, public_ip_address_name, public_ip_allocation_method]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        if public_ip_allocation_method != "Static" and public_ip_allocation_method != "Dynamic":
            return AZURE_STATUS_PARAM_INVALID, AZURE_INFO_PARAM_INVALID

        # check resource group
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if not result:
            status_code, result = op_resource_group.create(resource_group_name, location)
            if status_code != AZURE_STATUS_OK:
                return status_code, result

        # check existence
        status_code, result = self.check_existence(resource_group_name, public_ip_address_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_NIC_EXIST

        dns_settings = PublicIPAddressDnsSettings(domain_name_label=domain_name_label)
        parameters = PublicIPAddress(location=location,
                                     tags=None,
                                     public_ip_allocation_method=public_ip_allocation_method,
                                     dns_settings=dns_settings,
                                     ip_address=None,
                                     idle_timeout_in_minutes=None)

        try:
            result = self.public_ip_client.create_or_update(resource_group_name, public_ip_address_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result
