"""
autowire.resource.utils
=======================

Resource utilties.

"""
import contextlib

from autowire.base import BaseContext
from autowire.exc import ResourceNotProvidedError


def create_default_impl(name: str, namespace: str):
    @contextlib.contextmanager
    def default_impl(context: BaseContext):
        """No such resource."""
        raise ResourceNotProvidedError(
            "No such resource {namespace}.{name}".format(
                namespace=namespace,
                name=name,
            ))
        yield None
    return default_impl
