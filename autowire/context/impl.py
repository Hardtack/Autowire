"""
autowire.context.impl
=====================

Context's implementations

"""
import contextlib
import functools

from autowire.base import BaseContext, BaseResource
from autowire.utils import autowire, RefCounter

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

    def provide_from_func(self, resource: BaseResource,
                          *dependencies: BaseResource,
                          decorators=(), shared: bool=False):
        """
        Provide resource from function implementation. ::

            @context.provide_from_func(resource, dependency)
            def get_resource(dependency):
                return os.path.join(dependency, 'resource.json')

        """
        def decorator(fn):
            @self.provide_autowired(resource, *dependencies,
                                    decorators=decorators,
                                    shared=shared)
            @contextlib.contextmanager
            @functools.wraps(fn)
            def impl(*args, **kwargs):
                yield fn(*args, **kwargs)
            return fn
        return decorator

    def provide_autowired(self, resource: BaseResource,
                          *dependencies: BaseResource,
                          decorators=(), shared: bool=False):
        """
        Provide implementation with autowired dependencies :.:

            @context.provide_autowired(resource, dependency1, dependency2)
            @contextlib.contextmanager
            def create_resource(dependency1, dependency2):
                yield dependency1.make_resource(dependency2)

        """
        def decorator(fn):
            implementation = autowire(fn, *dependencies)
            for decorator in decorators:
                implementation = decorator(implementation)
            if shared:
                self.shared(resource)(implementation)
            else:
                self.provide(resource)(implementation)

            return fn
        return decorator

    def shared(self, resource: BaseResource):
        """
        Provide a resource shared in this context & its childrend.

        The resource will be tied into this context. It means that children's
        context will not be able to be used in this resource. ::

            res1 = Resource('res1', __name__)
            res2 = Resource('res2', __name__)

            @res2.autowire(res1)
            @contextlib.contextmanager
            def with_res1(res2):
                res1 = res2.create_res1()
                try:
                    yield res1
                finally:
                    res1.teardown()

            context = Context()
            context.share(res1)

            child = Context(context)

            @child.autowired(res2)
            def with_res2():
                yield ...

            # Get ResourceNotProvidedError,
            # even though child provides res2.
            # Because res1 was shared in parent.
            with child.resolve(res1):
                ...

        """
        def decorator(impl):
            counter = None

            @self.provide(resource)
            @contextlib.contextmanager
            def wrapper(context: BaseContext):
                nonlocal counter
                if counter is None:
                    provider = context.provided_by(resource)  # Find me
                    counter = RefCounter(impl(provider))
                try:
                    with counter as value:
                        yield value
                finally:
                    if counter.count == 0:
                        counter = None
            return impl

        return decorator
