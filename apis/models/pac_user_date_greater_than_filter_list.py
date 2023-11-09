from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from business.pac import PacBusObj
from helpers import TypeConversion
from reports.row_models.pac_user_date_greater_than_filter_list import ReportItemPacUserDateGreaterThanFilterList
from apis.models.list_model import ListModel
from helpers import SessionContext
from models import Pac
from reports.pac_user_date_greater_than_filter_list import ReportManagerPacUserDateGreaterThanFilterList
from reports.report_request_validation_error import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
### request. expect camel case. use marshmallow to validate.
class PacUserDateGreaterThanFilterListGetModelRequest(SnakeModel):
    page_number:int = 0
    item_count_per_page:int = 0
    order_by_column_name:str = ""
    order_by_descending:bool = False
    force_error_message:str = ""

class PacUserDateGreaterThanFilterListGetModelResponseItem(CamelModel):
    date_greater_than_filter_code:UUID4 = uuid.UUID(int=0)
    date_greater_than_filter_day_count:int = 0
    date_greater_than_filter_description:str = ""
    date_greater_than_filter_display_order:int = 0
    date_greater_than_filter_is_active:bool = False
    date_greater_than_filter_lookup_enum_name:str = ""
    date_greater_than_filter_name:str = ""

    def load_report_item(self,data:ReportItemPacUserDateGreaterThanFilterList):
        self.date_greater_than_filter_code = data.date_greater_than_filter_code
        self.date_greater_than_filter_day_count = data.date_greater_than_filter_day_count
        self.date_greater_than_filter_description = data.date_greater_than_filter_description
        self.date_greater_than_filter_display_order = data.date_greater_than_filter_display_order
        self.date_greater_than_filter_is_active = data.date_greater_than_filter_is_active
        self.date_greater_than_filter_lookup_enum_name = data.date_greater_than_filter_lookup_enum_name
        self.date_greater_than_filter_name = data.date_greater_than_filter_name

class PacUserDateGreaterThanFilterListGetModelResponse(ListModel):
    request:PacUserDateGreaterThanFilterListGetModelRequest = None
    items:List[PacUserDateGreaterThanFilterListGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserDateGreaterThanFilterListGetModelRequest):
        try:
            logging.debug("loading model...PacUserDateGreaterThanFilterListGetModelResponse")
            # pac_bus_obj = PacBusObj(session=session)
            # await pac_bus_obj.load(code=pac_code)
            generator = ReportManagerPacUserDateGreaterThanFilterList(session_context)
            logging.debug("processing...PacUserDateGreaterThanFilterListGetModelResponse")
            items = await generator.generate(
                    pac_code,

                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
            self.items = list()
            for item in items:
                report_item = PacUserDateGreaterThanFilterListGetModelResponseItem()
                report_item.load_report_item(item)
                self.items.append(report_item)
            self.success = True
            self.message = "Success."
        except ReportRequestValidationError as ve:
            self.success = False
            self.message = "Validation Error..."
            self.validation_errors = list()
            for key in ve.error_dict:
                self.message = self.message + ve.error_dict[key] + ','
                # self.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
