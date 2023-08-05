# coding:utf-8
import pymongo

from motor.motor_asyncio import (AsyncIOMotorCollection, AsyncIOMotorClient, AsyncIOMotorDatabase,
                                 AsyncIOMotorCommandCursor)
from flyshare.util.log import log_info


def util_sql_mongo_setting(ip='127.0.0.1', port=27017):
    sql_mongo_client = pymongo.MongoClient(ip, int(port))
    log_info('ip1:{},port:{}'.format(str(ip), str(port)))
    return sql_mongo_client

# async


def util_sql_async_mongo_setting(ip='127.0.0.1', port=27017):
    sql_async_mongo_client = AsyncIOMotorClient(ip, int(port))
    log_info('ip2:{},port{}'.format(str(ip), str(port)))
    return sql_async_mongo_client