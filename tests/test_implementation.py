import contextlib

from autowire.exc import ResourceNotProvidedError
from autowire.implementation import (
    ConstantImplementation,
    ContextManagerImplementation,
    PlainFunctionImplementation,
)
from autowire.provider import ResourceProvider
from autowire.resource import Resource


def test_plain():
    """
    Test for plain implementations

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
    Test for context manager implementation

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


def test_constant():
    """
    Test for constant implementation

    """

    resource = Resource("foo", "test")
    value = "FOO"

    class MockProvider(ResourceProvider):
        def resolve(self, resource):
            raise ResourceNotProvidedError(
                "No resources provided to this provider"
            )

    implementation = ConstantImplementation(value)
    with implementation.reify(resource, MockProvider()) as reified:
        assert value == reified
