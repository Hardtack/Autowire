"""
autowire.base
=============

Base definitions of autowire.

"""
from __future__ import annotations

import collections
import contextlib
import sys
from typing import (
    Any,
    ContextManager,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from autowire.base_container import BaseContainer
from autowire.base_resource import BaseResource
from autowire.provider import ResourceProvider

R = TypeVar("R")


class NotPooled(Exception):
    """
    Internal class for fiding pooled resource
    """

    pass


class Context(ResourceProvider, ContextManager["Context"]):
    """
    Resource management context base class

    """

    def __init__(self, container: BaseContainer, parent: Optional[Context]):
        super().__init__()
        self.container = container
        self.parent = parent
        self.resource_pool: collections.OrderedDict[
            BaseResource[Any], Tuple[Any, ContextManager[Any]]
        ] = collections.OrderedDict()
        self.children: List[Context] = []

    def drain(self):
        """
        Drain all resources resolved by this context.

        """

        def children_drainer(children: List[Context]):
            if not children:
                return
            child = children.pop(0)
            try:
                children_drainer(children)
            finally:
                child.drain()

        items = list(self.resource_pool.items())

        def drainer(
            items: list[BaseResource[Any], Tuple[Any, ContextManager[Any]]]
        ):
            if not items:
                # Drain all children
                children_drainer(self.children)
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

    @contextlib.contextmanager
    def child(self, preload: Sequence[BaseResource] = ()):
        """
        Create a child context ::

            with context.child() as child:
                value = child.resolve(resource)
                ...

        :param preload: resources to be preloaded
        """
        with Context(self.container, self) as child:
            self.children.append(child)
            # Preload
            for resource in preload:
                child.resolve(resource)
            yield child

    #
    # Resource provider implementation
    #

    def resolve(self, resource: BaseResource[R]) -> R:
        """
        Resolve resource in this context.

        """
        try:
            return self._find_resource(resource)
        except NotPooled:
            pass

        # Create new resource if pooled resource not found
        impl = self.container.find_implementation(resource)
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

    #
    # Privates
    #

    def _find_resource(self, resource: BaseResource[R]) -> R:
        # Find resolved resource from resource pool
        if resource in self.resource_pool:
            resolved, manager = self.resource_pool[resource]
            return resolved
        # Find from parent
        if self.parent is not None:
            return self.parent._find_resource(resource)
        else:
            raise NotPooled()
