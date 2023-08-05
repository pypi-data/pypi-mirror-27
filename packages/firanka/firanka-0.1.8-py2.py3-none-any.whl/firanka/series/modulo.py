# coding=UTF-8
from __future__ import print_function, absolute_import, division

import math

from .base import Series
from ..ranges import REAL_SET


class ModuloSeries(Series):
    def __init__(self, series, *args, **kwargs):
        """
        Construct a modulo series
        :param series: base series to use
        :raise ValueError: invalid domain length
        """
        super(ModuloSeries, self).__init__(REAL_SET, *args, **kwargs)

        self.series = series
        self.period = self.series.domain.length()

        if self.period == 0:
            raise ValueError('Modulo series cannot have a period of 0')
        elif math.isinf(self.period):
            raise ValueError('Modulo series cannot have an infinite period')

    def _get_for(self, item):
        if item < 0:
            item = -(item // self.period) * self.period + item
        elif item > self.period:
            item = item - (item // self.period) * self.period
        elif item == self.period:
            item = 0

        return self.series._get_for(self.series.domain.start + item)
