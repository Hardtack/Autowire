import contextlib

from autowire import Context, Resource, impl


def test_implement():
    context = Context()
    resource = Resource('test', __name__)

    @impl.implement(resource)
    @contextlib.contextmanager
    def resource_impl(context: Context):
        yield 'Test'

    with context.resolve(resource) as value:
        assert 'Test' == value


def test_contextual():
    context = Context()
    foo = Resource('foo', __name__)
    bar = Resource('bar', __name__)

    @impl.contextual(foo)
    @contextlib.contextmanager
    def foo_impl():
        yield 'foo'

    @impl.contextual(bar, foo)
    @contextlib.contextmanager
    def bar_impl(foo):
        yield 'bar-' + foo

    with context.resolve(foo) as value:
        assert 'foo' == value

    with context.resolve(bar) as value:
        assert 'bar-foo' == value


def test_plain():
    context = Context()
    foo = Resource('foo', __name__)
    bar = Resource('bar', __name__)

    @impl.plain(foo)
    def foo_impl():
        return 'foo'

    @impl.plain(bar, foo)
    def bar_impl(foo):
        return 'bar-' + foo

    with context.resolve(foo) as value:
        assert 'foo' == value

    with context.resolve(bar) as value:
        assert 'bar-foo' == value


def test_partial():
    context = Context()
    foo = Resource('foo', __name__)
    bar = Resource('bar', __name__)

    @impl.plain(foo)
    def foo_impl():
        return 'foo'

    @impl.partial(bar, foo=foo)
    def bar_impl(number, foo):
        return foo + '-' + str(number)

    with context.resolve(bar) as f:
        assert f(1) == 'foo-1'
        assert f(2) == 'foo-2'
        assert f(3) == 'foo-3'
