# reports/row_models/tests/pac_user_tri_state_filter_list_test.py
"""
This module contains unit tests for the `ReportItemPacUserTriStateFilterList` class.
The `ReportItemPacUserTriStateFilterList` class represents a
report item for a pac Pac User Tri State Filter List Report.
It contains various fields with default values and
provides methods to load data from a dictionary.
The unit tests in this module ensure that the default
values of the fields are set correctly
and that data can be loaded into the model from a dictionary.
"""
import math
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
from helpers.type_conversion import TypeConversion
from reports.row_models.pac_user_tri_state_filter_list import ReportItemPacUserTriStateFilterList
class TestReportItemPacUserTriStateFilterList:
    """
    Test class for the ReportItemPacUserTriStateFilterList model.
    """
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
# endset
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
# endset  # noqa: E122
        }
        # report_item = ReportItemPacUserTriStateFilterList(**data)
        report_item = ReportItemPacUserTriStateFilterList()
        report_item.load_data_provider_dict(data)
        assert report_item.tri_state_filter_code == UUID(int=2)
        assert report_item.tri_state_filter_description == "test"
        assert report_item.tri_state_filter_display_order == 1
        assert report_item.tri_state_filter_is_active is True
        assert report_item.tri_state_filter_lookup_enum_name == "test"
        assert report_item.tri_state_filter_name == "test"
        assert report_item.tri_state_filter_state_int_value == 1
# endset

