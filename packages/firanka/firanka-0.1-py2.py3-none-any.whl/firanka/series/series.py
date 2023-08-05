
# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import functools
import itertools

from .range import Range


class Series(object):

    def __init__(self, domain):
        if not isinstance(domain, Range):
            domain = Range(domain)
        self.domain = domain

    def __getitem__(self, item):
        if isinstance(item, slice):
            item = Range(item)
            if item not in self.domain:
                raise ValueError('slicing beyond series domain')

            newdom = self.domain.intersection(item)
            return SlicedSeries(self, newdom)
        else:
            if item not in self.domain:
                raise ValueError('item not in domain')

            return self._get_for(item)

    def _get_for(self, item):
        raise NotImplementedError

    def eval_points(self, points):
        return [self[p] for p in points]

    def apply(self, series, fun):
        return AppliedSeries(self, series, fun)

    def compute(self):
        """Simplify self"""
        return self


class SlicedSeries(Series):
    def __init__(self, parent, domain):
        super(SlicedSeries, self).__init__(domain)
        self.parent = parent

    def _get_for(self, item):
        return self.parent._get_for(item)

class DiscreteSeries(Series):

    def __init__(self, data, domain=None):
        if domain is None:
            domain = Range(data[0][0], data[-1][0], True, True)

        self.data = data
        super(DiscreteSeries, self).__init__(domain)

    def _get_for(self, item):
        for k, v in reversed(self.data):
            if k <= item:
                return v

        raise RuntimeError('should never happen')

    def compute(self):
        """Simplify self"""
        nd = [self.data[0]]
        for i in six.moves.range(1, len(self.data)):
             if self.data[i][1] != nd[-1][1]:
                 nd.append(self.data[i])
        return DiscreteSeries(nd, self.domain)


class FunctionBasedSeries(Series):
    def __init__(self, fun, domain):
        super(FunctionBasedSeries, self).__init__(domain)
        self.fun = fun
        self._get_for = fun


class AppliedSeries(Series):
    def __init__(self, ser1, ser2, op):
        super(AppliedSeries, self).__init__(
            ser1.domain.intersection(ser2.domain))
        self.ser1 = ser1
        self.ser2 = ser2
        self.op = op

    def _get_for(self, item):
        return self.op(self.ser1._get_for(item), self.ser2._get_for(item))

    def compute(self):
        """
        Attempt to simplify the call tree
        """
        if isinstance(self.ser1, DiscreteSeries) and isinstance(self.ser2,
                                                                DiscreteSeries):
            a = [p for p, q in reversed(self.ser1.data)]
            b = [p for p, q in reversed(self.ser2.data)]

            ptr = self.domain.start
            c = [(ptr, self._get_for(ptr))]

            while len(a) > 0 or len(b) > 0:
                if len(a) > 0 and len(b) > 0:
                    if a[-1] < b[-1]:
                        ptr = a.pop()
                    elif a[-1] > b[-1]:
                        ptr = b.pop()
                    else:
                        a.pop()
                        ptr = b.pop()

                    assert ptr >= c[-1][0]

                    if ptr > c[-1][0]:
                        c.append((ptr, self._get_for(ptr)))

                else:
                    rest = a if len(a) > 0 else b
                    c.extend((ptr, self._get_for(ptr)) for ptr, v in rest)
                    break

            return DiscreteSeries(c, self.domain)
        elif isinstance(self.ser1, DiscreteSeries) or isinstance(self.ser2,
                                                                DiscreteSeries):
            dis, nds = (self.ser1, self.ser2) if isinstance(self.ser1, DiscreteSeries) else (self.ser2, self.ser1)

            if dis.data[0][0] != self.domain.start:
                p = [(self.domain.start, self._get_for(self.domain.start))]
            else:
                p = []

            for ptr, v in dis.data:
                p.append((ptr, self._get_for(ptr)))

            if dis.data[-1][0] != self.domain.stop:
                dis.data.append((self.domain.stop, self._get_for(ptr)))

            return DiscreteSeries(p, self.domain)
        else:
            return self
