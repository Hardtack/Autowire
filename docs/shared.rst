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
