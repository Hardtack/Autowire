"""
autowire.resource
=================

Resource implementations.

"""
from .plain import Resource
from .function import FunctionResource


__all__ = [
    'Resource',
    'FunctionResource',
]
