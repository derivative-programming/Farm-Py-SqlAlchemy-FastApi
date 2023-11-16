from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from apis.models import validation_error
from helpers import TypeConversion
from flows.tac_register_init_obj_wf import FlowTacRegisterInitObjWFResult, FlowTacRegisterInitObjWF
from helpers import SessionContext
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class TacRegisterInitObjWFGetInitModelResponse(CamelModel):
    success:bool = Field(default=False, description="Success")
    message:str = Field(default="", description="Message")
    validation_errors:List[ValidationErrorItem] = Field(default_factory=list)
    email:str = Field(default="", description="Email")
    password:str = Field(default="", description="Password")
    confirm_password:str = Field(default="", description="Confirm Password")
    first_name:str = Field(default="", description="First Name")
    last_name:str = Field(default="", description="Last Name")

    def load_flow_response(self,data:FlowTacRegisterInitObjWFResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.email = data.email
        self.password = data.password
        self.confirm_password = data.confirm_password
        self.first_name = data.first_name
        self.last_name = data.last_name
    def to_json(self):
        return self.model_dump_json()
class TacRegisterInitObjWFGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session_context:SessionContext,
                        tac_code:uuid,
                        response:TacRegisterInitObjWFGetInitModelResponse) -> TacRegisterInitObjWFGetInitModelResponse:
        try:
            logging.info("loading model...TacRegisterInitObjWFGetInitModelRequest")
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load(code=tac_code)
            if(tac_bus_obj.get_tac_obj() is None):
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacRegisterInitObjWF(session_context)
            logging.info("process request...TacRegisterInitObjWFGetInitModelRequest")
            flowResponse = await flow.process(
                tac_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...TacRegisterInitObjWFGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(validation_error(key,ve.error_dict[key]))
        return response

