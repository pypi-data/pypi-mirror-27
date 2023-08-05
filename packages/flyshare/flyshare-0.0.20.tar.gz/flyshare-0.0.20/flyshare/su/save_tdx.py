# coding:utf-8

import concurrent
import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import pymongo

from flyshare.fetch import fetch_get_stock_block
from flyshare.fetch.tdx import (fetch_get_index_day,
                                fetch_get_index_min,
                                fetch_get_stock_day,
                                fetch_get_stock_info,
                                fetch_get_stock_list,
                                fetch_get_stock_min,
                                fetch_get_stock_transaction,
                                fetch_get_stock_xdxr, select_best_ip)
from flyshare.fetch.tushare import fetch_get_stock_time_to_market
from flyshare.util import (MongoDBSetting as ms, util_get_real_date,
                           log_info, util_to_json_from_pandas,
                           trade_date_sse)

# ip=select_best_ip()


def now_time():
    return str(util_get_real_date(str(datetime.date.today() - datetime.timedelta(days=1)), trade_date_sse, -1)) + ' 15:00:00' if datetime.datetime.now().hour < 15 else str(util_get_real_date(str(datetime.date.today()), trade_date_sse, -1)) + ' 15:00:00'


def SU_save_stock_day(client=ms.client):
    __stock_list = fetch_get_stock_time_to_market()
    coll_stock_day = client.flyshares.stock_day
    coll_stock_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    __err = []

    def __saving_work(code, coll_stock_day):
        try:
            log_info(
                '##JOB01 Now Saving STOCK_DAY==== %s' % (str(code)))

            ref = coll_stock_day.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]
            if ref.count() > 0:
                    # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现

                start_date = ref[ref.count() - 1]['date']
            else:
                start_date = '1990-01-01'
            log_info(' UPDATE_STOCK_DAY \n Trying updating %s from %s to %s' %
                     (code, start_date, end_date))
            if start_date != end_date:
                coll_stock_day.insert_many(
                    util_to_json_from_pandas(
                        fetch_get_stock_day(str(code), start_date, end_date, '00')[1::]))
        except:
            __err.append(str(code))
    for item in range(len(__stock_list)):
        log_info('The %s of Total %s' %
                 (item, len(__stock_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(item / len(__stock_list) * 100))[0:4] + '%')

        __saving_work(__stock_list.index[item], coll_stock_day)
    log_info('ERROR CODE \n ')
    log_info(__err)


def SU_save_stock_xdxr(client=ms.client):
    client.flyshares.drop_collection('stock_xdxr')
    __stock_list = fetch_get_stock_time_to_market()
    __coll = client.flyshares.stock_xdxr
    __coll.create_index([('code', pymongo.ASCENDING),
                         ('date', pymongo.ASCENDING)])
    __err = []

    def __saving_work(code, __coll):
        log_info('##JOB02 Now Saving XDXR INFO ==== %s' % (str(code)))
        try:
            __coll.insert_many(
                util_to_json_from_pandas(
                    fetch_get_stock_xdxr(str(code))))

        except:
            __err.append(str(code))
    for i_ in range(len(__stock_list)):
        #__saving_work('000001')
        log_info('The %s of Total %s' % (i_, len(__stock_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__stock_list) * 100))[0:4] + '%')
        __saving_work(__stock_list.index[i_], __coll)
    log_info('ERROR CODE \n ')
    log_info(__err)


def SU_save_stock_min(client=ms.client):
    __stock_list = fetch_get_stock_time_to_market()
    __coll = client.flyshares.stock_min
    __coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                       pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    __err = []

    def __saving_work(code, __coll):
        log_info('##JOB03 Now Saving STOCK_MIN ==== %s' % (str(code)))
        try:
            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = __coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']
                else:
                    start_time = '2015-01-01'
                log_info(
                    '##JOB03.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                if start_time != end_time:
                    __data = fetch_get_stock_min(
                        str(code), start_time, end_time, type)
                    if len(__data) > 1:
                        __coll.insert_many(
                            util_to_json_from_pandas(__data[1::]))

        except Exception as e:
            log_info(e)

            __err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)
    #executor.map((__saving_work, __stock_list.index[i_], __coll),URLS)
    res = {executor.submit(
        __saving_work, __stock_list.index[i_], __coll) for i_ in range(len(__stock_list))}
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        log_info('The %s of Total %s' % (count, len(__stock_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(__stock_list) * 100))[0:4] + '%')
        count = count + 1
    log_info('ERROR CODE \n ')
    log_info(__err)


def SU_save_index_day(client=ms.client):
    __index_list = fetch_get_stock_list('index')
    __coll = client.flyshares.index_day
    __coll.create_index([('code', pymongo.ASCENDING),
                         ('date_stamp', pymongo.ASCENDING)])
    __err = []

    def __saving_work(code, __coll):

        try:

            ref_ = __coll.find({'code': str(code)[0:6]})
            end_time = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']
            else:
                start_time = '1990-01-01'

            log_info('##JOB04 Now Saving INDEX_DAY==== \n Trying updating %s from %s to %s' %
                     (code, start_time, end_time))

            if start_time != end_time:
                __coll.insert_many(
                    util_to_json_from_pandas(
                        fetch_get_index_day(str(code), start_time, end_time)[1::]))
        except:
            __err.append(str(code))
    for i_ in range(len(__index_list)):
        #__saving_work('000001')
        log_info('The %s of Total %s' % (i_, len(__index_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__index_list) * 100))[0:4] + '%')
        __saving_work(__index_list.index[i_][0], __coll)
    log_info('ERROR CODE \n ')
    log_info(__err)


