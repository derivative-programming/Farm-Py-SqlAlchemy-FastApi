# helpers/type_conversion.py

"""
This module provides helper functions and classes for type conversion.
"""

from datetime import date, datetime, timezone
import uuid
from marshmallow import fields


class TypeConversion:
    """
    This class provides static methods for type conversion.
    """

    @staticmethod
    def get_default_date():
        """
        Returns the default date (January 1, 1753).
        """
        return date(1753, 1, 1)

    @staticmethod
    def get_default_date_time() -> datetime:
        """
        Returns the default datetime (January 1, 1753, 00:00:00).
        """
        return datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)

    @staticmethod
    def get_default_dt() -> datetime:
        """
        Returns the default datetime (January 1, 1753, 00:00:00).
        """
        return datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)

    @staticmethod
    def get_default_uuid():
        """
        Returns the default UUID (0).
        """
        return uuid.UUID(int=0)

    @staticmethod
    def get_uuid(val) -> uuid.UUID:
        """
        Converts the given value to a UUID object.

        Args:
            val: The value to be converted.

        Returns:
            A UUID object.

        Raises:
            ValueError: If the value cannot be converted to a UUID.
        """
        if isinstance(val, uuid.UUID):
            return val
        else:
            return uuid.UUID(val)

    @staticmethod
    def date_to_iso_format_z(val: datetime) -> str:
        """
        Converts the given date to an ISO 8601 string with 'Z' notation.
        """
        # Get the ISO 8601 string with +00:00 notation
        iso_format_str = val.isoformat()

        # Convert to 'Z' notation if the timezone is UTC
        if iso_format_str.endswith('+00:00'):
            return iso_format_str[:-6] + 'Z'
        return iso_format_str


class UUIDField(fields.Field):
    """
    A custom field for UUID serialization and deserialization.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        """
        Serializes the UUID value to a string.

        Args:
            value: The UUID value to be serialized.
            attr: The attribute name.
            obj: The object being serialized.

        Returns:
            The serialized UUID as a string.
        """
        if value is None:
            return ''
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Deserializes the string value to a UUID object.

        Args:
            value: The string value to be deserialized.
            attr: The attribute name.
            data: The data being deserialized.

        Returns:
            A UUID object.

        Raises:
            ValueError: If the value cannot be deserialized to a UUID.
        """
        return uuid.UUID(value)
