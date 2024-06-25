# reports/row_models/tests/pac_user_land_list_test.py

"""
This module contains unit tests for the
`ReportItemPacUserLandList` class.

The `ReportItemPacUserLandList` class represents a
report item for a pac Pac User Land List Report.
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
from reports.row_models.pac_user_land_list import ReportItemPacUserLandList


class TestReportItemPacUserLandList:
    """
    Test class for the
    ReportItemPacUserLandList model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacUserLandList()
        assert report_item.land_code.int == 0
        assert report_item.land_description == ""
        assert report_item.land_display_order == 0
        assert report_item.land_is_active is False
        assert report_item.land_lookup_enum_name == ""
        assert report_item.land_name == ""
        assert report_item.pac_name == ""

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "land_code": str(UUID(int=2)),
            "land_description": "test",
            "land_display_order": 1,
            "land_is_active": True,
            "land_lookup_enum_name": "test",
            "land_name": "test",
            "pac_name": "test",
# endset  # noqa: E122
        }

        # report_item = ReportItemPacUserLandList(**data)
        report_item = ReportItemPacUserLandList()
        report_item.load_data_provider_dict(data)
        assert report_item.land_code == UUID(int=2)
        assert report_item.land_description == "test"
        assert report_item.land_display_order == 1
        assert report_item.land_is_active is True
        assert report_item.land_lookup_enum_name == "test"
        assert report_item.land_name == "test"
        assert report_item.pac_name == "test"

