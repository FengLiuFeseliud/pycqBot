import logging
from logging.handlers import TimedRotatingFileHandler
import os

cqlogger = logging.getLogger('pycqBot')
cqlogger.setLevel(logging.CRITICAL)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)


def enable_logging(logPath, when, interval, backupCount):
    cqlogger.setLevel(logging.DEBUG)
    file_handler = TimedRotatingFileHandler(
        os.path.join(logPath, "cq.log"),
        when,
        interval,
        backupCount,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    cqlogger.addHandler(file_handler)
    cqlogger.addHandler(console_handler)
