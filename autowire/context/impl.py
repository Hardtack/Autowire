"""
autowire.context.impl
=====================

Context's implementations

"""
import itertools

from autowire.base import BaseContext, BaseResource
from autowire.decorators import autowired
from autowire.utils import apply_decorators, as_contextmanager

from .root import root_context


class Context(BaseContext):
    """
    Context implementation.
    """

    def __init__(self, parent: BaseContext=root_context):
        self.parent = parent
        self.implementations = {}

    def get_resource_impl(self, resource: BaseResource):
        """Get resource implementation from this context."""
        return self.implementations[resource.canonical_name]

    def provided_by(self, resource: BaseResource):
        """Find context that provides resource."""
        if resource.canonical_name in self.implementations:
            return self
        elif self.parent is not None:
            return self.parent.provided_by(resource)

    def set_resource_impl(self, resource: BaseResource, impl):
        """Set resource implementation to this context."""
        self.implementations[resource.canonical_name] = impl

    def provide(self, resource: BaseResource):
        """
        Provide implementation for resource in this context. ::

            @context.provide_autowired(resource, dependency1, dependency2)
            @contextlib.contextmanager
            def create_resource(dependency1, dependency2):
                yield dependency1.make_resource(dependency2)

        """
        def decorator(implementation):
            self.set_resource_impl(resource, implementation)
            return implementation
        return decorator

    def provide_with_decorators(self, resource, *decorators):
        def decorator(fn):
            decorated = apply_decorators(fn, decorators)
            self.provide(resource)(decorated)
            return fn
        return decorator

    def provide_from_func(self, resource: BaseResource,
                          *dependencies: BaseResource,
                          decorators=()):
        """
        Provide resource from function implementation. ::

            @context.provide_from_func(resource, dependency)
            def get_resource(dependency):
                return os.path.join(dependency, 'resource.json')

        """

        return self.provide_with_decorators(
            resource,
            as_contextmanager,
            autowired(*dependencies),
            *decorators
        )

    def provide_autowired(self, resource: BaseResource,
                          *dependencies: BaseResource,
                          decorators=()):
        """
        Provide implementation with autowired dependencies ::

            @context.provide_autowired(resource, dependency1, dependency2)
            @contextlib.contextmanager
            def create_resource(dependency1, dependency2):
                yield dependency1.make_resource(dependency2)

        """
        return self.provide_with_decorators(
            resource,
            autowired(*dependencies),
            *decorators
        )
