#coding=utf-8
import pytest
import os
if __name__ == '__main__':
    # pytest.main(["-s", "./"])
    pytest.main(["-s", "./test_roleManager.py", "--alluredir=./report/results/role"])
    os.system("allure serve ./report/results/role")