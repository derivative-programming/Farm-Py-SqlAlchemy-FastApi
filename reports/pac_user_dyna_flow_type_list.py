# reports/pac_user_dyna_flow_type_list.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module is the manager for report
'Pac User Dyna Flow Type List'
"""

import json
import csv
import uuid  # noqa: F401
import logging
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List
from helpers import SessionContext, TypeConversion  # noqa: F401
from reports.providers.pac_user_dyna_flow_type_list import (
    ReportProviderPacUserDynaFlowTypeList)
from reports.row_models.pac_user_dyna_flow_type_list import (
    ReportItemPacUserDynaFlowTypeList)
from .report_request_validation_error import (
    ReportRequestValidationError)
from .report_manager_base import ReportManagerBase


class ReportManagerPacUserDynaFlowTypeList(ReportManagerBase):
    """
    This class is the manager of report
    'Pac User Dyna Flow Type List'
    """

    _session_context: SessionContext

    def __init__(self, session_context: SessionContext):
        self._session_context = session_context
        if session_context.session is None:
            raise TypeError(
                "ReportManagerPacUserDynaFlowTypeList.init"
                " session_context has "
                "no session assigned"
            )

    async def generate(
        self,
        pac_code: uuid.UUID,

# endset  # noqa: E122
        page_number: int = 1,
        item_count_per_page: int = 1,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[ReportItemPacUserDynaFlowTypeList]:
        """
        Generate the
        'Pac User Dyna Flow Type List' report.

        Returns:
            List[ReportItemPacUserDynaFlowTypeList]: The
                list of report items.
        """
        logging.info("ReportManagerPacUserDynaFlowTypeList"
                     ".generate"
                     " Start")

        role_required = ""

        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                raise ReportRequestValidationError(
                    "",
                    f"Unauthorized access. {role_required} role not found."
                )

        if item_count_per_page <= 0:
            raise ReportRequestValidationError(
                "item_count_per_page",
                "Minimum count per page is 1"
            )

        if page_number <= 0:
            raise ReportRequestValidationError("page_number",
                                               "Minimum page number is 1")

        provider = ReportProviderPacUserDynaFlowTypeList(
            self._session_context)

        data_list = await provider.generate_list(
            pac_code,

# endset  # noqa: E122
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending,
        )

        result = []

        for data_item in data_list:
            report_item: ReportItemPacUserDynaFlowTypeList = \
                ReportItemPacUserDynaFlowTypeList()
            report_item.load_data_provider_dict(data_item)
            result.append(report_item)

        logging.info(
            "ReportManagerPacUserDynaFlowTypeList"
            ".generate Results: %s",
            json.dumps(data_list)
        )

        logging.info("ReportManagerPacUserDynaFlowTypeList"
                     ".generate End")
        return result

    async def build_csv(
        self,
        file_name: str,
        data_list: List[ReportItemPacUserDynaFlowTypeList]
    ):
        """
        Build a CSV file for the
        'Pac User Dyna Flow Type List' report.

        Args:
            file_name (str): The name of the CSV file.
            data_list (List[ReportItemPacUserDynaFlowTypeList]):
                The list of report items.
        """
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=vars(
                    ReportItemPacUserDynaFlowTypeList()).keys(),
                quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for obj in data_list:
                writer.writerow(obj.__dict__)

    async def read_csv(
        self,
        file_name: str
    ) -> List[ReportItemPacUserDynaFlowTypeList]:
        """
        Read a CSV file and return a
        list of report items.

        Args:
            file_name (str): The name of the CSV file.

        Returns:
            List[ReportItemPacUserDynaFlowTypeList]:
                The list of report items.
        """
        objects = []
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                obj = ReportItemPacUserDynaFlowTypeList()
                for key, value in row.items():
                    if value is None:
                        continue
                    if value == '':
                        continue
                    if hasattr(obj, key):
                        # Convert the value to the correct type
                        # based on the attribute
                        attr_type = type(getattr(obj, key))
                        converted_value = self._convert_value(value, attr_type)
                        setattr(obj, key, converted_value)
                objects.append(obj)
        return objects
