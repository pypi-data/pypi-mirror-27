# coding=utf-8
from flyshare.util import log_info, log_debug


class Backtest_Event_engine():
    def __init__(self, *args, **kwargs):
        pass


@classmethod
def sync_order_LM(cls, event_, order_=None, order_id_=None, trade_id_=None, market_message_=None):
    """
    订单事件: 生命周期管理 Order-Lifecycle-Management
    status1xx 订单待生成
    status3xx 初始化订单  临时扣除资产(可用现金/可卖股份)
    status3xx 订单存活(等待交易)
    status2xx 订单完全交易/未完全交易
    status4xx 主动撤单
    status500 订单死亡(每日结算) 恢复临时资产    
    =======
    1. 更新持仓
    2. 更新现金
    """
    if event_ is 'init_':

        cls.account.cash_available = cls.account.cash[-1]
        cls.account.sell_available = pd.DataFrame(cls.account.hold[1::], columns=cls.account.hold[0]).set_index(
            'code', drop=False)['amount'].groupby('code').sum()

    elif event_ is 'create_order':

        if order_ is not None:
            if order_.towards is 1:
                # 买入
                if cls.account.cash_available - order_.amount * order_.price > 0:
                    cls.account.cash_available -= order_.amount * order_.price
                    order_.status = 300  # 修改订单状态

                    cls.account.order_queue = cls.account.order_queue.append(
                        order_.to_df())
                else:
                    log_info('FROM ENGINE: NOT ENOUGH MONEY:CASH  %s Order %s' % (
                        cls.account.cash_available, order_.amount * order_.price))
            elif order_.towards is -1:

                if cls.backtest_sell_available(cls, order_.code) - order_.amount >= 0:
                    cls.account.sell_available[order_.code] -= order_.amount
                    cls.account.order_queue = cls.account.order_queue.append(
                        order_.to_df())

        else:
            log_info('Order Event Warning:%s in %s' %
                     (event_, str(cls.now)))

    elif event_ in ['wait', 'live']:
        # 订单存活 不会导致任何状态改变
        pass
    elif event_ in ['cancel_order']:  # 订单事件:主动撤单
        # try:
        assert isinstance(order_id_, str)
        cls.account.order_queue.loc[cls.account.order_queue['order_id']
                                     == order_id_, 'status'] = 400  # 注销事件
        if order_.towards is 1:
            # 多单 撤单  现金增加
            cls.account.cash_available += cls.account.order_queue.query('order_id=="order_id_"')[
                'amount'] * cls.account.order_queue.query('order_id=="order_id_"')['price']

        elif order_.towards is -1:
            # 空单撤单 可卖数量增加
            cls.account.sell_available[order_.code] += cls.account.order_queue.query(
                'order_id=="order_id_"')['price']
    elif event_ in ['daily_settle']:  # 每日结算/全撤/把成交的买入/卖出单标记为500 同时结转

        # 买入
        """
        每日结算流程
        - 同步实际的现金和仓位
        - 清空留仓单/未成功的订单
        """

        cls.account.cash_available = cls.account.cash[-1]
        cls.account.sell_available = pd.DataFrame(cls.account.hold[1::], columns=cls.account.hold[0]).set_index(
            'code', drop=False)['amount'].groupby('code').sum()

        cls.account.order_queue = pd.DataFrame()
    elif event_ in ['t_0']:
        """
        T+0交易事件

        同步t+0的账户状态 /允许卖出
        """
        cls.account.cash_available = cls.account.cash[-1]
        cls.account.sell_available = pd.DataFrame(cls.account.hold[1::], columns=cls.account.hold[0]).set_index(
            'code', drop=False)['amount'].groupby('code').sum()

    elif event_ in ['trade']:
        # try:
        assert isinstance(order_, QAMarket_bid)
        assert isinstance(order_id_, str)
        assert isinstance(trade_id_, str)
        assert isinstance(market_message_, dict)
        if order_.towards is 1:
            # 买入
            # 减少现金
            order_.trade_id = trade_id_
            order_.transact_time = cls.now
            order_.amount -= market_message_['body']['bid']['amount']

            if order_.amount == 0:  # 完全交易
                # 注销(成功交易)['买入单不能立即结转']
                cls.account.order_queue.loc[cls.account.order_queue['order_id']
                                             == order_id_, 'status'] = 200

            elif order_.amount > 0:
                # 注销(成功交易)
                cls.account.order_queue.loc[cls.account.order_queue['order_id']
                                             == order_id_, 'status'] = 203
                cls.account.order_queue.query('order_id=="order_id_"')[
                    'amount'] -= market_message_['body']['bid']['amount']
        elif order_.towards is -1:
            # cls.account.sell_available[order_.code] -= market_message_[
            #    'body']['bid']['amount']
            # 当日卖出的股票 可以继续买入/ 可用资金增加(要减去手续费)
            cls.account.cash_available += market_message_['body']['bid']['amount'] * market_message_[
                'body']['bid']['price'] - market_message_['body']['fee']['commission']
            order_.trade_id = trade_id_
            order_.transact_time = cls.now
            order_.amount -= market_message_['body']['bid']['amount']
            if order_.amount == 0:
                # 注销(成功交易)
                cls.account.order_queue.loc[cls.account.order_queue['order_id']
                                             == order_id_, 'status'] = 200
            else:
                # 注销(成功交易)
                cls.account.order_queue.loc[cls.account.order_queue['order_id']
                                             == order_id_, 'status'] = 203
                cls.account.order_queue[cls.account.order_queue['order_id'] ==
                                         order_id_]['amount'] -= market_message_['body']['bid']['amount']
    else:
        log_info(
            'EventEngine Warning: Unknown type of order event in  %s' % str(cls.now))
