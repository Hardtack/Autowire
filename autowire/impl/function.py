"""
impl.function
=============

Function implementation classes

"""
import abc
import contextlib
import functools
import types

from autowire.base import BaseResource, BaseContext, Implementation


# (FunctionType, BaseResource, BaseContext) -> ContextManager
Evaluator = types.FunctionType


class FunctionImplementation(Implementation, metaclass=abc.ABCMeta):
    """
    Implementation with wrapping function and evaluator

    :param function: function to be wrapped.
    :param evaluator: function evaluator for reifying.
    :type evaluator: (Function, BaseResource, BaseContext) -> ContextManager

    """

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
