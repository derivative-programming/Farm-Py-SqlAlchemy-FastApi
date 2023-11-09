from datetime import date, datetime
from decimal import Decimal
from typing import List
import uuid
from helpers import TypeConversion
from flows.tac_login_init_obj_wf import FlowTacLoginInitObjWFResult, FlowTacLoginInitObjWF
from helpers import SessionContext
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class TacLoginInitObjWFGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)
    email:str = ""
    password:str = ""

    def load_flow_response(self,data:FlowTacLoginInitObjWFResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.email = data.email
        self.password = data.password
class TacLoginInitObjWFGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        tac_code:uuid,
                        response:TacLoginInitObjWFGetInitModelResponse) -> TacLoginInitObjWFGetInitModelResponse:
        try:
            logging.debug("loading model...TacLoginInitObjWFGetInitModelRequest")
            tac_bus_obj = TacBusObj(session=session)
            await tac_bus_obj.load(code=tac_code)
            flow = FlowTacLoginInitObjWF(session_context)
            logging.debug("process request...TacLoginInitObjWFGetInitModelRequest")
            flowResponse = await flow.process(
                tac_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.debug("error...TacLoginInitObjWFGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

