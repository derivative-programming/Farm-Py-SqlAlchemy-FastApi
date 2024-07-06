# reports/row_models/tests/pac_config_dyna_flow_dft_build_to_do_list_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemPacConfigDynaFlowDFTBuildToDoList` class.

The `ReportItemPacConfigDynaFlowDFTBuildToDoList` class represents a
report item for a pac Dyna Flow Build Tasks Todo List.
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
from reports.row_models.pac_config_dyna_flow_dft_build_to_do_list import (
    ReportItemPacConfigDynaFlowDFTBuildToDoList)


class TestReportItemPacConfigDynaFlowDFTBuildToDoList:
    """
    Test class for the
    ReportItemPacConfigDynaFlowDFTBuildToDoList model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacConfigDynaFlowDFTBuildToDoList()
        assert report_item.dyna_flow_type_name == ""
        assert report_item.description == ""
        assert report_item.requested_utc_date_time == (
            TypeConversion.get_default_date_time())
        assert report_item.is_build_task_debug_required is False
        assert report_item.is_started is False
        assert report_item.started_utc_date_time == (
            TypeConversion.get_default_date_time())
        assert report_item.is_completed is False
        assert report_item.completed_utc_date_time == (
            TypeConversion.get_default_date_time())
        assert report_item.is_successful is False
        assert report_item.dyna_flow_code.int == 0

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "dyna_flow_type_name": "test",
            "description": "test",
            "requested_utc_date_time":
                datetime(2023, 1, 1, 0, 0, 0),  # "2023-01-01T00:00:00",
            "is_build_task_debug_required": True,
            "is_started": True,
            "started_utc_date_time":
                datetime(2023, 1, 1, 0, 0, 0),  # "2023-01-01T00:00:00",
            "is_completed": True,
            "completed_utc_date_time":
                datetime(2023, 1, 1, 0, 0, 0),  # "2023-01-01T00:00:00",
            "is_successful": True,
            "dyna_flow_code": str(UUID(int=2)),
# endset  # noqa: E122
        }

        # report_item = ReportItemPacConfigDynaFlowDFTBuildToDoList(**data)
        report_item = ReportItemPacConfigDynaFlowDFTBuildToDoList()
        report_item.load_data_provider_dict(data)
        assert report_item.dyna_flow_type_name == "test"
        assert report_item.description == "test"
        assert report_item.requested_utc_date_time == (
            datetime.fromisoformat("2023-01-01T00:00:00"))
        assert report_item.is_build_task_debug_required is True
        assert report_item.is_started is True
        assert report_item.started_utc_date_time == (
            datetime.fromisoformat("2023-01-01T00:00:00"))
        assert report_item.is_completed is True
        assert report_item.completed_utc_date_time == (
            datetime.fromisoformat("2023-01-01T00:00:00"))
        assert report_item.is_successful is True
        assert report_item.dyna_flow_code == UUID(int=2)
