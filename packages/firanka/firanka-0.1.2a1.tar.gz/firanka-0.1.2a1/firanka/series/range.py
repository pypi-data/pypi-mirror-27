# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import logging
import re
import functools
import math

logger = logging.getLogger(__name__)


def pre_range(fun):
    @functools.wraps(fun)
    def inner(self, arg, *args, **kwargs):
        if not isinstance(arg, Range):
            arg = Range(arg)
        return fun(self, arg, *args, **kwargs)
    return inner


class Range(object):
    """
    Range of real numbers
    """
    def __init__(self, *args):
        if len(args) == 1:
            rs, = args
            if isinstance(rs, type(self)):
                start = rs.start
                stop = rs.stop
                lend_inclusive = rs.lend_inclusive
                rend_inclusive = rs.rend_inclusive
            else:
                rs, = args

                if rs[0] not in '<(': raise ValueError('Must start with ( or <')
                if rs[-1] not in '>)': raise ValueError('Must end with ) or >')
                if ';' not in rs: raise ValueError('Separator ; required')

                lend_inclusive = rs[0] == '<'
                rend_inclusive = rs[-1] == '>'

                start, stop = rs[1:-1].split(';')
                start = float(start)
                stop = float(stop)
        else:
            start, stop, lend_inclusive, rend_inclusive = args

        if lend_inclusive and math.isinf(start):
            raise ValueError('Greater or equal with infinity!')
        if rend_inclusive and math.isinf(stop):
            raise ValueError('Greater or equal with infinity!')

        self.start = start
        self.stop = stop
        self.lend_inclusive = lend_inclusive
        self.rend_inclusive = rend_inclusive

    def __contains__(self, x):
        if x == self.start:
            return self.lend_inclusive

        if x == self.stop:
            return self.rend_inclusive

        return self.start < x < self.stop

    def is_empty(self):
        return (self.start == self.stop) and (not self.lend_inclusive) and (
        not self.rend_inclusive)

    def __len__(self):
        return self.stop - self.start

    def __repr__(self):
        return 'Range(%s, %s, %s, %s)' % (repr(self.start), repr(self.stop), repr(self.lend_inclusive), repr(self.rend_inclusive))

    def __bool__(self):
        """True if not empty"""
        return not self.is_empty()

    def __str__(self):
        return '%s%s;%s%s' % (
            '<' if self.lend_inclusive else '(',
            self.start,
            self.stop,
            '>' if self.rend_inclusive else ')',
        )

    @pre_range
    def intersection(self, y):
        if self.start > y.start:
            return y.intersection(self)

        assert self.start <= y.start

        if (self.stop < y.start) or (y.stop < y.start):
            return EMPTY_RANGE

        if self.stop == y.start and not (self.rend_inclusive and y.lend_inclusive):
            return EMPTY_RANGE

        if self.start == y.start:
            start = self.start
            lend_inclusive = self.lend_inclusive or y.lend_inclusive
        else:
            start = y.start
            lend_inclusive = y.lend_inclusive

        if self.stop == y.stop:
            stop = self.stop
            rend_inclusive = self.rend_inclusive or y.rend_inclusive
        else:
            p, q = (self, y) if self.stop < y.stop else (y, self)
            stop = p.stop
            rend_inclusive = p.rend_inclusive and (stop in q)

        return Range(start, stop, lend_inclusive, rend_inclusive)

    @pre_range
    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop and self.lend_inclusive == other.lend_inclusive and self.rend_inclusive == other.rend_inclusive

    def __hash__(self):
        return hash(self.start) ^ hash(self.stop)


EMPTY_RANGE = Range(0, 0, False, False)