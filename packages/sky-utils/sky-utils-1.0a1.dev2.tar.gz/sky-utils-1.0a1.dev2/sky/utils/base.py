"""
Miscellaneous base utility functions
"""
import importlib
import logging


def import_module(val, raise_exception=True):
    """
    Attempt to import a class from a string representation.
    copied from: djang_rest_framework
            (https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/settings.py#L169)

    modified to raise exception by default

    Args:
        raise_exception: boolean to declare if method should return None or raise exception
        val: string representation of a class to import
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s'. %s: %s." % (val, e.__class__.__name__, e)
        logging.warning(ImportError(msg))
        if raise_exception:
            raise ImportError(msg)
    return None
