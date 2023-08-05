# coding=UTF-8
from __future__ import print_function, absolute_import, division

import inspect

from sortedcontainers import SortedList

from firanka.exceptions import NotInDomainError
from firanka.intervals import Interval, EMPTY_SET


def _has_arguments(fun, n):  # used only in assert clauses
    assert hasattr(fun, '__call__'), 'function is not callable!'
    return len(inspect.getargspec(fun).args) >= n


class Series(object):
    """
    Abstract, base class for series.

    Your series needs to override just _get_for(x: float) -> v
    for minimum functionality
    """

    def __init__(self, domain, comment=u''):
        if not isinstance(domain, Interval):
            domain = Interval(domain)
        self.domain = domain
        self.comment = comment

    def __getitem__(self, item):
        """
        Return a value for given index, or a subslice of this series
        :param item: a float, or a slice, or a Interval
        :return: Series instance or a value
        :raises NotInDomainError: index not in domain
        """
        if isinstance(item, (Interval, slice)):
            if isinstance(item, slice):
                item = Interval(item)

            if item not in self.domain:
                raise NotInDomainError('slicing beyond series domain')

            return AlteredSeries(self, domain=self.domain.intersection(item))
        else:
            if item not in self.domain:
                raise NotInDomainError('item not in domain')

            return self._get_for(item)

    def _get_for(self, item):
        raise NotImplementedError('This is abstract, override me!')

    def eval_points(self, points):
        """
        Return values for given points. A mass [] one could say
        :param points: iterable of indices
        :return: a list of values
        """
        return [self[p] for p in points]

    def apply(self, fun):
        """
        Return this series with a function applied to each value
        :param fun: callable(index: float, value: any) => 1
        :return: Series instance
        """
        assert _has_arguments(fun, 2), 'Callable to apply needs 2 arguments'

        return AlteredSeries(self, fun=fun)

    def discretize(self, points, domain=None):
        """
        Return this as a DiscreteSeries, sampled at points
        :return: a DiscreteSeries instance
        """
        if len(points) == 0:
            return DiscreteSeries([])

        points = list(sorted(points))

        domain = domain or Interval(points[0], points[-1], True, True)

        if domain not in self.domain:
            raise NotInDomainError('points not inside this series!')

        return DiscreteSeries([(i, self[i]) for i in points], domain)

    def join(self, series, fun):
        """
        Return a new series with values of fun(index, v1, v2)

        :param series: series to join against
        :param fun: callable(t: float, v1: any, v2: any) => value
        :return: new Series instance
        """
        assert _has_arguments(fun, 3), 'Callable to join needs 3 arguments'

        return JoinedSeries(self, series, fun)

    def translate(self, x):
        """
        Translate the series by some distance
        :param x: a float
        :return: new Series instance
        """
        return AlteredSeries(self, x=x)


