"""
autowire.base
=============

Base definitions of autowire.

"""
import abc

from autowire._compat import abstractproperty


class BaseResource(object, metaclass=abc.ABCMeta):
    """
    Decalarative contextual resource definition.
    """
    def __init__(self, name: str, namespace: str) -> None:
        """
        Create a resource with name.
        Namespace generally be the module's name.

        `name` cannot include any dot(.) characters.

            >>> resource = Resource('name', __name__)

        """
        super().__init__()
        self.name = name
        self.namespace = namespace

    def is_valid_name(self, name: str) -> bool:
        """
        Resource name validation.
        """
        return '.' not in name

    @property
    def canonical_name(self) -> str:
        """
        Canonical name of resource.

        It's <namespace>.<name>

        """
        return self.namespace + '.' + self.name

    @abstractproperty
    def default_implementation(self):
        pass

    def __repr__(self):
        return "{cls}({name!r}, {namespace!r})".format(
            cls=type(self).__name__,
            name=self.name,
            namespace=self.namespace
        )


class BaseContext(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_implementation(self, resource: BaseResource):
        """Get resource implementation from this context."""
        pass

    @abc.abstractmethod
    def provided_by(self, resource: BaseResource) -> 'BaseContext':
        """Find context that provides resource."""
        pass

    def resolve(self, resource: BaseResource):
        """Resolve resource in this context."""
        impl = self.find_resource_impl(resource)
        return impl(self)

    def find_resource_impl(self, resource: BaseResource):
        """Find resource implementation from this context and its parents."""
        context = self.provided_by(resource)
        return context.get_implementation(resource)
