from .base import *


class CSVExtractor:
    """CSV 数据提取器"""

    fields: list = None

    def __init__(self, reader, *, fields=None, default=None):
        self.reader = reader
        fields = fields or self.fields
        self.row_extractor = RowExtractor(fields=fields, default=default)

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self.reader)
        return self.row_extractor.extract(row)
