import contextlib

import pytest

from autowire.container import Container
from autowire.exc import ResourceNotProvidedError
from autowire.implementation import Implementation
from autowire.resource import Resource


def test_provide():
    foo = Resource("foo", __name__)

    container = Container()

    class SimpleImplementation(Implementation):
        @contextlib.contextmanager
        def reify(self, resource, provider):
            pass

    impl = SimpleImplementation()

    with pytest.raises(ResourceNotProvidedError):
        container.find_implementation(foo)
    container.provide(foo, impl)
    assert impl == container.find_implementation(foo)


def test_plain():
    container = Container()

    foo = Resource("foo", __name__)
    bar = Resource("bar", __name__)

    @container.plain(bar)
    def get_bar():
        return "BAR"

    @container.plain(foo, bar)
    def get_foo(bar: str):
        return f"FOO.{bar}"

    with container.context() as context:
        "BAR" == context.resolve(bar)
        "FOO" == context.resolve(foo)

    # and functions should be left as plain functions
    assert "FOO.bar" == get_foo("bar")
    assert "BAR" == get_bar()


def test_contextual():
    container = Container()

    foo = Resource("foo", __name__)
    bar = Resource("bar", __name__)

    @container.contextual(bar)
    @contextlib.contextmanager
    def with_bar():
        yield "BAR"

    @container.contextual(foo, bar)
    @contextlib.contextmanager
    def with_foo(bar: str):
        yield f"FOO.{bar}"

    with container.context() as context:
        "BAR" == context.resolve(bar)
        "FOO" == context.resolve(foo)

    # and context managers should be left as context managers
    with with_foo("bar") as foo_value:
        assert "FOO.bar" == foo_value
    with with_bar() as bar_value:
        assert "BAR" == bar_value


def test_default_implemenation():
    container = Container()

    foo = Resource("foo", __name__)

    @foo.plain()
    def get_foo():
        return "FOO"

    class SimpleImplementation(Implementation):
        @contextlib.contextmanager
        def reify(self, resource, provider):
            yield "FOO-2"

    assert foo.default_implementation == container.find_implementation(foo)

    impl = SimpleImplementation()
    container.provide(foo, impl)
    assert impl == container.find_implementation(foo)


def test_inheritance():
    foo = Resource("foo", __name__)
    bar = Resource("bar", __name__)

    parent = Container()

    class NoopImplementation(Implementation):
        @contextlib.contextmanager
        def reify(self, resource, provider):
            yield

    foo_impl1 = NoopImplementation()
    foo_impl2 = NoopImplementation()
    bar_impl = NoopImplementation()

    parent.provide(foo, foo_impl1)
    parent.provide(bar, bar_impl)

    child = Container(parent)

    child.provide(foo, foo_impl2)

    assert foo_impl1 == parent.find_implementation(foo)
    assert bar_impl == parent.find_implementation(bar)
    assert foo_impl2 == child.find_implementation(foo)
    assert bar_impl == child.find_implementation(bar)
