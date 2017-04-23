import contextlib

import pytest

from autowire import Resource, Context, ResourceNotProvidedError


def test_resource():
    resource = Resource('resource', __name__)

    @resource.impl
    @contextlib.contextmanager
    def resource_impl(context):
        yield 'Hello'

    context = Context()

    with context.resolve(resource) as value:
        assert 'Hello' == value


def test_from_func():
    hello = Resource('hello', __name__)

    @hello.from_func()
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

    @child.provide_from_func(env)
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

    @parent.provide_from_func(level)
    def parent_level():
        return 1

    @child.provide_from_func(level)
    def child_level():
        return 2

    with parent.resolve(level) as parent_value, \
            child.resolve(level) as child_value:
        assert 1 == parent_value
        assert 2 == child_value
