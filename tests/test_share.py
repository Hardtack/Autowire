import contextlib

import pytest

from autowire import Resource, Context, ResourceNotProvidedError


def test_shared():
    counter = Resource('counter', __name__)

    context = Context()

    count = 0

    @context.shared(counter)
    @contextlib.contextmanager
    def increase_and_get_count(context):
        nonlocal count
        count += 1
        yield count

    with context.resolve(counter) as value:
        assert 1 == value
        with context.resolve(counter) as value:
            assert 1 == value
    with context.resolve(counter) as value:
        assert 2 == value


def test_shared_autowire():
    counter = Resource('counter', __name__)
    double = Resource('double', __name__)

    @double.from_func(counter)
    def double_count(counter):
        return counter * 2

    context = Context()

    count = 0

    @context.shared(counter)
    @contextlib.contextmanager
    def increase_and_get_count(context):
        nonlocal count
        count += 1
        yield count

    with context.resolve(double) as value:
        assert 2 == value
        with context.resolve(double) as value:
            assert 2 == value
    with context.resolve(counter) as value:
        assert 2 == value


def test_shared_not_provided():
    number = Resource('number', __name__)
    square = Resource('square', __name__)

    context = Context()

    @context.provide_from_func(square, number, shared=True)
    def square_value(value):
        return value * value

    child = Context(context)

    @child.provide_from_func(number)
    def get_three():
        return 3

    with pytest.raises(ResourceNotProvidedError):
        with child.resolve(square):
            pass
