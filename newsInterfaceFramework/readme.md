# about
本项目是接口自动化测试脚本
- 从Excel表格中读取测试脚本
- 通过requests模块发送请求
- 通过pytest框架进行结果断言
- allure生成测试报告
- 可以将测试报告发邮件

简介： 从Excel表格中读取测试脚本，后台通过requests模块发送请求，获取响应。 使用pytest框架进行断言，生成测试报告，可以将测试报告通过邮件发送。

目录介绍： conf---> settings.py 配置文件目录。 data---> 存放excel类型的接口测试用例 。 debugcode-->开发过程中写测试一些调试代码。 logs --> 日志目录。 report --> 测试报告。 utils --> 存放公共工具类的包。 pytest.ini --> pytest配置文件。 start.py 执行入口。

安装教程：需安装第三方模块：pytest、allure-pytest、xlrd==1.2.0、requests

使用说明： 直接运行start.py即可执行本接口自动化测试框架，默认的用例。 data目录中接口测试实例2.xls默认运行的接口实例。 接口测试实例2.xls实例中包含了工作中几乎所有使用场景
