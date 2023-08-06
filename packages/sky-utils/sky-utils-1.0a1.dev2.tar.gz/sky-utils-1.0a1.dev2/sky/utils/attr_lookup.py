"""
Deep attribute lookup
>> deep_getattr(obj,'attribute__attribute1__attribute2')
"""


def getattr_with_default(object, name, default=None):
    if hasattr(object, name):
        return getattr(object, name, default)
    else:
        return default


def deep_getattr(obj, attr, separator='__'):
    return reduce(getattr_with_default, attr.split(separator), obj)