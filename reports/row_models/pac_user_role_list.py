# reports/row_models/pac_user_role_list.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacUserRoleList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacUserRoleList():  # pylint: disable=too-few-public-methods
    """
    Represents a report item for a
    pac Pac User Role List Report.
    """
    role_code: uuid.UUID = (
        uuid.UUID(int=0))
    role_description: str = ""
    role_display_order: int = 0
    role_is_active: bool = False
    role_lookup_enum_name: str = ""
    role_name: str = ""
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
        self.role_code = (
            TypeConversion.get_uuid(data["role_code"]))
        self.role_description = (
            str(data["role_description"]))
        self.role_display_order = (
            int(data["role_display_order"]))
        self.role_is_active = (
            bool(data["role_is_active"]))
        self.role_lookup_enum_name = (
            str(data["role_lookup_enum_name"]))
        self.role_name = (
            str(data["role_name"]))
        self.pac_name = (
            str(data["pac_name"]))
