# tac_farm_dashboard_test.py
"""
    #TODO add comment
"""
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
from helpers.type_conversion import TypeConversion
from reports.row_models.tac_farm_dashboard import ReportItemTacFarmDashboard
class TestReportItemTacFarmDashboard:
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemTacFarmDashboard()
        assert report_item.field_one_plant_list_link_land_code.int == 0
        assert report_item.conditional_btn_example_link_land_code.int == 0
        assert report_item.is_conditional_btn_available is False

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "field_one_plant_list_link_land_code": str(UUID(int=5)),
            "conditional_btn_example_link_land_code": str(UUID(int=5)),
            "is_conditional_btn_available": True,

        }
        # report_item = ReportItemTacFarmDashboard(**data)
        report_item = ReportItemTacFarmDashboard()
        report_item.load_data_provider_dict(data)
        assert report_item.field_one_plant_list_link_land_code == UUID(int=5)
        assert report_item.conditional_btn_example_link_land_code == UUID(int=5)
        assert report_item.is_conditional_btn_available is True

