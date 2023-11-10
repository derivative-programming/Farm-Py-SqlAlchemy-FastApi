from datetime import date, datetime
from decimal import Decimal
import json
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows.land_user_plant_multi_select_to_not_editable import FlowLandUserPlantMultiSelectToNotEditable, FlowLandUserPlantMultiSelectToNotEditableResult
from helpers import SessionContext
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from apis.models.validation_error import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
class LandUserPlantMultiSelectToNotEditablePostModelRequest(SnakeModel):
    force_error_message:str = ""
    plant_code_list_csv:str = ""

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
class LandUserPlantMultiSelectToNotEditablePostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowLandUserPlantMultiSelectToNotEditableResult):
        placeholder = "" #to avoid pass line

    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        land_code:uuid,
                        request:LandUserPlantMultiSelectToNotEditablePostModelRequest):
        try:
            logging.info("loading model...LandUserPlantMultiSelectToNotEditablePostModelResponse")
            land_bus_obj = LandBusObj(session=session)
            await land_bus_obj.load(code=land_code)
            if(land_bus_obj.get_land_obj() is None):
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandUserPlantMultiSelectToNotEditable(session_context)
            logging.info("process flow...LandUserPlantMultiSelectToNotEditablePostModelResponse")
            flowResponse = await flow.process(
                land_bus_obj,
                request.plant_code_list_csv,

            )
            self.load_flow_response(flowResponse);
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...LandUserPlantMultiSelectToNotEditablePostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationError()
                validation_error.property = key
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        return self.model_dump_json()

