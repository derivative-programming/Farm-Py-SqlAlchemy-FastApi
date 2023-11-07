from dataclasses import dataclass
import json
import uuid
from typing import List
from reports.providers.pac_user_tri_state_filter_list import ReportProviderPacUserTriStateFilterList
from reports.row_models.pac_user_tri_state_filter_list import ReportItemPacUserTriStateFilterList
import logging
from .report_request_validation_error import ReportRequestValidationError
from helpers import SessionContext
from datetime import date, datetime
from decimal import Decimal
from helpers import SessionContext,TypeConversion
from sqlalchemy.ext.asyncio import AsyncSession
class ReportManagerPacUserTriStateFilterList():
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
                ) -> List[ReportItemPacUserTriStateFilterList]:
        logging.debug('ReportManagerPacUserTriStateFilterList.generate Start')
        role_required = ""
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                raise ReportRequestValidationError("","Unautorized access. " + role_required + " role not found.")
        if item_count_per_page <= 0:
            raise ReportRequestValidationError("item_count_per_page","Minimum count per page is 1")
        if page_number <= 0:
            raise ReportRequestValidationError("page_number","Minimum page number is 1")
        provider = ReportProviderPacUserTriStateFilterList(self._session, self._session_context)
        dataList = await provider.generate_list(
            pac_code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending,
            )
        result = list()
        for dataItem in dataList:
            reportItem:ReportItemPacUserTriStateFilterList = ReportItemPacUserTriStateFilterList()
            reportItem.load_data_provider_dict(dataItem)
            result.append(reportItem)
        logging.debug("ReportManagerPacUserTriStateFilterList.generate Results: " + json.dumps(dataList))
        logging.debug('ReportManagerPacUserTriStateFilterList.generate End')
        return result
