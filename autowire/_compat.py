"""
_compat
=======

Compatability support

"""
import abc
import sys
import typing

MAJOR, MINOR = sys.version_info[:2]
PY33 = MAJOR == 3 and MINOR >= 3
PY35 = MAJOR == 3 and MINOR >= 5


# abc.abstractproperty was deprecated since Python 3.3
if PY33:
    def abstractproperty(getter):
        return property(abc.abstractmethod(getter))
else:
    abstractproperty = abc.abstractproperty


ContextManger = getattr(typing, 'ContextManager', typing.Any)
