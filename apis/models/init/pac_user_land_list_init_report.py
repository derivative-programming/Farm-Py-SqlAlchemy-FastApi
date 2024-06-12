# apis/models/init/pac_user_land_list_init_report.py
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
from flows.pac_user_land_list_init_report import FlowPacUserLandListInitReportResult, FlowPacUserLandListInitReport
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from business.pac import PacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel, SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class PacUserLandListInitReportGetInitModelResponse(CamelModel):
    """
    #TODO add comment
    """
    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)

# endset
    def load_flow_response(
        self,
        data: FlowPacUserLandListInitReportResult
    ):
        self.validation_errors = list()
        self.success = False
        self.message = ""

    def to_json(self):
        return self.model_dump_json()
class PacUserLandListInitReportGetInitModelRequest(SnakeModel):
    """
    #TODO add comment
    """
    async def process_request(
            self,
            session_context: SessionContext,
            pac_code: uuid,
            response: PacUserLandListInitReportGetInitModelResponse
    ) -> PacUserLandListInitReportGetInitModelResponse:
        try:
            logging.info(
                "loading model...PacUserLandListInitReportGetInitModelRequest")
            pac_bus_obj = PacBusObj(session_context)
            await pac_bus_obj.load(code=pac_code)
            if pac_bus_obj.get_pac_obj() is None:
                logging.info("Invalid pac_code")
                raise ValueError("Invalid pac_code")
            flow = FlowPacUserLandListInitReport(session_context)
            logging.info(
                "process request...PacUserLandListInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                pac_bus_obj
            )
            response.load_flow_response(flowResponse)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...PacUserLandListInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response

