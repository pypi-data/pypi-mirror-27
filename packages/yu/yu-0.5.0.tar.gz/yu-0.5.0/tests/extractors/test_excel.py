import datetime
import os
import unittest

import xlrd

from yu.extractors import excel as ee

base_dir = os.path.dirname(__file__)


class TestExcelExtract(unittest.TestCase):
    def setUp(self):
        self.fields = [
            ee.StringField(min_length=2, max_length=4),  # 姓名
            ee.SkipField(),  # 民族
            ee.IntegerField(max_value=150),  # 年龄
            ee.FloatField(min_value=5, max_value=200),  # 体重
            ee.DateField(),  # 生日
            ee.StringField(),  # 备注
        ]

        data_filename = os.path.join(base_dir, 'data/person.xlsx')
        book = xlrd.open_workbook(data_filename)
        self.sheet = book.sheet_by_name('person')

    def assertResultValidate(self, result, expected, error_cols=[]):
        self.assertEqual(result.values, expected)
        self.assertEqual([col for col, _ in result.errors], error_cols)

    def test_excel_extract(self):
        results = list(ee.extract(self.sheet, self.fields))

        expected = ['岳飞', 39, 72.5, datetime.date(1103, 3, 24), '南宋抗金名将']
        self.assertResultValidate(results[0], expected)

        expected = [None, 55, None, datetime.date(1068, 8, 1), '金朝开国皇帝']
        self.assertResultValidate(results[1], expected, [1, 4])

        expected = ['完颜宗弼', 50, 81.3, None, '完颜阿骨打四子,也称金兀术']
        self.assertResultValidate(results[2], expected, [5])
