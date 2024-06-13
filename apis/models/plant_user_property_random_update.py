# apis/models/plant_user_property_random_update.py
"""
    #TODO add comment
"""
import json
import uuid
import logging
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from helpers import TypeConversion
from helpers import SessionContext
from flows.plant_user_property_random_update import FlowPlantUserPropertyRandomUpdate, FlowPlantUserPropertyRandomUpdateResult
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel
from apis.models.validation_error import ValidationErrorItem
from .post_reponse import PostResponse
class PlantUserPropertyRandomUpdatePostModelRequest(CamelModel):
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
class PlantUserPropertyRandomUpdatePostModelResponse(PostResponse):
    """
        #TODO add comment
    """

# endset
# endset
    def load_flow_response(self, data: FlowPlantUserPropertyRandomUpdateResult):
        """
            #TODO add comment
        """

# endset
    async def process_request(
        self,
        session_context: SessionContext,
        plant_code: uuid.UUID,
        request: PlantUserPropertyRandomUpdatePostModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...PlantUserPropertyRandomUpdatePostModelResponse")
            plant_bus_obj = PlantBusObj(session_context)
            await plant_bus_obj.load(code=plant_code)
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
        #TODO add comment
        """
        return self.model_dump_json()

