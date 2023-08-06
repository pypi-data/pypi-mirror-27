# -*- coding: utf-8 -*-


from unittest import TestCase
import pandas as pd
from pandas.util.testing import assert_frame_equal
import numpy as np
from datetime import datetime as dt
from numpy.testing import assert_array_almost_equal
from parameterized import parameterized
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.preprocess import (Winsorizer,
                                  FactorWinsorizer)


class TestWinsorizer(TestCase):
    @parameterized.expand([(np.array([1, 2, 3, 10, 4, 1, 3]),
                            (2.5, 97.5),
                            np.array([1, 2, 3, 9.1, 4, 1, 3]))])
    def test_winsorize(self, x, quantile_range, expected):
        calculated = Winsorizer(quantile_range).fit_transform(x)
        assert_array_almost_equal(calculated, expected)

    def test_factor_winsorizer(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003', '004', '005']],
                                           names=['trade_date', 'ticker'])
        data1 = pd.DataFrame(index=index, data=[1.0, 1.0, 1.2, 200.0, 0.9, 5.0, 5.0, 5.1, 5.9, 5.0])
        factor_test1 = Factor(data=data1, name='test1')

        data2 = pd.DataFrame(index=index, data=[2.6, 2.5, 2.8, 2.9, 2.7, 1.9, -10.0, 2.1, 2.0, 1.9])
        factor_test2 = Factor(data=data2, name='test2')

        data3 = pd.DataFrame(index=index, data=[3.0, 3.0, 30.0, 5.0, 4.0, 6.0, 7.0, 6.0, 6.0, 5.9])
        factor_test3 = Factor(data=data3, name='test3')

        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test1, factor_test2, factor_test3])
        quantile_range = (1, 99)
        calculated = FactorWinsorizer(quantile_range).fit_transform(fc)
        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['001', '002', '003', '004', '005']],
                                           names=['trade_date', 'ticker'])
        expected = pd.DataFrame({'test1': [1.0, 1.0, 1.2, 192.048, 0.904, 5.0, 5.0, 5.1, 5.868, 5.0],
                                 'test2': [2.6, 2.504, 2.8, 2.896, 2.7, 1.9, -9.524, 2.096, 2.0, 1.9],
                                 'test3': [3.0, 3.0, 29.0, 5.0, 4.0, 6.0, 6.96, 6.0, 6.0, 5.904]},
                                index=index)
        assert_frame_equal(calculated, expected)
