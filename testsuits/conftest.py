# coding=utf-8
import logging
from time import sleep

import pytest
from framework.idassDriver import idassDriver


idassBrowser = idassDriver()

@pytest.fixture(scope='session')
def init_driver(request):
    logging.info("开始执行测试用例")

    def fin():
        logging.info("测试用例结束")
        #idassBrowser.quit()


    request.addfinalizer(fin)
    return idassBrowser
