from xlrd import xldate_as_datetime
from xlrd.biffh import XL_CELL_TEXT, XL_CELL_DATE, XL_CELL_NUMBER
from xlrd.sheet import Cell, Sheet

from . import base

SkipField = base.SkipField
PassField = base.PassField


class CellMixin:
    def convert(self, value):
        if isinstance(value, Cell):
            return self.convert_cell(value)
        return value

    def convert_cell(self, cell):
        return cell.value


class StringField(CellMixin, base.StringField):
    pass


class IntegerField(CellMixin, base.IntegerField):
    def convert_cell(self, cell):
        return int(cell.value)


class FloatField(CellMixin, base.FloatField):
    def convert_cell(self, cell):
        return float(cell.value)


class DateField(CellMixin, base.DateField):
    datemode = None

    def convert_cell(self, cell: Cell, datemode=None):
        if cell.ctype == XL_CELL_DATE:
            if datemode is None:
                datemode = self.datemode
            assert datemode is not None, '必须指定 datemode.'
            return xldate_as_datetime(cell.value, self.datemode).date()
        elif cell.ctype == XL_CELL_TEXT:
            return base.DateField.convert(self, cell.value)
        elif cell.ctype == XL_CELL_NUMBER:
            return base.DateField.convert(self, int(cell.value))
        else:
            raise ValueError(f'单元格 {cell} ({cell.ctype}, {cell.value})无法转换成日期. ')


RowExtractor = base.RowExtractor


def extract(sheet: Sheet, fields=None, default=None, headers=0, skip_headers=True):
    # 为没有设置 datemode 的 DateField 设置 datemode
    datemode = sheet.book.datemode
    for field in fields:
        if isinstance(field, DateField) and field.datemode is None:
            field.datemode = datemode

    row_extractor = RowExtractor(fields=fields, default=default)
    for rowx in range(sheet.nrows):
        row = sheet.row(rowx)
        if headers:
            headers -= 1
            if not skip_headers:
                yield row
        yield row_extractor.extract(row)
