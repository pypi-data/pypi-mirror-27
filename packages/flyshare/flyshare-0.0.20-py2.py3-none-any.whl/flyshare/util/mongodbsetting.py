# coding:utf-8

from flyshare.su.user import user_sign_in, user_sign_up
from flyshare.util import log_info
import flyshare.ApiConfig as ac
import pymongo

def get_mongo_client(ip='127.0.0.1', port=27017):
    sql_mongo_client = pymongo.MongoClient(ip, int(port))
    # log_info('ip3:{},port:{}'.format(str(ip), str(port)))
    return sql_mongo_client


class MongoDBSetting():

    mongo_ip = ac.MONGODB_IP
    mongo_port = ac.MONGODB_PORT
    client = get_mongo_client(mongo_ip, mongo_port)

    setting_user_name = ''
    setting_user_password = ''
    user = {'username': '', 'password': '', 'login': False}

    def init_mongodb(self, ip='127.0.0.1', port=27017):
        self.mongo_ip = ip
        self.mongo_port = port
        self.client = get_mongo_client(self.mongo_ip, self.mongo_port)

        # return self
        self.user = self.setting_login()

    def set_ip(self, ip='127.0.0.1'):
        self.mongo_ip = ip
        self.client = get_mongo_client(self.mongo_ip, self.mongo_port)
        return self

    def setting_login(self):
        self.username = self.setting_user_name
        self.password = self.setting_user_password
        log_info('username:' + str(self.setting_user_name))
        result = user_sign_in(self.username, self.password, self.client)
        if result == True:
            self.user['username'] = self.username
            self.user['password'] = self.password
            self.user['login'] = True
            return self.user
        else:
            log_info('failed to login')


info_ip_list = ['101.227.73.20',
                '101.227.77.254',
                '114.80.63.12',
                '114.80.63.35',
                '115.238.56.198',
                '115.238.90.165',
                '124.160.88.183',
                '14.17.75.71',
                '14.215.128.18',
                '180.153.18.170',
                '180.153.18.171',
                '180.153.18.172',
                '180.153.39.51',
                '202.108.253.130',
                '202.108.253.131',
                '202.108.253.139',
                '218.108.47.69',
                '218.108.98.244',
                '218.57.11.101',
                '218.75.126.9',
                '221.231.141.60',
                '223.94.89.115',
                '58.58.33.123',
                '59.173.18.140',
                '60.12.136.250',
                '60.191.117.167',
                '60.28.23.80']
