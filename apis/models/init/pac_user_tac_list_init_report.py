from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from helpers import TypeConversion
from flows.pac_user_tac_list_init_report import FlowPacUserTacListInitReportResult, FlowPacUserTacListInitReport
from helpers import SessionContext
from business.pac import PacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class PacUserTacListInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)

    def load_flow_response(self,data:FlowPacUserTacListInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""

    def to_json(self):
        return self.model_dump_json()
class PacUserTacListInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        pac_code:uuid,
                        response:PacUserTacListInitReportGetInitModelResponse) -> PacUserTacListInitReportGetInitModelResponse:
        try:
            logging.info("loading model...PacUserTacListInitReportGetInitModelRequest")
            pac_bus_obj = PacBusObj(session=session)
            await pac_bus_obj.load(code=pac_code)
            if(pac_bus_obj.get_pac_obj() is None):
                logging.info("Invalid pac_code")
                raise ValueError("Invalid pac_code")
            flow = FlowPacUserTacListInitReport(session_context)
            logging.info("process request...PacUserTacListInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                pac_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...PacUserTacListInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

