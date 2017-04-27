"""
autowire.utils
==============

Common utilities.

"""
import contextlib
import functools


class RefCounter(object):
    """Preserve context until it has any references."""
    def __init__(self, contextmanager):
        super().__init__()
        self.count = 0
        self.contextmanager = contextmanager
        self.value = None

    def increase(self):
        self.count += 1
        if self.count == 1:
            self.value = self.contextmanager.__enter__()

    def decrease(self, exc_type, exc_value, tb):
        if self.count == 1:
            self.value = 0
            self.contextmanager.__exit__(exc_type, exc_value, tb)
        self.count -= 1

    def __enter__(self):
        self.increase()
        return self.value

    def __exit__(self, exc_type, exc_value, tb):
        self.decrease(exc_type, exc_value, tb)


def apply_decorators(fn, decorators):
    """Apply multiple decorators at once."""
    for decorator in decorators:
        fn = decorator(fn)
    return fn


def as_contextmanager(fn):
    """
    Convert to context manager. ::

        @as_contextmanager
        def foo(name):
            return 'Hello, {}'.format(name)

    is equivalent to ::

        @contextlib.contextmanager
        def foo(name):
            yield 'Hello, {}'.format(name)
    """
    @functools.wraps(fn)
    @contextlib.contextmanager
    def wrapper(*args, **kwargs):
        yield fn(*args, **kwargs)
    return wrapper
