from datetime import date, datetime
from decimal import Decimal
import json
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows.customer_build_temp_api_key import FlowCustomerBuildTempApiKey, FlowCustomerBuildTempApiKeyResult
from helpers import SessionContext
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from apis.models.validation_error import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
class CustomerBuildTempApiKeyPostModelRequest(SnakeModel):
    force_error_message:str = ""

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        data = self.model_dump()
    def to_dict_snake_serialized(self):
        data = json.loads(self.model_dump_json() )
    def _to_camel(self,string: str) -> str:
        return ''.join(word.capitalize() if i != 0 else word for i, word in enumerate(string.split('_')))
    def to_dict_camel(self):
        data = self.model_dump()
        return {self._to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        data = json.loads(self.model_dump_json() )
        return {self._to_camel(k): v for k, v in data.items()}
class CustomerBuildTempApiKeyPostModelResponse(PostResponse):
    tmp_org_api_key_code:UUID4 = uuid.UUID(int=0)

    def load_flow_response(self,data:FlowCustomerBuildTempApiKeyResult):
        placeholder = "" #to avoid pass line
        self.tmp_org_api_key_code = data.tmp_org_api_key_code

    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        customer_code:uuid,
                        request:CustomerBuildTempApiKeyPostModelRequest):
        try:
            logging.info("loading model...CustomerBuildTempApiKeyPostModelResponse")
            customer_bus_obj = CustomerBusObj(session=session)
            await customer_bus_obj.load(code=customer_code)
            if(customer_bus_obj.get_customer_obj() is None):
                logging.info("Invalid customer_code")
                raise ValueError("Invalid customer_code")
            flow = FlowCustomerBuildTempApiKey(session_context)
            logging.info("process flow...CustomerBuildTempApiKeyPostModelResponse")
            flowResponse = await flow.process(
                customer_bus_obj,

            )
            self.load_flow_response(flowResponse);
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...CustomerBuildTempApiKeyPostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationError()
                validation_error.property = key
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        return self.model_dump_json()

