from mock import patch

from .attr_dict import AttrDict, OrderedAttrDict
from .attr_lookup import deep_getattr
from .base import import_module
from .registry import Registry

__all__ = ['deep_getattr', 'import_module', 'patch', 'AttrDict', 'OrderedAttrDict', 'Registry']
