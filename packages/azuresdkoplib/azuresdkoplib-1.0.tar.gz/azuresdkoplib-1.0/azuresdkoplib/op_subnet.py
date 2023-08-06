# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_subnet.py
@time: 2016/12/14 18:02
"""

from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import UserPassCredentials
from azure.mgmt.network.models import Subnet
from msrestazure.azure_exceptions import CloudError

from op_virtual_network import OPVirtualNetwork
from op_func import param_is_null
from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL, \
    AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VN_NOT_EXIST, AZURE_INFO_SUBNET_NOT_EXIST, AZURE_STATUS_RES_EXIST, \
    AZURE_INFO_SUBNET_EXIST


class OPSubnet(object):
    """azure subnet sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.network_client = NetworkManagementClient(credentials, subscription_id)
        self.subnet_client = self.network_client.subnets

    def list(self, resource_group_name, virtual_network_name):
        """list all subnets in a virtual network"""
        if param_is_null([resource_group_name, virtual_network_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        op_virtual_network = OPVirtualNetwork(self.subscription_id, self.user_name, self.password)
        status_code, result = op_virtual_network.check_existence(resource_group_name, virtual_network_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result
        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_VN_NOT_EXIST

        try:
            result = self.subnet_client.list(resource_group_name, virtual_network_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def check_existence(self, resource_group_name, virtual_network_name, subnet_name):
        """check a subnet if exit"""
        if param_is_null([resource_group_name, virtual_network_name, subnet_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.list(resource_group_name, virtual_network_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        try:
            for item in result:
                if item.name == subnet_name:
                    return AZURE_STATUS_OK, True
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, False

    def get(self, resource_group_name, virtual_network_name, subnet_name):
        """get a subnet object"""
        if param_is_null([resource_group_name, virtual_network_name, subnet_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, virtual_network_name, subnet_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SUBNET_NOT_EXIST

        try:
            result = self.subnet_client.get(resource_group_name, virtual_network_name, subnet_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def create(self, resource_group_name, virtual_network_name, subnet_name, address_prefix):
        """create a subnet"""
        if param_is_null([resource_group_name, virtual_network_name, subnet_name, address_prefix]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, virtual_network_name, subnet_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is True:
            return AZURE_STATUS_RES_EXIST, AZURE_INFO_SUBNET_EXIST

        subnet_parameters = Subnet(address_prefix=address_prefix)
        try:
            result = self.subnet_client.create_or_update(resource_group_name,
                                                         virtual_network_name,
                                                         subnet_name,
                                                         subnet_parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    # async
    def delete(self, resource_group_name, virtual_network_name, subnet_name):
        """delete a subnet"""
        if param_is_null([resource_group_name, virtual_network_name, subnet_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        status_code, result = self.check_existence(resource_group_name, virtual_network_name, subnet_name)
        if status_code != AZURE_STATUS_OK:
            return status_code, result

        if result is False:
            return AZURE_STATUS_RES_NOT_EXIST, AZURE_INFO_SUBNET_NOT_EXIST

        try:
            result = self.subnet_client.delete(resource_group_name, virtual_network_name, subnet_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result
