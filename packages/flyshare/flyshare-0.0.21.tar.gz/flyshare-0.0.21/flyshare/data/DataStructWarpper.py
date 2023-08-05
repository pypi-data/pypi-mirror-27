# coding:utf-8
from flyshare.data.DataStruct import (DataStruct_Index_day,
                                      DataStruct_Index_min,
                                      DataStruct_Stock_day,
                                      DataStruct_Stock_min,
                                      DataStruct_Stock_transaction)
from flyshare.fetch.tdx import fetch_get_stock_xdxr


def stock_day_warpper(func, *args, **kwargs):
    return DataStruct_Stock_day(func(*args, **kwargs))


def stock_min_warpper(func, *args, **kwargs):
    return DataStruct_Stock_min(func(*args, **kwargs))
