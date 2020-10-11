import contextlib

import pytest

from autowire.implementation import (
    ContextManagerImplementation,
    PlainFunctionImplementation,
)
from autowire.resource import Resource


def test_create():
    """
    Test for name and namespace
    """
    wired = Resource("wired", "auto")
    assert wired.name == "wired"
    assert wired.namespace == "auto"
    assert wired.canonical_name == "auto.wired"

    with pytest.raises(ValueError):
        Resource("foo.bar", "baz")


def test_comparison():
    """
    Tests for comparison
    """
    wired1 = Resource("wired", "test.auto")
    wired2 = Resource("wired", "test.auto")
    wired3 = Resource("wired", "auto")

    assert wired1 == wired2
    assert hash(wired1) == hash(wired2)

    assert wired1 != wired3
    assert hash(wired1) != hash(wired3)


def test_plain():
    """
    Test for plain function implementation

    """

    resource_a = Resource("a", "test")
    resource_b = Resource("b", "test")
    resource_c = Resource("b", "test")

    @resource_c.plain(resource_a, b=resource_b)
    def get_c(a, *, b):
        return f"{a}.{b}.baz"

    assert resource_c.default_implementation is not None
    impl = resource_c.default_implementation
    assert isinstance(impl, PlainFunctionImplementation)
    assert impl.fn == get_c
    assert impl.arg_resources == (resource_a,)
    assert impl.kwarg_resources == dict(b=resource_b)

    # And get_c must be left as a plain function
    assert "bar.foo.baz" == get_c("bar", b="foo")


def test_contextual():
    """
    Test for contet manager implementation

    """

    resource_a = Resource("a", "test")
    resource_b = Resource("b", "test")
    resource_c = Resource("b", "test")

    @resource_c.contextual(resource_a, b=resource_b)
    @contextlib.contextmanager
    def with_c(a, *, b):
        yield f"{a}.{b}.baz"

    assert resource_c.default_implementation is not None
    impl = resource_c.default_implementation
    assert isinstance(impl, ContextManagerImplementation)
    assert impl.manager_generator == with_c
    assert impl.arg_resources == (resource_a,)
    assert impl.kwarg_resources == dict(b=resource_b)

    # And with_c must be left as a plain context manager
    with with_c("bar", b="foo") as c:
        assert "bar.foo.baz" == c
