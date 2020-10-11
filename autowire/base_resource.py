import abc
from typing import Generic, TypeVar

R = TypeVar("R")


class BaseResource(abc.ABC, Generic[R]):
    """
    Decalarative resource definition.

    """

    def __init__(self, name: str, namespace: str):
        super().__init__()
        if "." in name:
            raise ValueError(
                "Resource cannot contain a dot(.) in their name", name
            )
        self.name = name
        self.namespace = namespace

    @property
    def canonical_name(self) -> str:
        """
        Canonical name of resource.

        It's <namespace>.<name>

        """
        return self.namespace + "." + self.name

    def __eq__(self, other):
        return (
            isinstance(other, BaseResource)
            and self.canonical_name == other.canonical_name
        )

    def __hash__(self):
        return hash((BaseResource, self.canonical_name))

    def __repr__(self):  # pragma: no cover
        return f"Resource({self.name!r}, {self.namespace!r})"
