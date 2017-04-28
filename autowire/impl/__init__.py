"""
impl
====

Implementers.

"""
from autowire.base import BaseResource
from autowire.decorators import autowired
from autowire.utils import apply_decorators, as_contextmanager

from .types import Implementable, Implementation


def contextual(target: Implementable, *dependencies: BaseResource,
               decorators=()):
    """
    Implement with contextual & autowired resources. ::

        @implementble.autowired(dependency1, dependency2)
        @contextlib.contextmanager
        def create_resource(dependency1, dependency2):
            yield dependency1.make_resource(dependency2)

    To apply decorators to implementation ::

        @resource.autowired(dependency, decorators=[decorator])
        @contextlib.contextmanager
        def create_resource(dependency):
            return dependency.make_resource()

    """
    return with_decorators(target, autowired(*dependencies), *decorators)


def plain(target: Implementable, *dependencies, decorators=()):
    """
    Implement with plain function. ::

        @implementable.plain(dependency)
        def get_resource(dependency):
            return os.path.join(dependency, 'resource.json')

    """
    return with_decorators(
        target,
        as_contextmanager,
        autowired(*dependencies),
        *decorators)


def with_decorators(target: Implementable, *decorators):
    """
    Set default implementation with decorators.
    It sets implementation with decorators but returns original function
    not decorated function so that does not change function's interface.

    """
    def decorator(fn):
        implement(target)(apply_decorators(fn, decorators))
        return fn
    return decorator


def implement(target: Implementable):
    """
    Implement it. ::

        @implement(resource)
        @contextlib.contextmanager
        def implementation(context: Context):
            with open('output.log', 'w') as ouput:
                yield output

    """
    def decorator(implementation: Implementation):
        target.implement(implementation)
        return implementation
    return decorator


__all__ = [
    'implement',
    'with_decorators',
    'plain',
    'contextual',
    'Implementation',
]
