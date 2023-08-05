# -*- coding:utf-8 -*-
from __future__ import division

import time
import json
from bson.json_util import loads
import pandas as pd
import numpy as np
from pymongo import MongoClient
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

import json
import bson.json_util as ju
import flyshare.ApiConfig as ac
import tushare as ts
import datetime
import flyshare.util as util
from flyshare.util import vars
import flyshare as fs

def get_hist_data(code=None,
                  start=None,
                  end=None,
                  autype='qfq',
                  ktype='D',
                  data_source='default'):
    """
    Parameters
    ------
      code:string
                  Stock code e.g. 600848
      start:string
                  Start Date format：YYYY-MM-DD 
      end:string
                  End Date format：YYYY-MM-DD
      autype:string
                  复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
      ktype：string
                  Data Type，D=Day W=Week M=Month 5=5min 15=15min 30=30min 60=60min，Default is 'D'
      data_source: string
                  tushare, datareader, flyshare
    return
    -------
      DataFrame
        amount  close    code        date    date_stamp   high    low   open        vol
    """
    if code is None:
        return None

    if util.is_default(data_source) and ac.DATA_SOURCE is not None:
        data_source = ac.DATA_SOURCE
    elif util.is_default(data_source):
        data_source = 'tushare'

    if not code.isdigit():
        util.log_debug("The data is only available in Datareader: code ="+code)
        data_source = 'datareader'

    data_source = data_source.lower()
    util.log_debug("datasource = "+data_source)

    if util.is_tushare(data_source):

        if start is None:
            start = '2017-01-01'
        if end is None:
            end = util.get_date_today()
        util.log_debug("tushare data code:" + code+", start:"+start+", end:"+end)
        return ts.get_k_data(code=code, start=start, end=end, ktype=ktype, autype=autype)
    elif util.is_datareader(data_source):
        import pandas_datareader.data as web
        if start is None:
            start = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
        else:
            start = datetime.datetime.strptime(start, '%Y-%m-%d')

        if end is not None:
            end = datetime.datetime.strptime(end, '%Y-%m-%d')
        else:
            end = util.today()
        data = None
        try:
            data = web.DataReader(code, 'yahoo', start, end)
        except Exception as e:
            pass
        if data is not None:
            util.log_debug("Datareader-Yahoo data:")
            return data
        else:
            try:
                data = web.DataReader(code, 'google', start, end)
            except:
                pass
            if data is not None:
                util.log_debug("Datareader-Google data:")
                return data
    elif util.is_flyshare(data_source):
        url = vars.DATA_SOURCE+'/histdata?'
        if code is None:
            return None
        else:
            url += 'code='+code

        if start is not None:
            url += '&start='+start
        if end is not None:
            url += '&end='+end

        url += '&api_key='+ ac.api_key

        data = json.loads(ju.loads(urlopen(url).read()))
        df = pd.DataFrame(data)
        if '_id' in df:
            df = df.drop('_id',1)
        return df
    elif util.is_tdx(data_source):
        util.log_debug("TDX data: ")
        if ac.TDX_CONN is None:
            ac.TDX_CONN = fs.get_apis()

        start = start if start is not None else ''
        end = end if end is not None else util.get_date_today()

        return ts.bar(code, start_date=start, end_date=end, conn=ac.TDX_CONN)


def get_tick_data(code=None, date=None, retry_count=3, pause=0.001,
                  src='sn', asset='X', data_source = 'tushare'):
    """
    tick数据
    Parameters:
    ------------
    code:证券代码，支持股票,ETF/LOF,期货/期权,港股
    conn:服务器连接 ，通过ts.api()或者ts.xpi()获得
    date:日期
    asset:证券品种，E:沪深交易所股票和基金, INDEX:沪深交易所指数， X:其他证券品种，大致如下：
                     支持的扩展行情包括(asset='X')：
                            郑州商品期权         OZ 大连商品期权         OD 上海商品期权         OS
                            上海个股期权         QQ 香港指数         FH 郑州商品         QZ 大连商品         QD 上海期货         QS
                            香港主板         KH 香港权证         KR 开放式基金         FU 货币型基金         FB
                            招商理财产品         LC 招商货币产品         LB 国际指数         FW 国内宏观指标         HG 中国概念股         CH
                            美股知名公司         MG B股转H股         HB 股份转让         SB 股指期货         CZ 香港创业板         KG 香港信托基金         KT
                             国债预发行         GY 主力期货合约         MA
                              中证指数         ZZ 港股通         GH
    market:市场代码，通过ts.get_markets()获取

    Return
    ----------
    DataFrame
    date:日期
    time:时间
    price:成交价
    vol:成交量
    type:买卖方向，0-买入 1-卖出 2-集合竞价成交
            期货  0:开仓  1:多开   -1:空开
         期货多一列数据oi_change:增仓数据

    """
    if util.is_today(date):
        return ts.get_today_ticks(code, retry_count, pause)

    if util.is_tushare(data_source):
        return ts.get_tick_data(code, date, retry_count, pause, src)
    elif util.is_tdx(data_source):
        if ac.TDX_CONN is None:
            ac.TDX_CONN = fs.get_apis()

        return ts.tick(code, date=date, conn= ac.TDX_CONN, asset=asset)

def get_large_order(code=None, date=None, vol=400, retry_count=3, pause=0.001 , data_source = 'tushare'):
    if util.is_tushare(data_source):
        return ts.get_sina_dd(code, date, vol, retry_count, pause)

def get_today_all(data_source='tushare'):
    if util.is_tushare(data_source):
        return ts.get_today_all()

def get_realtime_quotes(symbols=None, data_source='tushare'):
    if util.is_tushare(data_source):
        return ts.get_realtime_quotes(symbols)

def get_h_data(code, start=None, end=None, autype='qfq',
               index=False, retry_count=3, pause=0.001, drop_factor=True, data_source='tushare'):
    if util.is_tushare(data_source):
        return ts.get_h_data(code, start, end, autype, index, retry_count, pause, drop_factor)

def get_index(data_source='tushare'):
    if util.is_tushare(data_source):
        return ts.get_index()




def _code_to_symbol(code):
    """
        convert code to symbol
    """
    if code in vars.INDEX_LABELS:
        return vars.INDEX_LIST[code]
    else:
        if len(code) != 6 :
            return code
        else:
            return 'sh%s'%code if code[:1] in ['5', '6', '9'] else 'sz%s'%code

if __name__ == '__main__':
    # print get_hist_data('AAPL',start='2017-01-01', end='2017-10-10', data_source='datareader').head(2)
    # print(get_hist_data('600519', start='2017-01-01', end='2017-10-10', data_source='tushare'))
    print(get_hist_data('600519', data_source='tushare'))