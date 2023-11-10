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
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from apis.models.validation_error import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
class LandUserPlantMultiSelectToEditablePostModelRequest(SnakeModel):
    force_error_message:str = ""
    plant_code_list_csv:str = ""

class LandUserPlantMultiSelectToEditablePostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowLandUserPlantMultiSelectToEditableResult):
        placeholder = "" #to avoid pass line

    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        land_code:uuid,
                        request:LandUserPlantMultiSelectToEditablePostModelRequest):
        try:
            logging.info("loading model...LandUserPlantMultiSelectToEditablePostModelResponse")
            land_bus_obj = LandBusObj(session=session)
            await land_bus_obj.load(code=land_code)
            flow = FlowLandUserPlantMultiSelectToEditable(session_context)
            logging.info("process flow...LandUserPlantMultiSelectToEditablePostModelResponse")
            flowResponse = await flow.process(
                land_bus_obj,
                request.plant_code_list_csv,

            )
            self.load_flow_response(flowResponse);
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...LandUserPlantMultiSelectToEditablePostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationError()
                validation_error.property = key
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            #TODO finish to_json
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)

