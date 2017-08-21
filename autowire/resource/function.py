"""
autowire.resource.function
==========================

Resource implementation as a function

"""
import functools

from autowire.base import BaseResource
from autowire.impl.types import Implementable, Implementation

from .utils import create_default_impl


class FunctionResource(BaseResource, Implementable):
    """
    Resource class that wraps a function.

    """

    def __init__(self, func, *, name=None, namespace=None):
        if name is None:
            name = func.__name__
        if namespace is None:
            namespace = func.__module__
        super().__init__(name, namespace)
        self.func = func
        self.default_implementation = create_default_impl(name, namespace)
        functools.update_wrapper(self, func)

    @property
    def default_implementation(self):
        return self._default_implementation

    @default_implementation.setter
    def default_implementation(self, default_implementation):
        self._default_implementation = default_implementation

    def implement(self, implementation: Implementation):
        """Set implementation of implementable."""
        self.default_implementation = implementation

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
