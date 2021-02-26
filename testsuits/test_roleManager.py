import logging
import pytest
import yaml
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from framework.logger import Logger
from pageobjects.roleManager import roleManager

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="class")
def roleAdminM(init_driver):

    roleAdminM = roleManager(init_driver)
    logger = Logger(logger="roleManager").getlog()
    logger.info("开始执行角色测试用例")
    yield roleAdminM,logger
    logger.info("角色测试用例执行完毕")

class TestIdass(object):

    @pytest.mark.parametrize("roleName, roleType, associatedResources, dic",
                             yaml.load(open("yamlpack/roleManager/roleAdd.yaml", encoding="utf-8"),
                                       Loader=yaml.FullLoader))
    def testRoleAdd(self, roleName, roleType, associatedResources, dic, roleAdminM):
        roleAdminM[1].info("角色新增测试用例: " + roleName + "-" + roleType + "-" + associatedResources)
        demo = roleAdminM[0].roleADD(roleName, roleType, associatedResources, **dic)
        roleAdminM[1].info("demo:" +demo.results)
        if demo.results == "1" :
            try:
                WebDriverWait(roleAdminM[0].driver, timeout=3, poll_frequency=1).until(
                    expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div.el-notification__content')))
            except:
                if roleName in roleAdminM[0].driver.page_source:
                    roleAdminM[1].info("测试通过，用例描述：角色添加成功")
                    assert True
                else:
                    self.failexcept(roleAdminM[1])
                    assert roleName in roleAdminM[0].driver.page_source
            else:
                text = roleAdminM[0].driver.find_element(By.CSS_SELECTOR, 'div.el-notification__content>p').text
                if "角色名称已存在" in text:
                    roleAdminM[1].info("测试通过，用例描述：角色名称重复")
                    roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                    assert True
                else:
                    roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                    self.failexcept(roleAdminM[1])
                    assert False
        if "未填" in demo.results:
            WebDriverWait(roleAdminM[0].driver, timeout=2, poll_frequency=1).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div.el-form-item__error')))
            if "角色名称是必须的" in roleAdminM[0].driver.page_source:
                roleAdminM[1].info("测试通过，用例描述：角色名称未填")
                roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                assert True
            elif "关联资源是必须的" in roleAdminM[0].driver.page_source:
                roleAdminM[1].info("测试通过，用例描述：关联资源未填")
                roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                assert True
            else:
                roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                self.failexcept(roleAdminM[1])
                assert demo.results in roleAdminM[0].driver.page_source

    @pytest.mark.parametrize("roleName, roleNameEdit, associatedResources, dic",
                             yaml.load(open("yamlpack/roleManager/roleEdit.yaml", encoding="utf-8"),
                                       Loader=yaml.FullLoader))
    def testRoleEdit(self, roleName, roleNameEdit, associatedResources, dic, roleAdminM):
        roleAdminM[1].info("角色新增测试用例: " + roleName + roleNameEdit + "-" + associatedResources)
        demo = roleAdminM[0].roleEdit(roleName, roleNameEdit , associatedResources, **dic)
        roleAdminM[1].info("demo:" + demo.results)
        if demo.results == "0":
            roleAdminM[1].error("请检查用例")
            self.failexcept(roleAdminM[1])
            assert False
        if demo.results == "1":
            try:
                WebDriverWait(roleAdminM[0].driver, timeout=2, poll_frequency=1).until(
                    expected_conditions.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'div.el-notification__content')))
            except:
                if roleNameEdit in roleAdminM[0].driver.page_source:
                    roleAdminM[1].info("测试通过，用例描述：角色编辑成功")
                    assert True
                else:
                    self.failexcept(roleAdminM[1])
                    assert roleNameEdit in roleAdminM[0].driver.page_source
            else:
                text = roleAdminM[0].driver.find_element(By.CSS_SELECTOR, 'div.el-notification__content>p').text
                if "角色名称已存在" in text:
                    roleAdminM[1].info("测试通过，用例描述：角色名称重复")
                    roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                    assert True
                else:
                    roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                    self.failexcept(roleAdminM[1])
                    assert False
        if "未填" in demo.results:
            WebDriverWait(roleAdminM[0].driver, timeout=2, poll_frequency=1).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div.el-form-item__error')))
            if "角色名称是必须的" in roleAdminM[0].driver.page_source:
                roleAdminM[1].info("测试通过，用例描述：角色名称未填")
                roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                assert True
            elif "关联资源是必须的" in roleAdminM[0].driver.page_source:
                roleAdminM[1].info("测试通过，用例描述：关联资源未填")
                roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                assert True
            else:
                roleAdminM[0].driver.find_element(By.XPATH, '//*[contains(span,"取消本次操作")]').click()
                self.failexcept(roleAdminM[1])
                assert demo.results in roleAdminM[0].driver.page_source

    def failexcept(self, *args):
        args[1].info("测试用例不通过:")
        args[1].info("---" * 50)


