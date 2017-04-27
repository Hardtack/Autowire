import contextlib

import pytest

from autowire import Resource, Context
from autowire.exc import ResourceNotProvidedError
from autowire.decorators import globally_shared, shared


def test_shared():
    counter = Resource('counter', __name__)

    context = Context()

    count = 0

    @context.provide(counter)
    @shared
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

    @context.provide(counter)
    @shared
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


def test_globally_shared():
    number = Resource('number', __name__)

    context = Context()

    counter = 0

    @number.impl
    @globally_shared
    @contextlib.contextmanager
    def get_next_number(context):
        nonlocal counter
        counter += 1
        yield counter

    child = Context(context)

    with child.resolve(number) as value1, context.resolve(number) as value2:
        assert 1 == value1
        assert 1 == value2


def test_globally_shared_failure():
    number = Resource('number', __name__)
    double = Resource('double', __name__)

    context = Context()

    @number.from_func(number, decorators=[globally_shared])
    def get_doubled(number):
        return number * 2

    child = Context(context)

    @child.provide_from_func(number)
    def get_one(context):
        return 1

    with pytest.raises(ResourceNotProvidedError):
        with child.resolve(double):
            pass
