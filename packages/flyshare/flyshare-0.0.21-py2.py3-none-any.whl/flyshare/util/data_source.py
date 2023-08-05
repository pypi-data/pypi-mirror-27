

def is_tushare(source):
    if source in ['tushare', 'ts', 'Tushare']:
        return True
    else:
        return False

def is_default(source):
    if source in ['default']:
        return True
    else:
        return False

def is_flyshare(source):
    if source in ['flyshare', 'fs', 'Flyshare']:
        return True
    else:
        return False

def is_datareader(source):
    if source in ['datareader', 'pandas_datareader']:
        return True
    else:
        return False


def is_tdx(source):
    if source in ['tdx']:
        return True
    else:
        return False