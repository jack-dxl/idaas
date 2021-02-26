#coding=utf-8
from selenium.webdriver.remote.webdriver import WebDriver

class idassPcinit(object):
    def __init__(self, browser, total_string="", results=""):
        '''
        构造函数有一个参数driver
        :param browser:
        :param total_string:
        :param results:
        '''
        self.driver: WebDriver = browser.driver
        self.host = ""
        self.db_account = ""
        self.db_passwd = ""
        self.db_name = ""
        self.total_string = total_string
        self.results = results
