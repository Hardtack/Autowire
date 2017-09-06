"""
autowire.resource.utils
=======================

Resource utilties.

"""
import contextlib

from autowire import impl
from autowire.base import BaseResource, BaseContext
from autowire.exc import ResourceNotProvidedError


@impl.implementation
@contextlib.contextmanager
def default_implementation(resource: BaseResource, context: BaseContext):
    """No such resource."""
    raise ResourceNotProvidedError(
        "No such resource {resource}".format(
            resource=resource.canonical_name,
        ))
    yield None
