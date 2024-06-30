# pac_config_dyna_flow_dft_build_to_do_list.py
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacConfigDynaFlowDFTBuildToDoList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacConfigDynaFlowDFTBuildToDoList():
    """
    Represents a report item for a
    pac Dyna Flow Build Tasks Todo List.
    """
    dyna_flow_type_name: str = ""
    description: str = ""
    requested_utc_date_time: datetime = (
        TypeConversion.get_default_date_time())
    is_build_task_debug_required: bool = False
    is_started: bool = False
    started_utc_date_time: datetime = (
        TypeConversion.get_default_date_time())
    is_completed: bool = False
    completed_utc_date_time: datetime = (
        TypeConversion.get_default_date_time())
    is_successful: bool = False
    dyna_flow_code: uuid.UUID = (
        uuid.UUID(int=0))

    def load_data_provider_dict(
            self, data: dict):
        """
        Loads data from a dictionary into the report item.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            None
        """
        self.dyna_flow_type_name = (
            str(data["dyna_flow_type_name"]))
        self.description = (
            str(data["description"]))
        self.requested_utc_date_time = (
            data["requested_utc_date_time"])
        self.is_build_task_debug_required = (
            bool(data["is_build_task_debug_required"]))
        self.is_started = (
            bool(data["is_started"]))
        self.started_utc_date_time = (
            data["started_utc_date_time"])
        self.is_completed = (
            bool(data["is_completed"]))
        self.completed_utc_date_time = (
            data["completed_utc_date_time"])
        self.is_successful = (
            bool(data["is_successful"]))
        self.dyna_flow_code = (
            TypeConversion.get_uuid(data["dyna_flow_code"]))
