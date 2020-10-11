import pytest

from autowire import Context, Resource, ResourceNotProvidedError, impl


def test_provide():
    env = Resource("env", __name__)

    parent = Context()
    child = Context(parent)

    @impl.plain
    def get_env():
        return "development"

    child.provide(env, get_env)

    with pytest.raises(ResourceNotProvidedError):
        with parent.resolve(env):
            pass

    with child.resolve(env) as value:
        assert "development" == value


def test_partial():
    name = Resource("name", __name__)
    env = Resource("env", __name__)

    context = Context()

    @impl.plain
    def get_env():
        return "development"

    @impl.plain
    def get_name():
        return "name"

    context.provide(name, get_name)
    context.provide(env, get_env)

    @context.partial(name, env=env)
    def runnable(name, phrase, env):
        return "{}, {}-{}!".format(phrase, name, env)

    assert "Hello, name-development!" == runnable("Hello")
