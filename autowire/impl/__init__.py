"""
impl
====

Implementers.

"""
import contextlib
import functools

from autowire.base import BaseContext, BaseResource
from autowire.decorators import autowired
from autowire.utils import apply_decorators, as_contextmanager

from .types import Implementable, Implementation


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


def contextual(target: Implementable, *dependencies: BaseResource,
               decorators=()):
    """
    Implement with contextual & autowired resources. ::

        @impl.contextual(resource, dependency1, dependency2)
        @contextlib.contextmanager
        def create_resource(dependency1, dependency2):
            yield dependency1.make_resource(dependency2)

    To apply decorators to implementation ::

        @impl.contextual(resource, dependency, decorators=[decorator])
        @contextlib.contextmanager
        def create_resource(dependency):
            yield dependency.make_resource()

    """
    return with_decorators(target, autowired(*dependencies), *decorators)


def plain(target: Implementable, *dependencies, decorators=()):
    """
    Implement with plain function. ::

        @impl.plain(resource, dependency)
        def get_resource(dependency):
            return os.path.join(dependency, 'resource.json')

    """
    return with_decorators(
        target,
        as_contextmanager,
        autowired(*dependencies),
        *decorators)


def partial(target: Implementable, *positionals, decorators=(), **keywords):
    """
    Implement the target by applying resolved resources partially
    to function. ::

        @partial(resource, dependency1, baz=dependency2):
        def implementation(foo, bar, baz):
            print(foo)  # dependency1
            print(bar)  # argument
            print(baz)  # dependency2

    You can use this resource like ::

        with context.resolve(resource) as function:
            function("argument")

    """
    def decorator(fn):
        @contextlib.contextmanager
        def implementation(context: BaseContext):
            keyword_items = list(keywords.items())
            keyword_keys = [k for k, _ in keyword_items]
            keyword_resources = [v for _, v in keyword_items]

            with context.resolve_all(positionals) as resolved_args, \
                    context.resolve_all(keyword_resources) as \
                    resolved_kwarg_values:
                resolved_kwargs = {}
                for k, v in zip(keyword_keys, resolved_kwarg_values):
                    resolved_kwargs[k] = v
                partial = functools.partial(fn,
                                            *resolved_args,
                                            **resolved_kwargs)
                yield partial
        implement(target)(apply_decorators(implementation, decorators))
    return decorator


__all__ = [
    'implement',
    'with_decorators',
    'plain',
    'contextual',
    'Implementation',
]
