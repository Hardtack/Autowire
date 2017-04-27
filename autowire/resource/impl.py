"""
autowire.resource.impl
======================

Resource implementations.

"""
import contextlib

from autowire.base import BaseContext, BaseResource
from autowire.exc import ResourceNotProvidedError
from autowire.decorators import autowired
from autowire.utils import apply_decorators, as_contextmanager


def create_default_impl(name: str, namespace: str):
    @contextlib.contextmanager
    def default_impl(context: BaseContext):
        """No such resource."""
        raise ResourceNotProvidedError(
            "No such resource {namespace}.{name}".format(
                namespace=namespace,
                name=name,
            ))
        yield None
    return default_impl


class Resource(BaseResource):
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

    def impl(self, implementation, decorators=()):
        """Set default implementation of resource."""
        self.default_implementation = implementation
        return implementation

    def with_decorators(self, *decorators):
        """
        Set default implementation with decorators.
        It sets implementation with decorators but returns original function
        not decorated function so that does not change function's interface.

        """
        def decorator(fn):
            decorated = apply_decorators(fn, decorators)
            self.impl(decorated)
            return fn
        return decorator

    def autowired(self, *dependencies: BaseResource, decorators=()):
        """
        Set default implementation to resource. ::

            @builder.autowired(dependency1, dependency2)
            @contextlib.contextmanager
            def create_resource(dependency1, dependency2):
                yield dependency1.make_resource(dependency2)

        To apply decorators to implementation ::

            @resource.autowired(dependency, decorators=[decorator])
            @contextlib.contextmanager
            def create_resource(dependency):
                return dependency.make_resource()

        """
        return self.with_decorators(autowired(*dependencies), *decorators)

    def from_func(self, *dependencies, decorators=()):
        """
        Get resource from function implementation. ::

            @resource.from_func(dependency)
            def get_resource(dependency):
                return os.path.join(dependency, 'resource.json')

        """
        return self.with_decorators(
            as_contextmanager,
            autowired(*dependencies),
            *decorators
        )
