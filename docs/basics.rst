Basic
=====

This page shows that how `Autowire` provides resource management and dependency injection.


Basic Resource Management
-------------------------


.. code-block:: python

    from contextlib import contextmanager

    from autowire import Context, Resource

    hello = Resource('hello', __name__)

    @hello.impl
    @contextmanager
    def with_hello_message(context):
        print("Setup hello message")
        try:
            yield "Hello, World!"
        finally:
            print("Teardown hello message")

    context = Context()

    with context.resolve(hello) as message:
        print(message)

    # Output:
    # Setup hello message
    # Hello, World!
    # Teardown hello message


The parameter of `impl` can be any function that takes `Context` as parameter 
and returns `ContextManager`. (`(Context) -> ContextManager`)


Basic Dependency Inejection
---------------------------

.. code-block:: python

    number = Resource('number', __name__)
    double = Resource('double', __name__)

    @double.autowired(number)
    @contextlib.contextmanager
    def get_double(number):
        yield number * 2

    context = Context()

    # You can provide resource only in specfic context
    @context.provide(number)
    @contextlib.contextmanager
    def get_one(context):
        yield 1

    with context.resolve(double) as value:
        print(value)
        # Output: 2

    another_context = Context()

    # Since another_context doesn't provide number resource,
    # It raises ResourceNotProvidedError
    with another_context.resolve(double) as value:
        pass
