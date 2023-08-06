# coding=utf-8
"""
Miscellaneous text utility functions
"""
from __future__ import unicode_literals

import re

RE_CAMEL_CASE = re.compile(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')


def camel_case_to_spaces(value):
    """
    Splits CamelCase and converts to lower case. Also strips leading and
    trailing whitespace.

    Examples:
        >>> print(camel_case_to_spaces('Device Type'))
        device type
    """
    return RE_CAMEL_CASE.sub(r'\1', value).strip().lower()


def camel_case_to_underscore(value):
    """
    Splits CamelCase and converts to lower case. Also strips leading and
    trailing whitespace.

    Examples:
        >>> print(camel_case_to_underscore('Device Type'))
        device_type
    """
    return RE_CAMEL_CASE.sub(r'\1', value).strip().lower().replace(" ", "_").lower()


def replace_path_chars(path):
    """

    utility to replace graphite path chars

    Examples:
        >>> print(replace_path_chars('|T/e s.t'))
        _T_e_s_t
    """
    if not path:
        return path
    return path.replace('.', '_').replace('|', '_').replace('/', '_').replace(' ', '_')


def tr2en(text, uppercase=False, underscore=False):
    """
    replaces TR chars

    Examples:
        >>> print(tr2en('Üsküdar Beşiktaş Kadıköy', uppercase=True, underscore=True))
        USKUDAR_BESIKTAS_KADIKOY
    """

    try:
        basestring
    except NameError:
        basestring = str  # py3

    _atypes = {basestring, unicode}

    if not text or not type(text) in _atypes:
        return text

    dic = {
        u'ç': 'c',
        u'ğ': 'g',
        u'Ç': 'C',
        u'Ğ': 'G',
        u'ı': 'i',
        u'İ': 'I',
        u'ö': 'o',
        u'Ö': 'O',
        u'ş': 's',
        u'Ş': 'S',
        u'ü': 'u',
        u'Ü': 'U',
    }

    try:
        values = dic.iteritems()
    except AttributeError:
        values = dic.items()  # py3

    for k, v in values:
        text = text.replace(k, v)

    text = text.replace(" ", "_") if underscore else text
    return text.upper() if uppercase else text
