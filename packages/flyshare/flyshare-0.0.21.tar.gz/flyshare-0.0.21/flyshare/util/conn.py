#coding=utf-8

from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API
from flyshare.util import vars,ping
import flyshare.ApiConfig as ac

def api(retry_count=3):
    for _ in range(retry_count):
        try:
            api = TdxHq_API(heartbeat=True)
            api.connect(_get_server(), vars.T_PORT)
        except Exception as e:
            print(e)
        else:
            return api
    raise IOError(vars.NETWORK_URL_ERROR_MSG)


def xapi(retry_count=3):
    for _ in range(retry_count):
        try:
            api = TdxExHq_API(heartbeat=True)
            api.connect(_get_xserver(), vars.X_PORT)
        except Exception as e:
            print(e)
        else:
            return api
    raise IOError(vars.NETWORK_URL_ERROR_MSG)


def xapi_x(retry_count=3):
    for _ in range(retry_count):
        try:
            api = TdxExHq_API(heartbeat=True)
            api.connect(_get_xxserver(), vars.X_PORT)
        except Exception as e:
            print(e)
        else:
            return api
    raise IOError(vars.NETWORK_URL_ERROR_MSG)


def get_apis():
    return api(), xapi()


def close_apis():
    print(ac.TDX_CONN)
    api, xapi = ac.TDX_CONN
    try:
        api.disconnect()
        xapi.disconnect()
    except Exception as e:
        print(e)


def _get_server():
    # if ac.TDX_BEST_IP is not None:
    #     return ac.TDX_BEST_IP
    # else:
    #     conn_times = [ping(x) for x in vars.SLIST]
    #     best_ip = vars.SLIST[conn_times.index(min(conn_times))]
    #     ac.TDX_BEST_IP = best_ip
    #     return best_ip
    import random
    ips = vars.SLIST
    random.shuffle(ips)
    return ips[0]

def _get_xserver():
    import random
    ips = vars.XLIST
    random.shuffle(ips)
    return ips[0]

def _get_xxserver():
    import random
    ips = vars.XXLIST
    random.shuffle(ips)
    return ips[0]