# coding: utf-8
"""Container data type"""


class ObjectDict(dict):
    """Dict subclass for support attribute style access.

    >>> from jzqt.containers import ObjectDict
    >>> obj = ObjectDict({'name': 'JZQT'})
    >>> obj.name
    'JZQT'
    >>> obj['name']
    'JZQT'
    >>> obj.get('name')
    'JZQT'
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)


class FrozenDict(dict):
    """Immutable dict."""

    def __setitem__(self, key, value):
        """Not implemented."""
        raise NotImplementedError('FrozenDict.__setitem__')

    def __delitem__(self, key):
        """Not implemented."""
        raise NotImplementedError('FrozenDict.__delitem__')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ''.join(('FrozenDict(', super(FrozenDict, self).__repr__(), ')'))

    def clear(self):
        """Not implemented."""
        raise NotImplementedError('FrozenDict.clear')

    def copy(self):
        return FrozenDict(super(FrozenDict, self).copy())

    @staticmethod
    def fromkeys(iterable, value=None):
        """Returns a new FrozenDict with keys from iterable and values equal to value."""
        return FrozenDict(dict.fromkeys(iterable, value))

    def pop(self, k, d=None):
        """Not implemented."""
        raise NotImplementedError('FrozenDict.pop')

    def popitem(self):
        """Not implemented."""
        raise NotImplementedError('FrozenDict.popitem')

    def setdefault(self, k, d=None):
        """Not implemented."""
        raise NotImplementedError('FrozenDict.setdefault')

    def update(self, *args, **kwargs):
        """Not implemented."""
        raise NotImplementedError('FrozenDict.update')
