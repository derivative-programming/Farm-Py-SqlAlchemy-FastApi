from datetime import date, datetime
from decimal import Decimal
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows import FlowLandUserPlantMultiSelectToNotEditableResult
from flows import FlowLandUserPlantMultiSelectToNotEditable
from helpers import SessionContext
from models import Land
from flows import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from models import Land
class LandUserPlantMultiSelectToNotEditablePostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowLandUserPlantMultiSelectToNotEditableResult):
        placeholder = "" #to avoid pass line

### request. expect camel case. use marshmallow to validate.
class LandUserPlantMultiSelectToNotEditablePostModelRequest(SnakeModel):
    plantCodeListCsv:str = ""

    def process_request(self,
                        session_context:SessionContext,
                        land_code:uuid,
                        response:LandUserPlantMultiSelectToNotEditablePostModelResponse) -> LandUserPlantMultiSelectToNotEditablePostModelResponse:
        try:
            logging.debug("loading model...")
            land = Land.objects.get(code=land_code)
            flow = FlowLandUserPlantMultiSelectToNotEditable(session_context)
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

