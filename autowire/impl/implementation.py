"""
impl.implementation
===================

Implementation classes

"""
import abc
import contextlib
import functools
import types
import typing

from autowire._compat import ContextManger
from autowire.base import BaseResource, BaseContext, Implementation


Evaluator = typing.Callable[
    [types.FunctionType, BaseResource, BaseContext], 
    ContextManger
]


class FunctionImplementation(Implementation, metaclass=abc.ABCMeta):
    """Implementation with wrapping function and evaluator"""

    def __init__(self, function: types.FunctionType, evaluator: Evaluator):
        super().__init__()
        self.function = function
        self.evaluator = evaluator
        functools.update_wrapper(self, function)

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    @contextlib.contextmanager
    def reify(self, resource: BaseResource, context: BaseContext):
        with self.evaluator(self.function, resource, context) as value:
            yield value
