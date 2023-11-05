import pytest
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
from reports.row_models.pac_user_tri_state_filter_list import ReportItemPacUserTriStateFilterList
class TestReportItemPacUserTriStateFilterList:
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacUserTriStateFilterList()
        assert report_item.tri_state_filter_code.int == 0
        assert report_item.tri_state_filter_description == ""
        assert report_item.tri_state_filter_display_order == 0
        assert report_item.tri_state_filter_is_active is False
        assert report_item.tri_state_filter_lookup_enum_name == ""
        assert report_item.tri_state_filter_name == ""
        assert report_item.tri_state_filter_state_int_value == 0
    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "tri_state_filter_code": str(UUID(int=2)),
            "tri_state_filter_description": "test",
            "tri_state_filter_display_order": 1,
            "tri_state_filter_is_active": True,
            "tri_state_filter_lookup_enum_name": "test",
            "tri_state_filter_name": "test",
            "tri_state_filter_state_int_value": 1,
        }
        report_item = ReportItemPacUserTriStateFilterList(**data)
        # report_item.load_data_provider_dict(data)
        assert report_item.tri_state_filter_code == UUID(int=2)
        assert report_item.tri_state_filter_description == "test"
        assert report_item.tri_state_filter_display_order == 1
        assert report_item.tri_state_filter_is_active is True
        assert report_item.tri_state_filter_lookup_enum_name == "test"
        assert report_item.tri_state_filter_name == "test"
        assert report_item.tri_state_filter_state_int_value == 1

