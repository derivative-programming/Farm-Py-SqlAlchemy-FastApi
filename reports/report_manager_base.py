# reports/reprot_manager_base.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module is the base class for report managers.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401


class ReportManagerBase():
    """
    This class is the base class for report managers.
    """

    def _parse_bool(self, value):
        """
        Parse a boolean value.

        Args:
            value (str): The value to parse.

        Returns:
            bool: The parsed boolean value.
        """
        return value.lower() in ['true', '1', 'yes']

    def _convert_value(self, value, attr_type):
        """
        Convert a value to the specified attribute type.

        Args:
            value: The value to convert.
            attr_type: The attribute type to convert to.

        Returns:
            The converted value.
        """
        if attr_type == int:
            return int(value)
        elif attr_type == bool:
            return self._parse_bool(value)
        elif attr_type == float:
            return float(value)
        elif attr_type == Decimal:
            return Decimal(value)
        elif attr_type == datetime:
            return datetime.fromisoformat(value)
        elif attr_type == date:
            return date.fromisoformat(value)
        elif attr_type == uuid.UUID:
            return uuid.UUID(value)

        return value
