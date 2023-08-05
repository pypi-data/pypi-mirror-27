# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/flyshare
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
from pytdx.reader import TdxMinBarReader
from flyshare.util import MongoDBSetting as ms, log_info, util_time_stamp, util_date_stamp


def save_tdx_to_mongo(file_dir, client=ms.client):
    reader = TdxMinBarReader()
    __coll = client.flyshares.stock_min_five
    for a, v, files in os.walk(file_dir):
        for file in files:
            if (str(file)[0:2] == 'sh' and int(str(file)[2]) == 6) or \
                (str(file)[0:2] == 'sz' and int(str(file)[2]) == 0) or \
                    (str(file)[0:2] == 'sz' and int(str(file)[2]) == 3):

                log_info('Now_saving ' + str(file)
                                 [2:8] + '\'s 5 min tick')
                fname = file_dir + '\\' + file
                df = reader.get_df(fname)
                df['code'] = str(file)[2:8]
                df['market'] = str(file)[0:2]
                df['datetime'] = [str(x) for x in list(df.index)]
                df['date'] = [str(x)[0:10] for x in list(df.index)]
                df['time_stamp'] = df['datetime'].apply(
                    lambda x: util_time_stamp(x))
                df['date_stamp'] = df['date'].apply(
                    lambda x: util_date_stamp(x))
                data_json = json.loads(df.to_json(orient='records'))
                __coll.insert_many(data_json)


if __name__ == '__main__':
    file_dir = ['/tdx',
                '/tdx2']
    for item in file_dir:
        save_tdx_to_mongo(item)
