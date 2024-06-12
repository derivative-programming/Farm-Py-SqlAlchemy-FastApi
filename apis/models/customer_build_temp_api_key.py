# apis/models/customer_build_temp_api_key.py
"""
    #TODO add comment
"""
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
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel
from pydantic import Field, UUID4
import logging
from apis.models.validation_error import ValidationErrorItem
from sqlalchemy.ext.asyncio import AsyncSession
class CustomerBuildTempApiKeyPostModelRequest(CamelModel):
    """
        #TODO add comment
    """
    force_error_message: str = Field(
        default="",
        description="Force Error Message")

# endset
    class Config:
        """
            #TODO add comment
        """
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        """
            #TODO add comment
        """
        data = self.model_dump()
        return data
    def to_dict_snake_serialized(self):
        """
            #TODO add comment
        """
        data = json.loads(self.model_dump_json())
        return data
    def to_dict_camel(self):
        """
            #TODO add comment
        """
        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        """
            #TODO add comment
        """
        data = json.loads(self.model_dump_json())
        return {snake_to_camel(k): v for k, v in data.items()}
class CustomerBuildTempApiKeyPostModelResponse(PostResponse):
    """
        #TODO add comment
    """
    tmp_org_api_key_code: UUID4 = Field(
        default=uuid.UUID(int=0),
        description="Tmp Org Api Key Code")
# endset
# endset
    def load_flow_response(self, data: FlowCustomerBuildTempApiKeyResult):
        """
            #TODO add comment
        """
        self.tmp_org_api_key_code = data.tmp_org_api_key_code
# endset
    async def process_request(
        self,
        session_context: SessionContext,
        customer_code: uuid.UUID,
        request: CustomerBuildTempApiKeyPostModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...CustomerBuildTempApiKeyPostModelResponse")
            customer_bus_obj = CustomerBusObj(session_context)
            await customer_bus_obj.load(code=customer_code)
            if customer_bus_obj.get_customer_obj() is None:
                logging.info("Invalid customer_code")
                raise ValueError("Invalid customer_code")
            flow = FlowCustomerBuildTempApiKey(session_context)
            logging.info("process flow...CustomerBuildTempApiKeyPostModelResponse")
            flowResponse = await flow.process(
                customer_bus_obj,

# endset
            )
            self.load_flow_response(flowResponse)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...CustomerBuildTempApiKeyPostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        """
        #TODO add comment
        """
        return self.model_dump_json()

