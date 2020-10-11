import contextlib
from typing import Sequence

from autowire.base_container import BaseContainer
from autowire.base_resource import BaseResource
from autowire.context import Context


class Container(BaseContainer):
    """
    Dependency injection container

    """

    @contextlib.contextmanager
    def context(self, preload: Sequence[BaseResource] = ()):
        """
        Get a DI context from this container. ::

            with container.context() as context:
                value = context.resolve(resource)
                ...

        :param preload: resources to be preloaded on this context.

        """
        with Context(self, None) as context:
            # Preload
            for resource in preload:
                context.resolve(resource)
            yield context
