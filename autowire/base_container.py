"""
autowire.base
=============

Base definitions of autowire.

"""
from __future__ import annotations

import abc
from typing import Any, Callable, ContextManager, Dict, Optional, TypeVar

from autowire.base_resource import BaseResource
from autowire.exc import ResourceNotProvidedError
from autowire.implementation import (
    ContextManagerImplementation,
    Implementation,
    PlainFunctionImplementation,
)
from autowire.resource import Resource

R = TypeVar("R")


class BaseContainer(abc.ABC):
    """
    Dependency injection container base class.

    """

    def __init__(self, parent: Optional[BaseContainer] = None):
        super().__init__()
        self.parent = parent
        self.implementations: Dict[BaseResource[Any], Implementation[Any]] = {}

    def provide(
        self, resource: Resource[R], implementation: Implementation[R]
    ):
        """
        Provide an implementation for resource.

        """
        self.implementations[resource] = implementation

    def find_implementation(
        self, resource: BaseResource[R]
    ) -> Implementation[R]:
        if resource in self.implementations:
            # Find from current container
            return self.implementations[resource]
        elif self.parent is not None:
            # Find from parent container
            return self.parent.find_implementation(resource)
        elif (
            isinstance(resource, Resource)
            and resource.default_implementation is not None
        ):
            # Use default implementation if available
            return resource.default_implementation
        else:
            raise ResourceNotProvidedError(
                "Resource not provided to this context",
                resource.canonical_name,
            )

    def plain(
        self,
        resource: Resource[R],
        *arg_resources: BaseResource[Any],
        **kwarg_resources: BaseResource[Any],
    ):
        """
        Provide resource's implementation with plain function

        arg_resources and kwarg_resources will be used for dependency injection.

        ::

            config = Resource("config", __name__)
            connection_pool = Resource("connection_pool", __name__)
            db_connection = Resource("db_connection", __name__)

            container = Container()

            @container.plain(db_connection, connection_pool, config=config)
            def get_db_connection(connection_pool: Pool, *, config: dict) -> Connection:
                # ...

        """

        def decorator(fn: Callable[..., R]):
            self.provide(
                resource,
                PlainFunctionImplementation(
                    fn, arg_resources, kwarg_resources
                ),
            )
            return fn

        return decorator

    def contextual(
        self,
        resource: Resource[R],
        *arg_resources: BaseResource[Any],
        **kwarg_resources: BaseResource[Any],
    ):
        """
        Provide resource's implementation with context manager

        arg_resources and kwarg_resources will be used for dependency injection.

        ::

            db_connection = Resource("db_connection", __name__)
            db_transaction = Resource("transaction", __name__)

            container = Container()

            @container.contextual(db_transaction, db_connection)
            @contextlib.contextmanager
            def begin_trasaction(db_connection: Connection):
                tx = db_connection.begin()
                try:
                    yield tx
                except Exception:
                    tx.rollback()
                    raise
                finally:
                    tx.commit()
        """

        def decorator(manager: Callable[..., ContextManager[R]]):
            self.provide(
                resource,
                ContextManagerImplementation(
                    manager, arg_resources, kwarg_resources
                ),
            )
            return manager

        return decorator
