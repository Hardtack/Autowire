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

    basic = Resource('basic', __name__)

The first parameter is name, and second parameter is namespace.
Generally you can pass ``__name__`` to second parameter.

.. note::
    Since python uses dot (``.``) as module separator, `name` cannot have any dot characters.

The resource will make canonical name with two names ::

    >>> basic.canonical_name
    'some.module.name.basic'

You can set default implementation to resource by :func:`autowire.impl.implement`


.. code-block:: python

    import contextlib
    from autowire import impl

    @impl.implementation
    @contextlib.contextmanager
    def implementaion(resource, context):
        print('Enter')
        try:
            yield 'Value'
        finally:
            print('Leave')
    
    basic.implement(implementation)

The implementation should be an instance of :class:`~autowire.base.Implementation`
:func:`~autowire.impl.implementation` decorator converts contextmanager function
to instance of :class:`~autowire.base.Implementation`.

You can also create resource with implementation at once.

.. code-block:: python

    import contextlib
    from autowire import resource

    @resource.create
    @impl.implementation
    @contextlib.contextmanager
    def basic(context):
        print('Enter')
        try:
            yield('Value')
        finally:
            print('Leave')

The function ``basic`` will be a resource and also be a function.


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

You can provide an implementation for the resource by using
:meth:`~autowire.base.BaseContext.provide` method.

.. code-block:: python

    @impl.implementation
    @contextlib.contextmanager
    def context_implementation(resource, context):
        yield 'Custom Value'

    child_context.provide(basic, context_implementation)

:meth:`~autowire.base.BaseContext.provide` also can be used as a decorator

.. code-block:: python

    @child_context.provide(basic)
    @impl.implementation
    @contextlib.contextmanager
    def context_implementation(resource, context):
        yield 'Custom Value'

Resolving Resource
~~~~~~~~~~~~~~~~~~

Resources can have different implementations for each contexts.
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


Functional Interface
--------------------

You don't always need neither resource or context for your implementation.
And also you don't need any resource management for providing implementation.

There are some useful utilities for these use cases.

First one is :func:`~autowire.impl.contextual`. It converts simple context manager
function to implementation.

.. code-block:: python

    import contextlib
    from autowire import impl

    @res.implement
    @impl.contexual
    @contextlib.contextmanager
    def res_impl():
        value = build_resource()
        try:
            yield value
        finally:
            destroy_resource(value)

Second one is :func:`~autowire.impl.contextmanager`, which is a shortcut for above.

.. code-block:: python

    from autowire import impl

    @res.implement
    @impl.contextmanager
    def res_impl():
        value = build_resource()
        try:
            yield value
        finally:
            destroy_resource(value)

Last one is :func:`~autowire.impl.plain`. It converts plain function to implementation.

.. code-block:: python

    from autowire import impl

    @res.implement
    @impl.plain
    def get_impl():
        return "Implementation!"

All functional interface decorators preserve decorated function's interface.

.. code-block:: python
    
    >>> get_impl()
    "Implementation!"


Dependency Inejection
---------------------

Basically, you can resolve some other resources from the context in impementations.

.. code-block:: python

    @impl.implementation
    @contextlib.contextmanager
    def some_implementation(resource, context):
        with context.resolve(basic) as value:
            yield 'Hello, {}'.format(value)

By the above code, we injected ``basic`` resource to implementation of ``other_resource``.

This is clear, but little boilerplateful.

So we provide :func:`~autowire.impl.autowired` decorator to do this simply.

.. code-block:: python

    @other_resource.implement
    @impl.autowired('basic', basic)
    @impl.plain
    def with_other_resource(basic)
        reutnr 'Hello, {}'.format(basic)

First argument is a name that be used for keyword argument. Second one is resource to be resolved.
When the name is not provided, The ``name`` property of resource will be used by default.

:func:`~autowire.impl.autowired` decorator can be only used for functional interface implementations.
