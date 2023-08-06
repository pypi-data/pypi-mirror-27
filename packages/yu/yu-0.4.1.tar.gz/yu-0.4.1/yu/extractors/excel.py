from xlrd import xldate_as_datetime, cellname
from xlrd.biffh import XL_CELL_TEXT, XL_CELL_DATE, XL_CELL_NUMBER, XL_CELL_EMPTY
from xlrd.sheet import Cell, Sheet

from . import base

SkipField = base.SkipField
PassField = base.PassField


class StringField(base.StringField):
    def convert(self, cell: Cell):
        if cell.ctype == XL_CELL_TEXT:
            return super().convert(cell.value)
        elif cell.ctype == XL_CELL_NUMBER:
            # 如果是数字，需要猜测一下，结果并不一定可靠
            if cell.value % 1 == 0.0:
                # 如果小数部分为零，则认为是整数
                return str(int(cell.value))
            else:
                # 如果小数部分为零，则认为是浮点数
                return str(cell.value)
        elif cell.ctype == XL_CELL_EMPTY:
            return ''
        else:
            raise ValueError(f'单元格格式不对: {cell.ctype} - {cell.value}')


class IntegerField(base.IntegerField):
    def convert(self, cell):
        return int(cell.value)


class FloatField(base.FloatField):
    def convert(self, cell):
        return float(cell.value)


class DateField(base.DateField):
    datemode = None

    def convert(self, cell: Cell, datemode=None):
        if cell.ctype == XL_CELL_DATE:
            if datemode is None:
                datemode = self.datemode
            assert datemode is not None, '必须指定 datemode.'
            return xldate_as_datetime(cell.value, self.datemode).date()
        elif cell.ctype == XL_CELL_TEXT:
            return super().convert(cell.value)
        elif cell.ctype == XL_CELL_NUMBER:
            return super().convert(int(cell.value))
        else:
            raise ValueError(f'单元格 {cell} ({cell.ctype}, {cell.value})无法转换成日期. ')


RowExtractor = base.RowExtractor


def format_error_message(rowx, errors):
    error_messages = []
    for colx, error_message in errors:
        cell_name = cellname(rowx, colx)
        error_messages.append(f'{cell_name} 错误: {error_message}')
    return '\n'.join(error_messages)


def extract(sheet: Sheet, fields=None, default=None, headers=0):
    # 为没有设置 datemode 的 DateField 设置 datemode
    datemode = sheet.book.datemode
    for field in fields:
        if isinstance(field, DateField) and field.datemode is None:
            field.datemode = datemode

    row_extractor = RowExtractor(fields=fields, default=default)
    for rowx in range(sheet.nrows):
        row = sheet.row(rowx)
        if rowx < headers:
            continue
        yield row_extractor.extract(row)
