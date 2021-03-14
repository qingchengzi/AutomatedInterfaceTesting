#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tian'
__data__ = '2021/3/11 17:05'

"""
allure报告相关
"""
import os

import zipfile  # 打包
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import subprocess  # 执行cmd命令
from conf import settings
from utils.LogHandler import logger


class AllureOperate:

    def get_allure_report(self):
        """生成报告"""
        # os.system(ALLURE_COMMAND) 运行cmd命令，但是不安全
        logger().info("正在生成测试报告......")
        subprocess.call(settings.ALLURE_COMMAND, shell=True)
        logger().info("生成测试报告成功......")

    def check_zip(self):
        """打包"""
        try:
            logger().info("正在打包测试报告......")
            BASE_DIR = os.path.join(settings.BASE_DIR, "report")
            start_zip_dir = os.path.join(BASE_DIR, "allure_result")  # 要压缩文件夹的根路径
            zip_file_name = 'allure_report.zip'  # 为压缩后的文件起个名字
            zip_file_path = os.path.join(BASE_DIR, zip_file_name)
            f = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
            for dir_path, dir_name, file_names in os.walk(start_zip_dir):
                # 要是不replace，就从根目录开始复制
                file_path = dir_path.replace(start_zip_dir, '')
                # 实现当前文件夹以及包含的所有文件
                file_path = file_path and file_path + os.sep or ''
                for file_name in file_names:
                    f.write(os.path.join(dir_path, file_name), file_path + file_name)
            f.close()
            logger().info("打包测试报告完成......")
        except Exception as er:
            logger().error("打包测试报告失败:{0}".format(er))

    def send_mail(self):
        """发送邮件"""
        # 第三方SMTP服务
        mail_host = settings.MAIL_HOST  # 设置服务器
        mail_user = settings.MAIL_USER  # 用户名
        mail_pass = settings.MAIL_TOKEN  # 口令
        # 设置收件人和发件人
        sender = settings.SENDER
        receivers = settings.RECEIVERS  # 接收邮箱可以设置你的qq或者其它邮箱
        # 创建一个带附件的实例对象
        message = MIMEMultipart()
        # 邮箱主题、收件人、发件人
        subject = settings.THEME  # 邮件主题
        message["Subject"] = Header(subject, "utf-8")
        message["From"] = Header("{0}".format(sender), "utf-8")
        message["To"] = Header("{0}".format(";".join(receivers)), "utf-8")
        # 邮件正文内容
        send_content = settings.SEND_CONTENT
        content_obj = MIMEText(send_content, "plain", "utf-8")  # 第一个参数为邮件内容
        message.attach(content_obj)
        # 构造附件
        att = MIMEText(_text=self._get_zip_file(), _subtype="base64", _charset="utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment;filename="{}"'.format(settings.SEND_FILE_NAME)  # 邮件附件中显示什么名字
        message.attach(att)
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(mail_host, 25)  # 25 为 SMTP端口号
            smtp_obj.login(mail_user, mail_pass)
            smtp_obj.send_message(sender, receivers, message.as_string())
            smtp_obj.quit()
            logger().info("邮件发送成功")
            print("邮箱发送成功")
        except smtplib.SMTPException as er:
            logger().error("email end error:{0}".format(er))

    def _get_zip_file(self):
        """获取zip文件内容"""
        with open(file=os.path.join(settings.BASE_DIR, "report", "allure_report.zip"), mode="rb") as f:
            return f.read()


if __name__ == '__main__':
    AllureOperate().get_allure_report()
