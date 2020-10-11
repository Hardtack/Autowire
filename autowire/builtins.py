"""
autowire.builtins
=================

Builtin resources.

"""
from autowire.resource import Resource

context: Resource = Resource("context", __name__)
