from datetime import date, datetime
from decimal import Decimal
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows import FlowPlantUserDeleteResult
from flows import FlowPlantUserDelete
from helpers import SessionContext
from models import Plant
from flows import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from models import Plant
class PlantUserDeletePostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowPlantUserDeleteResult):
        placeholder = "" #to avoid pass line

### request. expect camel case. use marshmallow to validate.
class PlantUserDeletePostModelRequest(SnakeModel):

    def process_request(self,
                        session_context:SessionContext,
                        plant_code:uuid,
                        response:PlantUserDeletePostModelResponse) -> PlantUserDeletePostModelResponse:
        try:
            logging.debug("loading model...")
            plant = Plant.objects.get(code=plant_code)
            flow = FlowPlantUserDelete(session_context)
            logging.debug("process flow...")
            flowResponse = flow.process(
                plant,

            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
        return response

