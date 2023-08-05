# coding:utf-8


from flyshare.backtest import analysis
from flyshare.util import log_exception, log_info
import math
import numpy
import pandas
"""收益性的包括年化收益率、净利润、总盈利、总亏损、有效年化收益率、资金使用率。

风险性主要包括胜率、平均盈亏比、最大回撤比例、最大连续亏损次数、最大连续盈利次数、持仓时间占比、贝塔。

综合性指标主要包括风险收益比，夏普比例，波动率，VAR，偏度，峰度等"""

"""
the account datastruct should be a standard struct which can be directly sended to another function
"""


def risk_eva_account(message, days, client):
    cookie = message['header']['cookie']
    account = message['body']['account']
    # 绩效表现指标分析
    """ 
    message= {
            'annualized_returns':annualized_returns,
            'benchmark_annualized_returns':benchmark_annualized_returns,
            'benchmark_Assets':benchmark_Assets,
            'vol':volatility_year,
            'benchmark_vol':benchmark_volatility_year,
            'sharpe':sharpe,
            'alpha':alpha,
            'beta':beta,
            'max_drop':max_drop,
            'win_rate':win_rate}
    """
    try:
        # 1.可用资金占当前总资产比重
        risk_account_freeCash_currentAssets = risk_account_freeCash_currentAssets(float(account['Assets_free']), float(account['Assets_now']))
        # 2.当前策略速动比率(流动资产/流动负债)
        risk_account_freeCash_initAssets = risk_account_freeCash_initAssets(account['Assets_free'], account['init_Assets'])
        risk_account_freeCash_frozenAssets = risk_account_freeCash_frozenAssets(float(account['Assets_free']), float(account['Assets_fix']))

        return {""}

    except:
        log_expection('error in risk evaluation')


def risk_account_freeCash_initAssets(freeCash, initAssets):
    try:
        result = float(freeCash) / float(initAssets)
        return result
    except:
        return 0
        log_expection('error in risk_account_freeCash_initAssets')
        log_expection('freeCash: ' + str(freeCash))
        log_expection('currentAssets: ' + str(initAssets))
        log_expection('expected result: ' +
                      str(float(freeCash) / float(initAssets)))


def risk_account_freeCash_currentAssets(freeCash, currentAssets):
    try:
        result = float(freeCash) / float(currentAssets)
        return result
    except:
        return 0
        log_expection(
            'error in risk_account_freeCash_currentAssets')
        log_expection('freeCash: ' + str(freeCash))
        log_expection('currentAssets: ' + str(currentAssets))
        log_expection('expected result: ' +
                      str(float(freeCash) / float(currentAssets)))


def risk_account_freeCash_frozenAssets(freeCash, frozenAssets):
    try:
        result = float(freeCash) / float(frozenAssets)
        return result
    except:
        return 0
        log_expection('error in risk_account_freeCash_frozenAssets')
        log_expection('freeCash: ' + str(freeCash))
        log_expection('currentAssets: ' + str(frozenAssets))
        log_expection('expected result: ' +
                      str(float(freeCash) / float(frozenAssets)))


def risk_calc_assets(trade_history, assets):
    assets_d = []
    trade_date = []
    for i in range(0, len(trade_history), 1):
        if trade_history[i][0] not in trade_date:
            trade_date.append(trade_history[i][0])
            assets_d.append(assets[i])
        else:
            assets_d.pop(-1)
            assets_d.append(assets[i])

    return assets_d


def risk_result_check(datelist, message):
    pass


def risk_calc_benchmark(benchmark_data, init_assets):

    return list(benchmark_data['close'] / float(benchmark_data['open'][0]) * float(init_assets))


def risk_calc_alpha(annualized_returns, benchmark_annualized_returns, beta, r):

    alpha = (annualized_returns - r) - (beta) * \
        (benchmark_annualized_returns - r)
    return alpha


def risk_calc_beta(Assets_profit, benchmark_profit):
    if len(Assets_profit) < len(benchmark_profit):
        for i in range(0, len(benchmark_profit) - len(Assets_profit), 1):
            Assets_profit.append(0)
    elif len(Assets_profit) > len(benchmark_profit):
        for i in range(0, len(Assets_profit) - len(benchmark_profit), 1):
            benchmark_profit.append(0)
    calc_cov = numpy.cov(Assets_profit, benchmark_profit)
    beta = calc_cov[0, 1] / calc_cov[1, 1]
    return beta


def risk_calc_profit(Assets_history):
    return (Assets_history[-1] / Assets_history[1]) - 1


def risk_calc_profit_per_year(Assets_history, days):
    return math.pow(float(Assets_history[-1]) / float(Assets_history[0]), 250.0 / float(days)) - 1.0


def risk_calc_profit_matrix(Assets_history):
    Assets_profit = []
    if len(Assets_history) > 1:
        Assets_profit = [Assets_history[i + 1] / Assets_history[i] -
                         1.0 for i in range(len(Assets_history) - 1)]
    return Assets_profit


def risk_calc_volatility(Assets_profit_matrix):
    # 策略每日收益的年化标准差
    Assets_profit = Assets_profit_matrix

    volatility_day = numpy.std(Assets_profit)
    volatility_year = volatility_day * math.sqrt(250)
    return volatility_year


def risk_calc_dropback_max(history):
    drops = []
    for i in range(1, len(history), 1):
        maxs = max(history[:i])
        cur = history[i - 1]
        drop = 1 - cur / maxs
        drops.append(drop)
    max_drop = max(drops)
    return max_drop


def risk_calc_sharpe(annualized_returns, r, volatility_year):
    '计算夏普比率'
    return (annualized_returns - r) / volatility_year


def risk_calc_trade_date(history):
    '计算交易日期'
    trade_date = []

    # trade_date_sse.index(history[-1][0])-trade_date_sse.index(history[0][0])
    for i in range(0, len(history), 1):
        if history[i][0] not in trade_date:
            trade_date.append(history[i][0])
    return trade_date


def risk_calc_trade_time_profit():
    pass


def risk_calc_trade_time_loss():
    pass


def risk_calc_win_rate(profit_day):
    # 大于0的次数
    abovez = 0
    belowz = 0
    for i in range(0, len(profit_day) - 1, 1):
        if profit_day[i] > 0:
            abovez = abovez + 1
        elif profit_day[i] < 0:
            belowz = belowz + 1
    if belowz == 0:
        belowz = 1
    if abovez == 0:
        abovez = 1
    win_rate = abovez / (abovez + belowz)
    return win_rate


class Risk():
    pass
