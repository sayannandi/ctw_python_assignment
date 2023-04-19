from datetime import datetime, timedelta

from marshmallow import Schema, fields, ValidationError, validates_schema, post_load
from marshmallow.validate import Range, Validator



class DateValidator(Validator):
    default_error_message = "Invalid date"

    def __init__(self, required=False):
        self.required = required
        self.format = '%Y-%m-%d'
    
    def __call__(self, value):
        if not self.required and not value:
            return None
        try:
            datetime.strptime(value, self.format)
        except Exception as ex:

            raise ValidationError("{} is not in the form of {}".format(value,))
        
        return value


class FinancialDataRequestSchema(Schema):
    symbol = fields.Str(load_default=None)
    start_date = fields.Str(required=False, load_default=None, validate=DateValidator())
    end_date = fields.Str(required=False, load_default=None, validate=DateValidator())
    page = fields.Int(load_default=1, validate=Range(min=1))
    limit = fields.Int(load_default=5, validate=Range(min=1))

    @post_load
    def validate_start_end_date(self, data, **kwargs):
        start_date, end_date = data['start_date'], data['end_date']
        if start_date and end_date and start_date > end_date:
            raise ValidationError('start_date must be less than end_date')
        return data

class StatisticsRequestSchema(Schema):
    symbol = fields.Str(required=True)
    start_date = fields.Str(validate=DateValidator(required=True))
    end_date = fields.Str(validate=DateValidator(required=True))

    @post_load
    def validate_start_end_date(self, data, **kwargs):
        start_date, end_date = data['start_date'], data['end_date']
        if start_date and end_date and start_date > end_date:
            raise ValidationError('start_date must be less than end_date')
        return data
