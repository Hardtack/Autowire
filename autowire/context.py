from typing import Any, Callable, ContextManager, Optional, TypeVar

from autowire.base_context import BaseContext
from autowire.base_resource import BaseResource
from autowire.builtins import context
from autowire.implementation import (
    ContextManagerImplementation,
    PlainFunctionImplementation,
)
from autowire.resource import Resource

R = TypeVar("R")


class Context(BaseContext):
    """
    Resource management context

    """

    def __init__(self, parent: Optional[BaseContext] = None):
        super().__init__(parent)
        self._set_builtins()

    def _set_builtins(self):
        # Current context
        @self.plain(context)
        def get_context():
            return self

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

            context = Context()

            @context.plain(db_connection, connection_pool, config=config)
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

            context = Context()

            @context.contextual(db_transaction, db_connection)
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
