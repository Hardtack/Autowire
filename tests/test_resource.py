import contextlib

from autowire import Context, resource


def test_implement():
    context = Context()

    @resource.implement()
    @contextlib.contextmanager
    def test(context: Context):
        yield 'Test'

    with context.resolve(test) as value:
        assert 'Test' == value


def test_contextual():
    context = Context()

    @resource.contextual()
    @contextlib.contextmanager
    def foo():
        yield 'foo'

    @resource.contextual(foo)
    @contextlib.contextmanager
    def bar(foo):
        yield 'bar-' + foo

    with context.resolve(foo) as value:
        assert 'foo' == value

    with context.resolve(bar) as value:
        assert 'bar-foo' == value


def test_plain():
    context = Context()

    @resource.plain()
    def foo():
        return 'foo'

    @resource.plain(foo)
    def bar(foo):
        return 'bar-' + foo

    with context.resolve(foo) as value:
        assert 'foo' == value

    with context.resolve(bar) as value:
        assert 'bar-foo' == value


def test_partial():
    context = Context()

    @resource.plain()
    def foo():
        return 'foo'

    @resource.partial(foo=foo)
    def bar(number, foo):
        return foo + '-' + str(number)

    with context.resolve(bar) as f:
        assert f(1) == 'foo-1'
        assert f(2) == 'foo-2'
        assert f(3) == 'foo-3'
