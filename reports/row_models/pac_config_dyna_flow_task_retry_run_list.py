# reports/row_models/pac_config_dyna_flow_task_retry_run_list.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the definition of the
ReportItemPacConfigDynaFlowTaskRetryRunList class.
"""

import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401

from helpers.type_conversion import TypeConversion  # noqa: F401


class ReportItemPacConfigDynaFlowTaskRetryRunList():  # pylint: disable=too-few-public-methods
    """
    Represents a report item for a
    pac Dyna Flow Task Retry Run List.
    """
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
        self.dyna_flow_task_code = (
            TypeConversion.get_uuid(data["dyna_flow_task_code"]))
