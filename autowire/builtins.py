"""
autowire.builtins
=================

Builtin resources.

"""
from autowire.base_context import BaseContext
from autowire.resource import Resource

#: Resource that indicating current context
context: Resource[BaseContext] = Resource("context", __name__)
