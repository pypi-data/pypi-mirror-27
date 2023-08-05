# coding: utf-8

import datetime

import pandas as pd
from pandas import DataFrame

from flyshare.data import (data_make_hfq,
                           data_make_qfq,
                           DataStruct_Index_day,
                           DataStruct_Index_min,
                           DataStruct_Stock_block,
                           DataStruct_Stock_day,
                           DataStruct_Stock_min,
                           DataStruct_Stock_transaction)
from flyshare.fetch.query import (fetch_indexlist_day,
                                  fetch_stocklist_day,
                                  fetch_stocklist_min)
from flyshare.util import (MongoDBSetting as ms,
                           util_date_stamp,
                           util_date_valid,
                           log_info,
                           util_time_stamp)


"""
按要求从数据库取数据，并转换成numpy结构

"""


def fetch_stock_day_adv(code, __start, __end, if_drop_index=False, collections=ms.client.flyshares.stock_day):
    '获取股票日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]

    if isinstance(code, str):
        if util_date_valid(__end) == True:
            __data = []
            for item in collections.find({'code': str(code)[0:6],
                                          "date_stamp": {"$lte": util_date_stamp(__end),
                                                         "$gte": util_date_stamp(__start)}}):
                __data.append([str(item['code']),
                               float(item['open']),
                               float(item['high']),
                               float(item['low']),
                               float(item['close']),
                               float(item['vol']),
                               float(item['amount']),
                               item['date']])
            __data = DataFrame(__data, columns=['code', 'open', 'high', 'low', 'close', 'volume', 'amount','date'])
            __data['date'] = pd.to_datetime(__data['date'])
            return DataStruct_Stock_day(__data.query('volume>1').set_index(['date', 'code'], drop=if_drop_index))
        else:
            log_info('something wrong with date')
    elif isinstance(code, list):
        return DataStruct_Stock_day(pd.concat(fetch_stocklist_day(code, [__start, __end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index))


def fetch_stocklist_day_adv(code, __start, __end, if_drop_index=False, collections=ms.client.flyshares.stock_day):
    '获取股票日线'
    return DataStruct_Stock_day(pd.concat(fetch_stocklist_day(code, [__start, __end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index))


def fetch_index_day_adv(code, __start, __end, if_drop_index=False, collections=ms.client.flyshares.index_day):
    '获取指数日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]
    if isinstance(code, str):
        if util_date_valid(__end) == True:
            __data = []
            for item in collections.find({'code': str(code)[0:6],
                                          "date_stamp": {"$lte": util_date_stamp(__end),
                                                         "$gte": util_date_stamp(__start)}}):
                __data.append([str(item['code']),
                               float(item['open']),
                               float(item['high']),
                               float(item['low']),
                               float(item['close']),
                               float(item['vol']),
                               item['date']])
            __data = DataFrame(__data, columns=['code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            return DataStruct_Index_day(__data.query('volume>1').set_index(['date', 'code'], drop=if_drop_index))
        else:
            log_info('something wrong with date')

    elif isinstance(code, list):
        return DataStruct_Index_day(pd.concat(fetch_indexlist_day(code, [__start, __end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index))


def fetch_index_min_adv(code, start, end, type_='1min', if_drop_index=False, collections=ms.client.flyshares.index_min):
    '获取股票分钟线'
    if type_ in ['1min', '1m']:
        type_ = '1min'
    elif type_ in ['5min', '5m']:
        type_ = '5min'
    elif type_ in ['15min', '15m']:
        type_ = '15min'
    elif type_ in ['30min', '30m']:
        type_ = '30min'
    elif type_ in ['60min', '60m']:
        type_ = '60min'
    __data = []
    if isinstance(code, str):
        for item in collections.find({'code': str(code),
                                      "time_stamp": {"$gte": util_time_stamp(start), "$lte": util_time_stamp(end)},
                                      'type': type_}):

            __data.append([str(item['code']),
                           float(item['open']),
                           float(item['high']),
                           float(item['low']),
                           float(item['close']),
                           float(item['vol']),
                           item['datetime'],
                           item['time_stamp'],
                           item['date']])

        __data = DataFrame(__data, columns=['code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

        __data['datetime'] = pd.to_datetime(__data['datetime'])
        return DataStruct_Index_min(__data.query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index))

    elif isinstance(code, list):
        return DataStruct_Index_min(pd.concat([fetch_index_min_adv(code_, start, end, type_, if_drop_index).data for code_ in code]).set_index(['datetime', 'code'], drop=if_drop_index))


def fetch_stock_min_adv(
        code,
        start, end,
        type_='1min',
        if_drop_index=False,
        collections=ms.client.flyshares.stock_min):
    '获取股票分钟线'
    if type_ in ['1min', '1m']:
        type_ = '1min'
    elif type_ in ['5min', '5m']:
        type_ = '5min'
    elif type_ in ['15min', '15m']:
        type_ = '15min'
    elif type_ in ['30min', '30m']:
        type_ = '30min'
    elif type_ in ['60min', '60m']:
        type_ = '60min'
    __data = []

    if isinstance(code, str):
        for item in collections.find({'code': str(code),
                                      "time_stamp": {"$gte": util_time_stamp(start), "$lte": util_time_stamp(end)},
                                      'type': type_}):
            __data.append([str(item['code']),
                           float(item['open']),
                           float(item['high']),
                           float(item['low']),
                           float(item['close']),
                           float(item['vol']),
                           item['datetime'],
                           item['time_stamp'],
                           item['date']])

        __data = DataFrame(__data, columns=['code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

        __data['datetime'] = pd.to_datetime(__data['datetime'])

        return DataStruct_Stock_min(__data.query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index))
    elif isinstance(code, list):
        '新增codelist的代码'
        return DataStruct_Stock_min(pd.concat([fetch_stock_min_adv(code_, start, end, type_, if_drop_index).data for code_ in code]).set_index(['datetime', 'code'], drop=if_drop_index))


def fetch_stocklist_min_adv(code,
                            start,
                            end,
                            type_='1min',
                            if_drop_index=False,
                            collections=ms.client.flyshares.stock_min):
    return DataStruct_Stock_min(pd.concat(fetch_stocklist_min(code, [start, end], type_)).query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index))


def fetch_stock_transaction_adv(
        code,
        start, end,
        if_drop_index=False,
        collections=ms.client.flyshares.stock_transaction):
    data = DataFrame([item for item in collections.find({
        'code': str(code), "date": {
            "$gte": start,
            "$lte": end
        }})]).drop('_id', axis=1, inplace=False)
    data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])
    return DataStruct_Stock_transaction(data.set_index('datetime', drop=if_drop_index))


def fetch_security_list_adv(collections=ms.client.flyshares.stock_list):
    '获取股票列表'
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False)


def fetch_stock_list_adv(collections=ms.client.flyshares.stock_list):
    '获取股票列表'
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False)


def fetch_stock_block_adv(code=None, collections=ms.client.flyshares.stock_block):
    if code is not None:
        data = pd.DataFrame([item for item in collections.find(
            {'code': code})]).drop(['_id'], axis=1)
        return DataStruct_Stock_block(data.set_index('code', drop=False).drop_duplicates())
    else:
        data = pd.DataFrame(
            [item for item in collections.find()]).drop(['_id'], axis=1)
        return DataStruct_Stock_block(data.set_index('code', drop=False).drop_duplicates())


