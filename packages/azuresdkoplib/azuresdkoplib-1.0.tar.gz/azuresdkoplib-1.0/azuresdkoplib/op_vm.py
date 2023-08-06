# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_vm.py
@time: 2016/12/14 16:25
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.compute.models import OSProfile
from azure.mgmt.compute.models import HardwareProfile
from azure.mgmt.compute.models import NetworkProfile
from azure.mgmt.compute.models import StorageProfile
from azure.mgmt.compute.models import VirtualMachine
from azure.mgmt.compute.models import ImageReference
from azure.mgmt.compute.models import NetworkInterfaceReference
from azure.mgmt.compute.models import VirtualMachineCaptureParameters
from azure.mgmt.compute.models import LinuxConfiguration
from azure.mgmt.compute.models import SshConfiguration
from azure.mgmt.compute.models import SshPublicKey
from msrestazure.azure_exceptions import CloudError

from op_resource_group import OPResourceGroup
from op_nic import OPNic
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST, AZURE_STATUS_RES_EXIST, \
    AZURE_INFO_VM_EXIST


class OPVirtualMachine(object):
    """azure virtual machine wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.compute_client = ComputeManagementClient(credentials, subscription_id)
        self.vm_client = self.compute_client.virtual_machines

    def list_all(self):
        """list all vms"""
        try:
            result = self.vm_client.list_all()
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_by_resource_group(self, resource_group_name):
        """list all vms in a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.vm_client.list(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, vm_name):
        """check a vm if exist"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_by_resource_group(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == vm_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, vm_name):
        """get a vm object"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        try:
            result = self.vm_client.get(resource_group_name, vm_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get_instance_view(self, resource_group_name, vm_name):
        """get a vm instance view"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        try:
            result = self.vm_client.get(resource_group_name, vm_name, expand='instanceview')
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def generalize(self, resource_group_name, vm_name):
        """generalize a vm"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        try:
            result = self.vm_client.generalize(resource_group_name, vm_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def capture(self, capture_configs):
        """capture from a generalized vm"""
        resource_group_name = capture_configs.get("resource_group_name", None)
        vm_name = capture_configs.get("vm_name", None)
        vhd_prefix = capture_configs.get("vhd_prefix", None)
        destination_container_name = capture_configs.get("destination_container_name", None)
        if param_is_null([resource_group_name, vm_name, vhd_prefix, destination_container_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        parameters = VirtualMachineCaptureParameters(vhd_prefix=vhd_prefix,
                                                     destination_container_name=destination_container_name,
                                                     overwrite_vhds=False)

        try:
            result = self.vm_client.capture(resource_group_name, vm_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete(self, resource_group_name, vm_name):
        """delete a vm"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        try:
            result = self.vm_client.delete(resource_group_name, vm_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def deallocate(self, resource_group_name, vm_name):
        """deallocate a vm"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        try:
            result = self.vm_client.deallocate(resource_group_name, vm_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def power_off(self, resource_group_name, vm_name):
        """power off a vm"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        try:
            result = self.vm_client.power_off(resource_group_name, vm_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def restart(self, resource_group_name, vm_name):
        """restart a vm"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        try:
            result = self.vm_client.restart(resource_group_name, vm_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def start(self, resource_group_name, vm_name):
        """start a vm"""
        if param_is_null([resource_group_name, vm_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VM_NOT_EXIST

        try:
            result = self.vm_client.start(resource_group_name, vm_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def create(self, create_configs):
        """create a vm"""
        resource_group_name = create_configs.get("resource_group_name", None)
        vm_name = create_configs.get("vm_name", None)
        location = create_configs.get("location", None)
        if param_is_null([resource_group_name, vm_name, location]):
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
        status_code, result = self.check_existence(resource_group_name, vm_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_VM_EXIST

        # os profile
        computer_name = create_configs.get("computer_name", None)
        admin_username = create_configs.get("admin_username", None)
        admin_password = create_configs.get("admin_password", None)
        custom_data = create_configs.get("custom_data", None)
        key_data = create_configs.get("key_data", None)
        if param_is_null([computer_name, admin_username]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        if param_is_null([admin_password]) and not param_is_null([key_data]):
            path = "/home/" + admin_username + "/.ssh/authorized_keys"
            public_key = SshPublicKey(path=path, key_data=key_data)
            ssh = SshConfiguration(public_keys=[public_key])
            linux_configuration = LinuxConfiguration(disable_password_authentication=True, ssh=ssh)
        elif not param_is_null([admin_password]) and param_is_null([key_data]):
            linux_configuration = None
        else:
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        os_profile = OSProfile(computer_name=computer_name,
                               admin_username=admin_username,
                               admin_password=admin_password,
                               custom_data=custom_data,
                               windows_configuration=None,
                               linux_configuration=linux_configuration,
                               secrets=None)

        # vm size
        vm_size = create_configs.get("vm_size", None)
        if param_is_null([vm_size]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
        hardware_profile = HardwareProfile(vm_size=vm_size)

        # network
        nic_resource_group = create_configs.get("nic_resource_group", None)
        nic_name = create_configs.get("nic_name", None)
        if param_is_null([nic_resource_group, nic_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_nic = OPNic(self.subscription_id, self.user_name, self.password)
        status_code, nic = op_nic.get(nic_resource_group, nic_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, nic
        primary = True
        network_interfaces = [NetworkInterfaceReference(id=nic.id, primary=primary)]
        network_profile = NetworkProfile(network_interfaces=network_interfaces)

        # image
        subscription_id = create_configs.get("subscription_id", None)
        image_resource_group_name = create_configs.get("image_resource_group_name", None)
        image_name = create_configs.get("image_name", None)

        if param_is_null([subscription_id, image_resource_group_name, image_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # image
        image_reference = ImageReference(OPVirtualMachine.construct_image_reference_id(subscription_id,
                                                                                       image_resource_group_name,
                                                                                       image_name))
        storage_profile = StorageProfile(image_reference=image_reference)

        # vm parameters
        parameters = VirtualMachine(location=location,
                                    plan=None,
                                    hardware_profile=hardware_profile,
                                    storage_profile=storage_profile,
                                    os_profile=os_profile,
                                    network_profile=network_profile,
                                    diagnostics_profile=None,
                                    availability_set=None)
        try:
            result = self.vm_client.create_or_update(resource_group_name, vm_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    @staticmethod
    def construct_image_reference_id(subscription_id, resource_group_name, image_name):
        """construct image id"""
        return ('/subscriptions/{}'
                '/resourceGroups/{}'
                '/providers/Microsoft.Compute'
                '/images/{}').format(
                    subscription_id, resource_group_name, image_name
                )
