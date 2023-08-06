from . import base

SkipField = base.SkipField
PassField = base.PassField
StringField = base.StringField
IntegerField = base.IntegerField
FloatField = base.FloatField
DateField = base.DateField
RowExtractor = base.RowExtractor


def extract(reader, fields=None, default=None, headers=0, skip_headers=True):
    row_extractor = RowExtractor(fields=fields, default=default)
    for row in reader:
        if headers:
            headers -= 1
            if not skip_headers:
                yield row
        yield row_extractor.extract(row)
