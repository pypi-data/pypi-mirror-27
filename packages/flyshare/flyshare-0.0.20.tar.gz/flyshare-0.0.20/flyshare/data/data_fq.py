# coding:utf-8


from flyshare.fetch import fetch_get_stock_day, fetch_get_stock_xdxr
from flyshare.util import MongoDBSetting as ms, log_info

import datetime
import pandas as pd


def data_get_qfq(code, start, end):
    '使用网络数据进行复权/需要联网'
    xdxr_data = fetch_get_stock_xdxr('tdx', code)
    bfq_data = fetch_get_stock_day(
        'tdx', code, '1990-01-01', str(datetime.date.today())).dropna(axis=0)
    return data_make_qfq(bfq_data[start:end], xdxr_data)


def data_get_hfq(code, start, end):
    '使用网络数据进行复权/需要联网'
    xdxr_data = fetch_get_stock_xdxr('tdx', code)
    bfq_data = fetch_get_stock_day(
        'tdx', code, '1990-01-01', str(datetime.date.today())).dropna(axis=0)
    return data_make_hfq(bfq_data[start:end], xdxr_data)


def data_make_qfq(bfq_data, xdxr_data):
    '使用数据库数据进行复权'
    info = xdxr_data[xdxr_data['category'] == 1]
    bfq_data['if_trade'] = 1
    data = pd.concat([bfq_data, info[['category']]
                      [bfq_data.index[0]:bfq_data.index[-1]]], axis=1)
    data['if_trade'].fillna(value=0, inplace=True)
    data = data.fillna(method='ffill')
    data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                  'songzhuangu']][bfq_data.index[0]:bfq_data.index[-1]]], axis=1)
    data = data.fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                        * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
    data['adj'] = (data['preclose'].shift(-1) /
                   data['close']).fillna(1)[::-1].cumprod()
    data['open'] = data['open'] * data['adj']
    data['high'] = data['high'] * data['adj']
    data['low'] = data['low'] * data['adj']
    data['close'] = data['close'] * data['adj']
    data['preclose'] = data['preclose'] * data['adj']

    return data.query('if_trade==1').drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu',
                                           'if_trade', 'category'], axis=1)[data['open'] != 0]


def data_make_hfq(bfq_data, xdxr_data):
    '使用数据库数据进行复权'
    info = xdxr_data[xdxr_data['category'] == 1]
    bfq_data['if_trade'] = 1
    data = pd.concat([bfq_data, info[['category']]
                      [bfq_data.index[0]:bfq_data.index[-1]]], axis=1)

    data['if_trade'].fillna(value=0, inplace=True)
    data = data.fillna(method='ffill')

    data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                  'songzhuangu']][bfq_data.index[0]:bfq_data.index[-1]]], axis=1)

    data = data.fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                        * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
    data['adj'] = (data['preclose'].shift(-1) /
                   data['close']).fillna(1).cumprod()
    data['open'] = data['open'] / data['adj']
    data['high'] = data['high'] / data['adj']
    data['low'] = data['low'] / data['adj']
    data['close'] = data['close'] / data['adj']
    data['preclose'] = data['preclose'] / data['adj']
    return data.query('if_trade==1').drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu'], axis=1)[data['open'] != 0]


def data_stock_to_fq(__data, type_='01'):

    def __fetch_stock_xdxr(code, format_='pd', collections=ms.client.flyshares.stock_xdxr):
        '获取股票除权信息/数据库'
        try:
            data = pd.DataFrame([item for item in collections.find(
                {'code': code})]).drop(['_id'], axis=1)
            data['date'] = pd.to_datetime(data['date'])
            return data.set_index(['date', 'code'], drop=False)
        except:
            return pd.DataFrame(columns=['category', 'category_meaning', 'code', 'date', 'fenhong',
                                         'fenshu', 'liquidity_after', 'liquidity_before', 'name', 'peigu', 'peigujia',
                                         'shares_after', 'shares_before', 'songzhuangu', 'suogu', 'xingquanjia'])
    '股票 日线/分钟线 动态复权接口'
    if type_ in ['01', 'qfq']:
        #print(data_make_qfq(__data, __fetch_stock_xdxr(__data['code'][0])))
        return data_make_qfq(__data, __fetch_stock_xdxr(__data['code'][0]))
    elif type_ in ['02', 'hfq']:
        return data_make_hfq(__data, __fetch_stock_xdxr(__data['code'][0]))
    else:
        log_info('wrong fq type! Using qfq')
        return data_make_qfq(__data, __fetch_stock_xdxr(__data['code'][0]))
