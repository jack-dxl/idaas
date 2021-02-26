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


class roleManager(idassPcinit):

    def roleADD(self, roleName='', roleType="", associatedResources='', **roleAdd_dic):
        '''
        新增角色操作
        :param roleName: 角色名称
        :param roleType: 角色类型
        :param associatedResources:关联资源
        :param roleAdd_dic: 非必填项
        :return: 返回提示信息
        '''
        self.getRole()
        self.driver.find_element(By.XPATH, '//*[contains(span,"新增角色")]').click()
        # 必填项输入
        self.driver.find_element(By.CSS_SELECTOR, 'div.el-form-item__content>div>input').send_keys(roleName)
        self.driver.find_elements(By.XPATH, '//input[@placeholder="请选择"]')[1].click()
        sleep(0.5)
        if roleType == '2':
            self.driver.find_element(By.XPATH, '//*[contains(span,"企业级角色")]').click()
        else:
            self.driver.find_element(By.XPATH, '//*[contains(span,"平台级角色")]').click()
        if associatedResources != "":
            self.driver.find_element(By.XPATH,
                                     '//span[text()="必要的基本资源（必选）"]/preceding-sibling::label[1]/span').click()
            element = '//span[text()="' + associatedResources + '"]/preceding-sibling::label[1]/span'
            self.driver.find_element(By.XPATH, element).click()
        # 非必填项
        if roleAdd_dic.__contains__('roleSuperior'):
            self.driver.find_elements(By.XPATH, '//input[@placeholder="请选择"]')[2].send_keys(roleAdd_dic["roleSuperior"])
        if roleAdd_dic.__contains__('remark'):
            self.driver.find_element(By.CSS_SELECTOR, 'form.el-form>div:nth-child(5)>div>div>input').send_keys(
                roleAdd_dic['remark'])
        self.driver.find_element(By.XPATH, '//*[contains(span," 保存 ")]').click()
        if roleName == '':
            return roleManager(self, results="姓名未填")
        if associatedResources == '':
            return roleManager(self, results="关联资源未填")
        return roleManager(self, results="1")

    def roleEdit(self, roleName='', roleNameEdit='', associatedResources='', **roleAdd_dic):
        '''
        角色编辑操作
        :param roleName:角色名称（修改前）
        :param roleNameEdit:角色名称（修改后）
        :param associatedResources: 关联资源
        :param roleAdd_dic: 非必填项
        :return: 返回提示信息
        '''
        self.getRole()
        if roleName != '':
            roleNameElement = self.driver.find_element(By.XPATH, '//input[@placeholder="搜索角色名称或角色编码"]')
            roleNameElement.send_keys(Keys.CONTROL, 'a')
            roleNameElement.send_keys(Keys.BACK_SPACE)
            roleNameElement.send_keys(roleName)
            sleep(0.5)
            roleNameElement.send_keys(Keys.ENTER)
            sleep(1)
        else:
            return roleManager(self, results="0")
        self.driver.find_element(By.CSS_SELECTOR, 'i.el-icon-edit').click()
        # 必填项输入
        roleNameEditElement = self.driver.find_element(By.CSS_SELECTOR, 'div.el-form-item__content>div>input')
        roleNameEditElement.send_keys(Keys.CONTROL, 'a')
        roleNameEditElement.send_keys(Keys.BACK_SPACE)
        roleNameEditElement.send_keys(roleNameEdit)
        if associatedResources != "":
            self.driver.find_element(By.CSS_SELECTOR, 'ul.ant-select-selection__rendered').click()
            sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, 'span.ant-select-tree-switcher_close').click()
            sleep(0.5)
            element = "//span[@title='" + associatedResources + "']"
            self.driver.find_element(By.XPATH, element).click()
        # 非必填项
        if roleAdd_dic.__contains__('roleGroupName'):
            self.driver.find_elements(By.XPATH, '//input[@placeholder="请选择"]')[1].send_keys(
                roleAdd_dic["roleGroupName"])
        if roleAdd_dic.__contains__('roleSuperior'):
            self.driver.find_elements(By.XPATH, '//input[@placeholder="请选择"]')[2].send_keys(roleAdd_dic["roleSuperior"])
        if roleAdd_dic.__contains__('remark'):
            self.driver.find_element(By.CSS_SELECTOR, 'form.el-form>div:nth-child(5)>div>div>input').send_keys(
                roleAdd_dic['remark'])
        self.driver.find_element(By.XPATH, '//*[contains(span," 保存 ")]').click()
        if roleName == '':
            return roleManager(self, results="姓名未填")
        if associatedResources == '':
            return roleManager(self, results="关联资源未填")
        return roleManager(self, results="1")

    def roleDelete(self, roleName='', Status=''):
        self.getRole()
        if roleName != '':
            roleNameElement = self.driver.find_element(By.XPATH, '//input[@placeholder="搜索角色名称或角色编码"]')
            roleNameElement.send_keys(Keys.CONTROL, 'a')
            roleNameElement.send_keys(Keys.BACK_SPACE)
            roleNameElement.send_keys(roleName)
            sleep(0.5)
            roleNameElement.send_keys(Keys.ENTER)
            sleep(1)
        else:
            return roleManager(self, results="0")
        if Status == "delete":
            self.driver.find_element(By.CSS_SELECTOR, 'i.el-icon-delete').click()
            self.driver.find_element(By.XPATH, '//*[contains(span,"确定")]').click()
        #sql语句构造
        db_operation = DBOperateAction(self.host, self.db_account, self.db_passwd, self.db_name, port=3306)
        db_operation.connect()
        sql_string = "seletc * from PC_T_ROLE where NAME=" + "'  " + roleName + "'  " + "and Status == 'DELETE'"
        print(sql_string)
        results = db_operation.get_one_result(sql_string)

    def getRole(self):
        '''
        进入租户角色管理界面
        :return:
        '''
        try:
            WebDriverWait(self.driver, timeout=1, poll_frequency=0.5).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '//*[contains(span,"角色管理")]')))
        except:
            self.driver.find_element(By.XPATH, '//*[contains(span,"管理员管理")]').click()
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[contains(span,"角色管理")]').click()
            sleep(1)
        else:
            self.driver.find_element(By.XPATH, '//*[contains(span,"角色管理")]').click()



if __name__ == "__main__":
    roleName = "123"
    sql_string = "select * from PC_T_ROLE where NAME=" + "'" + roleName + "' " + "and STATUS = 'DELETE'"
    print(sql_string)
