# coding=UTF-8
from __future__ import print_function, absolute_import, division

from .ranges import Range
from .series import Series


class BijectionMapping(object):
    def __init__(self, user2float, float2user):
        """
        :param user2float: callable/1 => float, mapping from your time system to floats
        :param float2user: callable/float => 1, mapping from float to your time systen
        """
        self.user2float = user2float
        self.float2user = float2user

    def to_float(self, user):
        return self.user2float(user)

    def to_user(self, flt):
        return self.float2user(flt)


class TimeProvidedSeries(Series):
    """
    If your time is something else than simple floats, this will help you out
    """

    def __init__(self, series, mapping, *args, **kwargs):
        """
        :param series: series to overlay
        """
        super(TimeProvidedSeries, self).__init__(series.domain, *args,
                                                 **kwargs)
        self.mapping = mapping
        self.series = series

    def _withmap(self, series):
        return TimeProvidedSeries(series, self.mapping)

    def __getitem__(self, item):
        if isinstance(item, slice):
            item = slice(
                float('-inf') if slice.start is None else self.to_float(
                    slice.start),
                float('+inf') if slice.stop is None else self.to_float(
                    slice.stop), )

            return self._withmap(self.series[item])
        elif isinstance(item, Range):
            return self._withmap(self.series[item])
        else:
            return self.series[self.mapping.to_float(item)]

    def _get_for(self, item):
        return self.series[self.l2f(item)]

    def join(self, series, fun):
        return TimeProvidedSeries(self.series.join(series, fun), self.mapping)
