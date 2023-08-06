# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_ss_vm.py
@time: 2016/10/31 15:04
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import UserPassCredentials
from msrestazure.azure_exceptions import CloudError

from op_scale_set import OPScaleSet
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST


class OPScaleSetVM(object):
    """azure scale set vm sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.compute_client = ComputeManagementClient(credentials, subscription_id)
        self.scale_set_vm_client = self.compute_client.virtual_machine_scale_set_vms

    def list_vms_by_scale_set(self, resource_group_name, vm_scale_set_name):
        """list all vms in a scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_scale_set = OPScaleSet(self.subscription_id, self.user_name, self.password)
        status_code, result = op_scale_set.check_existence(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_NOT_EXIST

        try:
            result = self.scale_set_vm_client.list(resource_group_name, vm_scale_set_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, vm_scale_set_name, instance_id):
        """check vm scale set instance if exist"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_vms_by_scale_set(resource_group_name, vm_scale_set_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.instance_id == instance_id:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, vm_scale_set_name, instance_id):
        """get a instance from vm scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name, instance_id)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST

        try:
            result = self.scale_set_vm_client.get(resource_group_name, vm_scale_set_name, instance_id)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get_instance_view(self, resource_group_name, vm_scale_set_name, instance_id):
        """get a instance view from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name, instance_id)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST

        try:
            result = self.scale_set_vm_client.get_instance_view(resource_group_name, vm_scale_set_name, instance_id)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def deallocate(self, resource_group_name, vm_scale_set_name, instance_id):
        """deallocate instance from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name, instance_id)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST

        try:
            result = self.scale_set_vm_client.deallocate(resource_group_name, vm_scale_set_name, instance_id)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete(self, resource_group_name, vm_scale_set_name, instance_id):
        """delete instance from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name, instance_id)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST

        try:
            result = self.scale_set_vm_client.delete(resource_group_name, vm_scale_set_name, instance_id)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def power_off(self, resource_group_name, vm_scale_set_name, instance_id):
        """power off instance from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name, instance_id)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST

        try:
            result = self.scale_set_vm_client.power_off(resource_group_name, vm_scale_set_name, instance_id)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def restart(self, resource_group_name, vm_scale_set_name, instance_id):
        """restart instance from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name, instance_id)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST

        try:
            result = self.scale_set_vm_client.restart(resource_group_name, vm_scale_set_name, instance_id)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def start(self, resource_group_name, vm_scale_set_name, instance_id):
        """start instance from scale set"""
        if param_is_null([resource_group_name, vm_scale_set_name, instance_id]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, vm_scale_set_name, instance_id)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SS_VM_NOT_EXIST

        try:
            result = self.scale_set_vm_client.start(resource_group_name, vm_scale_set_name, instance_id)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result
