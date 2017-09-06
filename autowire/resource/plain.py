"""
autowire.resource.plain
=======================

Plain resource implementation

"""
from autowire.base import BaseResource, Implementation
from autowire.impl.implementable import Implementable

from .utils import default_implementation


class Resource(BaseResource, Implementable):
    """
    Resource class of some functionalities like default implementation.

    """
    def __init__(self, name, namespace):
        super().__init__(name, namespace)
        self.default_implementation = default_implementation

    @property
    def default_implementation(self):
        return self._default_implementation

    @default_implementation.setter
    def default_implementation(self, default_implementation):
        self._default_implementation = default_implementation

    def implement(self, implementation: Implementation):
        """Set implementation of implementable."""
        self.default_implementation = implementation
