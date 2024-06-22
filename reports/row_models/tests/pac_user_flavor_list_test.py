# reports/row_models/tests/pac_user_flavor_list_test.py
"""
This module contains unit tests for the
`ReportItemPacUserFlavorList` class.
The `ReportItemPacUserFlavorList` class represents a
report item for a pac Pac User Flavor List Report.
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
from reports.row_models.pac_user_flavor_list import ReportItemPacUserFlavorList
class TestReportItemPacUserFlavorList:
    """
    Test class for the
    ReportItemPacUserFlavorList model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacUserFlavorList()
        assert report_item.flavor_code.int == 0
        assert report_item.flavor_description == ""
        assert report_item.flavor_display_order == 0
        assert report_item.flavor_is_active is False
        assert report_item.flavor_lookup_enum_name == ""
        assert report_item.flavor_name == ""
        assert report_item.pac_name == ""
# endset
    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "flavor_code": str(UUID(int=2)),
            "flavor_description": "test",
            "flavor_display_order": 1,
            "flavor_is_active": True,
            "flavor_lookup_enum_name": "test",
            "flavor_name": "test",
            "pac_name": "test",
# endset  # noqa: E122
        }
        # report_item = ReportItemPacUserFlavorList(**data)
        report_item = ReportItemPacUserFlavorList()
        report_item.load_data_provider_dict(data)
        assert report_item.flavor_code == UUID(int=2)
        assert report_item.flavor_description == "test"
        assert report_item.flavor_display_order == 1
        assert report_item.flavor_is_active is True
        assert report_item.flavor_lookup_enum_name == "test"
        assert report_item.flavor_name == "test"
        assert report_item.pac_name == "test"
# endset

