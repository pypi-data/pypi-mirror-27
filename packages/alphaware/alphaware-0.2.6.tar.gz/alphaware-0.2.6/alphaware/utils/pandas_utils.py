# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from argcheck import (expect_types,
                      optional,
                      preprocess)
from PyFin.Utilities import pyFinAssert
from alphaware.const import INDEX_FACTOR
from alphaware.enums import (FreqType,
                             OutputDataFormat)
from .input_validation import ensure_pd_df


@expect_types(data=(pd.Series, pd.DataFrame))
def convert_df_format(data, target_format=OutputDataFormat.MULTI_INDEX_DF, col_name='factor',
                      multi_index=INDEX_FACTOR):
    if target_format == OutputDataFormat.MULTI_INDEX_DF:
        tmp = data.stack()
        data_ = pd.DataFrame(tmp)
        data_.index.names = multi_index.full_index
        data_.columns = [col_name]
    else:
        tmp = data.unstack()
        index = tmp.index
        columns = tmp.columns.get_level_values(multi_index.sec_index).tolist()
        data_ = pd.DataFrame(tmp.values, index=index, columns=columns)

    return data_


@expect_types(df=(pd.Series, pd.DataFrame))
def top(df, column=None, n=5):
    if isinstance(df, pd.Series):
        ret = df.sort_values(ascending=False)[:n]
    else:
        pyFinAssert(column is not None, "Specify the col name or use pandas Series type of data")
        ret = df.sort_values(by=column, ascending=False)[:n]

    return ret


@expect_types(data=(pd.DataFrame, pd.Series), freq=optional(FreqType, str))
def group_by_freq(data, freq=FreqType.EOM):
    data_ = pd.DataFrame(data) if isinstance(data, pd.Series) else data
    if freq == FreqType.EOD:
        return data_.groupby([lambda x: x.year, lambda x: x.month, lambda x: x.day])
    elif freq == FreqType.EOM:
        return data_.groupby(pd.TimeGrouper(freq='M'))
    elif freq == FreqType.EOQ:
        return data_.groupby(pd.TimeGrouper(freq='Q'))
    elif freq == FreqType.EOY:
        return data_.groupby(pd.TimeGrouper(freq='A'))


@expect_types(x=(pd.DataFrame, pd.Series))
def quantile_calc(x, quantiles, bins):
    if quantiles is not None and bins is None:
        return pd.qcut(x, quantiles, labels=False) + 1
    elif bins is not None and quantiles is None:
        return pd.cut(x, bins, labels=False) + 1
    raise ValueError('Either quantiles or bins should be provided')


@expect_types(x=(pd.DataFrame, pd.Series))
def fwd_return(x, date_index=INDEX_FACTOR.date_index, sec_index=INDEX_FACTOR.sec_index, period=1):
    """
    每个日期和股票代码对应的未来收益
    """
    dates = sorted(set(x.index.get_level_values(date_index)))
    ret = pd.DataFrame()
    for i in range(len(dates) - period):
        shift_date = dates[i + period]
        data_concat = x.loc[shift_date].reset_index()
        data_concat[date_index] = [dates[i]] * len(data_concat)
        ret = pd.concat([ret, data_concat], axis=0)
    ret.set_index([date_index, sec_index], inplace=True)
    ret.columns = ['fwd_return']
    return ret


def load_factor_data_from_csv(csv_file, date_index=INDEX_FACTOR.date_index, sec_index=INDEX_FACTOR.sec_index):
    data = pd.read_csv(csv_file, encoding='gbk')
    data[date_index] = pd.to_datetime(data[date_index])
    data.set_index([date_index, sec_index], inplace=True)
    return data


@preprocess(data=ensure_pd_df)
def weighted_rank(data, ascend_order=None, weight=None, out_df=False):
    nb_col = len(data.columns)
    ascend_order = [1] * nb_col if ascend_order is None else ascend_order
    weight = [1.0 / nb_col] * nb_col if weight is None else weight
    rank = np.zeros([len(data), nb_col])
    for i in range(len(data.columns)):
        rank[:, i] = np.argsort(data[data.columns[i]]) if ascend_order[i] else np.argsort(data[data.columns[i]])[::-1]
    weight_rank = np.dot(rank, np.array(weight))
    return pd.DataFrame(weight_rank, index=data.index) if out_df else weight_rank
