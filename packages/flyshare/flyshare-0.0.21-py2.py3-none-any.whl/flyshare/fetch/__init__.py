# coding:utf-8
#

from . import wind as wind
from . import tushare as tushare
from . import tdx as tdx
from . import ths as ths


class Fetcher():
    """
    一个通用的数据获取方法类


    """

    def __init__(self, *args, **kwargs):
        pass

    @property
    def security_list(self):
        return self.security_list


def use(package):
    if package in ['wind']:
        from WindPy import w
        # w.start()
        return wind
    elif package in ['tushare', 'ts']:
        return tushare
    elif package in ['tdx', 'pytdx']:
        return tdx
    elif package in ['ths', 'THS']:
        return ths


def fetch_get_stock_day(package, code, startDate, endDate, if_fq='01', level='day', type_='json'):
    Engine = use(package)
    if package in ['ths', 'THS', 'wind']:
        return Engine.fetch_get_stock_day(code, startDate, endDate, if_fq)
    elif package in ['ts', 'tushare']:
        return Engine.fetch_get_stock_day(code, startDate, endDate, if_fq, type_)
    elif package in ['tdx', 'pytdx']:
        return Engine.fetch_get_stock_day(code, startDate, endDate, if_fq, level)
    else:
        return Engine.fetch_get_stock_day(code, startDate, endDate)


def fetch_get_stock_realtime(package, code):
    Engine = use(package)
    return Engine.fetch_get_stock_realtime(code)


def fetch_get_stock_indicator(package, code, startDate, endDate):
    Engine = use(package)
    return Engine.fetch_get_stock_indicator(code, startDate, endDate)


def fetch_get_trade_date(package, endDate, exchange):
    Engine = use(package)
    return Engine.fetch_get_trade_date(endDate, exchange)


def fetch_get_stock_min(package, code, start, end, level='1min'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.fetch_get_stock_min(code, start, end, level)
    else:
        return 'Unsupport packages'


def fetch_get_stock_list(package, type_='stock'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.fetch_get_stock_list(type_)
    else:
        return 'Unsupport packages'


def fetch_get_stock_transaction(package, code, start, end, retry=2):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.fetch_get_stock_transaction(code, start, end, retry)
    else:
        return 'Unsupport packages'


def fetch_get_stock_xdxr(package, code):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.fetch_get_stock_xdxr(code)
    else:
        return 'Unsupport packages'


def fetch_get_index_day(package, code, start, end, level='day'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.fetch_get_index_day(code, start, end, level)
    else:
        return 'Unsupport packages'


def fetch_get_index_min(package, code, start, end, level='1min'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.fetch_get_index_min(code, start, end, level)
    else:
        return 'Unsupport packages'


def fetch_get_stock_block(package):
    Engine = use(package)
    if package in ['tdx', 'pytdx', 'ths']:
        return Engine.fetch_get_stock_block()
    else:
        return 'Unsupport packages'


def fetch_get_stock_info(package, code):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.fetch_get_stock_info(code)
    else:
        return 'Unsupport packages'


def fetch_security_bars(code, _type, lens):
    return tdx.fetch_security_bars(code, _type, lens)
