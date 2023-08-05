# coding:utf-8


import datetime
import random
import time

"""
重新定义bid模式

bid不应该以一个简单的报价模板的形式引入,而应该直接作为一个下单/回报/状态系统

比如*  Send_bid()
会回报一个状态 
{
    下单成功(10x):{
        交易成功:100,
        交易失败-报价不在范围:101,
        交易失败-报价数量不符合规定:102,
        交易状态-订单未完全成交:103,
        交易状态-订单数量过大(交易价格变动):104,
    },
    下单失败(20x):{
        下单格式不符合规定:201,
        下单关键数据缺失:202,
        下单时间错误:203
    }
}
同时需要一个队列对于订单进行管理,形成一个先进先出的队列:
Bid-Job-Management-Center

队列应该对于订单进行处理和排序,并分发给各种交易中心,然后得到各种交易中心的回报以后,封装结果并返回状态

2017/6/18

"""


class QAMarket_order_tree():
    def __init__(self):
        self.bid = {
            'price': float(16),
            'date': str('2015-01-05'),
            'time': str(time.mktime(datetime.datetime.now().timetuple())),
            'amount': int(10),
            'towards': int(1),
            'code': str('000001'),
            'user': str('root'),
            'strategy': str('example01'),
            'status': '0x01',
            'order_id': str(random.random())
        }
        self.bid_list = [self.bid]
    # 报价队列  插入/取出/查询pytho

    def bid_insert(self):
        self.bid_list.append(self.bid)

    def bid_pop(self):
        self.bid_list.pop()

    def bid_status(self):
        lens = len(self.bid_list)
        return {'status': lens}
