# -*- coding: utf-8 -*-

#  unicum
#  ------------
#  Simple object cache and __factory.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Copyright: 2016, 2017 Deutsche Postbank AG
#  Website: https://github.com/pbrisk/unicum
#  License: APACHE Version 2 License (see LICENSE file)


import json


def load_json_dicts(file_name):
    """
    Loads the json dictionary from the given file.
    """
    file_text = '{todo:"todovalue"}' #read_file_text(file_name) todo
    ret = parse_json_str(file_text)
    return ret

def parse_json_str(json_str):
    """
    Parses the given json string in a dictionary.
    """
    return json.loads(json_str, object_hook=decode_dict)


def decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
            if type(item) == type(""):
                if not item.isdigit():
                    try:
                        item = float(item)
                    except:
                        item = item
        elif isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv


def decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        rv[key] = value
    return rv


class NestedList(list):

    def __init__(self, iterable=[]):
        if iterable:
            super(NestedList, self).__init__([iterable])
        else:
            super(NestedList, self).__init__([])


class NestedListEncoder(json.JSONEncoder):
    @staticmethod
    def _is_nested_list(obj):
        return all(isinstance(o, list) for o in obj) if isinstance(obj, list) else False

    def default(self, obj):
        if isinstance(obj, NestedList):
            return ',\n'.join([json.JSONEncoder().encode(o) for o in obj])
        return json.JSONEncoder.default(self, obj)

    def encode(self, obj):
        if self._is_nested_list(obj):
            return ',\n'.join([json.JSONEncoder().encode(o) for o in obj])
        # Let the base class default method raise the TypeError
        s = super(NestedListEncoder, self).encode(obj)
        return s

    def iterencode(self, obj, _one_shot=True):
        if self._is_nested_list(obj):
            return ',\n'.join([json.JSONEncoder().encode(o) for o in obj])
        # Let the base class default method raise the TypeError
        s = super(NestedListEncoder, self).iterencode(obj, 1)
        return s
