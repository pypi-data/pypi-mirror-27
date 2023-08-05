# coding:utf-8

import numpy as np
import pandas as pd
import requests
from lxml import etree
from flyshare.util import trade_date_sse


def fetch_get_stock_day_in_year(code, year, if_fq='00'):
    data_ = []
    url = 'http://d.10jqka.com.cn/v2/line/hs_%s/%s/%s.js' % (
        str(code), str(if_fq), str(year))
    try:
        for item in requests.get(url).text.split('\"')[3].split(';'):
            data_.append(item.split(','))

        data = pd.DataFrame(data_, index=list(np.asarray(data_).T[0]), columns=[
                            'date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'factor'])
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        return data
    except:
        pass


def fetch_get_stock_day(code, start, end, if_fq='00'):
    start_year = int(str(start)[0:4])
    end_year = int(str(end)[0:4])
    data = fetch_get_stock_day_in_year(code, start_year, if_fq)
    if start_year < end_year:
        for i_ in range(start_year + 1, end_year + 1):
            data = pd.concat(
                [data, fetch_get_stock_day_in_year(code, i_, if_fq)], axis=0)
    else:
        pass
    if data is None:
        return pd.DataFrame()
    else:
        return data[start:end]


def fetch_get_stock_block():
    url_list = ['gn', 'dy', 'thshy', 'zjhhy']  # 概念/地域/同花顺板块/证监会板块
    data = []
    for item in url_list:
        tree = etree.HTML(requests.get(
            'http://q.10jqka.com.cn/{}/'.format(item)).text)
        gn = tree.xpath('/html/body/div/div/div/div/div/a/text()')
        gpath = tree.xpath('/html/body/div/div/div/div/div/a/@href')
        for _i in range(len(gn)):
            for i in range(1, 15):
                _data = etree.HTML(requests.get(
                    'http://q.10jqka.com.cn/{}/detail/order/desc/page/{}/ajax/1/code/{}'.format(item, i, gpath[_i].split('/')[-2])).text)
                name = _data.xpath('/html/body/table/tbody/tr/td[3]/a/text()')
                code = _data.xpath('/html/body/table/tbody/tr/td[3]/a/@href')
                for i_ in range(len(name)):
                    print('Now Crawling-{}-{}-{}-{}'.format(gn[_i], code[i_].split('/')[-1], item, 'ths'))
                    data.append([gn[_i], code[i_].split('/')[-1], item, 'ths'])

    return pd.DataFrame(data, columns=['blockname',  'code', 'type', 'source']).set_index('code', drop=False)


if __name__ == '__main__':
    # print(get_k_data_year('000001','2016','01'))
    # print(get_k_data_year(600010,2016,'01'))
    print(fetch_get_stock_day('000001', '2016-05-01', '2017-07-01', '01'))