class DiscreteSeries(Series):
    """
    A series with lots of small rectangles interpolating something
    """

    def __init__(self, data, domain=None, *args, **kwargs):

        data = SortedList(data)

        if len(data) == 0:
            domain = EMPTY_SET
        elif domain is None:
            domain = Interval(data[0][0], data[-1][0], True, True)

        self.data = data
        super(DiscreteSeries, self).__init__(domain, *args, **kwargs)

        if len(data) > 0:
            if self.domain.start < data[0][0]:
                raise ValueError(
                    'some domain space is not covered by definition!')

    def apply(self, fun):
        assert _has_arguments(fun, 2), 'fun must have at least 2 arguments'

        return DiscreteSeries([(k, fun(k, v)) for k, v in self.data],
                              self.domain)

    def _get_for(self, item):
        if item == self.data[0]:
            return self.data[0][1]

        for k, v in reversed(self.data):
            if k <= item:
                return v

        raise RuntimeError('should never happen')

    def translate(self, x):
        return DiscreteSeries([(k + x, v) for k, v in self.data],
                              self.domain.translate(x))

    def _join_discrete_other_discrete(self, series, fun):
        new_domain = self.domain.intersection(series.domain)

        assert isinstance(series, DiscreteSeries)

        a = self.data[::-1]
        b = series.data[::-1]

        ptr = self.domain.start
        c = [(ptr, fun(ptr, self._get_for(ptr), series._get_for(ptr)))]

        while len(a) > 0 and len(b) > 0:
            if a[-1] < b[-1]:
                ptr, v1 = a.pop()
                v2 = series._get_for(ptr)
            elif a[-1] > b[-1]:
                ptr, v1 = b.pop()
                v2 = self._get_for(ptr)
            else:
                ptr, v1 = a.pop()
                _, v2 = b.pop()

            _appendif(c, ptr, fun(ptr, v1, v2))

        if len(a) > 0 or len(b) > 0:
            if len(a) > 0:
                assert len(b) == 0
                rest = a
                static_v = series._get_for(ptr)
                op = lambda ptr, me, const: fun(ptr, me, const)
            else:
                assert len(a) == 0
                rest = b
                static_v = self._get_for(ptr)
                op = lambda ptr, me, const: fun(ptr, const, me)

            for ptr, v in rest:
                _appendif(c, ptr, op(ptr, v, static_v))

        return DiscreteSeries(c, new_domain)

    def join(self, series, fun):
        if isinstance(series, DiscreteSeries):
            return self.join_discrete(series, fun)  # same effect
        else:
            super(DiscreteSeries, self).join(series, fun)

    def join_discrete(self, series, fun):
        """
        Very much like join, but it will evaluate only existing discrete points.
        :param series:
        :param fun:
        :return:
        """
        assert _has_arguments(fun, 3), 'fun must have at least 3 arguments!'

        new_domain = self.domain.intersection(series.domain)

        if isinstance(series, DiscreteSeries):
            return self._join_discrete_other_discrete(series, fun)

        def get_both_for_t(t):
            return fun(t, self._get_for(t), series._get_for(t))

        c = []
        if new_domain.start > self.data[0][0]:
            c.append((new_domain.start, get_both_for_t(new_domain.start)))

        for k, v in ((k, v) for k, v in self.data if
                     new_domain.start <= k <= new_domain.stop):
            _appendif(c, k, fun(k, v, series._get_for(k)))

        if c[-1][0] != new_domain.stop:
            c.append((new_domain.stop, get_both_for_t(new_domain.stop)))

        return DiscreteSeries(c, new_domain)


class AlteredSeries(Series):
    """
    Internal use - for applyings, translations and slicing
    """

    def __init__(self, series, domain=None, fun=lambda k, v: v, x=0, *args, **kwargs):
        """
        :param series: original series
        :param domain: new domain to use [if sliced]
        :param fun: (index, v) -> newV [if applied]
        :param x: translation vector [if translated]
        """
        domain = domain or series.domain
        super(AlteredSeries, self).__init__(domain.translate(x), *args, **kwargs)
        self.fun = fun
        self.series = series
        self.x = x

    def _get_for(self, item):
        return self.fun(item, self.series._get_for(item + self.x))


def _appendif(lst, ptr, v):
    if len(lst) > 0:
        assert lst[-1][0] <= ptr
        if lst[-1][0] == ptr:
            return  # same ptr as before? Not required.
        if lst[-1][1] == v:
            return  # same value as before? Redundant
    lst.append((ptr, v))


class JoinedSeries(Series):
    """
    Series stemming from performing an operation on two series
    """

    def __init__(self, ser1, ser2, op, *args, **kwargs):
        """:type op: callable(time: float, v1, v2: any) -> v"""
        assert _has_arguments(op, 3), 'op must have 3 arguments'

        super(JoinedSeries, self).__init__(ser1.domain.intersection(ser2.domain), *args, **kwargs)
        self.ser1 = ser1
        self.ser2 = ser2
        self.op = op

    def _get_for(self, item):
        return self.op(item, self.ser1._get_for(item), self.ser2._get_for(item))
