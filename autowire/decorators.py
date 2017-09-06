"""
autowire.decorators
===================

Decorators for autowire.

"""
from .helpers import GloballySharedImplementation, SharedImplementation


def shared(impl):
    """
    Convert implementation to shared resource implementation.

    Shared resource shares contexxt using reference counting.
    When you try to resolve shared resource that already resolve but not teared
    down, It brings previously resolved resouce. ::

        from contextlib import contextmanager

        from autowire import Context, Resource
        from autowire.decorators import shared

        dog = Resource('dog', __name__)
        walk = Resource('walk', __name__)

        @dog.impl
        @shared
        @contextmanager
        def with_dog(context):
            print("Dog is entering")
            try:
                yield "🐶"
            finally:
                print("Dog leaved")

        @walk.impl
        @contextmanager
        def with_walking(context):
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

    """
    return SharedImplementation(impl)


def globally_shared(impl):
    """
    Convert implementation to globally shared resource implementation.
    Which "globally shared" means resource is shared in providing context.

    Shared resource shares contexxt using reference counting.
    When you try to resolve shared resource that already resolve but not teared
    down, It brings previously resolved resouce.

    The resource will be tied into resource's providing context.
    It means that children's context will not be able to be used
    in this resource. ::

        res1 = Resource('res1', __name__)
        res2 = Resource('res2', __name__)

        @res2.impl
        @globally_shared
        @contextlib.contextmanager
        def with_res1(context):
            with context.resolve(res2) as res1_factory:
                res1 = res1_factory.create_res1()
                try:
                    yield res1
                finally:
                    res1.teardown()

        context = Context()

        child = Context(context)

        @child.autowired(res2)
        def with_res2():
            yield ...

        # Get ResourceNotProvidedError, even though child provides res2.
        # Because res1 was shared in parent context.
        with child.resolve(res1):
            ...

    """
    return GloballySharedImplementation(impl)
