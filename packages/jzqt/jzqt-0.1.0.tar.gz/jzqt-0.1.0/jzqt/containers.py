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
