# coding: utf-8

import json

import tushare as QATs
import pandas as pd
from flyshare.util import util_date_stamp, log_info, util_to_json_from_pandas,util_date_int2str


def fetch_get_stock_day(name, startDate='', endDate='', if_fq='01', type_='json'):
    if (len(name) != 6):
        name = str(name)[0:6]

    if str(if_fq) in ['qfq', '01']:
        if_fq = 'qfq'
    elif str(if_fq) in ['hfq', '02']:
        if_fq = 'hfq'
    elif str(if_fq) in ['bfq', '00']:
        if_fq = 'bfq'
    else:
        log_info('wrong with fq_factor! using qfq')
        if_fq = 'qfq'

    data = QATs.get_k_data(str(name), startDate, endDate,
                           ktype='D', autype=if_fq, retry_count=200, pause=0.005).sort_index()
    
    data['date_stamp'] = data['date'].apply(lambda x: util_date_stamp(x))
    data['fqtype'] = if_fq
    if type_ in ['json']:
        data_json = util_to_json_from_pandas(data)
        return data_json
    elif type_ in ['pd', 'pandas', 'p']:
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date',drop=False)
        data['date'] = data['date'].apply(lambda x: str(x)[0:10])
        return data

def fetch_get_stock_realtime():
    data = QATs.get_today_all()
    data_json = util_to_json_from_pandas(data)
    return data_json


def fetch_get_stock_info(name):
    data = QATs.get_stock_basics()
    data_json = util_to_json_from_pandas(data)

    for i in range(0, len(data_json) - 1, 1):
        data_json[i]['code'] = data.index[i]
    return data_json


def fetch_get_stock_tick(name, date):
    if (len(name) != 6):
        name = str(name)[0:6]
    return QATs.get_tick_data(name, date)


def fetch_get_stock_list():
    df = QATs.get_stock_basics()
    return list(df.index)
def fetch_get_stock_time_to_market():
    data = QATs.get_stock_basics()
    return data[data['timeToMarket']!=0]['timeToMarket'].apply(lambda x:util_date_int2str(x))

def fetch_get_trade_date(endDate, exchange):
    data = QATs.trade_cal()
    da = data[data.isOpen > 0]
    data_json = util_to_json_from_pandas(data)
    message = []
    for i in range(0, len(data_json) - 1, 1):
        date = data_json[i]['calendarDate']
        num = i + 1
        exchangeName = 'SSE'
        data_stamp = util_date_stamp(date)
        mes = {'date': date, 'num': num,
               'exchangeName': exchangeName, 'date_stamp': data_stamp}
        message.append(mes) 
    return message
# test

# print(get_stock_day("000001",'2001-01-01','2010-01-01'))
# print(get_stock_tick("000001.SZ","2017-02-21"))
