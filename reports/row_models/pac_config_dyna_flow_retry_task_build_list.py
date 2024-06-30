# pac_config_dyna_flow_retry_task_build_list.py
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacConfigDynaFlowRetryTaskBuildList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacConfigDynaFlowRetryTaskBuildList():
    """
    Represents a report item for a
    pac Dyna Flow Retry Task Build List.
    """
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
        self.dyna_flow_code = (
            TypeConversion.get_uuid(data["dyna_flow_code"]))
