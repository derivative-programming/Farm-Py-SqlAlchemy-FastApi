# reports/row_models/pac_user_date_greater_than_filter_list.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacUserDateGreaterThanFilterList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacUserDateGreaterThanFilterList():  # pylint: disable=too-few-public-methods
    """
    Represents a report item for a
    pac Pac User Date Greater Than Filter List Report.
    """
    date_greater_than_filter_code: uuid.UUID = (
        uuid.UUID(int=0))
    date_greater_than_filter_day_count: int = 0
    date_greater_than_filter_description: str = ""
    date_greater_than_filter_display_order: int = 0
    date_greater_than_filter_is_active: bool = False
    date_greater_than_filter_lookup_enum_name: str = ""
    date_greater_than_filter_name: str = ""

    def load_data_provider_dict(
            self, data: dict):
        """
        Loads data from a dictionary into the report item.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            None
        """
        self.date_greater_than_filter_code = (
            TypeConversion.get_uuid(data["date_greater_than_filter_code"]))
        self.date_greater_than_filter_day_count = (
            int(data["date_greater_than_filter_day_count"]))
        self.date_greater_than_filter_description = (
            str(data["date_greater_than_filter_description"]))
        self.date_greater_than_filter_display_order = (
            int(data["date_greater_than_filter_display_order"]))
        self.date_greater_than_filter_is_active = (
            bool(data["date_greater_than_filter_is_active"]))
        self.date_greater_than_filter_lookup_enum_name = (
            str(data["date_greater_than_filter_lookup_enum_name"]))
        self.date_greater_than_filter_name = (
            str(data["date_greater_than_filter_name"]))
