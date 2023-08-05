import time
import datetime

def date_stamp(date):
    datestr = str(date)[0:10]
    date = time.mktime(time.strptime(datestr, '%Y-%m-%d'))
    return date

def now():
    return datetime.datetime.now()

def today():
    return datetime.datetime.today()

def get_date_today():
    return datetime.date.today().strftime("%Y-%m-%d")

def validate_date(date):
    try:
        time.strptime(date, '%Y-%m-%d')
        return True
    except:
        return False

def is_today(date):
    if validate_date(date):
        if str(today().date()) == date:
            return True
        else:
            return False
    else:
        return False

def util_time_now():
    return datetime.datetime.now()


def util_date_today():
    return datetime.date.today()


def util_date_str2int(date):
    return int(str(date)[0:4] + str(date)[5:7] + str(date)[8:10])


def util_date_int2str(date):
    return str(str(date)[0:4] + '-' + str(date)[4:6] + '-' + str(date)[6:8])


def util_date_stamp(date):
    datestr = str(date)[0:10]
    date = time.mktime(time.strptime(datestr, '%Y-%m-%d'))
    return date


def util_time_stamp(time_):
    '''
    数据格式最好是%Y-%m-%d %H:%M:%S 中间要有空格
    '''
    if len(str(time_)) == 10:
        # yyyy-mm-dd格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d'))
    elif len(str(time_)) == 16:
            # yyyy-mm-dd hh:mm格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d %H:%M'))
    else:
        timestr = str(time_)[0:19]
        return time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))


def util_ms_stamp(ms):
    return ms


def util_date_valid(date):
    try:

        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def util_realtime(strtime, client):
    time_stamp = util_date_stamp(strtime)
    coll = client.flyshare.trade_date
    temp_str = coll.find_one({'date_stamp': {"$gte": time_stamp}})
    time_real = temp_str['date']
    time_id = temp_str['num']
    return {'time_real': time_real, 'id': time_id}


def util_id2date(id, client):
    coll = client.flyshare.trade_date
    temp_str = coll.find_one({'num': id})
    return temp_str['date']


def util_is_trade(date, code, client):
    coll = client.flyshare.stock_day
    date = str(date)[0:10]
    is_trade = coll.find_one({'code': code, 'date': date})
    try:
        len(is_trade)
        return True
    except:
        return False


def util_get_date_index(date, trade_list):
    return trade_list.index(date)


def util_get_index_date(id, trade_list):
    return trade_list[id]


def util_select_hours(time=None, gt=None, lt=None, gte=None, lte=None):
    '时间选择函数,约定时间的范围,比如早上9点到11点'
    if time is None:
        __realtime = datetime.datetime.now()
    else:
        __realtime = time

    fun_list = []
    if gt != None:
        fun_list.append('>')
    if lt != None:
        fun_list.append('<')
    if gte != None:
        fun_list.append('>=')
    if lte != None:
        fun_list.append('<=')

    assert len(fun_list) > 0
    true_list = []
    try:
        for item in fun_list:
            if item == '>':
                if __realtime.strftime('%H') > gt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<':
                if __realtime.strftime('%H') < lt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '>=':
                if __realtime.strftime('%H') >= gte:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<=':
                if __realtime.strftime('%H') <= lte:
                    true_list.append(0)
                else:
                    true_list.append(1)

    except:
        return Exception
    if sum(true_list) > 0:
        return False
    else:
        return True


def util_select_min(time=None, gt=None, lt=None, gte=None, lte=None):
    'quantaxis的时间选择函数,约定时间的范围,比如30分到59分'
    if time is None:
        __realtime = datetime.datetime.now()
    else:
        __realtime = time

    fun_list = []
    if gt != None:
        fun_list.append('>')
    if lt != None:
        fun_list.append('<')
    if gte != None:
        fun_list.append('>=')
    if lte != None:
        fun_list.append('<=')

    assert len(fun_list) > 0
    true_list = []
    try:
        for item in fun_list:
            if item == '>':
                if __realtime.strftime('%M') > gt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<':
                if __realtime.strftime('%M') < lt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '>=':
                if __realtime.strftime('%M') >= gte:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<=':
                if __realtime.strftime('%M') <= lte:
                    true_list.append(0)
                else:
                    true_list.append(1)

    except:
        return Exception
    if sum(true_list) > 0:
        return False
    else:
        return True


def util_time_delay(time_=0):
    '这是一个用于复用/比如说@装饰器的延时函数\
    使用threading里面的延时,为了是不阻塞进程\
    有时候,同时发进去两个函数,第一个函数需要延时\
    第二个不需要的话,用sleep就会阻塞掉第二个进程'
    def _exec(func):
        threading.Timer(time_, func)
    return _exec


def util_calc_time(func, *args, **kwargs):
    '耗时长度的装饰器'
    _time = datetime.datetime.now()
    func(*args, **kwargs)
    print(datetime.datetime.now() - _time)
    #return datetime.datetime.now() - _time


if __name__ == '__main__':
    print(util_time_stamp('2017-01-01 10:25:08'))
