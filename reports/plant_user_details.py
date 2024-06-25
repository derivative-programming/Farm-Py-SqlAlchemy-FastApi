# plant_user_details.py

"""
This module is the manager for report
'Plant User Details'
"""

import json
import csv
import uuid
import logging
from datetime import date, datetime
from decimal import Decimal
from typing import List
from helpers import SessionContext, TypeConversion
from reports.providers.plant_user_details import ReportProviderPlantUserDetails
from reports.row_models.plant_user_details import ReportItemPlantUserDetails
from .report_request_validation_error import ReportRequestValidationError


class ReportManagerPlantUserDetails():
    """
    This class is the manager of report
    'Plant User Details'
    """

    _session_context: SessionContext

    def __init__(self, session_context: SessionContext):
        self._session_context = session_context
        if session_context.session is None:
            raise TypeError(
                "ReportManagerPlantUserDetails.init"
                " session_context has "
                "no session assigned"
            )

    async def generate(
        self,
        plant_code: uuid.UUID,

# endset  # noqa: E122
        page_number: int = 1,
        item_count_per_page: int = 1,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[ReportItemPlantUserDetails]:
        """
        Generate the
        'Plant User Details' report.

        Returns:
            List[ReportItemPlantUserDetails]: The
                list of report items.
        """
        logging.info("ReportManagerPlantUserDetails.generate"
                     " Start")

        role_required = "User"

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

        provider = ReportProviderPlantUserDetails(
            self._session_context)

        data_list = await provider.generate_list(
            plant_code,

# endset  # noqa: E122
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending,
        )

        result = list()

        for data_item in data_list:
            report_item: ReportItemPlantUserDetails = \
                ReportItemPlantUserDetails()
            report_item.load_data_provider_dict(data_item)
            result.append(report_item)

        logging.info(
            "ReportManagerPlantUserDetails.generate Results: %s",
            json.dumps(data_list)
        )

        logging.info('ReportManagerPlantUserDetails.generate End')
        return result

    async def build_csv(
        self,
        file_name: str,
        data_list: List[ReportItemPlantUserDetails]
    ):
        """
        Build a CSV file for the
        'Plant User Details' report.

        Args:
            file_name (str): The name of the CSV file.
            data_list (List[ReportItemPlantUserDetails]):
                The list of report items.
        """
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=vars(
                    ReportItemPlantUserDetails()).keys(),
                quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for obj in data_list:
                writer.writerow(obj.__dict__)

    def _parse_bool(self, value):
        """
        Parse a boolean value.

        Args:
            value (str): The value to parse.

        Returns:
            bool: The parsed boolean value.
        """
        return value.lower() in ['true', '1', 'yes']

    def _convert_value(self, value, attr_type):
        """
        Convert a value to the specified attribute type.

        Args:
            value: The value to convert.
            attr_type: The attribute type to convert to.

        Returns:
            The converted value.
        """
        if attr_type == int:
            return int(value)
        elif attr_type == bool:
            return self._parse_bool(value)
        elif attr_type == float:
            return float(value)
        elif attr_type == Decimal:
            return Decimal(value)
        elif attr_type == datetime:
            return datetime.fromisoformat(value)
        elif attr_type == date:
            return date.fromisoformat(value)
        elif attr_type == uuid.UUID:
            return uuid.UUID(value)
        else:
            return value

    async def read_csv(
        self,
        file_name: str
    ) -> List[ReportItemPlantUserDetails]:
        """
        Read a CSV file and return a
        list of report items.

        Args:
            file_name (str): The name of the CSV file.

        Returns:
            List[ReportItemPlantUserDetails]:
                The list of report items.
        """
        objects = []
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                obj = ReportItemPlantUserDetails()
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
                        # if attr_type == int:
                        #     setattr(obj, key, int(value))
                        # elif attr_type == bool:
                        #     setattr(obj, key, self._parse_bool(value))
                        # elif attr_type == float:
                        #     setattr(obj, key, float(value))
                        # elif attr_type == Decimal:
                        #     setattr(obj, key, Decimal(value))
                        # elif attr_type == datetime:
                        #     setattr(obj, key, datetime.fromisoformat(value))
                        # elif attr_type == date:
                        #     setattr(obj, key, date.fromisoformat(value))
                        # elif attr_type == uuid.UUID:
                        #     setattr(obj, key, uuid.UUID(value))
                        # else:
                        #     setattr(obj, key, value)
                objects.append(obj)
        return objects

