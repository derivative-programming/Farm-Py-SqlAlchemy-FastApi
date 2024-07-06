# reports/row_models/tests/pac_user_date_greater_than_filter_list_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemPacUserDateGreaterThanFilterList` class.

The `ReportItemPacUserDateGreaterThanFilterList` class represents a
report item for a pac Pac User Date Greater Than Filter List Report.
It contains various fields with default values and
provides methods to load data from a dictionary.

The unit tests in this module ensure that the default
values of the fields are set correctly
and that data can be loaded into the model from a dictionary.
"""
import math  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
from uuid import UUID  # noqa: F401
from helpers.type_conversion import TypeConversion  # noqa: F401
from reports.row_models.pac_user_date_greater_than_filter_list import (
    ReportItemPacUserDateGreaterThanFilterList)


class TestReportItemPacUserDateGreaterThanFilterList:
    """
    Test class for the
    ReportItemPacUserDateGreaterThanFilterList model.
    """
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
# endset  # noqa: E122
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
