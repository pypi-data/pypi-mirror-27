# coding:utf-8

import threading

from flyshare.util import (util_date_stamp, util_date_valid,
                           log_info)

from .account import Account
from .risk import Risk


class Portfolio():

    """
    在portfolio中,我们希望通过cookie来控制account_unit
    对于account的指标,要进行风险控制,组合成最优的投资组合的量

    portfolio通过每天结束的时候,计算总账户可用资金,来更新和计算总账户资金占比情况

    """

    def init(self):
        self.portfolio_code = ['']
        self.portfolio_account = []
        for i in range(0, len(self.portfolio_code) - 1, 1):
            self.portfolio_account[i] = Account()

    def portfolio_get_portfolio(self):
        # util_log_info(self.portfolio_account)
        return self.portfolio_account

    def portfolio_calc(self):

        pass

    def cookie_mangement(self):
        pass

    def portfolio_get_free_cash(self):
        pass
