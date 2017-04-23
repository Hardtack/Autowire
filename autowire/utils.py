"""
autowire.utils
==============

Common utilities.

"""
import contextlib
import functools

from autowire.base import BaseContext, BaseResource


def autowire(fn, *dependencies: BaseResource):
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

        impl = autowire(with_foo, bar)  # Convert to implementation.
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


class RefCounter(object):
    """Preserve context until it has any references."""
    def __init__(self, contextmanager):
        super().__init__()
        self.count = 0
        self.contextmanager = contextmanager
        self.value = None

    def increase(self):
        self.count += 1
        if self.count == 1:
            self.value = self.contextmanager.__enter__()

    def decrease(self, exc_type, exc_value, tb):
        if self.count == 1:
            self.value = 0
            self.contextmanager.__exit__(exc_type, exc_value, tb)
        self.count -= 1

    def __enter__(self):
        self.increase()
        return self.value

    def __exit__(self, exc_type, exc_value, tb):
        self.decrease(exc_type, exc_value, tb)
