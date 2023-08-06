# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_storage.py
@time: 2016/12/14 16:25
"""

from azure.mgmt.storage import StorageManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.storage.models import StorageAccountCreateParameters
from azure.mgmt.storage.models import Kind, SkuName
from azure.mgmt.storage.models import Sku
from msrestazure.azure_exceptions import CloudError

from op_resource_group import OPResourceGroup
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST, AZURE_INFO_STORAGE_EXIST, AZURE_INFO_RG_EXIST, \
    AZURE_INFO_STORAGE_NOT_EXIST


class OPStorage(object):
    """azure storage sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.storage_management_client = StorageManagementClient(credentials, subscription_id)
        self.storage_client = self.storage_management_client.storage_accounts

    def list(self):
        """list all storage"""
        try:
            result = self.storage_client.list()
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def list_by_resource_group(self, resource_group_name):
        """list all storage in a resource group"""
        if param_is_null([resource_group_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_resource_group = OPResourceGroup(self.subscription_id, self.user_name, self.password)
        status_code, result = op_resource_group.check_existence(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_RG_NOT_EXIST

        try:
            result = self.storage_client.list_by_resource_group(resource_group_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, storage_account_name):
        """check a storage account if exit"""
        if param_is_null([resource_group_name, storage_account_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list_by_resource_group(resource_group_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == storage_account_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

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

    # async
    def create(self, create_configs):
        """create a storage account"""
        resource_group_name = create_configs.get("resource_group_name", None)
        location = create_configs.get("location", None)
        storage_account_name = create_configs.get("storage_account_name", None)

        if param_is_null([resource_group_name, location, storage_account_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        # pre-create resource group
        status_code, result = self._pre_create_rg(resource_group_name, location)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        status_code, result = self.check_existence(resource_group_name, storage_account_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is True:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_STORAGE_EXIST

        sku = Sku(name=SkuName.standard_lrs)
        kind = Kind.storage
        parameters = StorageAccountCreateParameters(sku, kind, location)
        try:
            result = self.storage_client.create(resource_group_name, storage_account_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def delete(self, resource_group_name, storage_account_name):
        """delete a storage account"""
        if param_is_null([resource_group_name, storage_account_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, storage_account_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_STORAGE_NOT_EXIST

        try:
            result = self.storage_client.delete(resource_group_name, storage_account_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get(self, resource_group_name, storage_account_name):
        """get a storage account"""
        if param_is_null([resource_group_name, storage_account_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, storage_account_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_STORAGE_NOT_EXIST

        try:
            result = self.storage_client.get_properties(resource_group_name, storage_account_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def update(self, resource_group_name, account_name, parameters):
        """update a storage account"""
        pass
