# apis/models/customer_build_temp_api_key.py

"""
This module contains the models for the
Customer Build Temp Api Key API.
"""

import json
import logging
import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import UUID4, Field

from apis.models.validation_error import ValidationErrorItem
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.customer_build_temp_api_key import FlowCustomerBuildTempApiKey, FlowCustomerBuildTempApiKeyResult
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel

from .post_reponse import PostResponse


class CustomerBuildTempApiKeyPostModelRequest(CamelModel):
    """
    Represents the request model for the
    Customer Build Temp Api Key API.
    """

    force_error_message: str = Field(
        default="",
        description="Force Error Message")


    class Config:
        """
        Configuration class for the CustomerBuildTempApiKeyPostModelRequest.
        """

        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_dict_snake(self):
        """
        Convert the model to a dictionary with snake_case keys.
        """

        data = self.model_dump()
        return data

    def to_dict_snake_serialized(self):
        """
        Convert the model to a dictionary with snake_case
        keys and serialized values.
        """

        data = json.loads(self.model_dump_json())
        return data

    def to_dict_camel(self):
        """
        Convert the model to a dictionary with camelCase keys.
        """

        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}

    def to_dict_camel_serialized(self):
        """
        Convert the model to a dictionary with camelCase
        keys and serialized values.
        """

        data = json.loads(self.model_dump_json())
        return {snake_to_camel(k): v for k, v in data.items()}


class CustomerBuildTempApiKeyPostModelResponse(PostResponse):
    """
    Represents the response model for the
    Customer Build Temp Api Key API.
    """
    tmp_org_api_key_code: UUID4 = Field(
        default=uuid.UUID(int=0),
        description="Tmp Org Api Key Code")
    def load_flow_response(self, data: FlowCustomerBuildTempApiKeyResult):
        """
        Loads the flow response data into the response model.
        """
        self.tmp_org_api_key_code = data.tmp_org_api_key_code

    async def process_request(
        self,
        session_context: SessionContext,
        customer_code: uuid.UUID,
        request: CustomerBuildTempApiKeyPostModelRequest
    ):
        """
        Processes the request and generates the response.
        """

        try:
            logging.info("loading model...CustomerBuildTempApiKeyPostModelResponse")
            customer_bus_obj = CustomerBusObj(session_context)
            await customer_bus_obj.load_from_code(code=customer_code)
            if customer_bus_obj.get_customer_obj() is None:
                logging.info("Invalid customer_code")
                raise ValueError("Invalid customer_code")
            flow = FlowCustomerBuildTempApiKey(session_context)
            logging.info("process flow...CustomerBuildTempApiKeyPostModelResponse")
            flow_response = await flow.process(
                customer_bus_obj,

# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
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
        Converts the object to a JSON representation.

        Returns:
            str: The JSON representation of the object.
        """
        return self.model_dump_json()

