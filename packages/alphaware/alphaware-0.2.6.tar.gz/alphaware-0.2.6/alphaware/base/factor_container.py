# -*- coding: utf-8 -*-

import copy
import pandas as pd
from collections import defaultdict
from toolz.dicttoolz import (merge,
                             dissoc)
from PyFin.Utilities import (pyFinWarning,
                             pyFinAssert)
from argcheck import (expect_types,
                      optional,
                      preprocess)
from alphaware.utils import (ensure_datetime,
                             ensure_pd_df,
                             convert_df_format,
                             get_tiaocang_date,
                             ensure_np_array,
                             ensure_pd_index_names)
from alphaware.enums import (FreqType,
                             FactorType,
                             OutputDataFormat,
                             FactorNormType)
from alphaware.const import INDEX_FACTOR

_REQUIRED_FACTOR_PROPERTY = {'type': FactorType.ALPHA_FACTOR,
                             'data_format': OutputDataFormat.MULTI_INDEX_DF,
                             'norm_type': FactorNormType.Null,
                             'freq': FreqType.EOM}


@expect_types(factor_property=dict)
def update_factor_property(factor_property):
    ret = merge(_REQUIRED_FACTOR_PROPERTY, factor_property)
    return ret


class Factor(object):
    @preprocess(data=ensure_pd_df)
    def __init__(self, data, name, property_dict=defaultdict(str), **kwargs):
        self.data = copy.deepcopy(data)
        self.name = name
        self.property = update_factor_property(property_dict)
        self.production_data_format = kwargs.get('production_data_format', OutputDataFormat.MULTI_INDEX_DF)

        self._validate_data_format()
        self._validate_data_name()
        self._validate_date_index()

    def _validate_data_format(self):
        if self.property['data_format'] != self.production_data_format:
            self.data = convert_df_format(self.data, target_format=self.production_data_format)
        return

    def _validate_data_name(self):
        if self.production_data_format == OutputDataFormat.MULTI_INDEX_DF:
            self.data.columns = [self.name]
        return

    def _validate_date_index(self):
        self.data = ensure_pd_index_names(self.data,
                                          data_format=self.production_data_format,
                                          valid_index=INDEX_FACTOR)
        date_format = self.property.get('date_format', '%Y-%m-%d')
        date_index = self.data.index.get_level_values(INDEX_FACTOR.date_index)
        date_index = [ensure_datetime(date_, date_format) for date_ in date_index]
        self.data.reset_index(inplace=True)
        self.data[INDEX_FACTOR.date_index] = date_index
        if self.production_data_format == OutputDataFormat.MULTI_INDEX_DF:
            self.data.set_index(keys=INDEX_FACTOR.full_index, inplace=True)
        else:
            self.data.set_index(keys=INDEX_FACTOR.date_index, inplace=True)

    @property
    def type(self):
        return self.property['type']

    @property
    def freq(self):
        return self.property['freq']

    @property
    def production_format(self):
        return self.production_data_format

    @property
    def trade_date_list(self):
        if self.production_data_format == OutputDataFormat.MULTI_INDEX_DF:
            ret = set(self.data.index.get_level_values(INDEX_FACTOR.date_index))
            ret = list(sorted(set(ret)))
        else:
            ret = self.data.index.tolist()

        return ret


