"""
impl.implementable
==================

Abstract base class for implementable things.

"""
import abc

from .implementation import Implementation


class Implementable(object, metaclass=abc.ABCMeta):
    """Some type that can be implemented"""
    @abc.abstractmethod
    def implement(self, implementation: Implementation):
        """Implement me"""
        pass
