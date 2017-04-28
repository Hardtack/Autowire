"""
autowire.context.root
=====================

Root context.

"""
from autowire.base import BaseContext, BaseResource

__all__ = ['root_context']


class _RootContext(BaseContext):
    """
    Root context.
    """
    def get_implementation(self, resource: BaseResource):
        """Get resource implementation from this context."""
        return resource.default_implementation

    def provided_by(self, resource: BaseResource):
        """Find context that provides resource."""
        return self


#: Parent of all contexts
root_context = _RootContext()
del _RootContext
