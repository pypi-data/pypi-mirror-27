# -*- coding: utf-8 -*-

import numpy as np
from PyFin.Utilities import pyFinWarning
from sklearn_pandas import DataFrameMapper
from sklearn.utils import check_array
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from sklearn.utils.validation import FLOAT_DTYPES
from ..base import FactorTransformer
from ..enums import FactorType


class Winsorizer(BaseEstimator, TransformerMixin):
    def __init__(self, quantile_range=(2.5, 97.5), copy=True):
        pyFinWarning(quantile_range[0] >= 1 and quantile_range[1] >= 1, Warning,
                     'quantile_range value will be divided by 100 in calculation')
        self.quantile_range = quantile_range
        self.copy = copy
        self.q_max = None
        self.q_min = None

    def fit(self, X):
        q = np.percentile(X, self.quantile_range, axis=0)
        self.q_max = q[1]
        self.q_min = q[0]
        return self

    def transform(self, X):
        X = check_array(X, accept_sparse=('csr', 'csc'), copy=self.copy,
                        ensure_2d=False, estimator=self, dtype=FLOAT_DTYPES)
        X[X > self.q_max] = self.q_max
        X[X < self.q_min] = self.q_min
        return X


class FactorWinsorizer(FactorTransformer):
    def __init__(self, quantile_range=(2.5, 97.5), copy=True, out_container=False):
        super(FactorWinsorizer, self).__init__(copy=copy, out_container=out_container)
        self.quantile_range = quantile_range
        self.q_max = None
        self.q_min = None

    def _build_mapper(self, factor_container):
        data = factor_container.data
        data_mapper = [([factor_name], self._get_mapper(factor_container.property[factor_name]['type']))
                       for factor_name in data.columns]
        return DataFrameMapper(data_mapper)

    def _get_mapper(self, factor_type):
        if factor_type == FactorType.INDUSTY_CODE:
            return None
        else:
            return Winsorizer(quantile_range=self.quantile_range, copy=self.copy)
