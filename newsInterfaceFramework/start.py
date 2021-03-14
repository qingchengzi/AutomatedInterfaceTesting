#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tian'
__data__ = '2021/3/12 16:27'

import os

import shutil
import pytest

from conf.settings import BASE_DIR
from utils.AllureHandler import AllureOperate  # 生成测试报告

if __name__ == '__main__':

    dir_path = os.path.join(BASE_DIR, "report", "json_result")
    if os.path.isdir(dir_path):
        # 执行用例前，首先清除上一次测试生成的json文件
        shutil.rmtree(dir_path)
        pytest.main()  # 执行测试用例
        # 生成allure测试报告
        allure_obj = AllureOperate()
        allure_obj.get_allure_report()
        # 压缩文件
        allure_obj.check_zip()
        # 执行完毕后发送邮件
        # allure_obj.send_mail()
    else:
        os.makedirs(dir_path)
