# coding=UTF-8
from __future__ import print_function, absolute_import, division

__all__ = [
    'FirankaError',
    'NotInDomainError',
]


class FirankaError(Exception):
    """
    Base class for firanka's exceptions
    """


class NotInDomainError(FirankaError, ValueError):
    """
    Requested index is beyond this domain
    """
