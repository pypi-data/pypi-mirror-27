# coding: utf-8
#
import numpy
import pandas as pd

from pandas import DataFrame
from flyshare.util import (MongoDBSetting as ms,
                           util_date_stamp,
                           trade_date_sse,
                           util_date_valid,
                           log_info,
                           util_time_stamp,
                           util_to_json_from_pandas,
                           util_to_list_from_pandas)
"""
按要求从数据库取数据，并转换成numpy结构

"""


def fetch_stock_day(code, __start, __end, format_='numpy', collections=ms.client.flyshare.stock_day):
    '获取股票日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]

    if util_date_valid(__end) == True:

        __data = []

        for item in collections.find({
            'code': str(code)[0:6], "date_stamp": {
                "$lte": util_date_stamp(__end),
                "$gte": util_date_stamp(__start)}}):

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['date']])

        # 多种数据格式
        if format_ in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif format_ in ['list', 'l', 'L']:
            __data = __data
        elif format_ in ['P', 'p', 'pandas', 'pd']:
            __data = DataFrame(__data, columns=['code', 'open', 'high', 'low', 'close', 'volume', 'date'])

            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date', drop=False)
        return __data
    else:
        log_info('something wrong with date')


def fetch_trade_date():
    '获取交易日期'
    return trade_date_sse


def fetch_stock_list(collections=ms.client.flyshare.stock_list):
    '获取股票列表'
    return [item for item in collections.find()]


def fetch_stock_full(date_, format_='numpy', collections=ms.client.flyshare.stock_day):
    '获取全市场的某一日的数据'
    #__start = str(__start)[0:10]
    Date = str(date_)[0:10]
    if util_date_valid(Date) == True:

        __data = []
        for item in collections.find({
            "date_stamp": {
                "$lte": util_date_stamp(Date),
                "$gte": util_date_stamp(Date)}}):
            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['volume']), item['date']])
        # 多种数据格式
        if format_ in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif format_ in ['list', 'l', 'L']:
            __data = __data
        elif format_ in ['P', 'p', 'pandas', 'pd']:
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date', drop=True)
        return __data
    else:
        log_info('something wrong with date')


def fetch_stock_info(code, collections):
    '获取股票信息'
    pass


def fetch_stocklist_day(stock_list, date_range, collections=ms.client.flyshare.stock_day):
    '获取多个股票的日线'
    __data = []
    for item in stock_list:
        __data.append(fetch_stock_day(
            item, date_range[0], date_range[-1], 'pd', collections))
    return __data


def fetch_index_day(code, __start, __end, format_='numpy', collections=ms.client.flyshare.index_day):
    '获取指数日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]

    if util_date_valid(__end) == True:

        __data = []

        for item in collections.find({
            'code': str(code)[0:6], "date_stamp": {
                "$lte": util_date_stamp(__end),
                "$gte": util_date_stamp(__start)}}):

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['date']])

        # 多种数据格式
        if format_ in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif format_ in ['list', 'l', 'L']:
            __data = __data
        elif format_ in ['P', 'p', 'pandas', 'pd']:

            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])

            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date', drop=False)
        return __data
    else:
        log_info('something wrong with date')


def fetch_indexlist_day(stock_list, date_range, collections=ms.client.flyshare.index_day):
    '获取多个股票的日线'
    __data = []
    for item in stock_list:
        __data.append(fetch_index_day(
            item, date_range[0], date_range[-1], 'pd', collections))
    return __data


