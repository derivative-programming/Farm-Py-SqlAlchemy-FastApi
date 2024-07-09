# reports/row_models/pac_user_dyna_flow_type_list.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacUserDynaFlowTypeList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacUserDynaFlowTypeList():  # pylint: disable=too-few-public-methods
    """
    Represents a report item for a
    pac Pac User Dyna Flow Type List Report.
    """
    dyna_flow_type_code: uuid.UUID = (
        uuid.UUID(int=0))
    dyna_flow_type_description: str = ""
    dyna_flow_type_display_order: int = 0
    dyna_flow_type_is_active: bool = False
    dyna_flow_type_lookup_enum_name: str = ""
    dyna_flow_type_name: str = ""
    dyna_flow_type_priority_level: int = 0

    def load_data_provider_dict(
            self, data: dict):
        """
        Loads data from a dictionary into the report item.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            None
        """
        self.dyna_flow_type_code = (
            TypeConversion.get_uuid(data["dyna_flow_type_code"]))
        self.dyna_flow_type_description = (
            str(data["dyna_flow_type_description"]))
        self.dyna_flow_type_display_order = (
            int(data["dyna_flow_type_display_order"]))
        self.dyna_flow_type_is_active = (
            bool(data["dyna_flow_type_is_active"]))
        self.dyna_flow_type_lookup_enum_name = (
            str(data["dyna_flow_type_lookup_enum_name"]))
        self.dyna_flow_type_name = (
            str(data["dyna_flow_type_name"]))
        self.dyna_flow_type_priority_level = (
            int(data["dyna_flow_type_priority_level"]))
