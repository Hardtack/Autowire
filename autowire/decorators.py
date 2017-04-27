"""
autowire.decorators
===================

Decorators for autowire.

"""
from . import helpers
from .base import BaseResource


def autowired(*dependencies: BaseResource):
    """
    Convert a plain function to resource implementation with dependencies.
    It changes interface of decorated function to implementation interface.
    """
    def decorator(fn):
        return helpers.autowired(fn, *dependencies)
    return decorator


# It already has decorator interface
shared = helpers.shared
