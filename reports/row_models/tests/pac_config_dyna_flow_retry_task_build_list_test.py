# reports/row_models/tests/pac_config_dyna_flow_retry_task_build_list_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemPacConfigDynaFlowRetryTaskBuildList` class.

The `ReportItemPacConfigDynaFlowRetryTaskBuildList` class represents a
report item for a pac Dyna Flow Retry Task Build List.
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
from reports.row_models.pac_config_dyna_flow_retry_task_build_list import (
    ReportItemPacConfigDynaFlowRetryTaskBuildList)


class TestReportItemPacConfigDynaFlowRetryTaskBuildList:
    """
    Test class for the
    ReportItemPacConfigDynaFlowRetryTaskBuildList model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacConfigDynaFlowRetryTaskBuildList()
        assert report_item.dyna_flow_code.int == 0

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "dyna_flow_code": str(UUID(int=2)),
# endset  # noqa: E122
        }
        report_item = ReportItemPacConfigDynaFlowRetryTaskBuildList()
        report_item.load_data_provider_dict(data)
        assert report_item.dyna_flow_code == UUID(int=2)
