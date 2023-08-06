# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_load_balance.py
@time: 2016/12/14 18:12
"""

from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.network.models import LoadBalancer
from azure.mgmt.network.models import FrontendIPConfiguration
from azure.mgmt.network.models import IPAllocationMethod
from azure.mgmt.network.models import BackendAddressPool
from azure.mgmt.network.models import LoadBalancingRule
from azure.mgmt.network.models import Probe
from azure.mgmt.network.models import InboundNatRule
from azure.mgmt.network.models import PublicIPAddress
from msrestazure.azure_exceptions import CloudError

from op_resource_group import OPResourceGroup
from op_public_ip import OPPublicIP
from op_subnet import OPSubnet
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_RES_EXIST, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, AZURE_INFO_RG_EXIST, \
    AZURE_INFO_LB_EXIST, AZURE_INFO_PUBLIC_IP_NOT_EXIST, AZURE_INFO_LB_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST


class OPLoadBalance(object):
    """azure load balance wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.network_client = NetworkManagementClient(credentials, subscription_id)
        self.lb_client = self.network_client.load_balancers

    def list_all(self):
        """list all load balance

        :rtype: int, :class:`LoadBalancerPaged <azure.mgmt.network.models.LoadBalancerPaged>`
        """
        try:
            result = self.lb_client.list_all()
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_by_resource_group(self, resource_group_name):
        """list all load balance in a resource group

        :param resource_group_name:
        :rtype: int, :class:`LoadBalancerPaged <azure.mgmt.network.models.LoadBalancerPaged>`
        """
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.lb_client.list(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, lb_name):
        """check load balance if exist

        :param resource_group_name:
        :param lb_name:
        :rtype: int, boolean
        """
        if param_is_null([resource_group_name, lb_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_by_resource_group(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == lb_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, lb_name):
        """get a load balance object

        :param resource_group_name:
        :param lb_name:
        :rtype: :class:`LoadBalancer <azure.mgmt.network.models.LoadBalancer>`
        """
        if param_is_null([resource_group_name, lb_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, lb_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_LB_NOT_EXIST

        try:
            result = self.lb_client.get(resource_group_name, lb_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete(self, resource_group_name, lb_name):
        """delete a load balance

        :param resource_group_name:
        :param lb_name:
        :rtype: int, :class:`AzureOperationPoller<msrestazure.azure_operation.AzureOperationPoller>`
        """
        if param_is_null([resource_group_name, lb_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, lb_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_LB_NOT_EXIST

        try:
            result = self.lb_client.delete(resource_group_name, lb_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def create(self, create_configs):
        """ create a load balance

        :param create_configs: config dict
        :rtype: int, :class:`AzureOperationPoller<msrestazure.azure_operation.AzureOperationPoller>`
        """
        subscription_id = create_configs.get("subscription_id", None)
        resource_group_name = create_configs.get("resource_group_name", None)
        lb_name = create_configs.get("lb_name", None)
        location = create_configs.get("location", None)
        if param_is_null([resource_group_name, lb_name, subscription_id, location]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # pre-create resource group
        status_code, result = self.__pre_create_rg(resource_group_name, location)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        # check existence
        status_code, result = self.check_existence(resource_group_name, lb_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_LB_EXIST

        lb_info = create_configs.get("lb_info", None)

        # fip lb_info
        status_code, frontend_ip_list = self.__create_fip(lb_info)
        if status_code != AZURE_STATUS_OK:
            return status_code, frontend_ip_list

        # bap
        status_code, backend_address_pool_list = self.__create_bap(lb_info)
        if status_code != AZURE_STATUS_OK:
            return status_code, backend_address_pool_list

        # probe
        status_code, probe_list = self.__create_probe(lb_info)
        if status_code != AZURE_STATUS_OK:
            return status_code, probe_list
        # rule
        status_code, load_balancing_rule_list = self.__create_rule(resource_group_name, lb_name, lb_info)
        if status_code != AZURE_STATUS_OK:
            return status_code, load_balancing_rule_list

        # create inbound nat
        inbound_nat_rules_list = self.__create_inbound_nat(create_configs, fip_sub_resource=None)

        # create lb
        lb_parameters = self.create_lb_parameters(location=location,
                                                  frontend_ip_configurations=frontend_ip_list,
                                                  backend_address_pools=backend_address_pool_list,
                                                  load_balancing_rules=load_balancing_rule_list,
                                                  probes=probe_list,
                                                  inbound_nat_rules=inbound_nat_rules_list)

        try:
            result = self.lb_client.create_or_update(resource_group_name, lb_name, lb_parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    @staticmethod
    def create_lb_parameters(location, frontend_ip_configurations, backend_address_pools, load_balancing_rules,
                             probes, inbound_nat_rules=None):
        """construct load balance parameter object"""
        load_balance_parameters = LoadBalancer(location=location,
                                               frontend_ip_configurations=frontend_ip_configurations,
                                               backend_address_pools=backend_address_pools,
                                               load_balancing_rules=load_balancing_rules,
                                               probes=probes,
                                               inbound_nat_rules=inbound_nat_rules)
        return load_balance_parameters

    @staticmethod
    def create_private_fip(frontend_ip_name, private_ip_address, subnet,
                           private_ip_allocation_method=IPAllocationMethod.static):
        """construct private frontend ip configuration"""
        frontend_ip_configuration = FrontendIPConfiguration(name=frontend_ip_name,
                                                            private_ip_address=private_ip_address,
                                                            private_ip_allocation_method=private_ip_allocation_method,
                                                            subnet=subnet)
        return frontend_ip_configuration

    @staticmethod
    def create_public_fip(frontend_ip_name, public_ip_address):
        """construct public frontend ip configuration"""
        frontend_ip_configuration = FrontendIPConfiguration(name=frontend_ip_name,
                                                            public_ip_address=public_ip_address)
        return frontend_ip_configuration

    @staticmethod
    def create_backend_address_pool(backend_address_pool_name):
        """construct backend address pool object"""
        backend_address_pool_info = BackendAddressPool(name=backend_address_pool_name)
        return backend_address_pool_info

    @staticmethod
    def create_probe(probe_name, protocol, port, request_path, interval_in_seconds, number_of_probes):
        """construct probe object"""
        probe = Probe(name=probe_name, protocol=protocol, port=port,
                      interval_in_seconds=interval_in_seconds, number_of_probes=number_of_probes,
                      request_path=request_path)
        return probe

    @staticmethod
    def create_lb_rule(load_balance_rule_name, protocol, frontend_port, backend_port,
                       fip_sub_resource, bap_sub_resource, probe_sub_resource):
        """construct load balance rule object"""
        load_balance_rule = LoadBalancingRule(name=load_balance_rule_name,
                                              protocol=protocol,
                                              frontend_port=frontend_port,
                                              backend_port=backend_port,
                                              frontend_ip_configuration=fip_sub_resource,
                                              backend_address_pool=bap_sub_resource,
                                              probe=probe_sub_resource)
        return load_balance_rule

    @staticmethod
    def create_inbound_nat_rule(inbound_nat_rule_name, fip_sub_resource, protocol, frontend_port, backend_port):
        """construct inbound nat rule object"""
        inbound_nat_rule = InboundNatRule(name=inbound_nat_rule_name,
                                          frontend_ip_configuration=fip_sub_resource,
                                          protocol=protocol,
                                          frontend_port=frontend_port,
                                          backend_port=backend_port)
        return inbound_nat_rule

    @staticmethod
    def construct_fip_id(subscription_id, resource_group_name, lb_name, fip_name):
        """construct fip id"""
        return ('/subscriptions/{}'
                '/resourceGroups/{}'
                '/providers/Microsoft.Network'
                '/loadBalancers/{}'
                '/frontendIPConfigurations/{}').format(
                    subscription_id, resource_group_name, lb_name, fip_name
                )

    @staticmethod
    def construct_public_ip_id(subscription_id, resource_group_name, public_ip_name):
        """construct public ip id"""
        return ('/subscriptions/{}'
                '/resourceGroups/{}'
                '/providers/Microsoft.Network'
                '/publicIPAddresses/{}').format(
                    subscription_id, resource_group_name, public_ip_name
                )

    @staticmethod
    def construct_bap_id(subscription_id, resource_group_name, lb_name, address_pool_name):
        """construct bap id"""
        return ('/subscriptions/{}'
                '/resourceGroups/{}'
                '/providers/Microsoft.Network'
                '/loadBalancers/{}'
                '/backendAddressPools/{}').format(
                    subscription_id, resource_group_name, lb_name, address_pool_name
                )

    @staticmethod
    def construct_probe_id(subscription_id, resource_group_name, lb_name, probe_name):
        """construct probe id"""
        return ('/subscriptions/{}'
                '/resourceGroups/{}'
                '/providers/Microsoft.Network'
                '/loadBalancers/{}'
                '/probes/{}').format(
                    subscription_id, resource_group_name, lb_name, probe_name
                )

    def __pre_create_rg(self, resource_group_name, location):
        """create resource group if not exist"""
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if not result:
            status_code, result = op_resource_group.create(resource_group_name, location)
            if status_code != AZURE_STATUS_OK:
                return status_code, result
        return AZURE_STATUS_OK, AZURE_INFO_RG_EXIST

    def __pre_get_subnet(self, resource_group_name, virtual_network_name, subnet_name):
        """get subnet object"""
        op_subnet = OPSubnet(self.subscription_id, self.user_name, self.password)
        status_code, result = op_subnet.get(resource_group_name, virtual_network_name, subnet_name)
        return status_code, result

    def __create_inbound_nat(self, create_configs, fip_sub_resource):
        # create inbound nat
        inbound_nat_rule_name = create_configs.get("inbound_nat_rule_name", None)
        inbound_nat_protocol = create_configs.get("inbound_nat_protocol", None)
        inbound_nat_frontend_port = create_configs.get("inbound_nat_frontend_port", None)
        inbound_nat_backend_port = create_configs.get("inbound_nat_backend_port", None)
        if inbound_nat_rule_name is None or inbound_nat_rule_name == "":
            inbound_nat_rule = None
        else:
            if param_is_null([inbound_nat_protocol, inbound_nat_frontend_port, inbound_nat_backend_port]):
                return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

            inbound_nat_rule = self.create_inbound_nat_rule(inbound_nat_rule_name=inbound_nat_rule_name,
                                                            fip_sub_resource=fip_sub_resource,
                                                            protocol=inbound_nat_protocol,
                                                            frontend_port=inbound_nat_frontend_port,
                                                            backend_port=inbound_nat_backend_port)
        if inbound_nat_rule is None:
            inbound_nat_rules_list = None
        else:
            inbound_nat_rules_list = [inbound_nat_rule]

        return inbound_nat_rules_list

    def __create_fip(self, lb_info):
        frontend_ip_list = []
        for fip_info in lb_info["fips"]:
            frontend_ip_name = fip_info.get("frontend_ip_name", None)
            if param_is_null([frontend_ip_name]):
                return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

            # if need, create public ip
            public_ip_resource_group_name = fip_info.get("public_ip_resource_group_name", None)
            public_ip_address_name = fip_info.get("public_ip_address_name", None)

            subnet_resource_group_name = fip_info.get("subnet_resource_group_name", None)
            subnet_virtual_network_name = fip_info.get("subnet_virtual_network_name", None)
            subnet_name = fip_info.get("subnet_name", None)
            private_ip_address = fip_info.get("private_ip_address", None)

            if public_ip_resource_group_name is not None and public_ip_address_name is not None:
                public_ip_client = OPPublicIP(self.subscription_id, self.user_name, self.password)
                status_code, result = public_ip_client.check_existence(public_ip_resource_group_name,
                                                                       public_ip_address_name)
                if status_code != AZURE_STATUS_OK:
                    return status_code, result

                if result:
                    public_ip_id = self.construct_public_ip_id(self.subscription_id, public_ip_resource_group_name,
                                                               public_ip_address_name)
                    public_ip_address = PublicIPAddress(id=public_ip_id)
                else:
                    return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_PUBLIC_IP_NOT_EXIST

                fip_object = self.create_public_fip(frontend_ip_name=frontend_ip_name,
                                                    public_ip_address=public_ip_address)

                frontend_ip_list.append(fip_object)
            else:
                if param_is_null([subnet_resource_group_name, subnet_virtual_network_name, subnet_name,
                                  private_ip_address]):
                    return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
                # pre-get subnet
                status_code, subnet_obj = self.__pre_get_subnet(subnet_resource_group_name,
                                                                subnet_virtual_network_name,
                                                                subnet_name)
                if status_code != AZURE_STATUS_OK:
                    return status_code, subnet_obj

                subnet = subnet_obj
                private_ip_allocation_method = fip_info.get("private_ip_allocation_method",
                                                            IPAllocationMethod.static)
                fip_object = self.create_private_fip(frontend_ip_name=frontend_ip_name,
                                                     private_ip_address=private_ip_address,
                                                     subnet=subnet,
                                                     private_ip_allocation_method=private_ip_allocation_method)
                frontend_ip_list.append(fip_object)
        return AZURE_STATUS_OK, frontend_ip_list

    def __create_bap(self, lb_info):
        backend_address_pool_list = []
        for bap_info in lb_info["baps"]:
            backend_address_pool_name = bap_info.get("backend_address_pool_name", None)
            if param_is_null([backend_address_pool_name]):
                return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
            bap_object = self.create_backend_address_pool(backend_address_pool_name=backend_address_pool_name)
            backend_address_pool_list.append(bap_object)
        return AZURE_STATUS_OK, backend_address_pool_list

    def __create_probe(self, lb_info):
        probe_list = []
        for probe_info in lb_info["probes"]:
            probe_name = probe_info.get("probe_name", None)
            probe_protocol = probe_info.get("probe_protocol", None)
            probe_port = probe_info.get("probe_port", None)
            probe_url = probe_info.get("probe_url", None)
            probe_interval = probe_info.get("probe_interval", 15)
            probe_number = probe_info.get("probe_number", 4)
            if param_is_null([probe_name, probe_protocol, probe_port, probe_interval, probe_number]):
                return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

            probe_object = self.create_probe(probe_name=probe_name,
                                             protocol=probe_protocol,
                                             port=probe_port,
                                             request_path=probe_url,
                                             interval_in_seconds=probe_interval,
                                             number_of_probes=probe_number)
            probe_list.append(probe_object)
        return AZURE_STATUS_OK, probe_list

    def __create_rule(self, resource_group_name, lb_name, lb_info):
        load_balancing_rule_list = []
        for rule_info in lb_info["rules"]:
            frontend_ip_name = rule_info.get("fip_name", None)
            backend_address_pool_name = rule_info.get("bap_name", None)
            probe_name = rule_info.get("probe_name", None)

            fip_sub_resource = {
                'id': self.construct_fip_id(self.subscription_id, resource_group_name, lb_name, frontend_ip_name)
            }
            bap_sub_resource = {
                'id': self.construct_bap_id(self.subscription_id, resource_group_name, lb_name,
                                            backend_address_pool_name)
            }
            probe_sub_resource = {
                'id': self.construct_probe_id(self.subscription_id, resource_group_name, lb_name, probe_name)
            }

            # create lb rule
            lb_rule_name = rule_info.get("lb_rule_name", None)
            lb_protocol = rule_info.get("lb_protocol", None)
            lb_frontend_port = rule_info.get("lb_frontend_port", None)
            lb_backend_port = rule_info.get("lb_backend_port", None)

            if param_is_null([lb_rule_name, lb_protocol, lb_frontend_port, lb_backend_port]):
                return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

            lb_rule_object = self.create_lb_rule(load_balance_rule_name=lb_rule_name,
                                                 protocol=lb_protocol,
                                                 frontend_port=lb_frontend_port,
                                                 backend_port=lb_backend_port,
                                                 fip_sub_resource=fip_sub_resource,
                                                 bap_sub_resource=bap_sub_resource,
                                                 probe_sub_resource=probe_sub_resource)
            load_balancing_rule_list.append(lb_rule_object)
        return AZURE_STATUS_OK, load_balancing_rule_list
