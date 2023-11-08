from datetime import date, datetime
from decimal import Decimal
from apis.models import ValidationError
from typing import List
import uuid
from helpers import TypeConversion
from flows import FlowPacUserTacListInitReportResult
from helpers import SessionContext
from models import Pac
from flows import FlowPacUserTacListInitReport
from flows import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
import apis.models as view_models
import logging
from models import Pac
class PacUserTacListInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)

    def load_flow_response(self,data:FlowPacUserTacListInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""

class PacUserTacListInitReportGetInitModelRequest(SnakeModel):
    def process_request(self,
                        session_context:SessionContext,
                        pac_code:uuid,
                        response:PacUserTacListInitReportGetInitModelResponse) -> PacUserTacListInitReportGetInitModelResponse:
        try:
            logging.debug("loading model...")
            pac = Pac.objects.get(code=pac_code)
            logging.debug("process request...")
            flow = FlowPacUserTacListInitReport(session_context)
            flowResponse = flow.process(
                pac
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
        return response

