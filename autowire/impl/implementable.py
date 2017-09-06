"""
impl.implementable
==================

Abstract base class for implementable things.

"""
import abc
import typing

from .implementation import Implementation


class Implementable(object, metaclass=abc.ABCMeta):
    """Some type that is implementable"""
    @abc.abstractmethod
    def implement(self, implementation: Implementation):
        """Implement me"""
        pass
