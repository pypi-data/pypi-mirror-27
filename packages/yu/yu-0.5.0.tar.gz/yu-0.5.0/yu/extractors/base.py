import collections
import datetime
import re
from ast import literal_eval

from yu.validators import ValueRangeValidator, LengthRangeValidator, DateRangeValidator

NOTSET = object()


class FieldExtractor:
    error = None
    notice = None

    def __init__(self, default=NOTSET, converter=None, validator=None):
        self.default = default
        self.converter = converter
        self.validator = validator

    def extract(self, value):
        if self.default is NOTSET:
            # 如果没有设置 default，则先转换然后进行有效性检查
            value = self.convert(value)
            self.validator(value)
            return value

        # 如果设置了 default，则在数据转换异常时返回 default
        try:
            return self.convert(value)
        except Exception as err:
            self.notice = str(err)
            return self.default

    def convert(self, value):
        if self.converter:
            return self.converter(value)
        raise NotImplementedError


class SkipField(FieldExtractor):
    """跳过"""


class PassField(FieldExtractor):
    """PASS, 不做转换"""

    def extract(self, value):
        return value


class StringField(FieldExtractor):
    def __init__(self, default=NOTSET, strip=True, spaceless=False,
                 min_length=None, max_length=None):
        validator = LengthRangeValidator(min_length, max_length)
        super().__init__(default, validator=validator)
        self.strip = strip
        self.spaceless = spaceless

    def convert(self, value):
        if self.spaceless:
            value = ''.join(value.split())
        elif self.strip:
            value = value.strip()
        return value


class IntegerField(FieldExtractor):
    def __init__(self, default=NOTSET, min_value=None, max_value=None, use_eval=False):
        validator = ValueRangeValidator(min_value, max_value)
        super().__init__(default, validator=validator)
        self.use_eval = use_eval

    def convert(self, value):
        if self.use_eval:
            value = literal_eval(value)
            if not isinstance(value, int):
                value = int(value)
        else:
            value = int(value)
        return value


# noinspection PyAbstractClass
class FloatField(FieldExtractor):
    def __init__(self, default=NOTSET, min_value=None, max_value=None):
        validator = ValueRangeValidator(min_value, max_value)
        super().__init__(default, float, validator)


class DateField(FieldExtractor):
    delimiters = re.compile(r'[-/.]')

    def __init__(self, default=NOTSET, start_date=None, end_date=None):
        validator = DateRangeValidator(start_date, end_date)
        super().__init__(default, validator=validator)

    def convert(self, value):
        # 先按照最标准的进行尝试
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            pass

        # 试试其他格式
        value = self.delimiters.sub('-', value.strip())
        if '-' in value:
            date_format = '%Y-%m-%d'
        else:
            date_format = '%Y%m%d'
        return datetime.datetime.strptime(value, date_format).date()


Result = collections.namedtuple('Result', 'values, errors, notices')


class RowExtractor:
    fields: list = None

    def __init__(self, *, fields=None, default=None):
        if fields is not None:
            self.fields = fields
        self.default = default

    def extract(self, row):
        values = []
        errors = []
        notices = []

        for col, (field, value) in enumerate(zip(self.fields, row), 1):
            if isinstance(field, SkipField):
                continue

            value = self.extract_field(field, value)
            values.append(value)

            # 保存并清除 field 中的错误
            if field.error:
                errors.append((col, field.error))
                field.error = None

            # 保存并清除 notice
            if field.notice:
                notices.append(field.notice)
                field.notice = None

        return Result(values, errors, notices)

    def extract_field(self, field, value):
        try:
            return field.extract(value)
        except Exception as err:
            field.error = err
            return self.default


def format_error_message(rowx, errors):
    error_messages = []
    for colx, error_message in errors:
        error_messages.append(f'{rowx}:{colx} 错误: {error_message}')
    return '\n'.join(error_messages)
