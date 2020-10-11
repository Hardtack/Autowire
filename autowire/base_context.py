"""
autowire.base
=============

Base definitions of autowire.

"""
from __future__ import annotations

import collections
import sys
from typing import Any, ContextManager, Dict, Optional, Tuple, TypeVar, cast

from autowire.base_resource import BaseResource
from autowire.exc import ResourceNotProvidedError
from autowire.implementation import Implementation
from autowire.provider import ResourceProvider
from autowire.resource import Resource

R = TypeVar("R")


class BaseContext(ResourceProvider, ContextManager["BaseContext"]):
    """
    Resource management context base class

    """

    def __init__(self, parent: Optional[BaseContext] = None):
        super().__init__()
        self.parent = parent
        self.resource_pool: collections.OrderedDict[
            BaseResource[Any], Tuple[Any, ContextManager[Any]]
        ] = collections.OrderedDict()
        self.implementations: Dict[BaseResource[Any], Implementation[Any]] = {}

    def drain(self):
        """
        Drain all resources resolved by this context.

        """
        items = list(self.resource_pool.items())

        def drainer(
            items: list[BaseResource[Any], Tuple[Any, ContextManager[Any]]]
        ):
            if not items:
                return
            resource, (resolve, manager) = items.pop(0)
            try:
                drainer(items)
            except Exception:
                type_, value, traceback = sys.exc_info()
                self.resource_pool.pop(resource)
                manager.__exit__(type_, value, traceback)
                raise
            else:
                self.resource_pool.pop(resource)
                manager.__exit__(None, None, None)

        drainer(items)

    def provide(
        self, resource: Resource[R], implementation: Implementation[R]
    ):
        """
        Provide an implementation for resource.

        """
        self.implementations[resource] = implementation

    #
    # Resource provider implementation
    #

    def resolve(self, resource: BaseResource[R]) -> R:
        """
        Resolve resource in this context.

        """
        # Find resolved resource from resource pool
        if resource in self.resource_pool:
            resolved, manager = self.resource_pool[resource]
            return resolved

        # Find an implementation
        impl = None
        if resource in self.implementations:
            impl = self.implementations[resource]
        else:
            if self.parent is not None:
                # find from parent
                return self.parent.resolve(resource)
            elif (
                isinstance(resource, Resource)
                and resource.default_implementation is not None
            ):
                # use default implementation
                impl = resource.default_implementation
        if impl is None:
            # finally we fail
            raise ResourceNotProvidedError(
                "Resource not provided to this context",
                resource.canonical_name,
            )
        # resolve
        impl = cast(Implementation[R], impl)
        manager = impl.reify(resource, self)
        resolved = manager.__enter__()
        # throw into resource pool
        self.resource_pool[resource] = (resolved, manager)
        return resolved

    #
    # Context manager implementation
    #

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.drain()
