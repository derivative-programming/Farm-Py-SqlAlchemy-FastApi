from datetime import date, datetime
from decimal import Decimal
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows.plant_user_delete import FlowPlantUserDelete, FlowPlantUserDeleteResult
from helpers import SessionContext
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from apis.models.validation_error import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
class PlantUserDeletePostModelRequest(SnakeModel):
    force_error_message:str = ""

class PlantUserDeletePostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowPlantUserDeleteResult):
        placeholder = "" #to avoid pass line

    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        plant_code:uuid,
                        request:PlantUserDeletePostModelRequest):
        try:
            logging.debug("loading model...PlantUserDeletePostModelResponse")
            plant_bus_obj = PlantBusObj(session=session)
            await plant_bus_obj.load(code=plant_code)
            flow = FlowPlantUserDelete(session_context)
            logging.debug("process flow...PlantUserDeletePostModelResponse")
            flowResponse = await flow.process(
                plant_bus_obj,

            )
            self.load_flow_response(flowResponse);
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.debug("error...PlantUserDeletePostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationError()
                validation_error.property = key
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)

