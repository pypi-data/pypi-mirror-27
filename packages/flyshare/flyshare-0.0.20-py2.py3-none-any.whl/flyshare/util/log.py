import datetime
from zenlog import logging
import flyshare.ApiConfig as ac

if ac.LOG_TO_FILE:
    logging.basicConfig(level=ac.LOG_LEVEL,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S',
                        filename='flyshare-' +
                        str(datetime.datetime.now().strftime(
                            '%Y-%m-%d')) + '.log',
                        filemode='a')
else:
    logging.basicConfig(level=ac.LOG_LEVEL,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def log_debug(logs):
    logging.debug(logs)

def log_info(logs):
    logging.info(logs)

def log_exception(logs):
    logging.exception(logs)

def log_critical(logs):
    logging.critical(logs)

if __name__ == '__main__':
    log_info("A quirky message only developers care about")