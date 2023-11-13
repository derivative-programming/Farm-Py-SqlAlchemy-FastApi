from dataclasses import dataclass
import json
import csv
import uuid
from typing import List
from reports.providers.pac_user_role_list import ReportProviderPacUserRoleList
from reports.row_models.pac_user_role_list import ReportItemPacUserRoleList
import logging
from .report_request_validation_error import ReportRequestValidationError
from helpers import SessionContext
from datetime import date, datetime
from decimal import Decimal
from helpers import SessionContext,TypeConversion
from sqlalchemy.ext.asyncio import AsyncSession
class ReportManagerPacUserRoleList():
    _session_context:SessionContext
    _session:AsyncSession
    def __init__(self, session:AsyncSession, session_context:SessionContext):
        self._session_context = session_context
        self._session = session
    async def generate(self,
                pac_code:uuid,

                page_number:int = 1,
                item_count_per_page:int = 1,
                order_by_column_name:str ="",
                order_by_descending:bool = False,
                ) -> List[ReportItemPacUserRoleList]:
        logging.info('ReportManagerPacUserRoleList.generate Start')
        role_required = ""
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                raise ReportRequestValidationError("","Unautorized access. " + role_required + " role not found.")
        if item_count_per_page <= 0:
            raise ReportRequestValidationError("item_count_per_page","Minimum count per page is 1")
        if page_number <= 0:
            raise ReportRequestValidationError("page_number","Minimum page number is 1")
        provider = ReportProviderPacUserRoleList(self._session, self._session_context)
        dataList = await provider.generate_list(
            pac_code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending,
            )
        result = list()
        for dataItem in dataList:
            reportItem:ReportItemPacUserRoleList = ReportItemPacUserRoleList()
            reportItem.load_data_provider_dict(dataItem)
            result.append(reportItem)
        logging.info("ReportManagerPacUserRoleList.generate Results: " + json.dumps(dataList))
        logging.info('ReportManagerPacUserRoleList.generate End')
        return result
    async def build_csv(self, file_name:str, data_list:List[ReportItemPacUserRoleList]):
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=vars(ReportItemPacUserRoleList()).keys(), quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for obj in data_list:
                writer.writerow(obj.__dict__)
    def _parse_bool(self, value):
        return value.lower() in ['true', '1', 'yes']
    async def read_csv(self, file_name:str) -> List[ReportItemPacUserRoleList]:
        objects = []
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                obj = ReportItemPacUserRoleList()
                for key, value in row.items():
                    if value is not None and value != '':
                        if hasattr(obj, key):
                            # Convert the value to the correct type based on the attribute
                            attr_type = type(getattr(obj, key))
                            if attr_type == int:
                                setattr(obj, key, int(value))
                            elif attr_type == bool:
                                setattr(obj, key, self.parse_bool(value))
                            elif attr_type == float:
                                setattr(obj, key, float(value))
                            elif attr_type == Decimal:
                                setattr(obj, key, Decimal(value))
                            elif attr_type == datetime:
                                setattr(obj, key, datetime.fromisoformat(value))
                            elif attr_type == date:
                                setattr(obj, key, date.fromisoformat(value))
                            elif attr_type == uuid.UUID:
                                setattr(obj, key, uuid.UUID(value))
                            else:
                                setattr(obj, key, value)
                objects.append(obj)
        return objects