def fetch_index_min(
        code,
        startTime, endTime,
        format_='numpy',
        type_='1min',
        collections=ms.client.flyshare.index_min):
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
    for item in collections.find({
        'code': str(code), "time_stamp": {
            "$gte": util_time_stamp(startTime),
            "$lte": util_time_stamp(endTime)
        }, 'type': type_
    }):

        __data.append([str(item['code']), float(item['open']), float(item['high']), float(
            item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])

    __data = DataFrame(__data, columns=[
        'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

    __data['datetime'] = pd.to_datetime(__data['datetime'])
    __data = __data.set_index('datetime', drop=False)
    #res = fetch_stock_to_fq(__data)
    if format_ in ['numpy', 'np', 'n']:
        return numpy.asarray(__data)
    elif format_ in ['list', 'l', 'L']:
        return numpy.asarray(__data).tolist()
    elif format_ in ['P', 'p', 'pandas', 'pd']:
        return __data


def fetch_stock_min(code, startTime, endTime, format_='numpy', type_='1min', collections=ms.client.flyshare.stock_min):
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
    for item in collections.find({
        'code': str(code), "time_stamp": {
            "$gte": util_time_stamp(startTime),
            "$lte": util_time_stamp(endTime)
        }, 'type': type_
    }):

        __data.append([str(item['code']), float(item['open']), float(item['high']), float(
            item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])

    __data = DataFrame(__data, columns=[
        'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

    __data['datetime'] = pd.to_datetime(__data['datetime'])
    __data = __data.set_index('datetime', drop=False)
    #res = fetch_stock_to_fq(__data)
    if format_ in ['numpy', 'np', 'n']:
        return numpy.asarray(__data)
    elif format_ in ['list', 'l', 'L']:
        return numpy.asarray(__data).tolist()
    elif format_ in ['P', 'p', 'pandas', 'pd']:
        return __data


def fetch_stocklist_min(stock_list, date_range, type_='1min', collections=ms.client.flyshare.stock_min):
    '获取不复权股票分钟线'
    __data = []
    for item in stock_list:
        __data.append(fetch_stock_min(
            item, date_range[0], date_range[-1], 'pd', type_, collections))
    return __data


def fetch_future_day():
    pass


def fetch_future_min():
    pass


def fetch_future_tick():
    pass


def fetch_stock_xdxr(code, format_='pd', collections=ms.client.flyshare.stock_xdxr):
    '获取股票除权信息/数据库'
    data = pd.DataFrame([item for item in collections.find(
        {'code': code})]).drop(['_id'], axis=1)
    data['date'] = pd.to_datetime(data['date'])
    return data.set_index('date', drop=False)
    # data['date']=data['date'].apply(lambda)


def fetch_backtest_info(user=None, account_cookie=None, strategy=None, stock_list=None, collections=ms.client.flyshare.backtest_info):

    return util_to_json_from_pandas(pd.DataFrame([item for item in collections.find(util_to_json_from_pandas(pd.DataFrame([user, account_cookie, strategy, stock_list], index=['user', 'account_cookie', 'strategy', 'stock_list']).dropna().T)[0])]).drop(['_id'], axis=1))


def fetch_backtest_history(cookie=None, collections=ms.client.flyshare.backtest_history):
    return util_to_json_from_pandas(pd.DataFrame([item for item in collections.find(util_to_json_from_pandas(pd.DataFrame([cookie], index=['cookie']).dropna().T)[0])]).drop(['_id'], axis=1))


def fetch_stock_block(code=None, format_='pd', collections=ms.client.flyshare.stock_block):
    if code is not None:
        data = pd.DataFrame([item for item in collections.find(
            {'code': code})]).drop(['_id'], axis=1)
        return data.set_index('code', drop=False)
    else:
        data = pd.DataFrame(
            [item for item in collections.find()]).drop(['_id'], axis=1)
        return data.set_index('code', drop=False)


def fetch_stock_info(code, format_='pd', collections=ms.client.flyshare.stock_info):
    try:
        data = pd.DataFrame([item for item in collections.find(
            {'code': code})]).drop(['_id'], axis=1)
        #data['date'] = pd.to_datetime(data['date'])
        return data.set_index('code', drop=False)
    except Exception as e:
        log_info(e)
        return None


def fetch_stock_name(code, collections=ms.client.flyshare.stock_list):
    try:
        return collections.find_one({'code': code})['name']
    except Exception as e:
        log_info(e)
