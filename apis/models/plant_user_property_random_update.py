# apis/models/plant_user_property_random_update.py
"""
This module contains the models for the Plant User Property Random Update API.
"""
import json
import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from pydantic import UUID4, Field
from apis.models.validation_error import ValidationErrorItem
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.plant_user_property_random_update import FlowPlantUserPropertyRandomUpdate, FlowPlantUserPropertyRandomUpdateResult
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel
from .post_reponse import PostResponse
class PlantUserPropertyRandomUpdatePostModelRequest(CamelModel):
    """
    Represents the request model for the Plant User Property Random Update API.
    """
    force_error_message: str = Field(
        default="",
        description="Force Error Message")

# endset
    class Config:
        """
        Configuration class for the PlantUserPropertyRandomUpdatePostModelRequest.
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
class PlantUserPropertyRandomUpdatePostModelResponse(PostResponse):
    """
    Represents the response model for the Plant User Property Random Update API.
    """

# endset
# endset
    def load_flow_response(self, data: FlowPlantUserPropertyRandomUpdateResult):
        """
        Loads the flow response data into the response model.
        """

# endset
    async def process_request(
        self,
        session_context: SessionContext,
        plant_code: uuid.UUID,
        request: PlantUserPropertyRandomUpdatePostModelRequest
    ):
        """
        Processes the request and generates the response.
        """
        try:
            logging.info("loading model...PlantUserPropertyRandomUpdatePostModelResponse")
            plant_bus_obj = PlantBusObj(session_context)
            await plant_bus_obj.load_from_code(code=plant_code)
            if plant_bus_obj.get_plant_obj() is None:
                logging.info("Invalid plant_code")
                raise ValueError("Invalid plant_code")
            flow = FlowPlantUserPropertyRandomUpdate(session_context)
            logging.info("process flow...PlantUserPropertyRandomUpdatePostModelResponse")
            flow_response = await flow.process(
                plant_bus_obj,

# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...PlantUserPropertyRandomUpdatePostModelResponse")
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

