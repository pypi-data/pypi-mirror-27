# -*- coding: utf-8 -*-
"""
 Created on 07.01.2017 and created by ramazan
 """
from __future__ import absolute_import

__author__ = 'ramazan'


def string_to_pretty_json_or_xml(input_string=None, encode='UTF-8'):
    """
        format given string to xml or json
    :param input_string:
    :param encode:
    :return:
    """
    if input_string:
        input_string = input_string.encode(encode)
        if input_string.startswith('{'): ## if json
            return string_to_pretty_json(input_string)
        elif input_string.startswith('<'): # if xml
            return string_to_pretty_xml(input_string)

    return input_string # any case return default


def string_to_pretty_xml(input_string=None, encode='UTF-8'):
    """
        format string to xml
    :param input_string:
    :param encode:
    :return: formatting string
    """
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(input_string)
    return xml.toprettyxml()


def string_to_pretty_json(input_string):
    """
        format string to json
    :param input_string:
    :return: formatting string in json
    """
    import json
    parsed = json.loads(input_string)
    return json.dumps(parsed, indent=4, sort_keys=True)