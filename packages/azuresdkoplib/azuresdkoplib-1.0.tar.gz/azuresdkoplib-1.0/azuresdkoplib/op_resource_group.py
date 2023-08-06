# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_resource_group.py
@time: 2016/12/14 16:25
"""

from azure.mgmt.resource.resources import ResourceManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.resource.resources.models import ResourceGroup
from msrestazure.azure_exceptions import CloudError

from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, AZURE_STATUS_CLOUD_ERROR, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST, AZURE_STATUS_RES_EXIST, AZURE_INFO_RG_EXIST
from op_func import param_is_null


class OPResourceGroup(object):
    """azure resource group sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.resource_client = ResourceManagementClient(credentials, subscription_id)
        self.resource_group_client = self.resource_client.resource_groups

    def list_all_resource_group(self):
        """list all resource groups"""
        try:
            result = self.resource_group_client.list()
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name):
        """check a resource group if exists"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.resource_group_client.check_existence(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get(self, resource_group_name):
        """get a resource group object"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.resource_group_client.get(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_resources(self, resource_group_name):
        """list all resources in a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.resource_group_client.list_resources(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def create(self, resource_group_name, location):
        """create a resource group"""
        if param_is_null([resource_group_name, location]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_RG_EXIST

        parameters = ResourceGroup(location=location)
        try:
            result = self.resource_group_client.create_or_update(resource_group_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete(self, resource_group_name):
        """delete a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.resource_group_client.delete(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result
