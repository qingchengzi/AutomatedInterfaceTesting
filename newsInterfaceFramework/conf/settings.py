#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tian'
__data__ = '2021/3/12 16:19'

import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 测试数据execl默认配置
FILE_NAME = "接口测试实例2.xls"
FILE_PATH = os.path.join(BASE_DIR, "data", FILE_NAME)

# -----------初始化为template cookies dict---------
COOKIES_DICT = {}

# ------allure报告相关---------

ALLURE_COMMAND = "allure generate {from_json_path} -o {save_to_path} --clean".format(
    from_json_path=os.path.join(BASE_DIR, "report", "json_result"),
    save_to_path=os.path.join(BASE_DIR, "report", "allure_result")
)

# -----------邮件相关

# 第三方SMTP服务
MAIL_HOST = "smtp.qq.com"  # 设置服务器
MAIL_USER = "1233333@qq.com"  # 用户名
MAIL_TOKEN = "hhhhhhhhm"  # 授权码
# 设置收件人和发件人
SENDER = "99999999@qq.com"
RECEIVERS = ["12335555@qq.com", "xiangxiang@163.com"]  # 接收邮箱可以设置你的qq或者其它邮箱

# 邮件主题
THEME = "请查阅-s28的第一个测试报告"
# 正文内容
SEND_CONTENT = "hi_man,你收到附件了吗？"
# 附件的file name
SEND_FILE_NAME = "allure_report.zip"

# 日志文件命令
# 日志级别
LOG_LEVEL = "debug"
LOG_STREAM_LEVEL = "debug"  # 屏幕输出流
LOG_FILE_LEVEL = "info"  # 文件输出流

# 日志文件命名
LOG_FILE_NAME = os.path.join(BASE_DIR, "logs", datetime.datetime.now().strftime("%Y-%m-%d") + ".log")

if __name__ == '__main__':
    print(FILE_PATH)
