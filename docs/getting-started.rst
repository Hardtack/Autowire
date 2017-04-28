Getting Started
===============

This page shows that how `Autowire` provides resource management and dependency injection.


Resource
--------

Resource is a unimplemented resorce definition.
It can have default implementation and also can have different implementation for each contexts.

Resource have two type of names. First is name, and second one is namespace name.

.. code-block:: python

    from autowire import Resource

    basic = Resource('basic', __name__)

The first parameter is name, and second parameter is namespace.
Generally you can pass ``__name__`` to second parameter.

.. note::
    Since python uses dot (``.``) as module separator, `name` cannot have any dot characters.

The resource will make canonical name with two names ::

    >>> basic.canonical_name
    'some.module.name.basic'

You can set default implementation to resource by :func:`autowire.impl.implement` decorator


.. code-block:: python

    import contextlib
    from autowire import impl

    @impl.implement(basic)
    def implementaion(context):
        print('Enter')
        try:
            yield 'Value'
        finally:
            print('Leave')

The implementation should be a function that takes :class:`~autowire.base.BaseContext` as parameter 
and returns ``ContextManager``. (``(BaseContext) -> ContextManager``)


Context
-------

Context is a resource implementation container.

You can provide different context for each context, so that you can configure running environment,
testing options, injecting mock-ups.

You can define context like this

.. code-block:: python

    from autowire import Context

    context = Context()

Each contexts can have parent context.

.. code-block:: python

    child_context = Context(context)

The root parent of all contexts is :const:`~autowire.context.root.root_context`.

Providing Implementation to context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Providing implementaion for resource in context is almost same with providing to resource.

Simply wrap resource like ``context(resource)`` and pass it to implementer.

.. code-block:: python

    @impl.implement(child_context(basic))
    @contextlib.contextmanager
    def context_implementation(context):
        yield 'Custom Value'

Resolving Resource
~~~~~~~~~~~~~~~~~~

So, resources can have different implementations for each contexts.
This is how to resolve implementation of them.

.. code-block:: python

    with context.resolve(basic) as value:
        print(value)

    with child_context.resolve(basic) as value:
        print(value)

The output will be like this ::

    Enter
    Value
    Leave
    Custom Value

When there's no implementaion to be provided, it will raise :class:`~autowire.exc.ResourceNotProvidedError`

.. code-block:: python

    null = Resource('null', __name__)
    
    with context.resolve(null) as value:  # raise ResourceNotProvidedError
        pass


Dependency Inejection
---------------------

Basically, you can resolve some other resources in impementation from context in arguments.

.. code-block:: python

    other_resource = Resource('other_resource', __name__)

    @impl.implement(other_resource)
    @contextlib.contextmanager
    def implement_other(context):
        with context.resolve(basic) as value:
            yield 'Hello, {}'.format(value)

By the above code, we injected ``basic`` resource to implementation of ``other_resource``.

This is clear, but little boilerplateful.

So we provide some convinience utils.

First one is :func:`autowire.impl.contextual`

This decorator convert any functions that returns ``ContextManager`` to implementation type.

.. code-block:: python

    @impl.contextual(other_resource, basic)
    @contextlib.contextmanager
    def with_other_resource(basic)
        yield 'Hello, {}'.format(basic)

But it doesn't change interface of ``with_other_resource`` so you can still use it like

.. code-block:: python

    with with_other_resource('Basic Mockup') as message:
        print(message)


When you don't even want a context management, you can use :func:`autowire.impl.plain`
which means plain function.

.. code-block:: python

    @impl.plain(other_resource, basic)
    def get_other_resource(basic):
        return 'Hello, {}'.format(basic)

You can surely use this as plain function

.. code-block:: python

    print(get_other_resource('Basic Mockup'))

Since :func:`~autowire.impl.contextual` and :func:`~autowire.impl.plain`
don't change original function's interface, you have care about decorators for implementation.

When you want to apply decoration to a original function, just use that normally

.. code-block:: python

    @impl.plain(other_resource, basic)
    @decorator
    def get_other_resource(basic):
        return 'Hello, {}'.format(basic)

But, when you want to apply them to actual implementation, add them to keyword-only argument
``decorators``.

.. code-block:: python

    @impl.plain(other_resource, basic, decorators=[decorator])
    def get_other_resource(basic):
        return 'Hello, {}'.format(basic)
