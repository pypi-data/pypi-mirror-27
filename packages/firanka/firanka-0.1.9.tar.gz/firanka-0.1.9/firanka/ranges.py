# coding=UTF-8
from __future__ import print_function, absolute_import, division

import functools
import math

import six

__all__ = [
    'Range',
    'REAL_SET',
    'EMPTY_SET'
]


def _pre_range(fun):
    @functools.wraps(fun)
    def inner(self, arg, *args, **kwargs):
        if not isinstance(arg, Range):
            arg = Range(arg)
        return fun(self, arg, *args, **kwargs)

    return inner


class Range(object):
    """
    Range of real numbers. Immutable.
    """

    def translate(self, x):
        if x == 0:
            return self
        else:
            return Range(self.start + x, self.stop + x, self.left_inc,
                         self.right_inc)

    def __fromslice(self, rs):
        start = float('-inf') if rs.start is None else rs.start
        stop = float('+inf') if rs.stop is None else rs.stop
        return start, stop, not math.isinf(start), not math.isinf(stop)

    def __fromrange(self, rs):
        return rs.start, rs.stop, rs.left_inc, rs.right_inc

    def __fromstr(self, rs):
        if rs[0] not in '<(': raise ValueError(
            'Must start with ( or <')
        if rs[-1] not in '>)': raise ValueError('Must end with ) or >')
        if ';' not in rs: raise ValueError('Separator ; required')

        start, stop = rs[1:-1].split(';')
        return float(start), float(stop), rs[0] == '<', rs[-1] == '>'

    def __getargs(self, args):
        if len(args) == 1:
            rs, = args
            if isinstance(rs, Range):
                args = self.__fromrange(rs)
            elif isinstance(rs, slice):
                args = self.__fromslice(rs)
            else:
                args = self.__fromstr(rs)
        elif len(args) == 2:
            args = args[0], args[1], not math.isinf(args[0]), not math.isinf(
                args[1])

        return args

    def __init__(self, *args):
        """
        Create like:

        * Range('<a;b>')
        * Range(a, b, is_left_closed_, is_right_closed)
        * Range(a, b) - will have both sides closed, unless one is inf
        * Range(slice(a, b)) - will have both sides closed, unless one is None

        :param args:
        """
        args = self.__getargs(args)

        def q(a, b, args):
            return args[a] and math.isinf(args[b])

        if q(2, 0, args) or q(3, 1, args):
            raise ValueError('Set with sharp closing but infinity set')

        self.start, self.stop, self.left_inc, self.right_inc = args

    def __contains__(self, x):
        """
        :type x: index or a Range
        """
        if isinstance(x, six.string_types):
            x = Range(x)

        if isinstance(x, Range):
            if ((x.start == self.start) and (x.left_inc ^ self.left_inc)) \
                or ((x.stop == self.stop) and (x.right_inc ^ self.right_inc)):
                return False

            return (x.start >= self.start) and (x.stop <= self.stop)
        else:
            if x == self.start:
                return self.left_inc

            if x == self.stop:
                return self.right_inc

            return self.start < x < self.stop

    def is_empty(self):
        return (self.start == self.stop) and not (
            self.left_inc or self.right_inc)

    def length(self):
        return self.stop - self.start

    def __repr__(self):
        return 'Range(%s, %s, %s, %s)' % (
            repr(self.start), repr(self.stop), repr(self.left_inc),
            repr(self.right_inc))

    def __getitem__(self, item):
        if not isinstance(item, slice):
            raise ValueError('must be a slice')

        return self.intersection(Range(item))

    def __str__(self):
        return '%s%s;%s%s' % (
            '<' if self.left_inc else '(',
            self.start,
            self.stop,
            '>' if self.right_inc else ')',
        )

    @_pre_range
    def intersection(self, y):
        if self.start > y.start:
            return y.intersection(self)

        assert self.start <= y.start

        if (self.stop < y.start) or (y.stop < y.start):
            return EMPTY_SET

        if self.stop == y.start and not (self.right_inc and y.left_inc):
            return EMPTY_SET

        if self.start == y.start:
            start = self.start
            left_inc = self.left_inc and y.left_inc
        else:
            start = y.start
            left_inc = y.left_inc

        if self.stop == y.stop:
            stop = self.stop
            right_inc = self.right_inc and y.right_inc
        else:
            p, q = (self, y) if self.stop < y.stop else (y, self)
            stop = p.stop
            right_inc = p.right_inc and (stop in q)

        return Range(start, stop, left_inc, right_inc)

    @_pre_range
    def __eq__(self, other):
        if self.is_empty() and other.is_empty():
            return True
        return self.start == other.start and self.stop == other.stop and self.left_inc == other.left_inc and self.right_inc == other.right_inc

    def __hash__(self):
        return hash(self.start) ^ hash(self.stop)


EMPTY_SET = Range(0, 0, False, False)
REAL_SET = Range(float('-inf'), float('+inf'), False, False)
