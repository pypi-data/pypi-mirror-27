import datetime

from flyshare.fetch.tdx import (fetch_get_stock_day,
                                fetch_get_stock_min,
                                fetch_get_stock_transaction,
                                fetch_get_stock_xdxr)
from flyshare.fetch.tushare import fetch_get_stock_time_to_market
from flyshare.su.save_tdx import SU_save_stock_xdxr
from flyshare.util import (MongoDBSetting as ms,
                           log_info,
                           util_to_json_from_pandas,
                           trade_date_sse)

"""
该模块已经废弃

目前都在save_tdx中 增量更新

"""


def SU_update_stock_day(client=ms.client):
    def save_stock_day(code, start, end, coll):
        log_info('##JOB01 Now Updating STOCK_DAY==== %s' % (str(code)))
        data = util_to_json_from_pandas(
            fetch_get_stock_day(str(code), start, end, '00'))

        if len(data) > 0:
            coll.insert_many(data)
        else:
            pass
    coll_stock_day = client.flyshare.stock_day
    for item in fetch_get_stock_time_to_market().index:

        if coll_stock_day.find({'code': str(item)[0:6]}).count() > 0:
            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现

            start_date = str(coll_stock_day.find({'code': str(item)[0:6]})[
                coll_stock_day.find({'code': str(item)[0:6]}).count() - 1]['date'])
            print('*' * 20)
            end_date = str(now_time())[0:10]
            start_date = trade_date_sse[trade_date_sse.index(
                start_date) + 1]
            log_info(' UPDATE_STOCK_DAY \n Trying updating %s from %s to %s' %
                     (item, start_date, end_date))

            save_stock_day(item, start_date, end_date, coll_stock_day)

        else:
            save_stock_day(item, '1990-01-01',
                           str(now_time())[0:10], coll_stock_day)

    log_info('Done == \n')


def SU_update_stock_xdxr(client=ms.client):
    client.flyshare.drop_collection('stock_xdxr')
    SU_save_stock_xdxr()


def SU_update_stock_min(client=ms.client):
    """
    stock_min 分三个库 type区分
    1. 1min_level 库
    2. 5min_level 库
    3. 15min_level 库
    """

def SU_update_index_day(client=ms.client):
    pass


def SU_update_index_min(client=ms.client):
    pass


if __name__ == '__main__':
    SU_update_stock_day()
    # SU_update_stock_xdxr()
