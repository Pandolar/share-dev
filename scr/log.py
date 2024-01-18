# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : log.py
# @Time : 2024/1/18 15:33
# -------------------------------
import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 日志类
class Logger():
    def __init__(self,log_name):

        LOG_NAME = log_name
        #LOG_NAME = 'wangsu_cdn_python'
        #global CONFIG
        LOG_PATH = os.getcwd() + os.sep + "log" + os.sep
        # LOG_PATH = CONFIG['LOG_PATH']
        #LOG_PATH = './log/'
        if not os.path.exists(LOG_PATH):
            os.mkdir(LOG_PATH)
        LOG_FILE = LOG_PATH + f"{LOG_NAME}.log"
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        self.logger.setLevel(logging.INFO)
        self.fh = TimedRotatingFileHandler(filename=LOG_FILE, when="MIDNIGHT", backupCount=10)
        self.formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s")
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)
        self.logger.removeHandler(logging.StreamHandler)

    def get_logger(self):
        return self.logger