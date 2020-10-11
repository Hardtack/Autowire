from __future__ import annotations

import abc
import contextlib
from typing import Any, Callable, ContextManager, Dict, Generic, Tuple, TypeVar

from autowire.base_resource import BaseResource
from autowire.provider import ResourceProvider

R = TypeVar("R")


class Implementation(Generic[R], metaclass=abc.ABCMeta):
    """
    Declarative base type for implementation

    """

    @abc.abstractmethod
    def reify(
        self,
        resource: BaseResource[R],
        provider: ResourceProvider,
    ) -> ContextManager[R]:  # pragma: no cover
        """
        Reify the resource

        """
        pass


class ContextManagerImplementation(Implementation[R]):
    """
    Use context manager as an implementaion

    """

    def __init__(
        self,
        manager_generator: Callable[..., ContextManager[R]],
        arg_resources: Tuple[BaseResource[Any], ...],
        kwarg_resources: Dict[str, BaseResource[Any]],
    ):
        super().__init__()
        self.manager_generator = manager_generator
        self.arg_resources = arg_resources
        self.kwarg_resources = kwarg_resources

    def reify(
        self,
        resource: BaseResource[R],
        provider: ResourceProvider,
    ):
        args = [provider.resolve(arg) for arg in self.arg_resources]
        kwargs = {
            name: provider.resolve(arg)
            for name, arg in self.kwarg_resources.items()
        }

        return self.manager_generator(*args, **kwargs)


class PlainFunctionImplementation(ContextManagerImplementation[R]):
    """
    Use plain function as an implementaion

    """

    def __init__(
        self,
        fn: Callable[..., R],
        arg_resources: Tuple[BaseResource[Any], ...],
        kwarg_resources: Dict[str, BaseResource[Any]],
    ):
        @contextlib.contextmanager
        def manager(*args, **kwargs):
            yield fn(*args, **kwargs)

        super().__init__(manager, arg_resources, kwarg_resources)
        self.fn = fn
