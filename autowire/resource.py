from __future__ import annotations

from typing import Any, Callable, ContextManager, Optional, TypeVar

from autowire.base_resource import BaseResource
from autowire.implementation import (
    ContextManagerImplementation,
    Implementation,
    PlainFunctionImplementation,
)

R = TypeVar("R")


class Resource(BaseResource[R]):
    """
    Decalarative resource definition.

    Namespace generally be the module's name.

    `name` cannot include any dot(.) characters. ::

        >>> resource = BaseResource('name', __name__)

    """

    def __init__(self, name: str, namespace: str):
        super().__init__(name, namespace)
        self.default_implementation: Optional[Implementation] = None

    def plain(
        self,
        *arg_resources: BaseResource[Any],
        **kwarg_resources: BaseResource[Any],
    ):
        """
        Set default implementation with plain function

        arg_resources and kwarg_resources will be used for dependency injection.

        ::

            config = Resource("config", __name__)
            connection_pool = Resource("connection_pool", __name__)
            db_connection = Resource("db_connection", __name__)

            @db_connection.plain(connection_pool, config=config)
            def get_db_connection(connection_pool: Pool, *, config: dict) -> Connection:
                # ...

        """

        def decorator(fn: Callable[..., R]):
            self.default_implementation = PlainFunctionImplementation(
                fn, arg_resources, kwarg_resources
            )
            return fn

        return decorator

    def contextual(
        self,
        *arg_resources: BaseResource[Any],
        **kwarg_resources: BaseResource[Any],
    ):
        """
        Set default implementation with context manager

        arg_resources and kwarg_resources will be used for dependency injection.

        ::

            db_connection = Resource("db_connection", __name__)
            db_transaction = Resource("transaction", __name__)

            @db_transaction.contextual(db_connection)
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
            self.default_implementation = ContextManagerImplementation(
                manager, arg_resources, kwarg_resources
            )
            return manager

        return decorator
