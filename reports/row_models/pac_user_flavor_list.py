# pac_user_flavor_list.py

"""
This module contains the definition of the
ReportItemPacUserFlavorList class.
"""

import uuid
from decimal import Decimal
from datetime import datetime, date

from helpers.type_conversion import TypeConversion


class ReportItemPacUserFlavorList():
    """
    Represents a report item for a pac Pac User Flavor List Report.
    """
    flavor_code: uuid.UUID = (
        uuid.UUID(int=0))
    flavor_description: str = ""
    flavor_display_order: int = 0
    flavor_is_active: bool = False
    flavor_lookup_enum_name: str = ""
    flavor_name: str = ""
    pac_name: str = ""

    def load_data_provider_dict(self, data: dict):
        """
        Loads data from a dictionary into the report item.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            None
        """
        self.flavor_code = (
            TypeConversion.get_uuid(data["flavor_code"]))
        self.flavor_description = (
            str(data["flavor_description"]))
        self.flavor_display_order = (
            int(data["flavor_display_order"]))
        self.flavor_is_active = (
            bool(data["flavor_is_active"]))
        self.flavor_lookup_enum_name = (
            str(data["flavor_lookup_enum_name"]))
        self.flavor_name = (
            str(data["flavor_name"]))
        self.pac_name = (
            str(data["pac_name"]))

