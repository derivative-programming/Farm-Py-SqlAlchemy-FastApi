from dataclasses import dataclass
import json
import uuid
from typing import List
from reports.providers.plant_user_details import ReportProviderPlantUserDetails
from reports.row_models.plant_user_details import ReportItemPlantUserDetails
import logging
from .report_request_validation_error import ReportRequestValidationError
from helpers import SessionContext
from datetime import date, datetime
from decimal import Decimal
from helpers import SessionContext,TypeConversion
from sqlalchemy.ext.asyncio import AsyncSession
class ReportManagerPlantUserDetails():
    _session_context:SessionContext
    _session:AsyncSession
    def __init__(self, session:AsyncSession, session_context:SessionContext):
        self._session_context = session_context
        self._session = session
    async def generate(self,
                plant_code:uuid,

                page_number:int = 1,
                item_count_per_page:int = 1,
                order_by_column_name:str ="",
                order_by_descending:bool = False,
                ) -> List[ReportItemPlantUserDetails]:
        logging.debug('ReportManagerPlantUserDetails.generate Start')
        role_required = "User"
        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                raise ReportRequestValidationError("","Unautorized access. " + role_required + " role not found.")
        if item_count_per_page <= 0:
            raise ReportRequestValidationError("item_count_per_page","Minimum count per page is 1")
        if page_number <= 0:
            raise ReportRequestValidationError("page_number","Minimum page number is 1")
        provider = ReportProviderPlantUserDetails(self._session, self._session_context)
        dataList = await provider.generate_list(
            plant_code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending,
            )
        result = list()
        for dataItem in dataList:
            reportItem:ReportItemPlantUserDetails = ReportItemPlantUserDetails()
            reportItem.load_data_provider_dict(dataItem)
            result.append(reportItem)
        logging.debug("ReportManagerPlantUserDetails.generate Results: " + json.dumps(dataList))
        logging.debug('ReportManagerPlantUserDetails.generate End')
        return result

