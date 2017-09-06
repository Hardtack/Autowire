"""
impl.implementable
==================

Abstract base class for implementable things.

"""
import abc

from autowire.base import Implementation


class Implementable(object, metaclass=abc.ABCMeta):
    """Some type that can be implemented"""
    @abc.abstractmethod
    def implement(self, implementation: Implementation) -> Implementation:
        """
        Implement this.

        It returns given implementation so that can be used as a decorator.
        """
        pass
