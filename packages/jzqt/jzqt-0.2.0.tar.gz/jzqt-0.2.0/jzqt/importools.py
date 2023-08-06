# coding: utf-8
"""Import related tools"""


def import_object(name):
    """Imports an object by name.

    ``import_object('a')`` is equivalent to ``import a``.

    ``import_object('a.b.c')`` is equivalent to ``from a.b import c``.

    >>> import os.path
    >>> import_object('os') is os
    True
    >>> import_object('os.path') is os.path
    True
    >>> import_object('os.path.dirname') is os.path.dirname
    True
    >>> import_object('os.path.object_not_exist')
    Traceback (most recent call last):
        ......
    ImportError: cannot from os.path import not_exist
    """
    if '.' not in name:
        return __import__(name, None, None)
    f, i = name.rsplit('.', 1)
    module_object = __import__(f, None, None, [i], 0)
    try:
        return getattr(module_object, i)
    except AttributeError:
        raise ImportError("cannot from {} import {}".format(f, i))
