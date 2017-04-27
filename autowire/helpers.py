"""
autowire.helpers
================

Helpers.

"""
import contextlib
import functools

from autowire.base import BaseContext, BaseResource

from .builtins import this
from .utils import RefCounter


def autowired(fn, *dependencies: BaseResource):
    """
    Convert plain contextmanager to resource implementation by autowiring
    dependencies. ::

        foo = Resource('foo', __name__)
        bar = Resource('bar', __name__)

        @contextlib.contextmanager
        def with_foo(bar):
            value = baz(bar)
            try:
                yield value
            finally:
                value.teardown()

        impl = autowired(with_foo, bar)  # Convert to implementation.
        foo.impl(impl)

    """
    @contextlib.contextmanager
    def implementation(context: BaseContext):
        # Resolve dependencies using context.
        def with_dependencies(fn, dependencies):
            if dependencies:
                first = dependencies[0]
                rest = dependencies[1:]
                with context.resolve(first) as value:
                    fn = functools.partial(fn, value)
                    yield from with_dependencies(fn, rest)
            else:
                with fn() as value:
                    yield value
        # Call implemenation with autowired resources.
        yield from with_dependencies(fn, dependencies)
    return implementation


def shared(impl):
    """
    Convert implementation to shared resource implementation.

    Shared resource shares contexxt using reference counting.
    When you try to resolve shared resource that already resolve but not teared
    down, It brings previously resolved resouce.

    The resource will be tied into resource's providing context.
    It means that children's context will not be able to be used
    in this resource. ::

        res1 = Resource('res1', __name__)
        res2 = Resource('res2', __name__)

        @res2.impl
        @shared
        @contextlib.contextmanager
        def with_res1(context):
            with context.resolve(res2) as res1_factory:
                res1 = res1_factory.create_res1()
                try:
                    yield res1
                finally:
                    res1.teardown()

        context = Context()

        child = Context(context)

        @child.autowired(res2)
        def with_res2():
            yield ...

        # Get ResourceNotProvidedError, even though child provides res2.
        # Because res1 was shared in parent context.
        with child.resolve(res1):
            ...

    """

    counter = None

    @functools.wraps(impl)
    @contextlib.contextmanager
    def wrapper(context: BaseContext):
        nonlocal counter
        with context.resolve(this) as resource:
            if counter is None:
                provider = context.provided_by(resource)  # Find me
                counter = RefCounter(impl(provider))
            try:
                with counter as value:
                    yield value
            finally:
                if counter.count == 0:
                    counter = None
    return wrapper
