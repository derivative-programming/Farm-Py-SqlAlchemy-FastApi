from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
from helpers.type_conversion import TypeConversion
from reports.row_models.pac_user_date_greater_than_filter_list import ReportItemPacUserDateGreaterThanFilterList
class TestReportItemPacUserDateGreaterThanFilterList:
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacUserDateGreaterThanFilterList()
        assert report_item.date_greater_than_filter_code.int == 0
        assert report_item.date_greater_than_filter_day_count == 0
        assert report_item.date_greater_than_filter_description == ""
        assert report_item.date_greater_than_filter_display_order == 0
        assert report_item.date_greater_than_filter_is_active is False
        assert report_item.date_greater_than_filter_lookup_enum_name == ""
        assert report_item.date_greater_than_filter_name == ""

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "date_greater_than_filter_code": str(UUID(int=2)),
            "date_greater_than_filter_day_count": 1,
            "date_greater_than_filter_description": "test",
            "date_greater_than_filter_display_order": 1,
            "date_greater_than_filter_is_active": True,
            "date_greater_than_filter_lookup_enum_name": "test",
            "date_greater_than_filter_name": "test",

        }
        # report_item = ReportItemPacUserDateGreaterThanFilterList(**data)
        report_item = ReportItemPacUserDateGreaterThanFilterList()
        report_item.load_data_provider_dict(data)
        assert report_item.date_greater_than_filter_code == UUID(int=2)
        assert report_item.date_greater_than_filter_day_count == 1
        assert report_item.date_greater_than_filter_description == "test"
        assert report_item.date_greater_than_filter_display_order == 1
        assert report_item.date_greater_than_filter_is_active is True
        assert report_item.date_greater_than_filter_lookup_enum_name == "test"
        assert report_item.date_greater_than_filter_name == "test"

