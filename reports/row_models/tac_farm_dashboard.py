# tac_farm_dashboard.py
"""
    #TODO add comment
"""
import uuid
from decimal import Decimal
from datetime import datetime, date
from helpers.type_conversion import TypeConversion
class ReportItemTacFarmDashboard():
    """
    #TODO add comment
    """
    field_one_plant_list_link_land_code: uuid.UUID = uuid.UUID(int=0)
    conditional_btn_example_link_land_code: uuid.UUID = uuid.UUID(int=0)
    is_conditional_btn_available: bool = False
# endset
    def load_data_provider_dict(self, data: dict):
        """
        #TODO add comment
        """
        self.field_one_plant_list_link_land_code = (
            TypeConversion.get_uuid(data["field_one_plant_list_link_land_code"]))
        self.conditional_btn_example_link_land_code = (
            TypeConversion.get_uuid(data["conditional_btn_example_link_land_code"]))
        self.is_conditional_btn_available = (
            bool(data["is_conditional_btn_available"]))
# endset

