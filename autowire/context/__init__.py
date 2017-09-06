"""
autowire.context.impl
=====================

Context's implementations

"""
from autowire.base import BaseContext, BaseResource, Implementation

from .provider import Provider, ImplementationConsumer
from .root import root_context


class Context(BaseContext, ImplementationConsumer):
    """
    Context implementation.
    """

    def __init__(self, parent: BaseContext=root_context):
        self.parent = parent
        self.implementations = {}

    def get_implementation(self, resource: BaseResource):
        """Get resource implementation from this context."""
        return self.implementations[resource.canonical_name]

    def provided_by(self, resource: BaseResource):
        """Find context that provides resource."""
        if resource.canonical_name in self.implementations:
            return self
        elif self.parent is not None:
            return self.parent.provided_by(resource)

    def set_implementation(self, resource: BaseResource,
                           implementation: Implementation):
        self.implementations[resource.canonical_name] = implementation

    def provide(self,
                resource: BaseResource,
                implementation: Implementation=None):
        """
        Provide an implementaion for resource in this context. ::

            context.provide(resource, implementation)

        Or as a decorator ::

            @context.provide(resource)
            @impl.autowired('dependency1', dependency1)
            @impl.autowired('dependency2', dependency2)
            @impl.contextmanager
            def create_resource(dependency1, dependency2):
                yield dependency1.make_resource(dependency2)

        """
        if implementation is not None:
            return self.set_implementation(resource, implementation)
        return Provider(resource, self)


__all__ = ['Context', 'root_context']
