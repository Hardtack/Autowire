import contextlib

from autowire.implementation import (
    ContextManagerImplementation,
    PlainFunctionImplementation,
)
from autowire.provider import ResourceProvider
from autowire.resource import Resource


def test_plain():
    """
    Test for plain function implementation

    """

    resource_a = Resource("a", "test")
    resource_b = Resource("b", "test")
    resource_c = Resource("b", "test")

    class MockProvider(ResourceProvider):
        def resolve(self, resource):
            if resource == resource_a:
                return "foo"
            elif resource == resource_b:
                return "bar"
            else:
                assert False

    def get_c(a, *, b):
        return f"{a}.{b}.baz"

    implementation = PlainFunctionImplementation(
        get_c, (resource_a,), dict(b=resource_b)
    )
    with implementation.reify(resource_c, MockProvider()) as c:
        assert "foo.bar.baz" == c


def test_contextual():
    """
    Test for contet manager implementation

    """

    resource_a = Resource("a", "test")
    resource_b = Resource("b", "test")
    resource_c = Resource("b", "test")

    class MockProvider(ResourceProvider):
        def resolve(self, resource):
            if resource == resource_a:
                return "foo"
            elif resource == resource_b:
                return "bar"
            else:
                assert False

    @resource_c.contextual(resource_a, b=resource_b)
    @contextlib.contextmanager
    def with_c(a, *, b):
        yield f"{a}.{b}.baz"

    implementation = ContextManagerImplementation(
        with_c, (resource_a,), dict(b=resource_b)
    )
    with implementation.reify(resource_c, MockProvider()) as c:
        assert "foo.bar.baz" == c
