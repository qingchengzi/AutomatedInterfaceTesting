#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tian'
__data__ = '2021/3/11 17:08'

"""
处理Excel
"""
import xlrd
from conf import settings
from utils.LogHandler import logger


class ExcelOperate:
    def __init__(self, file_path, sheet_by_index=0):
        self.file_path = file_path
        self.sheet_by_index = sheet_by_index
        book = xlrd.open_workbook(self.file_path)
        self.sheet = book.sheet_by_index(self.sheet_by_index)

    def get_excel(self):
        """
        获取excel数据
        :return:
        """
        title = self.sheet.row_values(0)
        data_list = [dict(zip(title, self.sheet.row_values(row))) for row in range(1, self.sheet.nrows)]
        logger().info("读取Excel成功,数据已返回")
        return data_list


if __name__ == '__main__':
    excel_data_list = ExcelOperate(settings.FILE_PATH, 0).get_excel()
    print(excel_data_list)
