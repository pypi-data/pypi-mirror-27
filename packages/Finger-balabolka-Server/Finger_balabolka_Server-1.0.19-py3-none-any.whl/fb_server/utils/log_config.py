import os
import re
import logging

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def get_log_path():
    log_path = os.path.join(
              os.path.dirname(
                   os.path.dirname(
                        os.path.abspath(__file__))), 'log')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    return log_path

LOG_PATH = get_log_path()

logger = logging.getLogger("server_log")

name = '{}.log'.format(datetime.now().date())

filename=os.path.join(LOG_PATH, name)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

fh = TimedRotatingFileHandler(filename, when="midnight", interval=1)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)