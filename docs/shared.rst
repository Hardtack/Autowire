Shared Resource
===============

The resource can be used multiple times in one context.
Sometimes you don't want to build a new resource for each usages.
You can share resources by `shared` decorator.


Sharing Resource
----------------


.. code-block:: python

    import contextlib
    from autowire import Context, Resource
    from autowire.decorators import shared

    dog = Resource('dog', __name__)
    walk = Resource('walk', __name__)

    @dog.implement
    @shared
    @impl.implementation
    @contextlib.contextmanager
    def with_dog(resource, context):
        print("Dog is entering")
        try:
            yield "🐶"
        finally:
            print("Dog leaved")

    @walk.implement
    @impl.implementation
    @contextlib.contextmanager
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

Since ``dog`` resource is shared resource, setup & teardown were called only once.


Globally Shared Resource
------------------------

When you have nested contexts, the shared resource will be created for each contexts.
If you want to have only one resource per whole contexts, you can do that by set
``globally`` to :const:`True`.


.. code-block:: python

    import contextlib

    from autowire import Context, Resource, impl
    from autowire.decorators import shared

    dog = Resource('dog', __name__)
    walk = Resource('walk', __name__)

    @dog.implement
    @shared(globally=True)
    @impl.implementation
    @contextlib.contextmanager
    def with_dog(resource, context):
        print("Dog is entering")
        try:
            yield "🐶"
        finally:
            print("Dog leaved")

    @walk.implement
    @impl.implementation
    @contextlib.contextmanager
    def with_walking(resource, context):
        with context.resolve(dog) as dog_value:
            yield "Walking with {}".format(dog_value)

    context = Context()
    child = Context(context)

    with context.resolve(walk) as message:
        print(message)
        with child.resolve(dog) as dog_value:
            print("Feeding {}".format(dog_value))

    # Output:
    # Dog is entering
    # Walking with 🐶
    # Feeding 🐶
    # Dog leaved

Since, globally shared resource can be only defined on providing context, it can't use
children context's resources.

.. code-block:: python

    import contextlib

    from autowire import Context, Resource
    from autowire.decorators import shared

    dog = Resource('dog', __name__)
    walk = Resource('walk', __name__)

    @walk.implement
    @shared(globally=True)
    @contextlib.contextmanager
    def with_walking(resource, context):
        with context.resolve(dog) as dog_value:
            yield "Walking with {}".format(dog_value)

    context = Context()
    child = Context(context)

    # Provide dog
    @child.provide(dog)
    @contextlib.contextmanager
    def with_dog(context):
        yield "🐶"

    # Will raise ResourceNotProvidedError
    with child.resolve(walk) as message:
        ...
