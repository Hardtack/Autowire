"""
autowire.builtins
=================

Builtin resources.

"""
import contextlib

from .base import BaseContext, BaseResource


#
# Types
#


class ContextResource(BaseResource):
    @property
    def default_implementation(self):
        @contextlib.contextmanager
        def impl(resource: BaseResource, context: BaseContext):
            yield context

        return impl

#
# Resources
#


#: Current context resource
context = ContextResource('context', __name__)
