# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_image.py
@time: 2016/12/14 16:25
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import UserPassCredentials
from msrestazure.azure_exceptions import CloudError

from op_status_code import AZURE_STATUS_CLOUD_ERROR, AZURE_STATUS_OK


class OPImage(object):
    """azure image sdk wrap class"""
    def __init__(self, subscription_id, user_name, password):
        self.subscription_id = subscription_id
        self.user_name = user_name
        self.password = password
        credentials = UserPassCredentials(user_name, password)
        self.compute_client = ComputeManagementClient(credentials, subscription_id)
        self.image_client = self.compute_client.images

    def list(self):
        """list all available images

        :rtype: int, :class:`ImagePaged <azure.mgmt.compute.models.ImagePaged>`
        """
        try:
            result = self.image_client.list()
        except CloudError as cloud_error_exception:
            return AZURE_STATUS_CLOUD_ERROR, cloud_error_exception.message
        return AZURE_STATUS_OK, result
