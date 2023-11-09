from typing import List
from datetime import date, datetime
import uuid
from decimal import Decimal
from business.pac import PacBusObj
from helpers import TypeConversion
from reports.row_models.pac_user_land_list import ReportItemPacUserLandList
from apis.models.list_model import ListModel
from helpers import SessionContext
from models import Pac
from reports.pac_user_land_list import ReportManagerPacUserLandList
from reports.report_request_validation_error import ReportRequestValidationError
import apis.models as view_models
from models import Pac
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from sqlalchemy.ext.asyncio import AsyncSession
### request. expect camel case. use marshmallow to validate.
class PacUserLandListGetModelRequest(SnakeModel):
    page_number:int = 0
    item_count_per_page:int = 0
    order_by_column_name:str = ""
    order_by_descending:bool = False
    force_error_message:str = ""

class PacUserLandListGetModelResponseItem(CamelModel):
    land_code:UUID4 = uuid.UUID(int=0)
    land_description:str = ""
    land_display_order:int = 0
    land_is_active:bool = False
    land_lookup_enum_name:str = ""
    land_name:str = ""
    pac_name:str = ""

    def load_report_item(self,data:ReportItemPacUserLandList):
        self.land_code = data.land_code
        self.land_description = data.land_description
        self.land_display_order = data.land_display_order
        self.land_is_active = data.land_is_active
        self.land_lookup_enum_name = data.land_lookup_enum_name
        self.land_name = data.land_name
        self.pac_name = data.pac_name

class PacUserLandListGetModelResponse(ListModel):
    request:PacUserLandListGetModelRequest = None
    items:List[PacUserLandListGetModelResponseItem] = Field(default_factory=list)
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        pac_code:uuid,
                        request:PacUserLandListGetModelRequest):
        try:
            logging.debug("loading model...PacUserLandListGetModelResponse")
            # pac_bus_obj = PacBusObj(session=session)
            # await pac_bus_obj.load(code=pac_code)
            generator = ReportManagerPacUserLandList(session_context)
            logging.debug("processing...PacUserLandListGetModelResponse")
            items = await generator.generate(
                    pac_code,

                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
            self.items = list()
            for item in items:
                report_item = PacUserLandListGetModelResponseItem()
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
