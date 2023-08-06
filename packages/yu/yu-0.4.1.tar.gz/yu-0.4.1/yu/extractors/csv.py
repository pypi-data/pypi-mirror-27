from . import base

SkipField = base.SkipField
PassField = base.PassField
StringField = base.StringField
IntegerField = base.IntegerField
FloatField = base.FloatField
DateField = base.DateField
RowExtractor = base.RowExtractor

format_error_message = base.format_error_message


def extract(reader, fields=None, default=None, headers=0):
    row_extractor = RowExtractor(fields=fields, default=default)
    for row in reader:
        if headers:
            headers -= 1
            continue
        yield row_extractor.extract(row)
