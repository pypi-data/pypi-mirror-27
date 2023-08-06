from collections import OrderedDict


class AttrDict(dict):
    """A dictionary with attribute access for keys."""

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state


class OrderedAttrDict(object):
    """Dict-like object that can be accessed by attributes

    Examples:
       >>> obj = AttrDict()
       >>> obj['test'] = 'hi'
       >>> print obj.test
       hi
       >>> del obj.test
       >>> obj.test = 'bye'
       >>> print obj['test']
       bye
       >>> print len(obj)
       1
       >>> obj.clear()
       >>> print len(obj)
       0
       """

    def __init__(self, *args, **kwargs):
        self._od = OrderedDict(*args, **kwargs)

    def __getattr__(self, name):
        return self._od[name]

    def __setattr__(self, name, value):
        if name == '_od':
            self.__dict__['_od'] = value
        else:
            self._od[name] = value

    def __delattr__(self, name):
        del self._od[name]

    def iteritems(self):
        return self._od.iteritems()
