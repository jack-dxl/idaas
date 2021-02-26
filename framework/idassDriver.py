from selenium import webdriver
from time import sleep
from framework.logger import Logger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from config.read_config import ReadIni
logger = Logger(logger="webDriver").getlog()


class idassDriver(object):
    def __init__(self):
        self.driver =webdriver.Chrome()
        self.config = ReadIni()
        self.driver.maximize_window()
        sleep(5)
        url = self.config.get_url("test_url")
        logger.info("打开网址:" + url)
        self.driver.get(url)
        WebDriverWait(self.driver, timeout=30, poll_frequency=1).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="loginForm_pwd.submit"]')))
        self.driver.find_element_by_name('username').send_keys('19900000002')
        self.driver.find_element_by_name('password').send_keys('123456')
        self.driver.find_element_by_id('loginForm_pwd.submit').click()
        WebDriverWait(self.driver, timeout=20, poll_frequency=1).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//*[contains(span,"平台总览")]')))



    def quit(self):
        '''
        退出浏览器
        :return:
        '''
        logger.info("退出浏览器")
        self.driver.quit()
