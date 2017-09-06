"""
autowire.decorators
===================

Decorators for autowire.

"""
from .helpers import GloballySharedImplementation, SharedImplementation
from .impl.function import FunctionImplementation


def shared(impl: FunctionImplementation=None, *, globally=False):
    """
    Convert implementation to shared resource implementation.

    Shared resource shares context using reference counting.
    When you try to resolve shared resource that already resolve but not teared
    down, It brings previously resolved resouce. ::

        from contextlib import contextmanager

        from autowire import Context, Resource
        from autowire.decorators import shared

        dog = Resource('dog', __name__)
        walk = Resource('walk', __name__)

        @dog.implement
        @shared
        @impl.implementation
        @contextmanager
        def with_dog(resource, context):
            print("Dog is entering")
            try:
                yield "🐶"
            finally:
                print("Dog leaved")

        @walk.implement
        @impl.implementation
        @contextmanager
        def with_walking(resource, context):
            with context.resolve(dog) as dog_value:
                yield "Walking with {}".format(dog_value)

        context = Context()

        with context.resolve(walk) as message:
            print(message)
            with context.resolve(dog) as dog_value:
                print("Feeding {}".format(dog_value))

        # Output:
        # Dog is entering
        # Walking with 🐶
        # Feeding 🐶
        # Dog leaved

    When set globally to `True` the resource will be shared globally.
    "Globally shared" means resource is shared in providing context.

    Globally shared resource will be tied into resource's providing context.
    It means that children's context will not be able to be used
    in this resource. ::

        res1 = Resource('res1', __name__)
        res2 = Resource('res2', __name__)

        @res2.implement
        @shared(globally=True)
        @impl.implementation
        @contextlib.contextmanager
        def with_res1(resource, context):
            with context.resolve(res2) as res1_factory:
                res1 = res1_factory()
                try:
                    yield res1
                finally:
                    res1.teardown()

        context = Context()

        child = Context(context)

        @child.autowired(res2)
        def with_res2():
            yield ...

        # Get ResourceNotProvidedError, even though child context provides
        # res2. Because res1 was shared globally in parent context.
        with child.resolve(res1):
            ...


    """
    if impl is not None:
        return shared(globally=globally)(impl)

    def decorator(impl: FunctionImplementation):
        if globally:
            return GloballySharedImplementation(impl)
        else:
            return SharedImplementation(impl)
    return decorator
