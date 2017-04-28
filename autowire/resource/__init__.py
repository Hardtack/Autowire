"""
autowire.resource
=================

Resource implementations.

"""
from autowire.base import BaseResource
from autowire.impl.types import Implementable, Implementation

from .utils import create_default_impl


class Resource(BaseResource, Implementable):
    """
    Resource class of some functionalities like default implementation.

    """

    def __init__(self, name, namespace):
        super().__init__(name, namespace)
        self.default_implementation = create_default_impl(name, namespace)

    @property
    def default_implementation(self):
        return self._default_implementation

    @default_implementation.setter
    def default_implementation(self, default_implementation):
        self._default_implementation = default_implementation

    def implement(self, implementation: Implementation):
        """Set implementation of implementable."""
        self.default_implementation = implementation


__all__ = ['Resource']
