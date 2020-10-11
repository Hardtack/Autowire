import abc
from typing import TypeVar

from autowire.base_resource import BaseResource

R = TypeVar("R")


class ResourceProvider(abc.ABC):
    """
    Declarative base class for resource provider
    """

    @abc.abstractmethod
    def resolve(self, resource: BaseResource[R]) -> R:  # pragma: no cover
        pass
