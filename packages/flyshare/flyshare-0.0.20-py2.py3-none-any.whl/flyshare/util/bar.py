#coding=utf-8

import json
import math
import datetime
import time
import numpy as np
import pandas as pd
from flyshare.util.date_trade import (util_get_real_datelist, util_date_gap,
                                      util_get_trade_range,
                                      util_if_trade, trade_date_sse)


def util_make_min_index(day, type_='1min'):
    if util_if_trade(day) is True:
        return pd.date_range(str(day) + ' 09:30:00', str(day) + ' 11:30:00', freq=type_, closed='right').append(
            pd.date_range(str(day) + ' 13:00:00', str(day) + ' 15:00:00', freq=type_, closed='right'))
    else:
        return pd.DataFrame(['No trade'])


def util_make_hour_index(day, type_='1h'):
    if util_if_trade(day) is True:
        return pd.date_range(str(day) + '09:30:00', str(day) + ' 11:30:00', freq=type_, closed='right').append(
            pd.date_range(str(day) + ' 13:00:00', str(day) + ' 15:00:00', freq=type_, closed='right'))
    else:
        return pd.DataFrame(['No trade'])


def util_time_gap(time, gap, methods, type_):

    '分钟线回测的时候的gap'
    min_len = int(240 / int(str(type_).split('min')[0]))
    day_gap = math.ceil(gap / min_len)

    if methods in ['>', 'gt']:
        data = pd.concat([pd.DataFrame(util_make_min_index(day, type_)) for day in trade_date_sse[trade_date_sse.index(str(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').date())):trade_date_sse.index(str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date())) + day_gap+1]]).reset_index()
        return np.asarray(data[data[0] > time].head(gap)[0].apply(lambda x: str(x))).tolist()[-1]
    elif methods in ['>=', 'gte']:
        data = pd.concat([pd.DataFrame(util_make_min_index(day, type_)) for day in trade_date_sse[trade_date_sse.index(str(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').date())):trade_date_sse.index(str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date())) + day_gap+1]]).reset_index()

        return np.asarray(data[data[0] >= time].head(gap)[0].apply(lambda x: str(x))).tolist()[-1]
    elif methods in ['<', 'lt']:
        data = pd.concat([pd.DataFrame(util_make_min_index(day, type_)) for day in trade_date_sse[trade_date_sse.index(str(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').date())) - day_gap:trade_date_sse.index(str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date()))+1]]).reset_index()

        return np.asarray(data[data[0] < time].tail(gap)[0].apply(lambda x: str(x))).tolist()[0]
    elif methods in ['<=', 'lte']:
        data = pd.concat([pd.DataFrame(util_make_min_index(day, type_)) for day in trade_date_sse[trade_date_sse.index(str(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').date())) - day_gap:trade_date_sse.index(str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date()))+1]]).reset_index()

        return np.asarray(data[data[0] <= time].tail(gap)[0].apply(lambda x: str(x))).tolist()[0]
    elif methods in ['==', '=', 'eq']:
        return time


if __name__ == '__main__':
    pass
