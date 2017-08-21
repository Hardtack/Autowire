"""
autowire.resource
=================

Resource implementations.

"""
from autowire import impl
from autowire.base import BaseResource

from .plain import Resource
from .function import FunctionResource


def implement(*, name=None, namespace=None):
    """
    Create a resource with implementation. ::

        @resource.implement()
        @contextlib.contextmanager
        def some_resource(context: Context):
            with open('output.log', 'w') as output:
                yield output

        with context.resolve(some_resource) as f:
            f.write('...')

    The default name and namespace will be resolved from decorated function.

    """
    def decorator(fn):
        resource = FunctionResource(fn, name=name, namespace=namespace)
        impl.implement(resource)(fn)
        return resource
    return decorator


def contextual(*dependencies: BaseResource,
               decorators=(), name=None, namespace=None):
    """
    Create a resource with contextual function implementation. ::

        @resource.contextual(dependency1, dependency2)
        @contextlib.contextmanager
        def contextual_resource(dependency1, dependency2):
            yield dependency1.make_resource(dependency2)

        with context.resolve(contextual_resource) as value:
            print(value)
            # ...


    The default name and namespace will be resolved from decorated function.

    """
    def decorator(fn):
        resource = FunctionResource(fn, name=name, namespace=namespace)
        impl.contextual(resource, *dependencies, decorators=decorators)(fn)
        return resource
    return decorator


def plain(*dependencies: BaseResource,
          decorators=(), name=None, namespace=None):
    """
    Create a resource with plain function implementation. ::

        @resource.plain(dependency)
        def resource_path(dependency):
            return os.path.join(dependency, 'resource.json')

        with context.resolve(resource_path) as path:
            with open(path) as f:
                # ...

    The default name and namespace will be resolved from decorated function.

    """
    def decorator(fn):
        resource = FunctionResource(fn, name=name, namespace=namespace)
        impl.plain(resource, *dependencies, decorators=decorators)(fn)
        return resource
    return decorator


def partial(*positionals,
            decorators=(), name=None, namespace=None,
            **keywords):
    """
    Create a partial resource which is a partial function of decorated
    function. Arguments will be partially filled with resolved resources. ::

        @resource.partial(user_repository=user_repository):
        def find_user_by_id(user_id, user_repository):
            return user_repository.find_by_id(user_id)

        with context.resolve(find_user_by_id) as func:
            user = func(100001)  # user_repository will be resolved partially.
            # ...

    The default name and namespace will be resolved from decorated function.

    """
    def decorator(fn):
        resource = FunctionResource(fn, name=name, namespace=namespace)
        impl.partial(resource, decorators=decorators,
                     *positionals, **keywords)(fn)
        return resource
    return decorator


__all__ = [
    'Resource',
    'FunctionResource',
    'implementation',
    'contextual',
    'plain',
    'partial',
]
