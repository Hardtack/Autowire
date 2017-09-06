"""
autowire.resource
=================

Resource implementations.

"""
from autowire import impl
from autowire.base import Implementation

from .plain import Resource
from .function import FunctionResource


def create(implementation: Implementation=None, *, name=None, namespace=None):
    """
    Create a resource with implementation. ::

        @resource.create
        @impl.implementation
        @contextlib.contextmanager
        def some_resource(resource, context: Context):
            with open('output.log', 'w') as output:
                yield output

        with context.resolve(some_resource) as f:
            f.write('...')

    The default name and namespace will be resolved from decorated function.

    """
    def decorator(implementation):
        resource = FunctionResource(
            implementation, name=name, namespace=namespace
        )
        resource.implement(implementation)
        return resource
    if impl is not None:
        return decorator(implementation)
    return decorator


__all__ = [
    'Resource',
    'FunctionResource',
    'create',
]
