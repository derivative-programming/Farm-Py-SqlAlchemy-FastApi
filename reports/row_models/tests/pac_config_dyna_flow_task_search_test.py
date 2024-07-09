# reports/row_models/tests/pac_config_dyna_flow_task_search_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemPacConfigDynaFlowTaskSearch` class.

The `ReportItemPacConfigDynaFlowTaskSearch` class represents a
report item for a pac Dyna Flow Task Search.
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
from reports.row_models.pac_config_dyna_flow_task_search import (
    ReportItemPacConfigDynaFlowTaskSearch)


class TestReportItemPacConfigDynaFlowTaskSearch:
    """
    Test class for the
    ReportItemPacConfigDynaFlowTaskSearch model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacConfigDynaFlowTaskSearch()
        assert report_item.started_utc_date_time == (
            TypeConversion.get_default_date_time())
        assert report_item.processor_identifier == ""
        assert report_item.is_started is False
        assert report_item.is_completed is False
        assert report_item.is_successful is False
        assert report_item.dyna_flow_task_code.int == 0

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "started_utc_date_time":
                datetime(2023, 1, 1, 0, 0, 0),  # "2023-01-01T00:00:00",
            "processor_identifier": "test",
            "is_started": True,
            "is_completed": True,
            "is_successful": True,
            "dyna_flow_task_code": str(UUID(int=2)),
# endset  # noqa: E122
        }
        report_item = ReportItemPacConfigDynaFlowTaskSearch()
        report_item.load_data_provider_dict(data)
        assert report_item.started_utc_date_time == (
            datetime.fromisoformat("2023-01-01T00:00:00"))
        assert report_item.processor_identifier == "test"
        assert report_item.is_started is True
        assert report_item.is_completed is True
        assert report_item.is_successful is True
        assert report_item.dyna_flow_task_code == UUID(int=2)
