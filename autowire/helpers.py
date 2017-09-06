"""
autowire.helpers
================

Helpers.

"""
import contextlib

from ._compat import ContextManger
from .base import BaseContext, BaseResource, Implementation
from .utils import RefCounter


class SharedImplementation(Implementation):
    def __init__(self, impl: Implementation):
        super().__init__()
        self.impl = impl
        self.counters = {}

    @contextlib.contextmanager
    def reify(self, resource: BaseResource, context: BaseContext) \
            -> ContextManger:
        if context not in self.counters:
            context_manager = self.impl.reify(resource, context)
            self.counters[context] = RefCounter(context_manager)
        counter = self.counters[context]
        try:
            with counter as value:
                yield value
        finally:
            if counter.count == 0:
                del self.counters[context]


class GloballySharedImplementation(Implementation):
    def __init__(self, impl: Implementation):
        super().__init__()
        self.impl = impl
        self.counter = None

    @contextlib.contextmanager
    def reify(self, resource: BaseResource, context: BaseContext) \
            -> ContextManger:
        if self.counter is None:
            provider = context.provided_by(resource)  # Find me
            self.counter = RefCounter(self.impl.reify(resource, provider))
        try:
            with self.counter as value:
                yield value
        finally:
            if self.counter.count == 0:
                self.counter = None
