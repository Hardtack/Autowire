"""
autowire.context.impl
=====================

Context's implementations

"""
from autowire.base import BaseContext, BaseResource
from autowire.impl import Implementation

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

    def provide(self, resource: BaseResource):
        """
        Resource resource's implementation provider which is
        :class:`Implementable` ::

            @autowired(context.provide(resource), dependency1, dependency2)
            @contextlib.contextmanager
            def create_resource(dependency1, dependency2):
                yield dependency1.make_resource(dependency2)

        __call__ method is alias for this method ::

            @autowired(context(resource), dependency1, dependency2)
            @contextlib.contextmanager
            def create_resource(dependency1, dependency2):
                yield dependency1.make_resource(dependency2)

        """
        return Provider(resource, self)

    def __call__(self, resource: BaseResource):
        return self.provide(resource)


__all__ = ['Context', 'root_context']
