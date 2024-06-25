# pac_user_tri_state_filter_list.py
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacUserTriStateFilterList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion


class ReportItemPacUserTriStateFilterList():
    """
    Represents a report item for a
    pac Pac User Tri State Filter List Report.
    """
    tri_state_filter_code: uuid.UUID = (
        uuid.UUID(int=0))
    tri_state_filter_description: str = ""
    tri_state_filter_display_order: int = 0
    tri_state_filter_is_active: bool = False
    tri_state_filter_lookup_enum_name: str = ""
    tri_state_filter_name: str = ""
    tri_state_filter_state_int_value: int = 0

    def load_data_provider_dict(
            self, data: dict):
        """
        Loads data from a dictionary into the report item.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            None
        """
        self.tri_state_filter_code = (
            TypeConversion.get_uuid(data["tri_state_filter_code"]))
        self.tri_state_filter_description = (
            str(data["tri_state_filter_description"]))
        self.tri_state_filter_display_order = (
            int(data["tri_state_filter_display_order"]))
        self.tri_state_filter_is_active = (
            bool(data["tri_state_filter_is_active"]))
        self.tri_state_filter_lookup_enum_name = (
            str(data["tri_state_filter_lookup_enum_name"]))
        self.tri_state_filter_name = (
            str(data["tri_state_filter_name"]))
        self.tri_state_filter_state_int_value = (
            int(data["tri_state_filter_state_int_value"]))

