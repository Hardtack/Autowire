"""
impl.types
==========

Types for implementation.

"""
import abc
import typing

from autowire.base import BaseContext


T = typing.TypeVar('T')

# mypy seems not work with typing.ContextManager, so commented it
# class Implementation(typing.Callable[[BaseContext],
#                                      typing.ContextManager[T]]):
#     pass

#: Implementation type
Implementation = typing.Callable[[BaseContext], typing.Any]


class Implementable(object, metaclass=abc.ABCMeta):
    """Some type that implementable"""
    @abc.abstractmethod
    def implement(self, implementation: Implementation):
        """Implement me"""
        pass
