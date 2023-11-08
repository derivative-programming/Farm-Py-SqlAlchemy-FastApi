from datetime import date, datetime
from decimal import Decimal
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows import FlowLandUserPlantMultiSelectToEditableResult
from flows import FlowLandUserPlantMultiSelectToEditable
from helpers import SessionContext
from models import Land
from flows import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from models import Land
class LandUserPlantMultiSelectToEditablePostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowLandUserPlantMultiSelectToEditableResult):
        placeholder = "" #to avoid pass line

### request. expect camel case. use marshmallow to validate.
class LandUserPlantMultiSelectToEditablePostModelRequest(SnakeModel):
    plantCodeListCsv:str = ""

    def process_request(self,
                        session_context:SessionContext,
                        land_code:uuid,
                        response:LandUserPlantMultiSelectToEditablePostModelResponse) -> LandUserPlantMultiSelectToEditablePostModelResponse:
        try:
            logging.debug("loading model...")
            land = Land.objects.get(code=land_code)
            flow = FlowLandUserPlantMultiSelectToEditable(session_context)
            logging.debug("process flow...")
            flowResponse = flow.process(
                land,
                self.plantCodeListCsv,

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

