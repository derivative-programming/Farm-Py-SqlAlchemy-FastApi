# apis/models/land_user_plant_multi_select_to_editable.py
"""
This module contains the models for the Land User Plant Multi Select To Editable API.
"""
import json
import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from pydantic import UUID4, Field
from apis.models.validation_error import ValidationErrorItem
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_user_plant_multi_select_to_editable import FlowLandUserPlantMultiSelectToEditable, FlowLandUserPlantMultiSelectToEditableResult
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel
from .post_reponse import PostResponse
class LandUserPlantMultiSelectToEditablePostModelRequest(CamelModel):
    """
    Represents the request model for the Land User Plant Multi Select To Editable API.
    """
    force_error_message: str = Field(
        default="",
        description="Force Error Message")
    plant_code_list_csv: str = Field(
        default="",
        description="plant Code List Csv")
# endset
    class Config:
        """
        Configuration class for the LandUserPlantMultiSelectToEditablePostModelRequest.
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
class LandUserPlantMultiSelectToEditablePostModelResponse(PostResponse):
    """
    Represents the response model for the Land User Plant Multi Select To Editable API.
    """

# endset
# endset
    def load_flow_response(self, data: FlowLandUserPlantMultiSelectToEditableResult):
        """
        Loads the flow response data into the response model.
        """

# endset
    async def process_request(
        self,
        session_context: SessionContext,
        land_code: uuid.UUID,
        request: LandUserPlantMultiSelectToEditablePostModelRequest
    ):
        """
        Processes the request and generates the response.
        """
        try:
            logging.info("loading model...LandUserPlantMultiSelectToEditablePostModelResponse")
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load_from_code(code=land_code)
            if land_bus_obj.get_land_obj() is None:
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandUserPlantMultiSelectToEditable(session_context)
            logging.info("process flow...LandUserPlantMultiSelectToEditablePostModelResponse")
            flow_response = await flow.process(
                land_bus_obj,
                request.plant_code_list_csv,
# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...LandUserPlantMultiSelectToEditablePostModelResponse")
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

