# tac_farm_dashboard.py
"""
This module is the manager for report 'Tac Farm Dashboard'
"""
import json
import csv
import uuid
import logging
from datetime import date, datetime
from decimal import Decimal
from typing import List
from helpers import SessionContext, TypeConversion
from reports.providers.tac_farm_dashboard import ReportProviderTacFarmDashboard
from reports.row_models.tac_farm_dashboard import ReportItemTacFarmDashboard
from .report_request_validation_error import ReportRequestValidationError
class ReportManagerTacFarmDashboard():
    """
    This class is the manager of report 'Tac Farm Dashboard'
    """
    _session_context: SessionContext
    def __init__(self, session_context: SessionContext):
        self._session_context = session_context
        if session_context.session is None:
            raise TypeError(
                "ReportManagerTacFarmDashboard.init session_context has "
                "no session assigned"
            )
    async def generate(
        self,
        tac_code: uuid.UUID,

# endset  # noqa: E122
        page_number: int = 1,
        item_count_per_page: int = 1,
        order_by_column_name: str = "",
        order_by_descending: bool = False,
    ) -> List[ReportItemTacFarmDashboard]:
        """
            #TODO add comment
        """
        logging.info('ReportManagerTacFarmDashboard.generate Start')
        role_required = ""
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                raise ReportRequestValidationError(
                    "",
                    "Unautorized access. " + role_required + " role not found."
                )
        if item_count_per_page <= 0:
            raise ReportRequestValidationError(
                "item_count_per_page",
                "Minimum count per page is 1"
            )
        if page_number <= 0:
            raise ReportRequestValidationError("page_number",
                                               "Minimum page number is 1")
        provider = ReportProviderTacFarmDashboard(self._session_context)
        data_list = await provider.generate_list(
            tac_code,

# endset  # noqa: E122
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending,
        )
        result = list()
        for data_item in data_list:
            report_item: ReportItemTacFarmDashboard = ReportItemTacFarmDashboard()
            report_item.load_data_provider_dict(data_item)
            result.append(report_item)
        logging.info(
            "ReportManagerTacFarmDashboard.generate Results: %s",
            json.dumps(data_list)
        )
        logging.info('ReportManagerTacFarmDashboard.generate End')
        return result
    async def build_csv(self,
                        file_name: str,
                        data_list: List[ReportItemTacFarmDashboard]):
        """
            #TODO add comment
        """
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=vars(ReportItemTacFarmDashboard()).keys(),
                quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for obj in data_list:
                writer.writerow(obj.__dict__)
    def _parse_bool(self, value):
        """
            #TODO add comment
        """
        return value.lower() in ['true', '1', 'yes']
    def _convert_value(self, value, attr_type):
        """
            #TODO add comment
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
    async def read_csv(self, file_name: str) -> List[ReportItemTacFarmDashboard]:
        """
            #TODO add comment
        """
        objects = []
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                obj = ReportItemTacFarmDashboard()
                for key, value in row.items():
                    if value is not None and value != '':
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

