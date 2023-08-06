import datetime
import unittest

from yu.extractors import base as be
from yu.validators import ValidationError


class TestFieldExtractor(unittest.TestCase):
    def test_extractor_with_default(self):
        extractor = be.FieldExtractor(default='DEFAULT', converter=int)
        self.assertEqual(extractor.extract('N/A'), 'DEFAULT')


class TestPassField(unittest.TestCase):
    def test_pass(self):
        field = be.PassField()
        self.assertEqual(field.extract('pass through'), 'pass through')


class TestStringField(unittest.TestCase):
    def test_normal_value(self):
        field = be.StringField()
        self.assertEqual(field.extract(' strip '), 'strip')
        self.assertEqual(field.extract('　全角　空格　'), '全角　空格')

    def test_no_strip(self):
        field = be.StringField(strip=False)
        self.assertEqual(field.extract(' strip '), ' strip ')

    def test_spaceless(self):
        field = be.StringField(spaceless=True)
        self.assertEqual(field.extract(' space less '), 'spaceless')
        self.assertEqual(field.extract('　全角　空格　'), '全角空格')

    def test_length_validate(self):
        field = be.StringField(min_length=5)
        with self.assertRaises(ValidationError):
            field.extract('ABC')


class TestIntegerField(unittest.TestCase):
    def test_normal_value(self):
        field = be.IntegerField()
        self.assertEqual(field.extract('100'), 100)

    def test_invalid_value(self):
        field = be.IntegerField()
        with self.assertRaises(ValueError):
            field.extract('N/A')

    def test_default_value(self):
        field = be.FloatField(default=8)
        self.assertAlmostEqual(field.extract('N/A'), 8)

    def test_without_use_eval(self):
        field = be.IntegerField()

        # 不能处理十六进制、八进制、二进制等
        with self.assertRaises(ValueError):
            field.extract('0x100')

        # 不能处理浮点数
        with self.assertRaises(ValueError):
            field.extract('100.5')

    def test_use_eval(self):
        field = be.IntegerField(use_eval=True)

        # 能处理十六进制、八进制、二进制等
        self.assertEqual(field.extract('0x100'), 0x100)
        self.assertEqual(field.extract('0o100'), 0o100)
        self.assertEqual(field.extract('0b100'), 0b100)

        # 能处理浮点数
        self.assertEqual(field.extract('100.5'), 100)


class TestFloatField(unittest.TestCase):
    def test_normal_value(self):
        field = be.FloatField()
        self.assertEqual(field.extract('3.1415926'), 3.1415926)

    def test_invalid_value(self):
        field = be.FloatField()
        with self.assertRaises(ValueError):
            field.extract('N/A')

    def test_default_value(self):
        field = be.FloatField(default=3.1415926)
        self.assertAlmostEqual(field.extract('N/A'), 3.1415926)


class TestDateField(unittest.TestCase):
    def test_normal_value(self):
        field = be.DateField()
        expected_date = datetime.date(2017, 12, 9)
        self.assertEqual(field.extract('2017-12-09'), expected_date)
        self.assertEqual(field.extract('2017/12/09'), expected_date)
        self.assertEqual(field.extract('2017.12.09'), expected_date)
        self.assertEqual(field.extract('20171209'), expected_date)

    def test_invalid_value(self):
        field = be.DateField()

        with self.assertRaises(ValueError):
            field.extract('2017-13-09')

        with self.assertRaises(ValueError):
            field.extract('2017:13:09')

    def test_out_of_range(self):
        start_date = datetime.date(2017, 1, 1)
        end_date = datetime.date(2017, 12, 31)
        field = be.DateField(start_date=start_date, end_date=end_date)

        with self.assertRaises(ValidationError):
            field.extract('2016-12-09')

        with self.assertRaises(ValidationError):
            field.extract('2018-12-09')


class TestRowExtractor(unittest.TestCase):
    def setUp(self):
        fields = [
            be.StringField(min_length=2, max_length=4),  # 姓名
            be.SkipField(),  # 民族
            be.IntegerField(max_value=150),  # 年龄
            be.FloatField(min_value=5, max_value=200),  # 体重
            be.DateField(),  # 生日
            be.PassField(),  # 备注
        ]
        self.row_extractor = be.RowExtractor(fields=fields)

    def test_normal_row(self):
        row = ['岳飞', '汉', '39', '72.5', '1103-03-24', '南宋抗金名将']
        result = self.row_extractor.extract(row)
        self.assertEqual(result.values, ['岳飞', 39, 72.5, datetime.date(1103, 3, 24), '南宋抗金名将'])
        self.assertEqual(result.errors, [])

    def test_invalid_row(self):
        row = ['完颜阿骨打', '女真', '55', '805', '1068-8-01', '金朝开国皇帝']
        result = self.row_extractor.extract(row)

        self.assertEqual(result.values, [None, 55, None, datetime.date(1068, 8, 1), '金朝开国皇帝'])
        self.assertEqual([col for col, _ in result.errors], [1, 4])
