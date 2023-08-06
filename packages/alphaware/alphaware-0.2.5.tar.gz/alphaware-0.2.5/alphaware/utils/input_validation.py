# -*- coding: utf-8 -*-


import pandas as pd
from datetime import datetime
import numpy as np
from argcheck import expect_types
from PyFin.DateUtilities import Date
from empyrical import cum_returns
from ..enums import (OutputDataFormat,
                     ReturnType)
from ..const import RETURN


@expect_types(date=(str, datetime, Date))
def ensure_pyfin_date(date, date_format='%Y-%m-%d'):
    """
    :param date: str, datetime, 日期
    :param date_format: str, 时间格式
    :return: PyFin.Date object 
    """
    if isinstance(date, Date):
        return date
    elif isinstance(date, str):
        return Date.strptime(date, date_format)
    else:
        return Date.fromDateTime(date)


@expect_types(date=(str, datetime))
def ensure_datetime(date, date_format='%Y-%m-%d'):
    """
    :param date: str, datetime, 日期
    :param date_format: str, 时间格式
    :return: datetime
    """
    if isinstance(date, datetime):
        return date
    else:
        return datetime.strptime(date, date_format)


@expect_types(data=(pd.DataFrame, pd.Series), data_format=OutputDataFormat)
def ensure_pd_index_names(data, data_format, valid_index):
    if data_format == OutputDataFormat.MULTI_INDEX_DF:
        data.index.names = valid_index.full_index
    else:
        data.index.name = valid_index.date_index
    return data


@expect_types(arg=(list, np.ndarray, pd.DataFrame, pd.Series))
def ensure_pd_series(func, argname, arg):
    if isinstance(arg, pd.Series):
        return arg
    elif isinstance(arg, pd.DataFrame):
        return arg[arg.columns[0]]
    else:
        return pd.Series(arg)


@expect_types(arg=(list, np.ndarray, pd.DataFrame, pd.Series))
def ensure_pd_df(func, argname, arg):
    if isinstance(arg, pd.DataFrame):
        return arg
    else:
        return pd.DataFrame(arg)


@expect_types(arg=(np.ndarray, pd.DataFrame, pd.Series))
def ensure_np_array(func, argname, arg):
    """
    :return: 转换成np.ndarray格式
    """
    if isinstance(arg, np.ndarray):
        return arg
    else:
        return arg.values


def ensure_cumul_return(func, argname, arg):
    if not isinstance(arg, RETURN):
        return arg
    if arg.type == ReturnType.Cumul:
        return arg.data
    else:
        data_ = cum_returns(arg.data, starting_value=1.0)
        return data_


def ensure_noncumul_return(func, argname, arg):
    if not isinstance(arg, RETURN):
        return arg
    if arg.type == ReturnType.Non_Cumul:
        return arg.data
    else:
        data_ = arg.data.pct_change()
        data_.dropna(inplace=True)
        return data_
