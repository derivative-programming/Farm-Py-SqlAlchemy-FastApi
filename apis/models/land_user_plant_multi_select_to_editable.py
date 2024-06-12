# apis/models/land_user_plant_multi_select_to_editable.py
"""
    #TODO add comment
"""
from datetime import date, datetime
from decimal import Decimal
import json
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows.land_user_plant_multi_select_to_editable import FlowLandUserPlantMultiSelectToEditable, FlowLandUserPlantMultiSelectToEditableResult
from helpers import SessionContext
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel
from pydantic import Field, UUID4
import logging
from apis.models.validation_error import ValidationErrorItem
from sqlalchemy.ext.asyncio import AsyncSession
class LandUserPlantMultiSelectToEditablePostModelRequest(CamelModel):
    """
        #TODO add comment
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
class LandUserPlantMultiSelectToEditablePostModelResponse(PostResponse):
    """
        #TODO add comment
    """

# endset
# endset
    def load_flow_response(self, data: FlowLandUserPlantMultiSelectToEditableResult):
        """
            #TODO add comment
        """

# endset
    async def process_request(
        self,
        session_context: SessionContext,
        land_code: uuid.UUID,
        request: LandUserPlantMultiSelectToEditablePostModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...LandUserPlantMultiSelectToEditablePostModelResponse")
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load(code=land_code)
            if land_bus_obj.get_land_obj() is None:
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandUserPlantMultiSelectToEditable(session_context)
            logging.info("process flow...LandUserPlantMultiSelectToEditablePostModelResponse")
            flowResponse = await flow.process(
                land_bus_obj,
                request.plant_code_list_csv,
# endset
            )
            self.load_flow_response(flowResponse)
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
        #TODO add comment
        """
        return self.model_dump_json()

