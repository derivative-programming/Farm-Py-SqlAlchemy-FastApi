# helpers/type_conversion.py

"""
    #TODO add comment
"""

from marshmallow import fields
from datetime import date, datetime
import uuid


class TypeConversion:
    """
    #TODO add comment
    """
    @staticmethod
    def get_default_date():
        return date(1753, 1, 1)

    @staticmethod
    def get_default_date_time() -> datetime:
        return datetime(1753, 1, 1, 0, 0)

    @staticmethod
    def get_default_dt() -> datetime:
        return datetime(1753, 1, 1, 0, 0)

    @staticmethod
    def get_default_uuid():
        return uuid.UUID(int=0)

    @staticmethod
    def get_uuid(val) -> uuid.UUID:
        if isinstance(val, uuid.UUID):
            return val
        else:
            return uuid.UUID(val)


class UUIDField(fields.Field):
    """
    #TODO add comment
    """
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return uuid.UUID(value)
