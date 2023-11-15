from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from helpers import TypeConversion
from flows.customer_user_log_out_init_obj_wf import FlowCustomerUserLogOutInitObjWFResult, FlowCustomerUserLogOutInitObjWF
from helpers import SessionContext
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class CustomerUserLogOutInitObjWFGetInitModelResponse(CamelModel):
    success:bool = Field(default=False, description="Success")
    message:str = Field(default="", description="Message")
    validation_errors:List[ValidationErrorItem] = Field(default_factory=list)
    tac_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'),
                                      description="Tac Code")

    def load_flow_response(self,data:FlowCustomerUserLogOutInitObjWFResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.tac_code = data.tac_code
    def to_json(self):
        return self.model_dump_json()
class CustomerUserLogOutInitObjWFGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        customer_code:uuid,
                        response:CustomerUserLogOutInitObjWFGetInitModelResponse) -> CustomerUserLogOutInitObjWFGetInitModelResponse:
        try:
            logging.info("loading model...CustomerUserLogOutInitObjWFGetInitModelRequest")
            customer_bus_obj = CustomerBusObj(session=session)
            await customer_bus_obj.load(code=customer_code)
            if(customer_bus_obj.get_customer_obj() is None):
                logging.info("Invalid customer_code")
                raise ValueError("Invalid customer_code")
            flow = FlowCustomerUserLogOutInitObjWF(session_context)
            logging.info("process request...CustomerUserLogOutInitObjWFGetInitModelRequest")
            flowResponse = await flow.process(
                customer_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...CustomerUserLogOutInitObjWFGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

