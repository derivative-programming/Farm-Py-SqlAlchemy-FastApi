# reports/row_models/tests/pac_user_tac_list_test.py
"""
    #TODO add comment
"""
import math
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
from helpers.type_conversion import TypeConversion
from reports.row_models.pac_user_tac_list import ReportItemPacUserTacList
class TestReportItemPacUserTacList:
    """
    #TODO add comment
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacUserTacList()
        assert report_item.tac_code.int == 0
        assert report_item.tac_description == ""
        assert report_item.tac_display_order == 0
        assert report_item.tac_is_active is False
        assert report_item.tac_lookup_enum_name == ""
        assert report_item.tac_name == ""
        assert report_item.pac_name == ""
# endset
    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "tac_code": str(UUID(int=2)),
            "tac_description": "test",
            "tac_display_order": 1,
            "tac_is_active": True,
            "tac_lookup_enum_name": "test",
            "tac_name": "test",
            "pac_name": "test",
# endset
        }
        # report_item = ReportItemPacUserTacList(**data)
        report_item = ReportItemPacUserTacList()
        report_item.load_data_provider_dict(data)
        assert report_item.tac_code == UUID(int=2)
        assert report_item.tac_description == "test"
        assert report_item.tac_display_order == 1
        assert report_item.tac_is_active is True
        assert report_item.tac_lookup_enum_name == "test"
        assert report_item.tac_name == "test"
        assert report_item.pac_name == "test"
# endset

