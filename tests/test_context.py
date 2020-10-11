import contextlib

import pytest

from autowire.context import Context
from autowire.exc import ResourceNotProvidedError
from autowire.implementation import Implementation
from autowire.resource import Resource


def test_provide():
    context = Context()

    foo = Resource("foo", __name__)

    class SimpleImplementation(Implementation):
        @contextlib.contextmanager
        def reify(self, resource, provider):
            assert foo == resource
            assert provider == context
            yield "FOO"

    with context:
        with pytest.raises(ResourceNotProvidedError):
            context.resolve(foo)

        context.provide(foo, SimpleImplementation())
        assert "FOO" == context.resolve(foo)


def test_plain():
    context = Context()

    foo = Resource("foo", __name__)
    bar = Resource("bar", __name__)

    @context.plain(bar)
    def get_bar():
        return "BAR"

    @context.plain(foo, bar)
    def get_foo(bar: str):
        return f"FOO.{bar}"

    with context:
        "BAR" == context.resolve(bar)
        "FOO" == context.resolve(foo)

    # and functions should be left as plain functions
    assert "FOO.bar" == get_foo("bar")
    assert "BAR" == get_bar()


def test_contextual():
    context = Context()

    foo = Resource("foo", __name__)
    bar = Resource("bar", __name__)

    @context.contextual(bar)
    @contextlib.contextmanager
    def with_bar():
        yield "BAR"

    @context.contextual(foo, bar)
    @contextlib.contextmanager
    def with_foo(bar: str):
        yield f"FOO.{bar}"

    with context:
        "BAR" == context.resolve(bar)
        "FOO" == context.resolve(foo)

    # and context managers should be left as context managers
    with with_foo("bar") as foo_value:
        assert "FOO.bar" == foo_value
    with with_bar() as bar_value:
        assert "BAR" == bar_value


def test_pool():
    context = Context()

    count = 0

    counter = Resource("counter", __name__)
    squared_counter = Resource("squared_counter", __name__)

    @counter.plain()
    def next_count():
        nonlocal count
        count += 1
        return count

    @squared_counter.plain(counter)
    def next_squred_counter(counter: int):
        return counter ** 2

    with context:
        assert 1 == context.resolve(counter)
        assert 1 == context.resolve(counter)
        assert 1 == context.resolve(counter)

        assert 1 == context.resolve(squared_counter)
        assert 1 == context.resolve(squared_counter)
        assert 1 == context.resolve(squared_counter)

    with context:
        assert 2 == context.resolve(counter)
        assert 2 == context.resolve(counter)
        assert 2 == context.resolve(counter)

        assert 4 == context.resolve(squared_counter)
        assert 4 == context.resolve(squared_counter)
        assert 4 == context.resolve(squared_counter)


def test_drain():
    context = Context()

    refcount = 0

    reference = Resource("reference", __name__)

    @reference.contextual()
    @contextlib.contextmanager
    def next_count():
        nonlocal refcount
        refcount += 1
        try:
            yield refcount
        finally:
            refcount -= 1

    with context:
        assert 1 == context.resolve(reference)
        assert 1 == refcount
    assert 0 == refcount


def test_drain_exception():
    context = Context()

    foo = Resource("foo", __name__)
    bar = Resource("bar", __name__)

    # aliving flag for foo
    foo_alive = False

    @foo.contextual()
    @contextlib.contextmanager
    def get_foo():
        nonlocal foo_alive
        foo_alive = True
        try:
            with pytest.raises(ZeroDivisionError):
                yield "foo"
        finally:
            foo_alive = False

    @bar.contextual(foo)
    @contextlib.contextmanager
    def get_bar(foo: str):
        try:
            yield "bar"
        finally:
            1 / 0

    assert "foo" == context.resolve(foo)
    assert "bar" == context.resolve(bar)
    assert foo_alive is True
    with pytest.raises(ZeroDivisionError):
        context.drain()
    assert foo_alive is False


def test_default_implemenation():
    context = Context()

    foo = Resource("foo", __name__)

    @foo.plain()
    def get_foo():
        return "FOO"

    class SimpleImplementation(Implementation):
        @contextlib.contextmanager
        def reify(self, resource, provider):
            yield "FOO-2"

    assert "FOO" == context.resolve(foo)

    context.provide(foo, SimpleImplementation())
    assert "FOO" == context.resolve(foo)


def test_inheritance():
    foo = Resource("foo", __name__)
    bar = Resource("bar", __name__)

    with Context() as parent:

        @parent.plain(foo, bar)
        def get_foo(bar: str):
            return f"foo.{bar}"

        @parent.plain(bar)
        def get_bar():
            return "bar"

        assert "foo.bar" == parent.resolve(foo)

        with Context(parent) as child:

            @child.plain(bar)
            def get_child_bar():
                return "bar2"

            assert "bar2" == child.resolve(bar)
            assert "bar" == parent.resolve(bar)

            # `foo` was implemented in parent context.
            # So `foo` must not be depend on child's `bar`
            assert "foo.bar" == child.resolve(foo)
            assert "foo.bar" == parent.resolve(foo)
