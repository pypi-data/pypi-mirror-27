import datetime
from argparse import ArgumentTypeError


class DateType:
    def __init__(self, format='%Y-%m-%d'):
        self.format = format

    def __call__(self, string):
        try:
            return datetime.datetime.strptime(string, self.format).date()
        except ValueError:
            message = f'{string} 不符合指定的日期格式 {self.format}'
            raise ArgumentTypeError(message)


class DatetimeType:
    def __init__(self, format='%Y-%m-%d %H:%M:%S'):
        self.format = format

    def __call__(self, string):
        try:
            return datetime.datetime.strptime(string, self.format)
        except ValueError:
            message = f'{string} 不符合指定的日期时间格式 {self.format}'
            raise ArgumentTypeError(message)
