from autowire import Context
from autowire.builtins import context


def test_context():
    with Context() as current_context:
        assert current_context is current_context.resolve(context)
        with Context(current_context) as child_context:
            assert child_context is child_context.resolve(context)
        assert current_context is current_context.resolve(context)
