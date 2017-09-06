import contextlib


from autowire import Context, Resource, impl


def test_implement():
    context = Context()
    resource = Resource('test', __name__)

    @resource.implement
    @impl.implementation
    @contextlib.contextmanager
    def resource_impl(resource, context):
        yield 'Test'

    with context.resolve(resource) as value:
        assert 'Test' == value


def test_contextual():
    context = Context()
    foo = Resource('foo', __name__)
    bar = Resource('bar', __name__)

    @foo.implement
    @impl.contextual
    @contextlib.contextmanager
    def foo_impl():
        yield 'foo'

    @bar.implement
    @impl.autowired('foo', foo)
    @impl.contextmanager
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

    @foo.implement
    @impl.plain
    def foo_impl():
        return 'foo'

    @bar.implement
    @impl.autowired('foo', foo)
    @impl.plain
    def bar_impl(foo):
        return 'bar-' + foo

    with context.resolve(foo) as value:
        assert 'foo' == value

    with context.resolve(bar) as value:
        assert 'bar-foo' == value
