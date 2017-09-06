"""
autowire.builtins
=================

Builtin resources.

"""
import contextlib

from . import impl, resource
from .base import BaseContext, BaseResource


@resource.create
@impl.implementation
@contextlib.contextmanager
def context(resource: BaseResource, context: BaseContext):
    yield context
