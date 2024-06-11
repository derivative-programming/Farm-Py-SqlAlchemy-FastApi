# apis/models/init/pac_user_role_list_init_report.py
"""
    #TODO add comment
"""
from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from apis.models import validation_error
from helpers import TypeConversion
from flows.pac_user_role_list_init_report import FlowPacUserRoleListInitReportResult, FlowPacUserRoleListInitReport
from helpers import SessionContext
from business.pac import PacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class PacUserRoleListInitReportGetInitModelResponse(CamelModel):
    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)

    def load_flow_response(self, data:FlowPacUserRoleListInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""

    def to_json(self):
        return self.model_dump_json()
class PacUserRoleListInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session_context: SessionContext,
                        pac_code: uuid,
                        response: PacUserRoleListInitReportGetInitModelResponse) -> PacUserRoleListInitReportGetInitModelResponse:
        try:
            logging.info("loading model...PacUserRoleListInitReportGetInitModelRequest")
            pac_bus_obj = PacBusObj(session_context)
            await pac_bus_obj.load(code=pac_code)
            if(pac_bus_obj.get_pac_obj() is None):
                logging.info("Invalid pac_code")
                raise ValueError("Invalid pac_code")
            flow = FlowPacUserRoleListInitReport(session_context)
            logging.info("process request...PacUserRoleListInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                pac_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...PacUserRoleListInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(validation_error(key,ve.error_dict[key]))
        return response

