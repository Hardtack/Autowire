import contextlib

import pytest

from autowire.utils import RefCounter, as_contextmanager


def test_refcounter():
    value = 0

    # Refcounter should hold the value until it has references.
    @contextlib.contextmanager
    def increase_and_get():
        nonlocal value
        value += 1
        try:
            yield value
        finally:
            value -= 1
    counter = RefCounter(increase_and_get())

    counter.increase()
    assert 1 == counter.count
    assert 1 == counter.value
    assert 1 == value

    counter.increase()
    assert 2 == counter.count
    assert 1 == counter.value
    assert 1 == value

    counter.decrease(None, None, None)
    assert 1 == counter.count
    assert 1 == counter.value
    assert 1 == value

    with counter as v:
        assert 1 == v
        assert 2 == counter.count
        assert 1 == counter.value
        assert 1 == value

        with counter as v2:
            assert 1 == v2
            assert 3 == counter.count
            assert 1 == counter.value
            assert 1 == value
        assert 2 == counter.count

    counter.decrease(None, None, None)
    assert 0 == counter.count
    assert 0 == counter.value
    assert 0 == value

    with pytest.raises(RuntimeError):
        counter.decrease(None, None, None)

    # Refcounter shouldn't increase count value when it failed.
    @contextlib.contextmanager
    def zero_div():
        1 / 0
        yield 1

    counter = RefCounter(zero_div())

    with pytest.raises(ArithmeticError):
        counter.increase()

    assert 0 == counter.count

    with pytest.raises(RuntimeError):
        counter.increase()


def test_as_contextmanager():
    @as_contextmanager
    def foo():
        return 'bar'

    with foo() as value:
        assert 'bar' == value
