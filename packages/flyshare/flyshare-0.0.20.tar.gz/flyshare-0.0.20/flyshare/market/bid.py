# coding:utf-8


import datetime
import random
import threading
import time
import pandas as pd
from flyshare.util import log_info, util_to_json_from_pandas
"""
重新定义bid模式



"""


class MarketBid():
    def __init__(self):
        self.price = 16
        self.date = '2015-01-05'
        self.datetime = '2015-01-05 09:01:00'
        self.sending_time = '2015-01-05 09:01:00'  # 下单时间
        self.transact_time = ''
        self.amount = 10
        self.towards = 1  # side 
        self.code = str('000001')
        self.user = 'root'
        self.strategy = 'example01'
        self.type = '0x01'  # see below
        self.bid_model = 'strategy'
        self.amount_model = 'amount'
        self.order_id = str(random.random())
        self.trade_id = ''
        self.status = '100'


    def stock_day(self):
        self.type = '0x01'

    def stock_min(self):
        self.type = '0x02'

    def index_day(self):
        self.type = '0x03'

    def index_min(self):
        self.type = '0x04'

    def stock_transaction(self):
        self.type = '0x05'

    def index_transaction(self):
        self.type = '0x06'

    def future_day(self):
        self.type = '1x01'

    def show(self):
        return vars(self)

    def to_df(self):
        return pd.DataFrame([vars(self), ])
    def to_dict(self):
        return vars(self)
    def from_dict(self, bid):
        try:
            self.price = bid['price']
            self.date = bid['date']
            self.datetime = bid['datetime']
            self.sending_time = bid['sending_time']  # 下单时间
            self.transact_time = bid['transact_time']
            self.amount = bid['amount']
            self.towards = bid['towards']
            self.code = bid['code']
            self.user = bid['user']
            self.strategy = bid['strategy']
            self.type = bid['type']
            self.bid_model = bid['bid_model']
            self.amount_model = bid['amount_model']
            self.order_id = bid['order_id']
            self.trade_id = bid['trade_id']
            return self
        except:
            log_info('Failed to tran from dict')

    def from_dataframe(self, dataframe):
        bid_list = []
        for item in util_to_json_from_pandas(dataframe):
            bid_list.append(self.from_dict(item))
        return bid_list
    
    def apply(self,bid):
        try:
            self.price = bid['price']
            self.date = bid['date']
            self.datetime = bid['datetime']
            self.sending_time = bid['sending_time']  # 下单时间
            self.transact_time = bid['transact_time']
            self.amount = bid['amount']
            self.towards = bid['towards']
            self.code = bid['code']
            self.user = bid['user']
            self.strategy = bid['strategy']
            self.type = bid['type']
            self.bid_model = bid['bid_model']
            self.amount_model = bid['amount_model']
            self.order_id = bid['order_id']
            self.trade_id = bid['trade_id']
            return self
        except:
            log_info('Failed to tran from dict')
        

class MarketBidList():   # also the order tree
    """
    一个待成交列表
    
    """
    def __init__(self):
        self.list = []

    def from_dataframe(self, dataframe):
        self.list=[MarketBid().from_dict(item) for item in util_to_json_from_pandas(dataframe)]
        return self.list

if __name__ == '__main__':
    ax = MarketBid()
    ax.stock_day()
    print(ax.type)
