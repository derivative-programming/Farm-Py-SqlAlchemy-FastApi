# helpers/type_conversion.py

"""
    #TODO add comment
"""

from datetime import date, datetime
import uuid
from marshmallow import fields


class TypeConversion:
    """
    #TODO add comment
    """
    @staticmethod
    def get_default_date():
        """
        #TODO add comment
        """

        return date(1753, 1, 1)

    @staticmethod
    def get_default_date_time() -> datetime:
        """
        #TODO add comment
        """

        return datetime(1753, 1, 1, 0, 0)

    @staticmethod
    def get_default_dt() -> datetime:
        """
        #TODO add comment
        """

        return datetime(1753, 1, 1, 0, 0)

    @staticmethod
    def get_default_uuid():
        """
        #TODO add comment
        """

        return uuid.UUID(int=0)

    @staticmethod
    def get_uuid(val) -> uuid.UUID:
        """
        #TODO add comment
        """

        if isinstance(val, uuid.UUID):
            return val
        else:
            return uuid.UUID(val)


class UUIDField(fields.Field):
    """
    #TODO add comment
    """
    def _serialize(self, value, attr, obj, **kwargs):
        """
        #TODO add comment
        """

        if value is None:
            return ''
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        """
        #TODO add comment
        """

        return uuid.UUID(value)
