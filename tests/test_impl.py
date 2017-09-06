import contextlib


from autowire import Context, Resource, impl


def test_implement():
    context = Context()
    resource = Resource('test', __name__)

    @impl.implement(resource)
    @contextlib.contextmanager
    def resource_impl(resource, context):
        yield 'Test'

    with context.resolve(resource) as value:
        assert 'Test' == value


def test_contextual():
    context = Context()
    foo = Resource('foo', __name__)
    bar = Resource('bar', __name__)

    @impl.implement(foo)
    @impl.contextual
    @contextlib.contextmanager
    def foo_impl():
        yield 'foo'

    @impl.implement(bar)
    @impl.autowired('foo', foo)
    @impl.contextual
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

    @impl.implement(foo)
    @impl.plain
    def foo_impl():
        return 'foo'

    @impl.implement(bar)
    @impl.autowired('foo', foo)
    @impl.plain
    def bar_impl(foo):
        return 'bar-' + foo

    with context.resolve(foo) as value:
        assert 'foo' == value

    with context.resolve(bar) as value:
        assert 'bar-foo' == value
