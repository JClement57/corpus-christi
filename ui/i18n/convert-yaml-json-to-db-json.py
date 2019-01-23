#! /usr/bin/env python3

import json
import sys

def get_json_object_from_file(file_name):
    json_string = None
    with open(file_name, 'r') as f:
        json_string = f.read()
    return json.loads(json_string)

def write_json_object_to_file(json_object, file_name):
    json_string = json.dumps(json_object)
    with open(file_name, 'w') as f:
        f.write(json_string)

def convert_yaml_format_to_db_format(i18n_object):
    return_object = dict()
    for locale_code, key_dict in i18n_object.items():
        return_object[locale_code] = dict()
        traverse_object_hierarchy(key_dict, locale_code, return_object[locale_code])
    return return_object

def traverse_object_hierarchy(i18n_object, locale_code, return_object, string_prefix=''):
    for key, val in i18n_object.items():
        new_prefix = string_prefix + key
        if isinstance(val, dict):
            new_prefix += '.'
            traverse_object_hierarchy(val, locale_code, return_object, new_prefix)
        else:
            return_object[new_prefix] = dict()
            return_object[new_prefix]['value'] = val
            return_object[new_prefix]['description'] = ''

if __name__ == '__main__':
    input_object = get_json_object_from_file(sys.argv[1])
    converted_object = convert_yaml_format_to_db_format(input_object)
    write_json_object_to_file(converted_object, (sys.argv[2] or sys.stdout))