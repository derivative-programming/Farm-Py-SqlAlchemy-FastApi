from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from helpers import TypeConversion
from flows.pac_user_tri_state_filter_list_init_report import FlowPacUserTriStateFilterListInitReportResult, FlowPacUserTriStateFilterListInitReport
from helpers import SessionContext
from business.pac import PacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class PacUserTriStateFilterListInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)

    def load_flow_response(self,data:FlowPacUserTriStateFilterListInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""

    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            #TODO finish to_json
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class PacUserTriStateFilterListInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        pac_code:uuid,
                        response:PacUserTriStateFilterListInitReportGetInitModelResponse) -> PacUserTriStateFilterListInitReportGetInitModelResponse:
        try:
            logging.info("loading model...PacUserTriStateFilterListInitReportGetInitModelRequest")
            pac_bus_obj = PacBusObj(session=session)
            await pac_bus_obj.load(code=pac_code)
            flow = FlowPacUserTriStateFilterListInitReport(session_context)
            logging.info("process request...PacUserTriStateFilterListInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                pac_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...PacUserTriStateFilterListInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

