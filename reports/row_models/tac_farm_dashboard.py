# reports/row_models/tac_farm_dashboard.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemTacFarmDashboard class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemTacFarmDashboard():  # pylint: disable=too-few-public-methods
    """
    Represents a report item for a
    tac Farm Dashboard.
    """
    field_one_plant_list_link_land_code: uuid.UUID = (
        uuid.UUID(int=0))
    conditional_btn_example_link_land_code: uuid.UUID = (
        uuid.UUID(int=0))
    is_conditional_btn_available: bool = False
    test_file_download_link_pac_code: uuid.UUID = (
        uuid.UUID(int=0))
    test_conditional_file_download_link_pac_code: uuid.UUID = (
        uuid.UUID(int=0))
    test_async_flow_req_link_pac_code: uuid.UUID = (
        uuid.UUID(int=0))
    test_conditional_async_flow_req_link_pac_code: uuid.UUID = (
        uuid.UUID(int=0))

    def load_data_provider_dict(
            self, data: dict):
        """
        Loads data from a dictionary into the report item.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            None
        """
        self.field_one_plant_list_link_land_code = (
            TypeConversion.get_uuid(data["field_one_plant_list_link_land_code"]))
        self.conditional_btn_example_link_land_code = (
            TypeConversion.get_uuid(data["conditional_btn_example_link_land_code"]))
        self.is_conditional_btn_available = (
            bool(data["is_conditional_btn_available"]))
        self.test_file_download_link_pac_code = (
            TypeConversion.get_uuid(
                data["test_file_download_link_pac_code"])
        )
        self.test_conditional_file_download_link_pac_code = (
            TypeConversion.get_uuid(
                data["test_conditional_file_download_link_pac_code"])
        )
        self.test_async_flow_req_link_pac_code = (
            TypeConversion.get_uuid(
                data["test_async_flow_req_link_pac_code"])
        )
        self.test_conditional_async_flow_req_link_pac_code = (
            TypeConversion.get_uuid(
                data["test_conditional_async_flow_req_link_pac_code"])
        )
