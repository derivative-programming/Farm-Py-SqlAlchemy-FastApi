# reports/row_models/tests/pac_user_role_list_test.py
# pylint: disable=unused-import

"""
This module contains unit tests for the
`ReportItemPacUserRoleList` class.

The `ReportItemPacUserRoleList` class represents a
report item for a pac Pac User Role List Report.
It contains various fields with default values and
provides methods to load data from a dictionary.

The unit tests in this module ensure that the default
values of the fields are set correctly
and that data can be loaded into the model from a dictionary.
"""
import math
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
from uuid import UUID  # noqa: F401
from helpers.type_conversion import TypeConversion
from reports.row_models.pac_user_role_list import (
    ReportItemPacUserRoleList)


class TestReportItemPacUserRoleList:
    """
    Test class for the
    ReportItemPacUserRoleList model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacUserRoleList()
        assert report_item.role_code.int == 0
        assert report_item.role_description == ""
        assert report_item.role_display_order == 0
        assert report_item.role_is_active is False
        assert report_item.role_lookup_enum_name == ""
        assert report_item.role_name == ""
        assert report_item.pac_name == ""

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "role_code": str(UUID(int=2)),
            "role_description": "test",
            "role_display_order": 1,
            "role_is_active": True,
            "role_lookup_enum_name": "test",
            "role_name": "test",
            "pac_name": "test",
# endset  # noqa: E122
        }

        # report_item = ReportItemPacUserRoleList(**data)
        report_item = ReportItemPacUserRoleList()
        report_item.load_data_provider_dict(data)
        assert report_item.role_code == UUID(int=2)
        assert report_item.role_description == "test"
        assert report_item.role_display_order == 1
        assert report_item.role_is_active is True
        assert report_item.role_lookup_enum_name == "test"
        assert report_item.role_name == "test"
        assert report_item.pac_name == "test"

