from marshmallow import fields
from datetime import date, datetime
import uuid

class TypeConversion:

    @staticmethod
    def get_default_date():
        return date(1753,1,1)

    @staticmethod
    def get_default_date_time():
        return datetime(1753,1,1,0,0) 
    
    @staticmethod
    def get_default_uuid():
        return uuid.UUID(int=0) 



class UUIDField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return uuid.UUID(value)