from autowire import Context, impl, resource
from autowire.builtins import context as context_resource


def test_context():
    @resource.create
    @impl.autowired("context", context_resource)
    @impl.plain
    def get_context(context):
        return context

    context = Context()

    with context.resolve(get_context) as resolved:
        assert context == resolved
