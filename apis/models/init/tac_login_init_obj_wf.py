# apis/models/init/tac_login_init_obj_wf.py
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
from flows.tac_login_init_obj_wf import FlowTacLoginInitObjWFResult, FlowTacLoginInitObjWF
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel, SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class TacLoginInitObjWFGetInitModelResponse(CamelModel):
    """
    #TODO add comment
    """
    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)
    email: str = Field(
        default="",
        description="Email")
    password: str = Field(
        default="",
        description="Password")
# endset
    def load_flow_response(
        self,
        data: FlowTacLoginInitObjWFResult
    ):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.email = (
            data.email)
        self.password = (
            data.password)
    def to_json(self):
        return self.model_dump_json()
class TacLoginInitObjWFGetInitModelRequest(SnakeModel):
    """
    #TODO add comment
    """
    async def process_request(
            self,
            session_context: SessionContext,
            tac_code: uuid,
            response: TacLoginInitObjWFGetInitModelResponse
    ) -> TacLoginInitObjWFGetInitModelResponse:
        try:
            logging.info(
                "loading model...TacLoginInitObjWFGetInitModelRequest")
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load(code=tac_code)
            if tac_bus_obj.get_tac_obj() is None:
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacLoginInitObjWF(session_context)
            logging.info(
                "process request...TacLoginInitObjWFGetInitModelRequest")
            flowResponse = await flow.process(
                tac_bus_obj
            )
            response.load_flow_response(flowResponse)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...TacLoginInitObjWFGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response

