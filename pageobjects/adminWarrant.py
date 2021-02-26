import os
from time import sleep
import re
from pageobjects.idassPcinit import idassPcinit
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from framework.MySQLdbTest import DBOperateAction


class adminWarrant(idassPcinit):

    def addAdmin(self, userPhone, role, jurisdiction):
        """
        新增管理员操作
        :param userPhone:人员或手机号
        :param role:角色
        :param jurisdiction:管辖范围
        :return:
        """
        self.driver.find_element(By.XPATH, '//*[contains(span,"新增管理员")]').click()
        if userPhone:
            self.driver.find_element(By.XPATH, '//input[@placeholder="搜索姓名、手机号"]').send_keys(userPhone)
            try:
                WebDriverWait(self.driver, timeout=8, poll_frequency=1).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//p[@class="info-1"]')))
            except:
                return adminWarrant(self, results=0)
            else:
                element = '//p[@class="info-1" and contains(text(), ' + userPhone + ')]'
                self.driver.find_element(By.XPATH, element).click()

    def getAdmin(self):
        """
        进入管理员管理界面
        :return:
        """
        try:
            WebDriverWait(self.driver, timeout=1, poll_frequency=0.5).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'li.el-submenu.is-opened')))
        except:
            self.driver.find_element(By.CSS_SELECTOR, 'ul.el-menu--collapse>li:nth-child(5)').click()
            self.driver.find_element(By.XPATH, '//*[contains(span,"管理员管理")]').click()
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[contains(span,"管理员授权")]').click()
            sleep(1)
        else:
            self.driver.find_element(By.XPATH, '//*[contains(span,"管理员授权")]').click()
