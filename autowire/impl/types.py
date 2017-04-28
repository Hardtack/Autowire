"""
impl.types
==========

Types for implementation.

"""
import abc
import types

from autowire._compat import PY35

if PY35:
    import typing

    from autowire.base import BaseContext

    T = typing.TypeVar('T')

    # mypy seems not work with typing.ContextManager, so commented it
    # class Implementation(typing.Callable[[BaseContext],
    #                                      typing.ContextManager[T]]):
    #     pass

    #: Implementation type
    Implementation = typing.Callable[[BaseContext], typing.Any]

else:
    Implementation = types.FunctionType


class Implementable(object, metaclass=abc.ABCMeta):
    """Some type that implementable"""
    @abc.abstractmethod
    def implement(self, implementation: Implementation):
        """Implement me"""
        pass
