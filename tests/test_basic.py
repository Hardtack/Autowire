import contextlib

import pytest

from autowire import Resource, Context, ResourceNotProvidedError, impl


def test_resource():
    resource = Resource('resource', __name__)

    @impl.implement(resource)
    @contextlib.contextmanager
    def resource_impl(context):
        yield 'Hello'

    context = Context()

    with context.resolve(resource) as value:
        assert 'Hello' == value


def test_plain():
    hello = Resource('hello', __name__)

    @impl.plain(hello)
    def get_resource():
        return 'Hello'

    context = Context()

    with context.resolve(hello) as value:
        assert 'Hello' == value


def test_not_provided():
    empty = Resource('empty', __name__)

    context = Context()

    with pytest.raises(ResourceNotProvidedError):
        with context.resolve(empty):
            pass


def test_provide():
    env = Resource('env', __name__)

    parent = Context()
    child = Context(parent)

    @impl.plain(child(env))
    def get_env():
        return 'development'

    with pytest.raises(ResourceNotProvidedError):
        with parent.resolve(env):
            pass

    with child.resolve(env) as value:
        assert 'development' == value


def test_scope():
    level = Resource('level', __name__)

    parent = Context()
    child = Context(parent)

    @impl.plain(parent(level))
    def parent_level():
        return 1

    @impl.plain(child(level))
    def child_level():
        return 2

    with parent.resolve(level) as parent_value, \
            child.resolve(level) as child_value:
        assert 1 == parent_value
        assert 2 == child_value
