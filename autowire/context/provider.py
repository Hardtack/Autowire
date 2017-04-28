"""
context.provider
================

Interface for providing resource's implementations.

"""
import abc

from autowire.base import BaseResource
from autowire.impl import Implementable, Implementation


class ImplementationConsumer(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_implementation(self, resource: BaseResource,
                           implementation: Implementation):
        pass


class Provider(Implementable):
    def __init__(self,
                 resource: BaseResource,
                 consumer: ImplementationConsumer):
        super().__init__()
        self.resource = resource
        self.consumer = consumer

    def implement(self, implementation: Implementation):
        """Set implementation of implementable."""
        self.consumer.set_implementation(self.resource, implementation)
