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

Context
-------

Context is a resource implementation container.

You can provide different context object for each context, so that you can configure running environment,
testing options, injecting mock-ups.

You can define context like this

.. code-block:: python

    from autowire import Context

    context = Context()

Each contexts can have parent context.

.. code-block:: python

    child_context = Context(context)

Providing Implementation to context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can provide an implementation for the resource by using
:meth:`~autowire.base_context.BaseContext.provide` method.

.. code-block:: python

    import contextlib

    from autowire.implementation import Implementation

    class BasicImplementation(Implementation):
        @contextlib.contextmanager
        def reify(self, resource, context):
            yield "some-value"

    child_context.provide(basic, BasicImplementation())

Actually, you don't have to make a subclass of :class:`~autowire.implementation.Implementation` for each resource.
:meth:`~autowire.context.Context.plain`, :meth:`~autowire.context.Context.contextual` provides similar functionalities
to :class:`~autowire.resource.Resource`

You can replace above example with

.. code-block:: python

    @child_context.contextual(basic)
    @contextlib.contextmanager
    def with_basic():
        yield "some-value"

Almost same with :meth:`autowire.resource.Resource.contextual` but you have to pass the resource as the first argument.


Resolving Resource
~~~~~~~~~~~~~~~~~~

Resources can have different implementations for each contexts.
This is how to resolve implementation of them.

.. code-block:: python

    with context:
        value = context.resolve(basic)
        print(value)

    with child_context:
        value = child_context.resolve(basic)
        print(value)

The output will be like this ::

    Enter
    Value
    Leave
    some-value

When there's no implementaion to be provided, it will raise :class:`~autowire.exc.ResourceNotProvidedError`

.. code-block:: python

    null = Resource("null", __name__)

    with context:
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

Dependency Inejection
---------------------

You can inject the dependencies when you using :meth:`~autowire.resource.Resource.plain`, :meth:`~autowire.resource.Resource.contextual`

Just pass depending resources to the decorator

.. code-block:: python

    hello = Resource("hello", __name__)

    @hello.plain(basic)
    def get_hello(basic: str):
        return f"Hello, {basic}"


Builtins
--------

There are some builtin resources provided by this package.

See :mod:`autowire.builtins` for more details.
