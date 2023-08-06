
import csv
import os
import datetime
import unittest

from yu.extractors import csv as ce

base_dir = os.path.dirname(__file__)

class TestCSVExtract(unittest.TestCase):
    def setUp(self):
        self.fields = [
            ce.StringField(min_length=2, max_length=4),  # 姓名
            ce.SkipField(),  # 民族
            ce.IntegerField(max_value=150),  # 年龄
            ce.FloatField(min_value=5, max_value=200),  # 体重
            ce.DateField(),  # 生日
            ce.PassField(),  # 备注
        ]

    def assertRowValidate(self, row, expected, error_cols=[]):
        self.assertEqual(row[0], expected)
        self.assertEqual([col for col, _ in row[1]], error_cols)

    def test_csv_extract(self):
        data_filename = os.path.join(base_dir, 'data/person.csv')
        with open(data_filename, encoding='utf-8') as fp:
            reader = csv.reader(fp)
            rows = list(ce.extract(reader, self.fields))

            expected = ['岳飞', 39, 72.5, datetime.date(1103, 3, 24), '南宋抗金名将']
            self.assertRowValidate(rows[0], expected)

            expected = [None, 55, None, datetime.date(1068, 8, 1), '金朝开国皇帝']
            self.assertRowValidate(rows[1], expected, [0, 3])

            expected = ['完颜宗弼', 50, 81.3, None, '完颜阿骨打四子,也称金兀术']
            self.assertRowValidate(rows[2], expected, [4])
