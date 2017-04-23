"""
autowire.resource.impl
======================

Resource implementations.

"""
import contextlib
import functools

from autowire.base import BaseContext, BaseResource
from autowire.exc import ResourceNotProvidedError
from autowire.utils import autowire


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
        def decorator(fn):
            impl = autowire(fn, *dependencies)

            # Apply decorators
            for decorator in decorators:
                impl = decorator(impl)
            self.impl(impl)

            return fn
        return decorator

    def impl(self, implementation):
        """
        Set default implementation of resource.
        """
        self.default_implementation = implementation
        return implementation

    def from_func(self, *dependencies, decorators=()):
        """
        Get resource from function implementation. ::

            @resource.from_func(dependency)
            def get_resource(dependency):
                return os.path.join(dependency, 'resource.json')

        """
        def decorator(fn):
            @self.autowired(*dependencies, decorators=decorators)
            @contextlib.contextmanager
            @functools.wraps(fn)
            def impl(*args, **kwargs):
                yield fn(*args, **kwargs)
            return fn
        return decorator
