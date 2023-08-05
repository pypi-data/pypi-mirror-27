# coding=utf-8

import subprocess

import pandas as pd
import pymongo
from flyshare.util import MongoDBSetting, log_info


def util_mongo_initial(db=MongoDBSetting.client.quantaxis):

    db.drop_collection('stock_day')
    db.drop_collection('stock_list')
    db.drop_collection('stock_info')
    db.drop_collection('trade_date')
    db.drop_collection('stock_min')
    db.drop_collection('stock_transaction')
    db.drop_collection('stock_xdxr')


def util_mongo_make_index(db=MongoDBSetting.client.quantaxis):
    try:
        db.stock_day.ensure_index('code')
        db.stock_min_five.ensure_index('code')
    except:
        pass


def util_mongo_status(db=MongoDBSetting.client.quantaxis):
    log_info(db.collection_names())
    log_info(db.last_status())
    log_info(subprocess.call('mongostat', shell=True))


def util_mongo_infos(db=MongoDBSetting.client.quantaxis):

    data_struct = []

    for item in db.collection_names():
        value = []
        value.append(item)
        value.append(eval('db.' + str(item) + '.find({}).count()'))
        value.append(list(eval('db.' + str(item) + '.find_one()').keys()))
        data_struct.append(value)
    return pd.DataFrame(data_struct, columns=['collection_name', 'counts', 'columns']).set_index('collection_name')


if __name__ == '__main__':
    print(util_mongo_infos())
    util_mongo_status()
