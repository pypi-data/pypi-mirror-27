# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: setup.py
@time: 2017/1/4 20:30
"""

from setuptools import setup, find_packages

setup(
    name='azuresdkoplib',
    version='1.0',
    description='azure python sdk op wrap lib',
    author='Sam',
	author_email='samrui0129@gmail.com',
	url='https://github.com/r00219985/azure-sdk-op-lib',
    packages=find_packages(),
    install_requires=['jmespath>0.7'],
    include_package_data=True,
    zip_safe=False,
)
