# reports/pac_config_dyna_flow_task_search.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module is the manager for report
'Pac Config Dyna Flow Task Search'
"""

import json
import csv
import uuid  # noqa: F401
import logging
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List
from helpers import SessionContext, TypeConversion  # noqa: F401
from reports.providers.pac_config_dyna_flow_task_search import (
    ReportProviderPacConfigDynaFlowTaskSearch)
from reports.row_models.pac_config_dyna_flow_task_search import (
    ReportItemPacConfigDynaFlowTaskSearch)
from .report_request_validation_error import (
    ReportRequestValidationError)
from .report_manager_base import ReportManagerBase


class ReportManagerPacConfigDynaFlowTaskSearch(ReportManagerBase):
    """
    This class is the manager of report
    'Pac Config Dyna Flow Task Search'
    """

    _session_context: SessionContext

    def __init__(self, session_context: SessionContext):
        self._session_context = session_context
        if session_context.session is None:
            raise TypeError(
                "ReportManagerPacConfigDynaFlowTaskSearch.init"
                " session_context has "
                "no session assigned"
            )

    async def generate(
        self,
        pac_code: uuid.UUID,
        started_date_greater_than_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        processor_identifier:
            str = "",
        is_started_tri_state_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        is_completed_tri_state_filter_code:
            uuid.UUID = uuid.UUID(int=0),
        is_successful_tri_state_filter_code:
            uuid.UUID = uuid.UUID(int=0),
# endset  # noqa: E122
        page_number: int = 1,
        item_count_per_page: int = 1,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[ReportItemPacConfigDynaFlowTaskSearch]:
        """
        Generate the
        'Pac Config Dyna Flow Task Search' report.

        Returns:
            List[ReportItemPacConfigDynaFlowTaskSearch]: The
                list of report items.
        """
        logging.info("ReportManagerPacConfigDynaFlowTaskSearch"
                     ".generate"
                     " Start")

        role_required = "Config"

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

        provider = ReportProviderPacConfigDynaFlowTaskSearch(
            self._session_context)

        data_list = await provider.generate_list(
            pac_code,
            started_date_greater_than_filter_code,
            processor_identifier,
            is_started_tri_state_filter_code,
            is_completed_tri_state_filter_code,
            is_successful_tri_state_filter_code,
# endset  # noqa: E122
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending,
        )

        result = []

        for data_item in data_list:
            report_item: ReportItemPacConfigDynaFlowTaskSearch = \
                ReportItemPacConfigDynaFlowTaskSearch()
            report_item.load_data_provider_dict(data_item)
            result.append(report_item)

        logging.info(
            "ReportManagerPacConfigDynaFlowTaskSearch"
            ".generate Results: %s",
            json.dumps(data_list)
        )

        logging.info("ReportManagerPacConfigDynaFlowTaskSearch"
                     ".generate End")
        return result

    async def build_csv(
        self,
        file_name: str,
        data_list: List[ReportItemPacConfigDynaFlowTaskSearch]
    ):
        """
        Build a CSV file for the
        'Pac Config Dyna Flow Task Search' report.

        Args:
            file_name (str): The name of the CSV file.
            data_list (List[ReportItemPacConfigDynaFlowTaskSearch]):
                The list of report items.
        """
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=vars(
                    ReportItemPacConfigDynaFlowTaskSearch()).keys(),
                quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for obj in data_list:
                writer.writerow(obj.__dict__)

    async def read_csv(
        self,
        file_name: str
    ) -> List[ReportItemPacConfigDynaFlowTaskSearch]:
        """
        Read a CSV file and return a
        list of report items.

        Args:
            file_name (str): The name of the CSV file.

        Returns:
            List[ReportItemPacConfigDynaFlowTaskSearch]:
                The list of report items.
        """
        objects = []
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                obj = ReportItemPacConfigDynaFlowTaskSearch()
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