class FactorContainer(object):
    def __init__(self, start_date=None, end_date=None, factors=None, freq=FreqType.EOM, **kwargs):
        self.start_date = start_date
        self.end_date = end_date
        self.freq = freq
        self._tiaocang_date = kwargs.get('tiaocang_date', None)
        self.calendar = kwargs.get('calendar', 'China.SSE')
        self.date_format = kwargs.get('date_format', '%Y-%m-%d')
        self.names = []
        self.property = defaultdict(str)
        self.data = pd.DataFrame()

        self._validate_tiaocang_date()
        self._update_tiaocang_date()
        self._merge_factors(factors)

    def _validate_tiaocang_date(self):
        if (self.start_date is None or self.end_date is None) and self._tiaocang_date is None:
            raise ValueError('tiaocang date must be set initially')

    def _update_tiaocang_date(self):
        if self._tiaocang_date is None:
            self._tiaocang_date = get_tiaocang_date(start_date=self.start_date,
                                                    end_date=self.end_date,
                                                    freq=self.freq,
                                                    calendar=self.calendar,
                                                    date_format=self.date_format)
        return

    @property
    def tiaocang_date(self):
        return self._tiaocang_date

    @expect_types(factor=(Factor))
    def _check_tiaocang_date(self, factor):
        """
        如果该因子的freq和container的freq一致，那么该因子的日期列应该包含所有的调仓日期，否则报错
        """
        pyFinAssert(set(self._tiaocang_date).issubset(set(factor.trade_date_list)),
                    ValueError,
                    'factor {0} does not contain all tiaocang date in its trade date list'.format(factor.name))
        return

    @expect_types(factors=optional(Factor, list))
    def _merge_factors(self, factors):
        if factors is None:
            return

        factors_ = factors if isinstance(factors, list) else list(factors)
        for factor in factors_:
            pyFinAssert(factor.production_format == OutputDataFormat.MULTI_INDEX_DF,
                        ValueError,
                        'factor {0} does not in multi-index dataframe format therefore can not be merged into container'
                        .format(factor.name))
            self._merge_factor(factor)
        self.data = self.data.loc[self._tiaocang_date]
        return

    def _merge_factor(self, factor):
        self.names.append(factor.name)
        self.property[factor.name] = factor.property
        self._concat_factor_data(factor)
        self.data.columns = self.names
        return

    def _concat_factor_data(self, factor):
        pyFinAssert(self.freq == factor.freq,
                    ValueError,
                    'Failed to concatenate: factor {0} has different freq from containter'.format(factor.name))

        self._check_tiaocang_date(factor)
        self.data = pd.concat([self.data, factor.data], axis=1)

    @expect_types(factor=Factor)
    def add_factor(self, factor, overwrite=False):
        if overwrite is True:
            try:
                self.remove_factor(factor.name)
            except Exception:
                pass
        self._merge_factor(factor)
        self.data = self.data.loc[self._tiaocang_date]
        return

    @expect_types(factor=(Factor, str))
    def remove_factor(self, factor):
        factor_name = factor if isinstance(factor, str) else factor.name
        pyFinAssert(factor_name in self.names, ValueError,
                    'unable to remove factor_name {0}, which does not exist in current container'.format(factor_name))
        self.names.remove(factor_name)
        self.data.drop(factor_name, axis=1, inplace=True)
        self.property = dissoc(self.property, factor_name)
        return

    @property
    def factor_names(self):
        return self.names

    @property
    def container_property(self):
        return self.property

    @property
    def industry_code(self):
        key = list(filter(lambda x: self.property[x]['type'] == FactorType.INDUSTY_CODE, self.names))
        pyFinWarning(len(key) == 1, Warning, 'factor container should have only one industry code')
        return self.data[key[0]]

    @property
    def score(self):
        key = list(filter(lambda x: self.property[x]['type'] == FactorType.SCORE, self.names))
        pyFinWarning(len(key) == 1, Warning, 'factor container should have only one score')
        return self.data[key[0]]

    @property
    def mkt_cap(self):
        key = list(filter(lambda x: self.property[x]['type'] == FactorType.ALPHA_FACTOR_MV, self.names))
        pyFinWarning(len(key) == 1, Warning, 'factor container should have only one mkt cap')
        return self.data[key[0]]

    @property
    def alpha_factor_col(self):
        def _is_alpha_factor(x):
            return self.property[x]['type'] == FactorType.ALPHA_FACTOR or \
                   self.property[x]['type'] == FactorType.ALPHA_FACTOR_MV

        return list(filter(_is_alpha_factor, self.names))

    @property
    def fwd_return_col(self):
        key = list(filter(lambda x: self.property[x]['type'] == FactorType.FWD_RETURN, self.names))
        return key

    @preprocess(data_=ensure_np_array)
    def replace_data(self, data_):
        self.data = pd.DataFrame(data_, index=self.data.index, columns=self.data.columns)
        return


def ensure_factor_container(func, argname, arg):
    if isinstance(arg, FactorContainer):
        return arg
    else:
        fc = FactorContainer(tiaocang_date=arg.trade_date_list)
        fc.add_factor(arg)
        return fc
