"""
autowire.base
=============

Base definitions of autowire.

"""
import abc
import contextlib
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
    def default_implementation(self) -> 'Implementation':
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
        return impl.reify(resource, self)

    def run(self, resource: BaseResource):
        """
        Resolve a resource just for side-effect.

        It is useful when you want entry-point resource. ::

            @resource.create
            @impl.autowire('foo', foo)
            @impl.autowire('bar', bar)
            @impl.plain
            def main(foo, bar):
                print(foo)
                print(bar)
                ...

            ...

            if __name__ == '__main__':
                context.run(main)

        """
        with self.resolve(resource) as value:
            return value

    def resolve_all(self, resources):
        """Resolve resources in this context."""
        contexts = [self.resolve(resource) for resource in resources]

        @contextlib.contextmanager
        def merged_context(rest: list):
            if rest:
                first, *rest = rest
                with first as value:
                    with merged_context(rest) as rest_values:
                        yield [value] + rest_values
            else:
                yield []
        return merged_context(contexts)

    def find_resource_impl(self, resource: BaseResource) -> 'Implementation':
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
                keyword_items = list(keywords.items())
                keyword_keys = [k for k, _ in keyword_items]
                keyword_resources = [v for _, v in keyword_items]

                with self.resolve_all(positionals) as resolved_args, \
                        self.resolve_all(
                            keyword_resources) as resolved_kwarg_values:
                    resolved_kwargs = {}
                    for k, v in zip(keyword_keys, resolved_kwarg_values):
                        resolved_kwargs[k] = v
                    partial = functools.partial(
                        fn, *resolved_args, **resolved_kwargs)
                    return partial(*args, **kwargs)
            return wrapper
        return decorator


class Implementation(object, metaclass=abc.ABCMeta):
    """Base implementation type"""
    @abc.abstractmethod
    def reify(self, resource: BaseResource, context: BaseContext):
        pass
