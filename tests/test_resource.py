from autowire import Context, resource, impl


def test_create():
    context = Context()

    @resource.create
    @impl.plain
    def foo():
        return 'foo'

    @resource.create
    @impl.autowired('foo', foo)
    @impl.plain
    def bar(foo):
        return 'bar-' + foo

    with context.resolve(foo) as value:
        assert 'foo' == value

    with context.resolve(bar) as value:
        assert 'bar-foo' == value
