# pac_user_land_list.py
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacUserLandList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacUserLandList():
    """
    Represents a report item for a
    pac Pac User Land List Report.
    """
    land_code: uuid.UUID = (
        uuid.UUID(int=0))
    land_description: str = ""
    land_display_order: int = 0
    land_is_active: bool = False
    land_lookup_enum_name: str = ""
    land_name: str = ""
    pac_name: str = ""

    def load_data_provider_dict(
            self, data: dict):
        """
        Loads data from a dictionary into the report item.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            None
        """
        self.land_code = (
            TypeConversion.get_uuid(data["land_code"]))
        self.land_description = (
            str(data["land_description"]))
        self.land_display_order = (
            int(data["land_display_order"]))
        self.land_is_active = (
            bool(data["land_is_active"]))
        self.land_lookup_enum_name = (
            str(data["land_lookup_enum_name"]))
        self.land_name = (
            str(data["land_name"]))
        self.pac_name = (
            str(data["pac_name"]))
