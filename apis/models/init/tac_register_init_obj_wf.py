from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from helpers import TypeConversion
from flows.tac_register_init_obj_wf import FlowTacRegisterInitObjWFResult, FlowTacRegisterInitObjWF
from helpers import SessionContext
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class TacRegisterInitObjWFGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)
    email:str = ""
    password:str = ""
    confirm_password:str = ""
    first_name:str = ""
    last_name:str = ""

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
        # Create a dictionary representation of the instance
        data = {
            #TODO finish to_json
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class TacRegisterInitObjWFGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        tac_code:uuid,
                        response:TacRegisterInitObjWFGetInitModelResponse) -> TacRegisterInitObjWFGetInitModelResponse:
        try:
            logging.info("loading model...TacRegisterInitObjWFGetInitModelRequest")
            tac_bus_obj = TacBusObj(session=session)
            await tac_bus_obj.load(code=tac_code)
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
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

