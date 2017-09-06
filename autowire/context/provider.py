"""
context.provider
================

Interface for providing resource's implementations.

"""
import abc

from autowire.base import BaseResource, Implementation
from autowire.impl.implementable import Implementable


class ImplementationConsumer(object, metaclass=abc.ABCMeta):
    """
    Declarative base type for objects that can bind resources with
    implementation.

    """
    @abc.abstractmethod
    def set_implementation(self, resource: BaseResource,
                           implementation: Implementation):
        pass


class Provider(Implementable):
    """
    Type that can provide implementation to specific resource.

    """
    def __init__(self,
                 resource: BaseResource,
                 consumer: ImplementationConsumer):
        super().__init__()
        self.resource = resource
        self.consumer = consumer

    def implement(self, implementation: Implementation):
        """Set implementation of implementable."""
        self.consumer.set_implementation(self.resource, implementation)

    def __call__(self, implementation: Implementation):
        """Set implementation and return. You can use it as a decorator"""
        self.implement(implementation)
        return implementation
