import abc


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'{cls_name}({self.message})'


class Validator(abc.ABC):
    @abc.abstractmethod
    def __call__(self, value):
        """检查数据有效性"""


class ValueRangeValidator(Validator):
    min_value_message = '过小: %s < %s'
    max_value_message = '过大: %s > %s'

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value):
        if self.min_value and value < self.min_value:
            message = self.format_message(self.min_value_message, value, self.min_value)
            raise ValidationError(message)
        if self.max_value and value > self.max_value:
            message = self.format_message(self.max_value_message, value, self.max_value)
            raise ValidationError(message)

    def format_message(self, format, value, threshold):
        return format % (self.format_value(value), self.format_value(threshold))

    def format_value(self, value):
        return str(value)


class LengthRangeValidator(ValueRangeValidator):
    min_value_message = '长度过小: %s < %s'
    max_value_message = '长度过大: %s > %s'

    def __call__(self, value):
        return super().__call__(len(value))


class DateRangeValidator(ValueRangeValidator):
    def format_value(self, value):
        return value.strftime('%Y-%m-%d')
