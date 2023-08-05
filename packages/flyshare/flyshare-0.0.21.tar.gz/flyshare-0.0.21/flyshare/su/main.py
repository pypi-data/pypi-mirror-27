
from flyshare.su import save_tdx as stdx
from flyshare.su import save_tdx_file as tdx_file
from flyshare.su import save_tushare as sts
from flyshare.su import save_wind as sw
from flyshare.su import update_tdx as utdx
from flyshare.su import update_tushare as uts
from flyshare.su import update_wind as uw
from flyshare.util import MongoDBSetting as ms


def save_trade_date(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_trade_date(client)


def save_stock_info(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_stock_info(client)


def save_stock_list(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_stock_list(client)


def save_stock_day(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_stock_day(client)


def save_stock_min(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_stock_min(client)


def save_index_day(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_index_day(client)


def save_index_min(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_index_min(client)


def save_etf_day(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_etf_day(client)


def save_etf_min(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_etf_min(client)


def save_stock_xdxr(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_stock_xdxr(client)

def save_stock_block(engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_stock_block(client)
def save_stock_day_init(startDate, engine, client=ms.client):
    engine = select_save_engine(engine)
    engine.save_stock_day_init(startDate, client)


def update_stock_day(engine, client=ms.client):
    engine = select_update_engine(engine)
    engine.update_stock_day(client)


def update_stock_xdxr(engine, client=ms.client):
    engine = select_update_engine(engine)
    engine.update_stock_xdxr(client)


def update_stock_min(engine, client=ms.client):
    engine = select_update_engine(engine)
    engine.update_stock_min(client)



def update_index_day(engine, client=ms.client):
    engine = select_update_engine(engine)
    engine.update_index_day(client)


def update_index_min(engine, client=ms.client):
    engine = select_update_engine(engine)
    engine.update_index_min(client)


def select_save_engine(engine):
    if engine in ['wind', 'Wind', 'WIND']:
        return sw
    elif engine in ['tushare', 'ts', 'Tushare']:
        return sts
    elif engine in ['tdx']:
        return stdx


def select_update_engine(engine):
    if engine in ['wind', 'Wind', 'WIND']:
        return uw
    elif engine in ['tushare', 'ts', 'Tushare']:
        return uts
    elif engine in ['tdx']:
        return utdx


def save_stock_min_5(file_dir, client=ms.client):
    return tdx_file.save_tdx_to_mongo(file_dir, client)
