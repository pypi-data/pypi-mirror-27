# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_nic.py
@time: 2016/12/14 18:02
"""

from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.network.models import NetworkInterface
from azure.mgmt.network.models import NetworkInterfaceIPConfiguration
from azure.mgmt.network.models import IPAllocationMethod
from azure.mgmt.network.models import PublicIPAddress
from msrestazure.azure_exceptions import CloudError

from op_resource_group import OPResourceGroup
from op_ss_vm import OPScaleSetVM
from op_public_ip import OPPublicIP
from op_subnet import OPSubnet
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_NIC_NOT_EXIST, AZURE_STATUS_RES_EXIST, AZURE_INFO_NIC_EXIST, \
    AZURE_INFO_RG_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST


class OPNic(object):
    """azure network interface wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.network_client = NetworkManagementClient(credentials, subscription_id)
        self.nic_client = self.network_client.network_interfaces

    def list_all(self):
        """list all nic"""
        try:
            result = self.nic_client.list_all()
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_by_resource_group(self, resource_group_name):
        """list all nics in a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.nic_client.list(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, nic_name):
        """check a nic if exits"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_by_resource_group(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == nic_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, nic_name):
        """get a nic object"""
        if param_is_null([resource_group_name, nic_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, nic_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_NIC_NOT_EXIST

        try:
            result = self.nic_client.get(resource_group_name, nic_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def create_dyn_private(self, create_configs):
        """create dynamic private ip """
        resource_group_name = create_configs.get("resource_group_name", None)
        location = create_configs.get("location", None)
        nic_name = create_configs.get("nic_name", None)
        if param_is_null([resource_group_name, location, nic_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # check resource group
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if not result:
            status_code, result = op_resource_group.create(resource_group_name, location)
            if status_code != AZURE_STATUS_OK:
                return status_code, result

        # exist check
        status_code, result = self.check_existence(resource_group_name, nic_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_NIC_EXIST

        # create parameters
        subnet_resource_group_name = create_configs.get("subnet_resource_group_name", None)
        subnet_virtual_network_name = create_configs.get("subnet_virtual_network_name", None)
        subnet_name = create_configs.get("subnet_name", None)
        if param_is_null([subnet_resource_group_name, subnet_virtual_network_name, subnet_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
        op_subnet = OPSubnet(self.subscription_id, self.user_name, self.password)
        status_code, subnet = op_subnet.get(subnet_resource_group_name, subnet_virtual_network_name, subnet_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, subnet

        name = 'default'
        primary = True
        private_ip_allocation_method = IPAllocationMethod.dynamic
        ip_configuration = NetworkInterfaceIPConfiguration(id=None,
                                                           application_gateway_backend_address_pools=None,
                                                           load_balancer_backend_address_pools=None,
                                                           load_balancer_inbound_nat_rules=None,
                                                           private_ip_address=None,
                                                           private_ip_allocation_method=private_ip_allocation_method,
                                                           private_ip_address_version=None,
                                                           subnet=subnet,
                                                           primary=primary,
                                                           public_ip_address=None,
                                                           provisioning_state=None,
                                                           name=name,
                                                           etag=None)
        ip_configurations = [ip_configuration]

        parameters = NetworkInterface(location=location,
                                      tags=None,
                                      virtual_machine=None,
                                      network_security_group=None,
                                      ip_configurations=ip_configurations,
                                      dns_settings=None,
                                      mac_address=None,
                                      primary=primary,
                                      enable_ip_forwarding=None)
        try:
            result = self.nic_client.create_or_update(resource_group_name, nic_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def create_public_ip_nic(self, create_configs):
        """create a nic with public ip"""
        resource_group_name = create_configs.get("resource_group_name", None)
        location = create_configs.get("location", None)
        nic_name = create_configs.get("nic_name", None)
        if param_is_null([resource_group_name, location, nic_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # check resource group
        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if not result:
            status_code, result = op_resource_group.create(resource_group_name, location)
            if status_code != AZURE_STATUS_OK:
                return status_code, result

        # exist check
        status_code, result = self.check_existence(resource_group_name, nic_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_NIC_EXIST

        # get public ip
        public_ip_resource_group_name = create_configs.get("public_ip_resource_group_name", None)
        public_ip_address_name = create_configs.get("public_ip_address_name", None)
        if param_is_null([public_ip_resource_group_name, public_ip_address_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
        op_public_ip = OPPublicIP(self.subscription_id, self.user_name, self.password)
        status_code, public_ip = op_public_ip.get(public_ip_resource_group_name, public_ip_address_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, public_ip

        public_ip_address = PublicIPAddress(id=public_ip.id)

        # create parameters
        subnet_resource_group_name = create_configs.get("subnet_resource_group_name", None)
        subnet_virtual_network_name = create_configs.get("subnet_virtual_network_name", None)
        subnet_name = create_configs.get("subnet_name", None)
        if param_is_null([subnet_resource_group_name, subnet_virtual_network_name, subnet_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
        op_subnet = OPSubnet(self.subscription_id, self.user_name, self.password)
        status_code, subnet = op_subnet.get(subnet_resource_group_name, subnet_virtual_network_name, subnet_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, subnet

        name = 'default'
        primary = True
        private_ip_allocation_method = IPAllocationMethod.dynamic
        ip_configuration = NetworkInterfaceIPConfiguration(id=None,
                                                           application_gateway_backend_address_pools=None,
                                                           load_balancer_backend_address_pools=None,
                                                           load_balancer_inbound_nat_rules=None,
                                                           private_ip_address=None,
                                                           private_ip_allocation_method=private_ip_allocation_method,
                                                           private_ip_address_version=None,
                                                           subnet=subnet,
                                                           primary=primary,
                                                           public_ip_address=public_ip_address,
                                                           provisioning_state=None,
                                                           name=name,
                                                           etag=None)
        ip_configurations = [ip_configuration]

        parameters = NetworkInterface(location=location,
                                      tags=None,
                                      virtual_machine=None,
                                      network_security_group=None,
                                      ip_configurations=ip_configurations,
                                      dns_settings=None,
                                      mac_address=None,
                                      primary=primary,
                                      enable_ip_forwarding=None)
        try:
            result = self.nic_client.create_or_update(resource_group_name, nic_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete(self, resource_group_name, nic_name):
        """delete a nic"""
        if param_is_null([resource_group_name, nic_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, nic_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_NIC_NOT_EXIST

        try:
            result = self.nic_client.delete(resource_group_name, nic_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_vmss_vm_nics(self, resource_group_name, vm_scale_set_name, instance_id):
        """list a vm scale set instance ip info"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_ss_vm = OPScaleSetVM(self.subscription_id, self.user_name, self.password)
        status_code, result = op_ss_vm.check_existence(resource_group_name, vm_scale_set_name, instance_id)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST

        try:
            result = self.nic_client.list_virtual_machine_scale_set_vm_network_interfaces(resource_group_name,
                                                                                          vm_scale_set_name,
                                                                                          instance_id)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result
