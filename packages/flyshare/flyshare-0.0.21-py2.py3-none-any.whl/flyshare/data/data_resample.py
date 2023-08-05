# coding:utf-8


from flyshare.util import util_make_min_index, log_info
from flyshare.fetch import fetch_get_stock_transaction
from datetime import time
import pandas as pd


def data_tick_resample(tick, type_='1min'):
    data = tick['price'].resample(
        type_, label='right', closed='left').ohlc()

    data['volume'] = tick['vol'].resample(
        type_, label='right', closed='left').sum()
    data['code'] = tick['code'][0]

    __data_ = pd.DataFrame()
    _temp=tick.drop_duplicates('date')['date']
    for item in _temp:
        __data = data[item]
        _data = __data[time(9, 31):time(11, 30)].append(
            __data[time(13, 1):time(15, 0)])
        __data_ = __data_.append(_data)

    __data_['datetime'] = __data_.index
    __data_['date'] = __data_['datetime'].apply(lambda x: str(x)[0:10])
    __data_['datetime'] = __data_['datetime'].apply(lambda x: str(x)[0:19])
    return __data_.fillna(method='ffill').set_index(['datetime', 'code'], drop=False)


if __name__ == '__main__':
    tick = fetch_get_stock_transaction(
        'tdx', '000001', '2017-01-03', '2017-01-05')
    print(data_tick_resample(tick))
