from dataclasses import dataclass
import json
import uuid
from typing import List
from reports.providers import ReportProviderPacUserRoleList
from reports.row_models import ReportItemPacUserRoleList
import logging
from .report_request_validation_error import ReportRequestValidationError
from helpers import SessionContext
from datetime import date, datetime
from decimal import Decimal
from helpers import SessionContext,TypeConversion
from sqlalchemy.ext.asyncio import AsyncSession
class ReportManagerPacUserRoleList():
    _session_context:SessionContext
    def __init__(self, session_context:SessionContext):
        self._session_context = session_context
    def generate(self,
                pac_code:uuid,

                page_number:int = 1,
                item_count_per_page:int = 1,
                order_by_column_name:str ="",
                order_by_descending:bool = False,
                ) -> List[ReportItemPacUserRoleList]:
        logging.debug('ReportManagerPacUserRoleList.generate Start')
        role_required = ""
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                raise ReportRequestValidationError("","Unautorized access. " + role_required + " role not found.")
        if item_count_per_page <= 0:
            raise ReportRequestValidationError("item_count_per_page","Minimum count per page is 1")
        if page_number <= 0:
            raise ReportRequestValidationError("page_number","Minimum page number is 1")
        provider = ReportProviderPacUserRoleList(self._session_context)
        dataList = provider.generate_list(
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
        logging.debug("ReportManagerPacUserRoleList.generate Results: " + json.dumps(dataList))
        logging.debug('ReportManagerPacUserRoleList.generate End')
        return result

