# reports/row_models/tests/pac_user_tac_list_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemPacUserTacList` class.

The `ReportItemPacUserTacList` class represents a
report item for a pac Pac User Tac List Report.
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
from reports.row_models.pac_user_tac_list import (
    ReportItemPacUserTacList)


class TestReportItemPacUserTacList:
    """
    Test class for the
    ReportItemPacUserTacList model.
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
# endset  # noqa: E122
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
