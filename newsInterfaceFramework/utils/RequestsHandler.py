#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tian'
__data__ = '2021/3/11 17:10'

"""
处理请求
"""
import json
import re

import requests

from jsonpath_rw import parse  # 第三方插件，需要pip install
from utils.ExcelHandler import ExcelOperate
from conf import settings
from utils.LogHandler import logger


class RequestsOperate:

    def __init__(self, current_case, all_excel_data_list):
        """
        :param current_case: 用例列表中的一条条单独测试用例(字典形式),用来给request构造发送请求
        :param all_excel_data_list: 全部用例列表
        """
        self.current_case = current_case
        self.all_excel_data_list = all_excel_data_list

    def get_response_msg(self):
        """
        发送请求并且获取结果
        :return:
        """
        return self._send_msg()

    def _send_msg(self):
        """发请求"""
        logger().info("正在向{0}发送请求,{1}".format(self.current_case.get("url"), self.current_case))
        response = requests.request(
            method=self.current_case.get("method"),
            url=self.current_case.get("url"),
            data=self._check_request_data(),
            params=self._check_request_params(),
            cookies=self._check_request_cookies(),
            headers=self._check_request_headers(),
        )
        self._write_cookies(response)
        return json.loads(self.current_case.get("except")), response.json()

    def _check_request_headers(self):
        """
        校验请求头，做携带cookies 和 数据依赖的问题
        {
            'user':'${}$',
            'testfan-id':'ca447223-876e-46ba-9e45-f775335dfcbe'
        }
        :return:
        """
        headers = self.current_case.get("headers", None)
        if headers:
            return self._operate_re_msg(headers)
        else:
            return {}

    def _write_cookies(self, response):
        """ 监测响应结果中是否含有cookies，有就保存起来"""
        for item in self.all_excel_data_list:
            if item.get("case_num") == self.current_case.get("case_num"):
                item["temporary_response_cookies"] = response.cookies.get_dict()
                if response.headers.get("Content-Type").lower() == "application/json;charset=utf-8":
                    item["temporary_response_json"] = response.json()
                # 如果去请求头中取数据都存一份
                item["temporary_request_headers"] = self.current_case.get("headers")
                item["temporary_request_data"] = self.current_case.get("data")
                item["temporary_request_json"] = self.current_case.get("json")
                item["temporary_request_params"] = self.current_case.get("params")
                # 所有去响应头中取值的都存一份
                item["temporary_response_headers"] = response.headers

    def _check_request_data(self):
        """处理请求的data参数，检查是否有依赖"""
        data = self.current_case.get("data")
        if data:
            return json.loads(data)
        else:
            return {}

    def _check_request_params(self):
        """处理请求的data参数，检查是否有依赖"""
        params = self.current_case.get("params")
        if params:
            return json.loads(params)
        else:
            return {}

    def _check_request_cookies(self):
        """处理请求中的cookies"""
        cookies_case_num = self.current_case.get("cookies")
        if cookies_case_num:  # 当前接口需要cookies
            for item in self.all_excel_data_list:
                if item.get("case_num") == cookies_case_num:
                    return item.get("temporary_response_cookies", {})
        else:
            return {}

    def _operate_re_msg(self, parameter):
        """
        正则校验,数据依赖的字段
        :param parameter: 各种参数，如：data,header,params
        :return:
        """
        # 使用re 将提取依赖字段 {"testfan-token":"${neeo_001>response_json>data}$"}
        if isinstance(parameter, dict):
            json.dumps(parameter)
        pattern = re.compile("\${(.*?)}\$")  # 定义规则
        rule_list = pattern.findall(parameter)  # 按照规则匹配
        if rule_list:  # 该参数有数据依赖要处理
            for rule in rule_list:
                case_num, params, json_path = rule.split(">")
                for line in self.all_excel_data_list:
                    if line.get("case_num") == case_num:
                        temp_data = line.get("temporary_{0}".format(params))
                        if isinstance(temp_data, str):
                            temp_data = json.loads(temp_data)
                        match_list = parse(json_path).find(temp_data)
                        if match_list:
                            match_data = [v.value for v in match_list][0]
                        # 将提取出来的值替换到原来规则,
                        # 如下：将${neeo_001>response_json>data}$ 替换为提取出来的值-->3c58cd285a6d4261b9a6271a6cceddd8
                        # {"testfan-token": "${neeo_001>response_json>data}$"}
                        parameter = re.sub(pattern=pattern, repl=match_data, string=parameter, count=1)
            return json.loads(parameter)
        else:
            if isinstance(parameter, str):
                parameter = json.loads(parameter)  # 反序列化
            return parameter


if __name__ == '__main__':
    excel_data_list = ExcelOperate(settings.FILE_PATH, 3).get_excel()
    for item in excel_data_list:
        RequestsOperate(current_case=item, all_excel_data_list=excel_data_list).get_response_msg()