def SU_save_index_min(client=ms.client):
    __index_list = fetch_get_stock_list('index')
    __coll = client.flyshares.index_min
    __coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                       pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    __err = []

    def __saving_work(code, __coll):

        log_info('##JOB05 Now Saving Index_MIN ==== %s' % (str(code)))
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = __coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']
                else:
                    start_time = '2015-01-01'
                log_info(
                    '##JOB05.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                if start_time != end_time:
                    __data = fetch_get_index_min(
                        str(code), start_time, end_time, type)
                    if len(__data) > 1:
                        __coll.insert_many(
                            util_to_json_from_pandas(__data[1::]))

        except:
            __err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __index_list.index[i_][0], __coll) for i_ in range(len(__index_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        log_info('The %s of Total %s' % (count, len(__index_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(__index_list) * 100))[0:4] + '%')
        count = count + 1
    log_info('ERROR CODE \n ')
    log_info(__err)


def SU_save_etf_day(client=ms.client):
    __index_list = fetch_get_stock_list('etf')
    __coll = client.flyshares.index_day
    __coll.create_index([('code', pymongo.ASCENDING),
                         ('date_stamp', pymongo.ASCENDING)])
    __err = []

    def __saving_work(code, __coll):

        try:

            ref_ = __coll.find({'code': str(code)[0:6]})
            end_time = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']
            else:
                start_time = '1990-01-01'

            log_info('##JOB06 Now Saving ETF_DAY==== \n Trying updating %s from %s to %s' %
                     (code, start_time, end_time))

            if start_time != end_time:
                __coll.insert_many(
                    util_to_json_from_pandas(
                        fetch_get_index_day(str(code), start_time, end_time)[1::]))
        except:
            __err.append(str(code))
    for i_ in range(len(__index_list)):
        #__saving_work('000001')
        log_info('The %s of Total %s' % (i_, len(__index_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__index_list) * 100))[0:4] + '%')
        __saving_work(__index_list.index[i_][0], __coll)
    log_info('ERROR CODE \n ')
    log_info(__err)


def SU_save_etf_min(client=ms.client):
    __index_list = fetch_get_stock_list('etf')
    __coll = client.flyshares.index_min
    __coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                       pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    __err = []

    def __saving_work(code, __coll):

        log_info('##JOB07 Now Saving ETF_MIN ==== %s' % (str(code)))
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = __coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']
                else:
                    start_time = '2015-01-01'
                log_info(
                    '##JOB07.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                if start_time != end_time:
                    __data = fetch_get_index_min(
                        str(code), start_time, end_time, type)
                    if len(__data) > 1:
                        __coll.insert_many(
                            util_to_json_from_pandas(__data[1::]))

        except:
            __err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __index_list.index[i_][0], __coll) for i_ in range(len(__index_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        log_info('The %s of Total %s' % (count, len(__index_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(__index_list) * 100))[0:4] + '%')
        count = count + 1
    log_info('ERROR CODE \n ')
    log_info(__err)


def SU_save_stock_list(client=ms.client):
    client.flyshares.drop_collection('stock_list')
    __coll = client.flyshares.stock_list
    __coll.create_index('code')
    __err = []

    try:
        log_info('##JOB08 Now Saving STOCK_LIST ====')
        __coll.insert_many(util_to_json_from_pandas(
            fetch_get_stock_list()))
    except:
        pass


def SU_save_stock_block(client=ms.client):
    client.flyshares.drop_collection('stock_block')
    __coll = client.flyshares.stock_block
    __coll.create_index('code')
    __err = []
    try:
        log_info('##JOB09 Now Saving STOCK_BlOCK ====')
        __coll.insert_many(util_to_json_from_pandas(
            fetch_get_stock_block('tdx')))
        __coll.insert_many(util_to_json_from_pandas(
            fetch_get_stock_block('ths')))
    except:
        pass
def SU_save_stock_info(client=ms.client):
    client.flyshares.drop_collection('stock_info')
    __stock_list = fetch_get_stock_time_to_market()
    __coll = client.flyshares.stock_info
    __coll.create_index('code')
    __err = []

    def __saving_work(code, __coll):
        log_info('##JOB010 Now Saving STOCK INFO ==== %s' % (str(code)))
        try:
            __coll.insert_many(
                util_to_json_from_pandas(
                    fetch_get_stock_info(str(code))))

        except:
            __err.append(str(code))
    for i_ in range(len(__stock_list)):
        #__saving_work('000001')
        log_info('The %s of Total %s' % (i_, len(__stock_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__stock_list) * 100))[0:4] + '%')
        __saving_work(__stock_list.index[i_], __coll)
    log_info('ERROR CODE \n ')
    log_info(__err)


def SU_save_stock_transaction(client=ms.client):
    __stock_list = fetch_get_stock_time_to_market()
    __coll = client.flyshares.stock_transaction
    __coll.create_index('code', pymongo.ASCENDING)
    __err = []

    def __saving_work(code):
        log_info(
            '##JOB10 Now Saving STOCK_TRANSACTION ==== %s' % (str(code)))
        try:
            __coll.insert_many(
                util_to_json_from_pandas(
                    fetch_get_stock_transaction(str(code), str(__stock_list[code]), str(now_time())[0:10])))
        except:
            __err.append(str(code))
    for i_ in range(len(__stock_list)):
        #__saving_work('000001')
        log_info('The %s of Total %s' % (i_, len(__stock_list)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__stock_list) * 100))[0:4] + '%')
        __saving_work(__stock_list.index[i_])
    log_info('ERROR CODE \n ')
    log_info(__err)


if __name__ == '__main__':
    # SU_save_stock_day()
    # SU_save_stock_xdxr()
    # SU_save_stock_min()
    # SU_save_stock_transaction()
    # SU_save_index_day()
    # SU_save_stock_list()
    # SU_save_index_min()
    pass
