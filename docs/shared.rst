Shared Resource
===============

The resource can be used multiple times in one context.
Sometimes you don't want to build a new resource for each usages.
You can share resources by `shared` decorator.


Sharing Resource
----------------


.. code-block:: python

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

Since ``dog`` resource is shared resource, setup & teardown were called only once.


Globally Shared Resource
------------------------

When you have nested contexts, the shared resource will be created for each contexts.
If you want to have only one resource per whole contexts, you can do that with
``globally_shared`` decorator.


.. code-block:: python

    from contextlib import contextmanager

    from autowire import Context, Resource, impl
    from autowire.decorators import shared

    dog = Resource('dog', __name__)
    walk = Resource('walk', __name__)

    @impl.implement(dog)
    @globally_shared
    @contextmanager
    def with_dog(context):
        print("Dog is entering")
        try:
            yield "🐶"
        finally:
            print("Dog leaved")

    @impl.implement(walk)
    @contextmanager
    def with_walking(context):
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

    from contextlib import contextmanager

    from autowire import Context, Resource
    from autowire.decorators import shared

    dog = Resource('dog', __name__)
    walk = Resource('walk', __name__)

    @impl.implement(walk)
    @globally_shared
    @contextmanager
    def with_walking(context):
        with context.resolve(dog) as dog_value:
            yield "Walking with {}".format(dog_value)

    context = Context()
    child = Context(context)

    # Provide dog
    @impl.implement(child(dog))
    @contextmanager
    def with_dog(context):
        yield "🐶"

    # Will raise ResourceNotProvidedError
    with child.resolve(walk) as message:
        ...
