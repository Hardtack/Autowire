"""
impl
====

Implementers.

"""
import contextlib
import functools

from autowire.base import BaseContext, BaseResource, Implementation
from autowire.utils import as_contextmanager

from .function import FunctionImplementation
from .implementable import Implementable


def implementation(fn):
    """
    Create an implmentation with function that compatible with reify method.

    The implementation can be called same as original function.

    """
    @contextlib.contextmanager
    def evaluator(fn, resource: BaseResource, context: BaseContext):
        with fn(resource, context) as value:
            yield value

    return FunctionImplementation(fn, evaluator)


def contextmanager(fn):
    """
    Shorcut for combination of ``@contextual`` and
    ``@contextlib.contextmanager`` ::

        @impl.contextual
        @contextlib.contextmanager
        def some_impl():
            ...

    is equivalent to ::

        @impl.contextmanager
        def some_impl(resource, context):
            ...

    """
    return contextual(contextlib.contextmanager(fn))


def contextual(fn):
    """
    Create an implementation with function that returns context manager.

    The implementation can be called same as original function.

    """
    @contextlib.contextmanager
    def evaluator(fn, resource: BaseResource, context: BaseContext):
        with fn() as value:
            yield value

    return FunctionImplementation(fn, evaluator)


def plain(fn):
    """
    Create an implementation with plain function.

    The implementation can be called same as original function.

    """
    @as_contextmanager
    def evaluator(fn, resource: BaseResource, context: BaseContext):
        return fn()

    return FunctionImplementation(fn, evaluator)


def autowired(argname_or_required, required=None):
    """
    Resolve a required resource and inject into function implementation
    as keyword argument. ::

        dependency = Resource('foo', __name__)

        @autowired('dependency', dependency)
        @impl.plain
        def create_something(dependency):
            return create(dependency)

    Resource's `name` property will be used by default for keyword name. ::

        dependency = Resource('foo', __name__)

        @autowired(dependency)
        @impl.plain
        def create_something(foo):
            return create(foo)

    """
    if required is None:
        argname = argname_or_required.name
        required = argname_or_required
    else:
        argname = argname_or_required

    def wrapper(func_impl: FunctionImplementation):
        if not isinstance(func_impl, FunctionImplementation):
            raise ValueError(
                "autowired should be applied to FunctionImplementation"
            )

        @contextlib.contextmanager
        def evaluator(fn, resource: BaseResource, context: BaseContext):
            with context.resolve(required) as arg:
                kwargs = {argname: arg}
                new_function = functools.partial(func_impl.function, **kwargs)
                with func_impl.evaluator(
                        new_function, resource, context) as value:
                    yield value
        return FunctionImplementation(func_impl.function, evaluator)
    return wrapper


__all__ = [
    'implement',
    'implementation',
    'contextual',
    'plain',
    'autowired',
    'Implementation',
    'Implementable',
]
