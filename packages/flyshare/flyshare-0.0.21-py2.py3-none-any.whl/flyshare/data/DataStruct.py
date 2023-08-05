# coding :utf-8

"""
定义一些可以扩展的数据结构

方便序列化/相互转换

"""

import datetime
import itertools
import os
import platform
import sys
import time
import webbrowser
from functools import lru_cache, reduce, partial

import numpy as np
import pandas as pd
import six
from pyecharts import Kline
from flyshare.data.data_fq import data_stock_to_fq
from flyshare.data.data_resample import data_tick_resample
from flyshare.util import (MongoDBSetting, log_info,
                           util_to_json_from_pandas, trade_date_sse)
from flyshare.fetch.tdx import fetch_get_stock_realtime


class __stock_hq_base():
    def __init__(self, DataFrame):
        self.data = DataFrame
        self.type = ''
        self.if_fq = 'bfq'
        self.mongo_coll = MongoDBSetting.client.quantaxis

    def __repr__(self):
        return '< Base_DataStruct with %s securities >' % len(self.code)

    def __call__(self):
        return self.data

    # 使用property进行懒运算

    @property
    def open(self):
        return self.data['open']

    @property
    def high(self):
        return self.data['high']

    @property
    def low(self):
        return self.data['low']

    @property
    def close(self):
        return self.data['close']

    @property
    def vol(self):
        if 'volume' in self.data.columns:
            return self.data['volume']
        else:
            return self.data['vol']

    @property
    def date(self):

        return self.data.index.levels[self.data.index.names.index(
            'date')] if 'date' in self.data.index.names else self.data['date']

    @property
    def datetime(self):

        return self.data.index.levels[self.data.index.names.index(
            'datetime')] if 'datetime' in self.data.index.names else self.data.index.levels[self.data.index.names.index(
                'date')]

    @property
    def index(self):
        return self.data.index

    @property
    def code(self):
        return self.data.index.levels[self.data.index.names.index('code')]

    @property
    @lru_cache()
    def dicts(self):
        return self.to_dict('index')

    @lru_cache()
    def plot(self, code=None):
        if code is None:
            path_name = '.' + os.sep + '' + self.type + \
                '_codepackage_' + self.if_fq + '.html'
            kline = Kline('CodePackage_' + self.if_fq + '_' + self.type,
                          width=1360, height=700, page_title='flyshare')

            data_splits = self.splits()

            for i_ in range(len(data_splits)):
                data = []
                axis = []
                for dates, row in data_splits[i_].data.iterrows():
                    open, high, low, close = row[1:5]
                    datas = [open, close, low, high]
                    axis.append(dates[0])
                    data.append(datas)

                kline.add(self.code[i_], axis, data, mark_point=[
                          "max", "min"], is_datazoom_show=True, datazoom_orient='horizontal')
            kline.render(path_name)
            webbrowser.open(path_name)
            log_info(
                'The Pic has been saved to your path: %s' % path_name)
        else:
            data = []
            axis = []
            for dates, row in self.select_code(code).data.iterrows():
                open, high, low, close = row[1:5]
                datas = [open, close, low, high]
                axis.append(dates[0])
                data.append(datas)

            path_name = '.' + os.sep + '' + self.type + \
                '_' + code + '_' + self.if_fq + '.html'
            kline = Kline(code + '__' + self.if_fq + '__' + self.type,
                          width=1360, height=700, page_title='flyshare')
            kline.add(code, axis, data, mark_point=[
                      "max", "min"], is_datazoom_show=True, datazoom_orient='horizontal')
            kline.render(path_name)
            webbrowser.open(path_name)
            log_info(
                'The Pic has been saved to your path: %s' % path_name)

    @lru_cache()
    def len(self):
        return len(self.data)

    def reverse(self):
        return __stock_hq_base(self.data[::-1])

    @lru_cache()
    def show(self):
        return log_info(self.data)

    @lru_cache()
    def query(self, query_text):
        return self.data.query(query_text)

    @lru_cache()
    def to_list(self):
        return np.asarray(self.data).tolist()

    @lru_cache()
    def to_pd(self):
        return self.data

    @lru_cache()
    def to_numpy(self):
        return np.asarray(self.data)

    @lru_cache()
    def to_json(self):
        return util_to_json_from_pandas(self.data)

    @lru_cache()
    def to_dict(self, orient='dict'):
        return self.data.to_dict(orient)

    @lru_cache()
    def sync_status(self, __stock_hq_base):
        '固定的状态要同步 尤其在创建新的datastruct时候'
        (__stock_hq_base.if_fq, __stock_hq_base.type, __stock_hq_base.mongo_coll) = (
            self.if_fq, self.type, self.mongo_coll)
        return __stock_hq_base

    @lru_cache()
    def splits(self):
        if self.type in ['stock_day', 'index_day']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: __stock_hq_base(
                self.data[self.data['code'] == x].set_index(['date', 'code'], drop=False)), self.code))))
        elif self.type in ['stock_min', 'index_min']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: __stock_hq_base(
                self.data[self.data['code'] == x].set_index(['datetime', 'code'], drop=False)), self.code))))

    @lru_cache()
    def add_func(self, func, *arg, **kwargs):
        return list(map(lambda x: func(
            self.data[self.data['code'] == x], *arg, **kwargs), self.code))

    @lru_cache()
    def pivot(self, column_):
        assert isinstance(column_, str)
        try:
            return self.data.pivot(index='datetime', columns='code', values=column_)
        except:
            return self.data.pivot(index='date', columns='code', values=column_)

    @lru_cache()
    def select_time(self, start, end=None):
        if self.type in ['stock_day', 'index_day']:
            if end is not None:
                return self.sync_status(__stock_hq_base(self.data[self.data['date'] >= start][self.data['date'] <= end].set_index(['date', 'code'], drop=False)))
            else:
                return self.sync_status(__stock_hq_base(self.data[self.data['date'] == start].set_index(['date', 'code'], drop=False)))
        elif self.type in ['stock_min', 'index_min']:
            if end is not None:
                return self.sync_status(__stock_hq_base(self.data[self.data['datetime'] >= start][self.data['datetime'] <= end].set_index(['datetime', 'code'], drop=False)))
            else:
                return self.sync_status(__stock_hq_base(self.data[self.data['datetime'] == start].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def select_time_with_gap(self, time, gap, method):

        if method in ['gt', '>=']:

            def __gt(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] > time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] > time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(__stock_hq_base(pd.concat(list(map(lambda x: __gt(x), self.splits())))))

        elif method in ['gte', '>']:
            def __gte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] >= time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] >= time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(__stock_hq_base(pd.concat(list(map(lambda x: __gte(x), self.splits())))))
        elif method in ['lt', '<']:
            def __lt(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] < time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] < time].tail(gap).set_index(['datetime', 'code'], drop=False)

            return self.sync_status(__stock_hq_base(pd.concat(list(map(lambda x: __lt(x), self.splits())))))
        elif method in ['lte', '<=']:
            def __lte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] <= time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] <= time].tail(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(__stock_hq_base(pd.concat(list(map(lambda x: __lte(x), self.splits())))))
        elif method in ['e', '==', '=', 'equal']:
            def __eq(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] == time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] == time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(__stock_hq_base(pd.concat(list(map(lambda x: __eq(x), self.splits())))))

    @lru_cache()
    def select_code(self, code):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(__stock_hq_base(self.data[self.data['code'] == code].set_index(['date', 'code'], drop=False)))

        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(__stock_hq_base(self.data[self.data['code'] == code].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def get_bar(self, code, time, if_trade):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(__stock_hq_base((self.data[self.data['code'] == code])[self.data['date'] == str(time)[0:10]].set_index(['date', 'code'], drop=False)))

        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(__stock_hq_base((self.data[self.data['code'] == code])[self.data['datetime'] == str(time)[0:19]].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def find_bar(self, code, time):
        if len(time) == 10:
            return self.dicts[(datetime.datetime.strptime(time, '%Y-%m-%d'), code)]
        elif len(time) == 19:
            return self.dicts[(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S'), code)]


class DataStruct_Index_day(__stock_hq_base):
    '自定义的日线数据结构'

    def __init__(self, DataFrame):
        self.data = DataFrame
        self.type = 'index_day'
        self.if_fq = ''
        self.mongo_coll = MongoDBSetting.client.flyshare.index_day

    """
    def __add__(self,DataStruct):
        'add func with merge list and reindex'
        assert isinstance(DataStruct,DataStruct_Index_day)
        if self.if_fq==DataStruct.if_fq:
            self.sync_status(pd.concat())
    """

    def __repr__(self):
        return '< DataStruct_Index_day with %s securities >' % len(self.code)

    def reverse(self):
        return DataStruct_Index_day(self.data[::-1])

    def sync_status(self, DataStruct_Index_day):
        '固定的状态要同步 尤其在创建新的datastruct时候'
        (DataStruct_Index_day.if_fq, DataStruct_Index_day.type, DataStruct_Index_day.mongo_coll) = (
            self.if_fq, self.type, self.mongo_coll)
        return DataStruct_Index_day

    @lru_cache()
    def splits(self):
        if self.type in ['stock_day', 'index_day']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: DataStruct_Index_day(
                self.data[self.data['code'] == x].set_index(['date', 'code'], drop=False)), self.code))))
        elif self.type in ['stock_min', 'index_min']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: (
                self.data[self.data['code'] == x].set_index(['datetime', 'code'], drop=False)), self.code))))

    @lru_cache()
    def pivot(self, column_):
        assert isinstance(column_, str)
        try:
            return self.data.pivot(index='datetime', columns='code', values=column_)
        except:
            return self.data.pivot(index='date', columns='code', values=column_)

    @lru_cache()
    def select_time(self, start, end):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(DataStruct_Index_day(self.data[self.data['date'] >= start][self.data['date'] <= end].set_index(['date', 'code'], drop=False)))
        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(DataStruct_Index_day(self.data[self.data['datetime'] >= start][self.data['datetime'] <= end].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def select_time_with_gap(self, time, gap, method):

        if method in ['gt', '>=']:

            def __gt(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] > time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] > time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Index_day(pd.concat(list(map(lambda x: __gt(x), self.splits())))))

        elif method in ['gte', '>']:
            def __gte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] >= time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] >= time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Index_day(pd.concat(list(map(lambda x: __gte(x), self.splits())))))
        elif method in ['lt', '<']:
            def __lt(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] < time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] < time].tail(gap).set_index(['datetime', 'code'], drop=False)

            return self.sync_status(DataStruct_Index_day(pd.concat(list(map(lambda x: __lt(x), self.splits())))))
        elif method in ['lte', '<=']:
            def __lte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] <= time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] <= time].tail(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Index_day(pd.concat(list(map(lambda x: __lte(x), self.splits())))))
        elif method in ['e', '==', '=', 'equal']:
            def __eq(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] == time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] == time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Index_day(pd.concat(list(map(lambda x: __eq(x), self.splits())))))

    @lru_cache()
    def select_code(self, code):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(DataStruct_Index_day(self.data[self.data['code'] == code].set_index(['date', 'code'], drop=False)))

        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(DataStruct_Index_day(self.data[self.data['code'] == code].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def get_bar(self, code, time, if_trade=True):

        if if_trade:
            return self.sync_status(DataStruct_Index_day((self.data[self.data['code'] == code])[self.data['date'] == str(time)[0:10]].set_index(['date', 'code'], drop=False)))
        else:
            return self.sync_status(DataStruct_Index_day((self.data[self.data['code'] == code])[self.data['date'] <= str(time)[0:10]].set_index(['date', 'code'], drop=False).tail(1)))


class DataStruct_Index_min(__stock_hq_base):
    '自定义的日线数据结构'

    def __init__(self, DataFrame):
        self.type = 'index_min'
        self.if_fq = ''
        self.data = DataFrame.ix[:, [
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'date']]
        self.mongo_coll = MongoDBSetting.client.flyshare.index_min

    def __repr__(self):
        return '< DataStruct_Index_Min with %s securities >' % len(self.code)

    def reverse(self):
        return DataStruct_Index_min(self.data[::-1])

    def to_json(self):
        return util_to_json_from_pandas(self.data)

    def sync_status(self, DataStruct_Index_min):
        '固定的状态要同步 尤其在创建新的datastruct时候'
        (DataStruct_Index_min.if_fq, DataStruct_Index_min.type, DataStruct_Index_min.mongo_coll) = (
            self.if_fq, self.type, self.mongo_coll)
        return DataStruct_Index_min

    @lru_cache()
    def splits(self):
        if self.type in ['stock_day', 'index_day']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: (
                self.data[self.data['code'] == x].set_index(['date', 'code'], drop=False)), self.code))))
        elif self.type in ['stock_min', 'index_min']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: DataStruct_Index_min(
                self.data[self.data['code'] == x].set_index(['datetime', 'code'], drop=False)), self.code))))

    @lru_cache()
    def pivot(self, column_):
        assert isinstance(column_, str)
        try:
            return self.data.pivot(index='datetime', columns='code', values=column_)
        except:
            return self.data.pivot(index='date', columns='code', values=column_)

    @lru_cache()
    def select_time(self, start, end):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(DataStruct_Index_min(self.data[self.data['date'] >= start][self.data['date'] <= end].set_index(['date', 'code'], drop=False)))
        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(DataStruct_Index_min(self.data[self.data['datetime'] >= start][self.data['datetime'] <= end].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def select_time_with_gap(self, time, gap, method):

        if method in ['gt', '>=']:

            def __gt(__dataS):
                print(__dataS)
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] > time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] > time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Index_min(pd.concat(list(map(lambda x: __gt(x), self.splits())))))

        elif method in ['gte', '>']:
            def __gte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] >= time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] >= time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Index_min(pd.concat(list(map(lambda x: __gte(x), self.splits())))))
        elif method in ['lt', '<']:
            def __lt(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] < time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] < time].tail(gap).set_index(['datetime', 'code'], drop=False)

            return self.sync_status(DataStruct_Index_min(pd.concat(list(map(lambda x: __lt(x), self.splits())))))
        elif method in ['lte', '<=']:
            def __lte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] <= time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] <= time].tail(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Index_min(pd.concat(list(map(lambda x: __lte(x), self.splits())))))
        elif method in ['e', '==', '=', 'equal']:
            def __eq(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] == time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] == time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Index_min(pd.concat(list(map(lambda x: __eq(x), self.splits())))))

    @lru_cache()
    def select_code(self, code):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(DataStruct_Index_min(self.data[self.data['code'] == code].set_index(['date', 'code'], drop=False)))

        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(DataStruct_Index_min(self.data[self.data['code'] == code].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def get_bar(self, code, time, if_trade=True):

        if if_trade:
            return self.sync_status(DataStruct_Index_min((self.data[self.data['code'] == code])[self.data['datetime'] == str(time)[0:19]].set_index(['datetime', 'code'], drop=False)))
        else:
            return self.sync_status(DataStruct_Index_min((self.data[self.data['code'] == code])[self.data['datetime'] <= str(time)[0:19]].set_index(['datetime', 'code'], drop=False).tail(1)))


class DataStruct_Stock_min(__stock_hq_base):
    def __init__(self, DataFrame):
        self.data = DataFrame.ix[:, [
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'date']]
        self.type = 'stock_min'
        self.if_fq = 'bfq'
        self.mongo_coll = MongoDBSetting.client.flyshare.stock_min

    def __repr__(self):
        return '< DataStruct_Stock_Min with %s securities >' % len(self.code)

    def to_qfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 20:
                data = DataStruct_Stock_min(pd.concat(list(map(lambda x: data_stock_to_fq(
                    self.data[self.data['code'] == x]), self.code))).set_index(['datetime', 'code'], drop=False))
                data.if_fq = 'qfq'
                return data
            else:
                data = DataStruct_Stock_min(
                    self.data.groupby('code').apply(data_stock_to_fq))
                return data
        else:
            log_info(
                'none support type for qfq Current type is:%s' % self.if_fq)
            return self

    def to_hfq(self):
        if self.if_fq is 'bfq':
            data = DataStruct_Stock_min(pd.concat(list(map(lambda x: data_stock_to_fq(
                self.data[self.data['code'] == x], '01'), self.code))).set_index(['datetime', 'code'], drop=False))
            data.if_fq = 'hfq'
            return data
        else:
            log_info(
                'none support type for qfq Current type is:%s' % self.if_fq)
            return self

    @lru_cache()
    def reverse(self):
        return DataStruct_Stock_min(self.data[::-1])

    @lru_cache()
    def sync_status(self, DataStruct_Stock_min):
        '固定的状态要同步 尤其在创建新的datastruct时候'
        (DataStruct_Stock_min.if_fq, DataStruct_Stock_min.type, DataStruct_Stock_min.mongo_coll) = (
            self.if_fq, self.type, self.mongo_coll)
        return DataStruct_Stock_min

    @lru_cache()
    def splits(self):
        if self.type in ['stock_day', 'index_day']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: (
                self.data[self.data['code'] == x].set_index(['date', 'code'], drop=False)), self.code))))
        elif self.type in ['stock_min', 'index_min']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: DataStruct_Stock_min(
                self.data[self.data['code'] == x].set_index(['datetime', 'code'], drop=False)), self.code))))

    @lru_cache()
    def pivot(self, column_):
        assert isinstance(column_, str)
        try:
            return self.data.pivot(index='datetime', columns='code', values=column_)
        except:
            return self.data.pivot(index='date', columns='code', values=column_)

    @lru_cache()
    def select_time(self, start, end):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(DataStruct_Stock_min(self.data[self.data['date'] >= start][self.data['date'] <= end].set_index(['date', 'code'], drop=False)))
        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(DataStruct_Stock_min(self.data[self.data['datetime'] >= start][self.data['datetime'] <= end].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def select_time_with_gap(self, time, gap, method):

        if method in ['gt', '>=']:

            def __gt(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] > time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] > time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Stock_min(pd.concat(list(map(lambda x: __gt(x), self.splits())))))

        elif method in ['gte', '>']:
            def __gte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] >= time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] >= time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Stock_min(pd.concat(list(map(lambda x: __gte(x), self.splits())))))
        elif method in ['lt', '<']:
            def __lt(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] < time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] < time].tail(gap).set_index(['datetime', 'code'], drop=False)

            return self.sync_status(DataStruct_Stock_min(pd.concat(list(map(lambda x: __lt(x), self.splits())))))
        elif method in ['lte', '<=']:
            def __lte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] <= time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] <= time].tail(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Stock_min(pd.concat(list(map(lambda x: __lte(x), self.splits())))))
        elif method in ['e', '==', '=', 'equal']:
            def __eq(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] == time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] == time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Stock_min(pd.concat(list(map(lambda x: __eq(x), self.splits())))))

    @lru_cache()
    def select_code(self, code):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(DataStruct_Stock_min(self.data[self.data['code'] == code].set_index(['date', 'code'], drop=False)))

        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(DataStruct_Stock_min(self.data[self.data['code'] == code].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def get_bar(self, code, time, if_trade=True):
        if if_trade:
            return self.sync_status(DataStruct_Stock_min((self.data[self.data['code'] == code])[self.data['datetime'] == str(time)[0:19]].set_index(['datetime', 'code'], drop=False)))
        else:
            return self.sync_status(DataStruct_Stock_min((self.data[self.data['code'] == code])[self.data['datetime'] <= str(time)[0:19]].set_index(['datetime', 'code'], drop=False).tail(1)))


class DataStruct_Stock_day(__stock_hq_base):
    def __init__(self, DataFrame):
        self.data = DataFrame
        self.type = 'stock_day'
        self.if_fq = 'bfq'
        self.mongo_coll = MongoDBSetting.client.flyshare.stock_day

    def __repr__(self):
        return '< DataStruct_Stock_day with %s securities >' % len(self.code)

    @lru_cache()
    def to_qfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 20:

                data = DataStruct_Stock_day(pd.concat(list(map(
                    lambda x: data_stock_to_fq(self.data[self.data['code'] == x]), self.code))))
                data.if_fq = 'qfq'
                return data
            else:
                data = DataStruct_Stock_day(
                    self.data.groupby('code').apply(data_stock_to_fq))
                data.if_fq = 'qfq'
                return data
        else:
            log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self

    @lru_cache()
    def to_hfq(self):
        if self.if_fq is 'bfq':
            data = DataStruct_Stock_day(pd.concat(list(map(lambda x: data_stock_to_fq(
                self.data[self.data['code'] == x], '01'), self.code))))
            data.if_fq = 'hfq'
            return data
        else:
            log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self

    @lru_cache()
    def reverse(self):
        return DataStruct_Stock_day(self.data[::-1])

    @lru_cache()
    def sync_status(self, DataStruct_Stock_day):
        '固定的状态要同步 尤其在创建新的datastruct时候'
        (DataStruct_Stock_day.if_fq, DataStruct_Stock_day.type, DataStruct_Stock_day.mongo_coll) = (
            self.if_fq, self.type, self.mongo_coll)
        return DataStruct_Stock_day

    @lru_cache()
    def splits(self):
        if self.type in ['stock_day', 'index_day']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: DataStruct_Stock_day(
                self.data[self.data['code'] == x].set_index(['date', 'code'], drop=False)), self.code))))
        elif self.type in ['stock_min', 'index_min']:
            return list(map(lambda data: self.sync_status(data), list(map(lambda x: (
                self.data[self.data['code'] == x].set_index(['datetime', 'code'], drop=False)), self.code))))

    @lru_cache()
    def pivot(self, column_):
        assert isinstance(column_, str)
        try:
            return self.data.pivot(index='datetime', columns='code', values=column_)
        except:
            return self.data.pivot(index='date', columns='code', values=column_)

    @lru_cache()
    def select_time(self, start, end):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(DataStruct_Stock_day(self.data[self.data['date'] >= start][self.data['date'] <= end].set_index(['date', 'code'], drop=False)))
        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(DataStruct_Stock_day(self.data[self.data['datetime'] >= start][self.data['datetime'] <= end].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def select_time_with_gap(self, time, gap, method):

        if method in ['gt', '>=']:

            def __gt(__dataS):

                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] > time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] > time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Stock_day(pd.concat(list(map(lambda x: __gt(x), self.splits())))))

        elif method in ['gte', '>']:
            def __gte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] >= time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] >= time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Stock_day(pd.concat(list(map(lambda x: __gte(x), self.splits())))))
        elif method in ['lt', '<']:
            def __lt(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] < time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] < time].tail(gap).set_index(['datetime', 'code'], drop=False)

            return self.sync_status(DataStruct_Stock_day(pd.concat(list(map(lambda x: __lt(x), self.splits())))))
        elif method in ['lte', '<=']:
            def __lte(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] <= time].tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] <= time].tail(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Stock_day(pd.concat(list(map(lambda x: __lte(x), self.splits())))))
        elif method in ['e', '==', '=', 'equal']:
            def __eq(__dataS):
                if self.type in ['stock_day', 'index_day']:
                    return __dataS.data[__dataS.data['date'] == time].head(gap).set_index(['date', 'code'], drop=False)
                elif self.type in ['stock_min', 'index_min']:
                    return __dataS.data[__dataS.data['datetime'] == time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.sync_status(DataStruct_Stock_day(pd.concat(list(map(lambda x: __eq(x), self.splits())))))

    @lru_cache()
    def select_code(self, code):
        if self.type in ['stock_day', 'index_day']:
            return self.sync_status(DataStruct_Stock_day(self.data[self.data['code'] == code].set_index(['date', 'code'], drop=False)))

        elif self.type in ['stock_min', 'index_min']:
            return self.sync_status(DataStruct_Stock_day(self.data[self.data['code'] == code].set_index(['datetime', 'code'], drop=False)))

    @lru_cache()
    def get_bar(self, code, time, if_trade=True):
        if if_trade:
            return self.sync_status(DataStruct_Stock_day((self.data[self.data['code'] == code])[self.data['date'] == str(time)[0:10]].set_index(['date', 'code'], drop=False)))
        else:
            return self.sync_status(DataStruct_Stock_day((self.data[self.data['code'] == code])[self.data['date'] <= str(time)[0:10]].set_index(['date', 'code'], drop=False).tail(1)))


class DataStruct_Stock_block():
    def __init__(self, DataFrame):
        self.data = DataFrame

    def __repr__(self):
        return '< DataStruct_Stock_Block >'

    def __call__(self):
        return self.data

    @property
    def len(self):
        return len(self.data)

    @property
    def block_name(self):
        return self.data.groupby('blockname').sum().index.unique().tolist()

    @property
    def code(self):
        return self.data.code.unique().tolist()

    def show(self):
        return self.data

    def get_code(self, code):
        return DataStruct_Stock_block(self.data[self.data['code'] == code])

    def get_block(self, _block_name):
        return DataStruct_Stock_block(self.data[self.data['blockname'] == _block_name])

    def get_type(self, _type):
        return DataStruct_Stock_block(self.data[self.data['type'] == _type])

    def get_price(self, _block_name=None):
        if _block_name is not None:
            try:
                code = self.data[self.data['blockname']
                                 == _block_name].code.unique().tolist()
                # try to get a datastruct package of lastest price
                return fetch_get_stock_realtime(code)

            except:
                return "Wrong Block Name! Please Check"
        else:
            code = self.data.code.unique().tolist()
            return fetch_get_stock_realtime(code)


class DataStruct_Stock_transaction():
    def __init__(self, DataFrame):
        self.type = 'stock_transaction'
        self.if_fq = 'None'
        self.mongo_coll = MongoDBSetting.client.flyshare.stock_transaction
        self.buyorsell = DataFrame['buyorsell']
        self.price = DataFrame['price']
        if 'volume' in DataFrame.columns:
            self.vol = DataFrame['volume']
        else:
            self.vol = DataFrame['vol']
        self.date = DataFrame['date']
        self.time = DataFrame['time']
        self.datetime = DataFrame['datetime']
        self.order = DataFrame['order']
        self.index = DataFrame.index
        self.data = DataFrame

    def resample(self, type_='1min'):
        return DataStruct_Stock_min(data_tick_resample(self.data, type_))


class DataStruct_Security_list():
    def __init__(self, DataFrame):
        self.data = DataFrame.loc[:, ['sse', 'code', 'name']].set_index(
            'code', drop=False)

    @property
    def code(self):
        return self.data.code

    @property
    def name(self):
        return self.data.name

    def get_stock(self, ST_option):
        return self.data

    def get_index(self):
        return self.data

    def get_etf(self):
        return self.data


class DataStruct_Market_reply():
    pass


class DataStruct_Market_bid():
    pass


class DataStruct_Market_bid_queue():
    pass


class DataStruct_ARP_account():
    pass


class DataStruct_Quantaxis_error():
    pass
