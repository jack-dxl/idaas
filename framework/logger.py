#coding=utf-8
import logging
import time
import os
from logging.handlers import RotatingFileHandler

from selenium import webdriver


class Logger(object):

    def __init__(self, logger):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件

        rq = time.strftime('%Y%m%d%H', time.localtime(time.time())) #%Y%m%d%H%M
        if not os.path.exists(os.path.dirname(os.getcwd())+ '/Logs/'): #无目录则新建
            os.makedirs(os.path.dirname(os.getcwd())+ '/Logs/')
        log_path = os.path.dirname(os.getcwd()) + '/Logs/'
        log_name = log_path + rq + '.log'
        # fh = logging.RotatingFileHandler(log_name,maxBytes=10240*10,backupCount=5)#输出到test.log
        # fh.setLevel(logging.INFO)

        format = '%(asctime)s %(name)s %(levelname)s %(module)s:%(lineno)d %(message)s'
        logging.basicConfig(level=20, format='%(asctime)s %(name)s %(levelname)s %(module)s:%(lineno)d %(message)s')
        rotateHandler = RotatingFileHandler(log_name, maxBytes=10240 * 10, backupCount=5,encoding='utf-8')  # 输出到test.log
        rotateHandler.setFormatter(logging.Formatter(format))
        rotateHandler.setLevel(logging.INFO)


        # 再创建一个handler，用于输出到控制台
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        rotateHandler.setFormatter(formatter)
        # ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(rotateHandler)
        #self.logger.addHandler(ch)

    def getlog(self):
        return self.logger