import unittest

import datetime

from yu.extractors.csv import CSVExtractor, StringField, SkipField, IntegerField, FloatField, DateField, PassField

class TestCSVExtractor(unittest.TestCase):
    def setUp(self):
        fields = [
            StringField(min_length=2, max_length=4), # 姓名
            SkipField(), # 民族
            IntegerField(max_value=150), # 年龄
            FloatField(min_value=5, max_value=200), # 体重
            DateField(), # 生日
            PassField(), # 备注
        ]

        rows = [
            ['岳飞', '汉', '39', '72.5', '1103-03-24', '南宋抗金名将'],
            ['完颜阿骨打', '女真', '55', '805', '1068-8-01', '金朝开国皇帝'],
        ]

        self.csv_extractor = CSVExtractor(iter(rows), fields=fields)

    def test_csv_extractor(self):
        rows = list(self.csv_extractor)
        result, errors = rows[0]
        self.assertEqual(result, ['岳飞', 39, 72.5, datetime.date(1103, 3, 24), '南宋抗金名将'])
        self.assertEqual(errors, [])

        result, errors = rows[1]
        self.assertEqual(result, [None, 55, None, datetime.date(1068, 8, 1), '金朝开国皇帝'])
        self.assertEqual([col for col, _ in errors], [0, 3])
