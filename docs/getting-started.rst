Getting Started
===============

This page shows that how `Autowire` provides resource management and dependency injection.


Resource
--------

Resource is a implementable resorce definition.
It can have default implementation and also can have different implementation for each contexts.

Resource have two type of names. First is name, and second one is namespace name.

.. code-block:: python

    from autowire import Resource

    basic = Resource("basic", __name__)

The first parameter is name, and second parameter is namespace.
Generally you can pass ``__name__`` to second parameter.

.. note::
    Since python uses dot (``.``) as module separator, `name` cannot have any dot characters.

The resource will make canonical name with two names ::

    >>> basic.canonical_name
    "some.module.name.basic"

You can set default implementation with context manager to resource by :meth:`~autowire.resource.Resource.contextual`


.. code-block:: python

    import contextlib

    @basic.contextual()
    @contextlib.contextmanager
    def implementaion():
        print("Enter")
        try:
            yield "Value"
        finally:
            print("Leave")

Or you can use a plain function for implementation by using :meth:`~autowire.resource.Resource.plain`

.. code-block:: python

    @basic.plain()
    def implementaion():
        return "Hello!"

This is equivalent to

.. code-block:: python

    import contextlib

    @basic.contextual()
    @contextlib.contextmanager
    def implementaion():
        yield "Hello!"

Container
---------

Context dependency injection & resource implementation provider

You can provide different container for each environment, so that you can configure running environment,
testing options, injecting mock-ups.

You can define context like this

.. code-block:: python

    from autowire import Container

    container = Container()

Each contexts can have parent context.

.. code-block:: python

    child_container = Container(container)

Providing Implementation to the container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can provide an implementation for the resource by using
:meth:`~autowire.base_container.BaseContainer.provide` method.

.. code-block:: python

    import contextlib

    from autowire.implementation import Implementation

    class BasicImplementation(Implementation):
        @contextlib.contextmanager
        def reify(self, resource, context):
            yield "some-value"

    child_container.provide(basic, BasicImplementation())

Actually, you don't have to make a subclass of :class:`~autowire.implementation.Implementation` for each resource.
:meth:`~autowire.base_container.BaseContainer.plain`, :meth:`~autowire.base_container.BaseContainer.contextual` provides similar functionalities
to :class:`~autowire.resource.Resource`

You can replace above example with

.. code-block:: python

    @child_container.contextual(basic)
    @contextlib.contextmanager
    def with_basic():
        yield "some-value"

Almost same with :meth:`autowire.resource.Resource.contextual` but you have to pass the resource as the first argument.


Container
~~~~~~~~~

To reify your resource implementation, you have to use :class:`~autowire.context.Context`.

You can get a root context by using :meth:`~autowire.container.Container.context`

.. code-block:: python

    with container.context() as context:
        value = context.resolve(basic)
        print(value)

The output will be like this ::

    Enter
    Value
    Leave

Since :meth:`~autowire.container.Container.context` is a context manager, you should use this method with ``with`` statement.

When there's no implementaion to be provided, it will raise :class:`~autowire.exc.ResourceNotProvidedError`

.. code-block:: python

    null = Resource("null", __name__)

    with container.context() as context:
        context.resolve(null)  # raise ResourceNotProvidedError

Resource Management
-------------------

The reason why you should use context object with `with` statement is resource management.

Every resolved resources will be released on context's ``__exit__`` call.

But if you want manage the lifecycle manually, you can use :meth:`~autowire.base_context.BaseContext.drain` for releasing all resources.

.. code-block:: python

    try:
        value = context.resolve(basic)
        print(value)
    finally:
        context.drain()

is equivalent to

.. code-block:: python

    with context:
        value = context.resolve(basic)
        print(value)

Child context
-------------

Contexts are nestable. You can hold some resources on your parent context and keep use them.

.. code-block:: python

    with container.context() as context:
        pool = context.resolve(global_connection_pool)
        connection = pool.get_connection()

        with context.child() as child:
            # This is same with pool above and retained until parent context be drained
            pool2 = child.resolve(global_connection_pool)

            # But this will be releases on child context be drained
            tx = child.resolve(transaction)


Dependency Inejection
---------------------

You can inject the dependencies when you using :meth:`~autowire.resource.Resource.plain`, :meth:`~autowire.resource.Resource.contextual`

Just pass depending resources to the decorator

.. code-block:: python

    hello = Resource("hello", __name__)

    @hello.plain(basic)
    def get_hello(basic: str):
        return f"Hello, {basic}"
