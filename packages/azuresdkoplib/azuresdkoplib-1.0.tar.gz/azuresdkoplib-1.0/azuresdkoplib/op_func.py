# encoding: utf-8

"""
@version: 1.0
@author: sam
@license: Apache Licence
@file: op_func.py
@time: 2017/1/5 10:46
"""

import re
import json


def param_is_null(param_list):
    """check param is null or not

    :param param_list: param list
    :type param_list: list
    :rtype: boolean
    """
    if not param_list:
        return True
    for item in param_list:
        if item is None or item == "":
            return True
    return False


def read_json_config(json_file_path):
    """read json from a file

    :param json_file_path: read json file path
    :type json_file_path: str
    :rtype: json object
    """
    with open(json_file_path, 'r') as json_file:
        json_result = json.load(json_file)
    return json_result


def write_json_config(json_config, json_file_path):
    """write json to a file

    :param json_config: json object to write
    :type json_config: json object
    :param json_file_path: file path to write
    :type json_file_path: str
    :rtype: None
    """
    with open(json_file_path, 'w') as json_file:
        json_file.write(json.dumps(json_config, indent=4))
    return None


def replace_tag(target_json_file, tag_json):
    """replace tag '@...@' in template file

    :param target_json_file: template json file
    :type target_json_file: str
    :param tag_json: json contains tag and value
    :type tag_json: json object
    :rtype: json object
    """
    with open(target_json_file) as target_file:
        target_string = target_file.read()
        tag_set = set(re.findall('@(.+?)@', target_string))

        for tag in tag_set:
            tag_value = tag_json.get(tag, "")
            replace_target = "@" + tag + "@"
            if isinstance(tag_value, list) or isinstance(tag_value, dict):
                tag_value = json.dumps(tag_value)
                replace_target = "\"" + replace_target + "\""
            target_string = target_string.replace(replace_target, str(tag_value))

        return json.loads(target_string)


def merge_all_info(template_file, role_file, common_file):
    """generate server role info

    :param template_file: template file path
    :type template_file: str
    :param role_file: role file path
    :type template_file: str
    :param common_file: common file path
    :type template_file: str
    :rtype: json object
    """
    with open(common_file) as common_f:
        common_string = common_f.read()
        common_json = json.loads(common_string)

    role_json = replace_tag(role_file, common_json)
    all_tag_json = dict(common_json.items() + role_json.items())
    template_json = replace_tag(template_file, all_tag_json)

    return template_json
