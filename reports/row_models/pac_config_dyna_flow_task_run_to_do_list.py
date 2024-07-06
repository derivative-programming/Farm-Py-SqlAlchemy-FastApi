# reports/row_models/pac_config_dyna_flow_task_run_to_do_list.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacConfigDynaFlowTaskRunToDoList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacConfigDynaFlowTaskRunToDoList():  # pylint: disable=too-few-public-methods
    """
    Represents a report item for a
    pac Dyna Flow Task.
    """
    dyna_flow_task_code: uuid.UUID = (
        uuid.UUID(int=0))
    is_run_task_debug_required: bool = False
    run_order: int = 0
    dyna_flow_priority_level: int = 0

    def load_data_provider_dict(
            self, data: dict):
        """
        Loads data from a dictionary into the report item.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            None
        """
        self.dyna_flow_task_code = (
            TypeConversion.get_uuid(data["dyna_flow_task_code"]))
        self.is_run_task_debug_required = (
            bool(data["is_run_task_debug_required"]))
        self.run_order = (
            int(data["run_order"]))
        self.dyna_flow_priority_level = (
            int(data["dyna_flow_priority_level"]))
