# coding:utf-8

import json
import pandas as pd
import numpy as np
import csv


def util_to_json_from_pandas(data):
    return json.loads(data.to_json(orient='records'))


def util_to_json_from_numpy(data):
    pass


def util_to_json_from_list(data):
    pass


def util_to_list_from_pandas(data):
    return np.asarray(data).tolist()


def util_to_list_from_numpy(data):
    return data.tolist()
