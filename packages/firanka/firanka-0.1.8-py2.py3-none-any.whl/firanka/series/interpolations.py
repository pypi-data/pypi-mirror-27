# coding=UTF-8
from __future__ import print_function, absolute_import, division

import six

from .base import DiscreteSeries, Series


def SCALAR_LINEAR_INTERPOLATOR(t0, v0, t1, v1, tt):
    """
    Good intepolator if our values can be added, subtracted, multiplied and divided
    """
    return v0 + (tt - t0) * (t1 - t0) / (v1 - v0)


class LinearInterpolationSeries(DiscreteSeries):
    def __init__(self, data, domain=None,
                 interpolator=SCALAR_LINEAR_INTERPOLATOR,
                 *args, **kwargs):
        """
        :param interpolator: callable(t0: float, v0: any, t1: float, v1: any, tt: float) -> any
            This, given intepolation points (t0, v0) and (t1, v1) such that t0 <= tt <= t1,
            return a value for index tt
        :raise TypeError: a non-discrete series was passed as data
        """
        self.interpolator = interpolator
        if isinstance(data, DiscreteSeries):
            data, domain = data.data, data.domain
        elif isinstance(data, Series):
            raise TypeError('non-discrete series not supported!')

        super(LinearInterpolationSeries, self).__init__(data, domain, *args,
                                                        **kwargs)

    def _get_for(self, item):
        if item == self.domain.start:
            return self.data[0][1]

        if len(self.data) == 1:
            return super(LinearInterpolationSeries, self).__getitem__(item)

        for i in six.moves.range(0, len(self.data) - 1):
            cur_i, cur_v = self.data[i]
            next_i, next_v = self.data[i + 1]

            if cur_i <= item <= next_i:
                return self.interpolator(cur_i, cur_v, next_i, next_v, item)

        return self.data[-1][1]
