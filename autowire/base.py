"""
autowire.base
=============

Base definitions of autowire.

"""
import abc
import functools

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

    def partial(self, *positionals, **keywords):
        """
        New function with partial application of the given resources. ::

            @context.partial(foo_resource, bar=bar_resource)
            def func(foo, baz, *, bar=None):
                print(foo)
                print(bar)
                print(baz)

            func('Bar')
            # Output:
            # Foo
            # Bar
            # Baz

        """
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                # Resolve dependencies recursively
                def with_dependencies(fn, positionals, keywords):
                    if positionals:
                        first = positionals[0]
                        rest = positionals[1:]
                        with self.resolve(first) as resolved:
                            partial = functools.partial(fn, resolved)
                            return with_dependencies(partial, rest, keywords)
                    elif keywords:
                        for name, resource in keywords.items():
                            break
                        rest = dict(keywords)
                        rest.pop(name)
                        with self.resolve(resource) as resolved:
                            partial = functools.partial(fn, **{name: resolved})
                            return with_dependencies(
                                partial, positionals, rest)
                    else:
                        return fn
                partial = with_dependencies(fn, positionals, keywords)
                return partial(*args, **kwargs)
            return wrapper
        return decorator
