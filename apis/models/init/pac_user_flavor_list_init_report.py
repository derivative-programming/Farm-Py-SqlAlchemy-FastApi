from datetime import date, datetime
from decimal import Decimal
from typing import List
import uuid
from helpers import TypeConversion
from flows.pac_user_flavor_list_init_report import FlowPacUserFlavorListInitReportResult, FlowPacUserFlavorListInitReport
from helpers import SessionContext
from business.pac import PacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class PacUserFlavorListInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)

    def load_flow_response(self,data:FlowPacUserFlavorListInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""

class PacUserFlavorListInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        pac_code:uuid,
                        response:PacUserFlavorListInitReportGetInitModelResponse) -> PacUserFlavorListInitReportGetInitModelResponse:
        try:
            logging.debug("loading model...PacUserFlavorListInitReportGetInitModelRequest")
            pac_bus_obj = PacBusObj(session=session)
            await pac_bus_obj.load(code=pac_code)
            flow = FlowPacUserFlavorListInitReport(session_context)
            logging.debug("process request...PacUserFlavorListInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                pac_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.debug("error...PacUserFlavorListInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

