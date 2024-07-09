# reports/row_models/tests/pac_user_dyna_flow_type_list_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemPacUserDynaFlowTypeList` class.

The `ReportItemPacUserDynaFlowTypeList` class represents a
report item for a pac Pac User Dyna Flow Type List Report.
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
from reports.row_models.pac_user_dyna_flow_type_list import (
    ReportItemPacUserDynaFlowTypeList)


class TestReportItemPacUserDynaFlowTypeList:
    """
    Test class for the
    ReportItemPacUserDynaFlowTypeList model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacUserDynaFlowTypeList()
        assert report_item.dyna_flow_type_code.int == 0
        assert report_item.dyna_flow_type_description == ""
        assert report_item.dyna_flow_type_display_order == 0
        assert report_item.dyna_flow_type_is_active is False
        assert report_item.dyna_flow_type_lookup_enum_name == ""
        assert report_item.dyna_flow_type_name == ""
        assert report_item.dyna_flow_type_priority_level == 0

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "dyna_flow_type_code": str(UUID(int=2)),
            "dyna_flow_type_description": "test",
            "dyna_flow_type_display_order": 1,
            "dyna_flow_type_is_active": True,
            "dyna_flow_type_lookup_enum_name": "test",
            "dyna_flow_type_name": "test",
            "dyna_flow_type_priority_level": 1,
# endset  # noqa: E122
        }
        report_item = ReportItemPacUserDynaFlowTypeList()
        report_item.load_data_provider_dict(data)
        assert report_item.dyna_flow_type_code == UUID(int=2)
        assert report_item.dyna_flow_type_description == "test"
        assert report_item.dyna_flow_type_display_order == 1
        assert report_item.dyna_flow_type_is_active is True
        assert report_item.dyna_flow_type_lookup_enum_name == "test"
        assert report_item.dyna_flow_type_name == "test"
        assert report_item.dyna_flow_type_priority_level == 1
