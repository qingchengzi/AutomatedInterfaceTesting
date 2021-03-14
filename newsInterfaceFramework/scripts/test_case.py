#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tian'
__data__ = '2021/3/11 17:00'

import pytest
import allure
from deepdiff import DeepDiff  # 进行断言的

from utils.ExcelHandler import ExcelOperate
from utils.RequestsHandler import RequestsOperate
from conf import settings
from utils.LogHandler import logger

# 读取excel表中所有的测试用例，以列表形式返回
excel_data_list = ExcelOperate(settings.FILE_PATH, 3).get_excel()


class TestCase(object):
    @pytest.mark.parametrize("item", excel_data_list)
    def test_case(self, item):
        logger().info("正在进行断言...")
        except_data, result = RequestsOperate(current_case=item, all_excel_data_list=excel_data_list).get_response_msg()
        allure.dynamic.title(item.get('title'))
        allure.dynamic.description(
            "<b style='color:red'>请求的url:</b>{0}<hr />"
            "<b style='color:red'>预期值:</b>{1}<hr />"
            "<b style='color:red'>实际执行结果:</b>{2}<hr />".format(item["url"], item["except"], result)
        )
        assert not DeepDiff(except_data, result).get("values_changed", None)
        logger().info("完成断言,{0}-{1}".format(except_data, result))
