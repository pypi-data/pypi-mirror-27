import os
import logging


def get_log_path():
    log_path = os.path.join(
                os.path.dirname(
                   os.path.dirname(
                        os.path.abspath(__file__))), 'log')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    return log_path

LOG_PATH = get_log_path()

logger = logging.getLogger("client_log")

filename=os.path.join(LOG_PATH, "fb.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

fh = logging.FileHandler(filename, encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

