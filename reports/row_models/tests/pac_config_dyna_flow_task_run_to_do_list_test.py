# reports/row_models/tests/pac_config_dyna_flow_task_run_to_do_list_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains unit tests for the
`ReportItemPacConfigDynaFlowTaskRunToDoList` class.

The `ReportItemPacConfigDynaFlowTaskRunToDoList` class represents a
report item for a pac Dyna Flow Task.
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
from reports.row_models.pac_config_dyna_flow_task_run_to_do_list import (
    ReportItemPacConfigDynaFlowTaskRunToDoList)


class TestReportItemPacConfigDynaFlowTaskRunToDoList:
    """
    Test class for the
    ReportItemPacConfigDynaFlowTaskRunToDoList model.
    """
    def test_default_values(self):
        """Test the default values of all fields."""
        report_item = ReportItemPacConfigDynaFlowTaskRunToDoList()
        assert report_item.dyna_flow_task_code.int == 0
        assert report_item.is_run_task_debug_required is False
        assert report_item.run_order == 0
        assert report_item.dyna_flow_priority_level == 0

    def test_load_data_provider_dict(self):
        """Test loading data into the model from a dictionary."""
        data = {
            "dyna_flow_task_code": str(UUID(int=2)),
            "is_run_task_debug_required": True,
            "run_order": 1,
            "dyna_flow_priority_level": 1,
# endset  # noqa: E122
        }

        # report_item = ReportItemPacConfigDynaFlowTaskRunToDoList(**data)
        report_item = ReportItemPacConfigDynaFlowTaskRunToDoList()
        report_item.load_data_provider_dict(data)
        assert report_item.dyna_flow_task_code == UUID(int=2)
        assert report_item.is_run_task_debug_required is True
        assert report_item.run_order == 1
        assert report_item.dyna_flow_priority_level == 1
