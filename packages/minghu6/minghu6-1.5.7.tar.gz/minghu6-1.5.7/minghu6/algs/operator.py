# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""

from .var import isiterable, get_typename_str

__all__ = ['getitem', 'pow', 'add', 'sub', 'neg']


def getitem(iterable, index, default=None):
    """ Golang style operation """

    if not isiterable(iterable) or not hasattr(iterable, '__getitem__'):
        type_name = get_typename_str(iterable)
        raise TypeError('{0} object is not iterable'.format(type_name))

    if isinstance(index, int):
        pass

    elif isinstance(index, slice):
        pass

    else:
        type_name = get_typename_str(iterable)
        raise TypeError('{0} object is not slice or int'.format(type_name))

    result = default
    try:
        result = iterable[index]

    except TypeError:  # don't have property __getitem__

        if isinstance(index, slice):
            result = list(iterable)[index]

        elif isinstance(index, int):
            if index < 0:
                result = list(iterable)[index]
            else:

                for i, elem in enumerate(iterable):
                    if index == i:
                        result = elem
                        break

            return result

    except IndexError:

        return result  # default

    except Exception:
        raise

    else:
        return result


add = lambda x, y: x + y
sub = lambda x, y: x - y
neg = lambda x: -x


def c_not(n: int):
    if int(n) == 0:
        return 1
    else:
        return 0


def pow(x, y, z=None):
    return __builtins__['pow'](x, y, z)
