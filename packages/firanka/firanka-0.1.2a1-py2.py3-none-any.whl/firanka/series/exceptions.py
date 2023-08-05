# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import logging

logger = logging.getLogger(__name__)


class FirankaException(Exception):
    pass


class OutOfRangeError(FirankaException):
    pass


class EmptyDomainError(FirankaException):
    pass