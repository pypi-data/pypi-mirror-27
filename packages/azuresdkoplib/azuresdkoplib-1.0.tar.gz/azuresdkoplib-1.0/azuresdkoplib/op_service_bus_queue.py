# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_service_bus_queue.py
@time: 2016/12/14 16:25
"""

from azure.mgmt.servicebus.service_bus_management_client import ServiceBusManagementClient
from azure.common.credentials import UserPassCredentials
from msrestazure.azure_exceptions import CloudError

from op_status_code import AZURE_STATUS_OK, AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL
from op_func import param_is_null


class OPServiceBusQueue(object):
    """azure service bus sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.sb_client = ServiceBusManagementClient(credentials, subscription_id)
        self.sb_queue_client = self.sb_client.queues

    def list_all(self, resource_group_name, namespace_name):
        """list all service bus"""
        if param_is_null([resource_group_name, namespace_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.sb_queue_client.list_all(resource_group_name, namespace_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def create_or_update(self, resource_group_name, namespace_name, queue_name, parameters):
        """create or update service bus"""
        if param_is_null([resource_group_name, namespace_name, parameters]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.sb_queue_client.create_or_update(resource_group_name, namespace_name, queue_name, parameters)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def delete(self, resource_group_name, namespace_name, queue_name):
        """delete service bus queue"""
        if param_is_null([resource_group_name, namespace_name, queue_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.sb_queue_client.delete(resource_group_name, namespace_name, queue_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get(self, resource_group_name, namespace_name, queue_name):
        """get a service bus queue object"""
        if param_is_null([resource_group_name, namespace_name, queue_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            result = self.sb_queue_client.get(resource_group_name, namespace_name, queue_name)
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, result

    def get_message_count_detail(self, resource_group_name, namespace_name, queue_name):
        """get service bus queue message detail info"""
        if param_is_null([resource_group_name, namespace_name, queue_name]):
            return AZURE_STATUS_PARAM_NULL, AZURE_INFO_PARAM_NULL

        try:
            queue_resource = self.sb_queue_client.get(resource_group_name, namespace_name, queue_name)
            message_count_detail = queue_resource.count_details
        except CloudError as cloud_error:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error.message
        return AZURE_STATUS_OK, message_count_detail
