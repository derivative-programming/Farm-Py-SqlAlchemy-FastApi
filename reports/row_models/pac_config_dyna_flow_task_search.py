# reports/row_models/pac_config_dyna_flow_task_search.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacConfigDynaFlowTaskSearch class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacConfigDynaFlowTaskSearch():  # pylint: disable=too-few-public-methods
    """
    Represents a report item for a
    pac Dyna Flow Task Search.
    """
    started_utc_date_time: datetime = (
        TypeConversion.get_default_date_time())
    processor_identifier: str = ""
    is_started: bool = False
    is_completed: bool = False
    is_successful: bool = False
    dyna_flow_task_code: uuid.UUID = (
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
        self.started_utc_date_time = (
            data["started_utc_date_time"])
        self.processor_identifier = (
            str(data["processor_identifier"]))
        self.is_started = (
            bool(data["is_started"]))
        self.is_completed = (
            bool(data["is_completed"]))
        self.is_successful = (
            bool(data["is_successful"]))
        self.dyna_flow_task_code = (
            TypeConversion.get_uuid(data["dyna_flow_task_code"]))
