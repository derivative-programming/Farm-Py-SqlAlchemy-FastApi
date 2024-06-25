# tac_farm_dashboard.py

"""
This module contains the definition of the
ReportItemTacFarmDashboard class.
"""

import uuid
from decimal import Decimal
from datetime import datetime, date

from helpers.type_conversion import TypeConversion


class ReportItemTacFarmDashboard():
    """
    Represents a report item for a
    tac Farm Dashboard.
    """
    field_one_plant_list_link_land_code: uuid.UUID = (
        uuid.UUID(int=0))
    conditional_btn_example_link_land_code: uuid.UUID = (
        uuid.UUID(int=0))
    is_conditional_btn_available: bool = False

    def load_data_provider_dict(self, data: dict):
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

