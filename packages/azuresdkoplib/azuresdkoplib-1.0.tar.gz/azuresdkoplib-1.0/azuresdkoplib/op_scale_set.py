# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_scale_set.py
@time: 2016/10/31 15:04
"""

import base64

from azure.mgmt.compute.models import Sku
from azure.mgmt.compute.models import UpgradePolicy
from azure.mgmt.compute.models import VirtualMachineScaleSet
from azure.mgmt.compute.models import VirtualMachineScaleSetVMProfile
from azure.mgmt.compute.models import VirtualMachineScaleSetNetworkProfile
from azure.mgmt.compute.models import VirtualMachineScaleSetStorageProfile
from azure.mgmt.compute.models import VirtualMachineScaleSetOSProfile
from azure.mgmt.compute.models import VirtualMachineScaleSetExtensionProfile
from azure.mgmt.compute.models import VirtualMachineScaleSetNetworkConfiguration
from azure.mgmt.compute.models import VirtualMachineScaleSetIPConfiguration
from azure.mgmt.compute.models import VirtualMachineScaleSetDataDisk
from azure.mgmt.compute.models import VirtualMachineScaleSetOSDisk
from azure.mgmt.compute.models import DiskCreateOptionTypes
from azure.mgmt.compute.models import CachingTypes
from azure.mgmt.compute.models import VirtualHardDisk
from azure.mgmt.compute.models import ImageReference
from azure.mgmt.compute.models import ApiEntityReference
from azure.mgmt.compute.models import SubResource
from azure.mgmt.compute.models import LinuxConfiguration
from azure.mgmt.compute.models import SshConfiguration
from azure.mgmt.compute.models import SshPublicKey
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import UserPassCredentials
from msrestazure.azure_exceptions import CloudError

from op_resource_group import OPResourceGroup
from op_subnet import OPSubnet
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST, AZURE_STATUS_RES_EXIST, \
    AZURE_INFO_SS_EXIST, AZURE_INFO_SUBNET_NOT_EXIST, AZURE_INFO_RG_EXIST, AZURE_INFO_SUBNET_EXIST


class OPScaleSet(object):
    """azure scale set sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.compute_client = ComputeManagementClient(credentials, subscription_id)
        self.scale_set_client = self.compute_client.virtual_machine_scale_sets

    def list_all(self):
        """list all scale set"""
        try:
            result = self.scale_set_client.list_all()
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_by_resource_group(self, resource_group_name):
        """list all scale set in a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.scale_set_client.list(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, vm_scale_set_name):
        """check scale set if exist"""
        if param_is_null([resource_group_name, vm_scale_set_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_by_resource_group(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == vm_scale_set_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, vm_scale_set_name):
        """get a scale set object"""
        if param_is_null([resource_group_name, vm_scale_set_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_client.get(resource_group_name, vm_scale_set_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete(self, resource_group_name, vm_scale_set_name):
        """delete a scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_client.delete(resource_group_name, vm_scale_set_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete_instances(self, resource_group_name, vm_scale_set_name, instance_ids):
        """delete instances from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_ids]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_client.delete_instances(resource_group_name, vm_scale_set_name, instance_ids)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def deallocate(self, resource_group_name, vm_scale_set_name, instance_ids=None):
        """deallocate instances from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_ids]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_client.deallocate(resource_group_name=resource_group_name,
                                                      vm_scale_set_name=vm_scale_set_name,
                                                      instance_ids=instance_ids)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def power_off(self, resource_group_name, vm_scale_set_name, instance_ids=None):
        """power off instances from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_ids]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_client.power_off(resource_group_name=resource_group_name,
                                                     vm_scale_set_name=vm_scale_set_name,
                                                     instance_ids=instance_ids)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def restart(self, resource_group_name, vm_scale_set_name, instance_ids=None):
        """restart instances from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_ids]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_client.restart(resource_group_name=resource_group_name,
                                                   vm_scale_set_name=vm_scale_set_name,
                                                   instance_ids=instance_ids)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def start(self, resource_group_name, vm_scale_set_name, instance_ids=None):
        """start instances from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_ids]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_client.start(resource_group_name=resource_group_name,
                                                 vm_scale_set_name=vm_scale_set_name,
                                                 instance_ids=instance_ids)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def _pre_create_rg(self, resource_group_name, location):
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

    def _pre_check_subnet(self, resource_group_name, virtual_network_name, subnet_name):
        """check subnet if exist"""
        op_subnet = OPSubnet(self.subscription_id, self.user_name, self.password)
        status_code, result = op_subnet.check_existence(resource_group_name, virtual_network_name, subnet_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if status_code == AZURE_STATUS_OK and result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SUBNET_NOT_EXIST
        return AZURE_STATUS_OK, AZURE_INFO_SUBNET_EXIST

    # async
    def create(self, create_configs):
        """create a scale set"""
        resource_group_name = create_configs.get("resource_group_name", None)
        location = create_configs.get("location", None)
        vm_scale_set_name = create_configs.get("vm_scale_set_name", None)
        if param_is_null([resource_group_name, location, vm_scale_set_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # pre-create resource group
        status_code, result = self._pre_create_rg(resource_group_name, location)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        # pre-check subnet
        subnet_resource_group_name = create_configs.get("subnet_resource_group_name", None)
        subnet_virtual_network_name = create_configs.get("subnet_virtual_network_name", None)
        subnet_name = create_configs.get("subnet_name", None)
        if param_is_null([subnet_resource_group_name, subnet_virtual_network_name, subnet_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
        status_code, result = self._pre_check_subnet(subnet_resource_group_name,
                                                     subnet_virtual_network_name,
                                                     subnet_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        # check existence
        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_SS_EXIST

        # os profile
        status_code, os_profile = self.create_ss_os_profile(create_configs)
        if status_code != AZURE_STATUS_OK:
            return status_code, os_profile

        # storage profile
        status_code, storage_profile = self.create_ss_storage_profile(create_configs)
        if status_code != AZURE_STATUS_OK:
            return status_code, storage_profile

        # network profile
        status_code, network_profile = self.create_ss_network_profile(create_configs)
        if status_code != AZURE_STATUS_OK:
            return status_code, network_profile

        # extension profile
        extension_profile = VirtualMachineScaleSetExtensionProfile(extensions=None)

        # vmss profile
        virtual_machine_profile = VirtualMachineScaleSetVMProfile(os_profile=os_profile,
                                                                  storage_profile=storage_profile,
                                                                  network_profile=network_profile,
                                                                  extension_profile=extension_profile)

        # vmss parameters
        status_code, parameters = self.create_ss_parameters(create_configs, virtual_machine_profile)
        if status_code != AZURE_STATUS_OK:
            return status_code, parameters

        try:
            result = self.scale_set_client.create_or_update(resource_group_name=resource_group_name,
                                                            name=vm_scale_set_name,
                                                            parameters=parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def update(self, update_configs):
        """update a scale set"""
        resource_group_name = update_configs.get("resource_group_name", None)
        vm_scale_set_name = update_configs.get("vm_scale_set_name", None)
        if param_is_null([resource_group_name, vm_scale_set_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # check existence
        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        # os profile
        status_code, os_profile = self.create_ss_os_profile(update_configs)
        if status_code != AZURE_STATUS_OK:
            return status_code, os_profile

        # storage profile
        status_code, storage_profile = self.create_ss_storage_profile(update_configs)
        if status_code != AZURE_STATUS_OK:
            return status_code, storage_profile

        # network profile
        status_code, network_profile = self.create_ss_network_profile(update_configs)
        if status_code != AZURE_STATUS_OK:
            return status_code, network_profile

        # extension profile
        extension_profile = VirtualMachineScaleSetExtensionProfile(extensions=None)

        # vmss profile
        virtual_machine_profile = VirtualMachineScaleSetVMProfile(os_profile=os_profile,
                                                                  storage_profile=storage_profile,
                                                                  network_profile=network_profile,
                                                                  extension_profile=extension_profile)

        # vmss parameters
        status_code, parameters = self.create_ss_parameters(update_configs, virtual_machine_profile)
        if status_code != AZURE_STATUS_OK:
            return status_code, parameters

        try:
            result = self.scale_set_client.create_or_update(resource_group_name=resource_group_name,
                                                            name=vm_scale_set_name,
                                                            parameters=parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def update_configs(self, resource_group_name, vm_scale_set_name, parameters):
        """update scale set configs"""
        if param_is_null([resource_group_name, vm_scale_set_name, parameters]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.scale_set_client.create_or_update(resource_group_name=resource_group_name,
                                                            name=vm_scale_set_name,
                                                            parameters=parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get_instance_view(self, resource_group_name, vm_scale_set_name):
        """get scale set instance view"""
        if param_is_null([resource_group_name, vm_scale_set_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_client.get_instance_view(resource_group_name, vm_scale_set_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    @staticmethod
    def create_ss_os_profile(create_configs):
        """create os profile"""
        computer_name_prefix = create_configs.get("computer_name_prefix", None)
        admin_username = create_configs.get("admin_username", None)
        admin_password = create_configs.get("admin_password", None)
        custom_data = create_configs.get("custom_data", None)
        key_data = create_configs.get("key_data", None)
        if param_is_null([computer_name_prefix, admin_username]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        if custom_data is not None and custom_data != "":
            custom_data = base64.b64encode(custom_data)
        else:
            custom_data = None

        if param_is_null([admin_password]) and not param_is_null([key_data]):
            path = "/home/" + admin_username + "/.ssh/authorized_keys"
            public_key = SshPublicKey(path=path, key_data=key_data)
            ssh = SshConfiguration(public_keys=[public_key])
            linux_configuration = LinuxConfiguration(disable_password_authentication=True, ssh=ssh)
        elif not param_is_null([admin_password]) and param_is_null([key_data]):
            linux_configuration = None
        else:
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        os_profile = VirtualMachineScaleSetOSProfile(computer_name_prefix=computer_name_prefix,
                                                     admin_username=admin_username,
                                                     admin_password=admin_password,
                                                     custom_data=custom_data,
                                                     windows_configuration=None,
                                                     linux_configuration=linux_configuration,
                                                     secrets=None)
        return AZURE_STATUS_OK, os_profile

    @staticmethod
    def create_ss_network_profile(create_configs):
        """create network profile"""
        subscription_id = create_configs.get("subscription_id", None)
        scale_set_network_config_name = create_configs.get("scale_set_network_config_name", None)
        ss_net_primary = create_configs.get("scale_set_network_config_primary", None)
        scale_set_ip_config_name = create_configs.get("scale_set_ip_config_name", None)

        subnet_resource_group_name = create_configs.get("subnet_resource_group_name", None)
        subnet_virtual_network_name = create_configs.get("subnet_virtual_network_name", None)
        subnet_name = create_configs.get("subnet_name", None)

        bap_rg_name = create_configs.get("bap_resource_group_name", None)
        bap_lb_name = create_configs.get("bap_lb_name", None)
        bap_name = create_configs.get("bap_name", None)

        if param_is_null([subscription_id, scale_set_network_config_name, ss_net_primary,
                          scale_set_ip_config_name, subnet_resource_group_name, subnet_virtual_network_name,
                          subnet_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        subnet = ApiEntityReference(id=OPScaleSet.construct_subnet_id(subscription_id=subscription_id,
                                                                      resource_group_name=subnet_resource_group_name,
                                                                      virtual_network_name=subnet_virtual_network_name,
                                                                      subnet_name=subnet_name))

        if bap_rg_name is None or bap_rg_name == "":
            lb_baps = None
        else:
            lb_baps = []
            public_lb_enable = create_configs.get("public_lb_enable", None)
            if public_lb_enable == "true":
                load_balance_bap = SubResource(id=OPScaleSet.construct_bap_id(subscription_id,
                                                                              bap_rg_name,
                                                                              bap_lb_name,
                                                                              bap_name))
                pub_bap_lb_name = bap_lb_name + "-public"
                pub_load_balance_bap = SubResource(id=OPScaleSet.construct_bap_id(subscription_id,
                                                                                  bap_rg_name,
                                                                                  pub_bap_lb_name,
                                                                                  bap_name))
                lb_baps.append(load_balance_bap)
                lb_baps.append(pub_load_balance_bap)
            elif public_lb_enable == "only":
                pub_bap_lb_name = bap_lb_name + "-public"
                pub_load_balance_bap = SubResource(id=OPScaleSet.construct_bap_id(subscription_id,
                                                                                  bap_rg_name,
                                                                                  pub_bap_lb_name,
                                                                                  bap_name))
                lb_baps.append(pub_load_balance_bap)
            else:
                load_balance_bap = SubResource(id=OPScaleSet.construct_bap_id(subscription_id,
                                                                              bap_rg_name,
                                                                              bap_lb_name,
                                                                              bap_name))
                lb_baps.append(load_balance_bap)

        ip_conf = VirtualMachineScaleSetIPConfiguration(name=scale_set_ip_config_name,
                                                        subnet=subnet,
                                                        application_gateway_backend_address_pools=None,
                                                        load_balancer_backend_address_pools=lb_baps,
                                                        load_balancer_inbound_nat_pools=None)

        network_interface_configuration = VirtualMachineScaleSetNetworkConfiguration(name=scale_set_network_config_name,
                                                                                     ip_configurations=[ip_conf],
                                                                                     primary=ss_net_primary)
        network_profile = VirtualMachineScaleSetNetworkProfile([network_interface_configuration])
        return AZURE_STATUS_OK, network_profile

    @staticmethod
    def deprecated_storage_profile(create_configs):
        """create storage profile"""
        os_disk_name = create_configs.get("os_disk_name", None)
        os_type = create_configs.get("os_type", None)
        storage_account_name = create_configs.get("storage_account_name", None)
        container_name = create_configs.get("container_name", None)
        vhd_name = create_configs.get("vhd_name", None)

        if param_is_null([os_disk_name, os_type, storage_account_name, container_name, vhd_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        image = VirtualHardDisk(
            uri='https://{0}.blob.core.windows.net/{1}/{2}.vhd'.format(
                storage_account_name,
                container_name,
                vhd_name,
            )
        )

        create_option = DiskCreateOptionTypes.from_image
        caching = CachingTypes.none

        os_disk = VirtualMachineScaleSetOSDisk(name=os_disk_name,
                                               create_option=create_option,
                                               caching=caching,
                                               os_type=os_type,
                                               image=image,
                                               vhd_containers=None)

        storage_profile = VirtualMachineScaleSetStorageProfile(image_reference=None, os_disk=os_disk)
        return AZURE_STATUS_OK, storage_profile

    @staticmethod
    def create_ss_storage_profile(create_configs):
        """create storage profile"""
        subscription_id = create_configs.get("subscription_id", None)
        image_resource_group_name = create_configs.get("image_resource_group_name", None)
        image_name = create_configs.get("image_name", None)

        if param_is_null([subscription_id, image_resource_group_name, image_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        image_reference = ImageReference(OPScaleSet.construct_image_reference_id(subscription_id,
                                                                                 image_resource_group_name,
                                                                                 image_name))

        disk_size_gb = create_configs.get("data_disk_size", None)
        if param_is_null([disk_size_gb]):
            data_disks = None
        else:
            data_disk = VirtualMachineScaleSetDataDisk(lun=1, create_option="Empty", name=None, caching=None,
                                                       disk_size_gb=disk_size_gb, managed_disk=None)
            data_disks = [data_disk]
        storage_profile = VirtualMachineScaleSetStorageProfile(image_reference=image_reference, os_disk=None,
                                                               data_disks=data_disks)
        return AZURE_STATUS_OK, storage_profile

    @staticmethod
    def create_ss_parameters(create_configs, virtual_machine_profile):
        """create scale set parameter object"""
        location = create_configs.get("location", None)
        sku_name = create_configs.get("sku_name", None)
        sku_capacity = create_configs.get("sku_capacity", None)
        upgrade_policy = create_configs.get("upgrade_policy", None)
        over_provision = create_configs.get("over_provision", None)
        tags = create_configs.get("tags", None)
        if param_is_null([location, sku_name, sku_capacity, upgrade_policy, over_provision]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        sku = Sku(name=sku_name, capacity=sku_capacity)
        upgrade_policy = UpgradePolicy(mode=upgrade_policy)

        parameters = VirtualMachineScaleSet(location=location,
                                            tags=tags,
                                            sku=sku,
                                            upgrade_policy=upgrade_policy,
                                            virtual_machine_profile=virtual_machine_profile,
                                            overprovision=over_provision)
        return AZURE_STATUS_OK, parameters

    @staticmethod
    def construct_subnet_id(subscription_id, resource_group_name, virtual_network_name, subnet_name):
        """construct subnet id"""
        return ('/subscriptions/{}'
                '/resourceGroups/{}'
                '/providers/Microsoft.Network'
                '/virtualNetworks/{}'
                '/subnets/{}').format(
                    subscription_id, resource_group_name, virtual_network_name, subnet_name
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
    def construct_image_reference_id(subscription_id, resource_group_name, image_name):
        """construct image id"""
        return ('/subscriptions/{}'
                '/resourceGroups/{}'
                '/providers/Microsoft.Compute'
                '/images/{}').format(
                    subscription_id, resource_group_name, image_name
                )
