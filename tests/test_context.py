import contextlib

import pytest

from autowire.container import Container
from autowire.resource import Resource


def test_pool():
    container = Container()

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

    with container.context() as context:
        assert 1 == context.resolve(counter)
        assert 1 == context.resolve(counter)
        assert 1 == context.resolve(counter)

        assert 1 == context.resolve(squared_counter)
        assert 1 == context.resolve(squared_counter)
        assert 1 == context.resolve(squared_counter)

    with container.context() as context:
        assert 2 == context.resolve(counter)
        assert 2 == context.resolve(counter)
        assert 2 == context.resolve(counter)

        assert 4 == context.resolve(squared_counter)
        assert 4 == context.resolve(squared_counter)
        assert 4 == context.resolve(squared_counter)


def test_drain():
    container = Container()

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

    with container.context() as context:
        assert 1 == context.resolve(reference)
        assert 1 == refcount
    assert 0 == refcount


def test_drain_exception():
    container = Container()

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

    with pytest.raises(ZeroDivisionError):
        with container.context() as context:
            assert "foo" == context.resolve(foo)
            assert "bar" == context.resolve(bar)
            assert foo_alive is True
    assert foo_alive is False


def test_child():
    foo = Resource("foo", __name__)
    bar = Resource("bar", __name__)

    container = Container()

    foo_refs = 0
    bar_refs = 0

    @container.plain(foo)
    def get_foo():
        nonlocal foo_refs
        foo_refs += 1
        return f"foo-{foo_refs}"

    @container.plain(bar)
    def get_bar():
        nonlocal bar_refs
        bar_refs += 1
        return f"bar-{bar_refs}"

    with container.context(preload=[foo]) as parent:
        assert 1 == foo_refs
        assert "foo-1" == parent.resolve(foo)

        with parent.child() as child1:
            assert "foo-1" == child1.resolve(foo)
            assert "bar-1" == child1.resolve(bar)

        with parent.child(preload=[bar]) as child2:
            assert 2 == bar_refs
            assert "foo-1" == child2.resolve(foo)
            assert "bar-2" == child2.resolve(bar)

    assert 1 == foo_refs
    assert 2 == bar_refs
