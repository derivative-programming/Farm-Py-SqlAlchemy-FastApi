from datetime import date, datetime
from decimal import Decimal
from apis.models import ValidationError
from typing import List
import uuid
from helpers import TypeConversion
from flows import FlowPlantUserDetailsInitReportResult
from helpers import SessionContext
from models import Plant
from flows import FlowPlantUserDetailsInitReport
from flows import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
import apis.models as view_models
import logging
from models import Plant
class PlantUserDetailsInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)
    landCode:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    tacCode:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))

    def load_flow_response(self,data:FlowPlantUserDetailsInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.landCode = data.land_code
        self.tacCode = data.tac_code
class PlantUserDetailsInitReportGetInitModelRequest(SnakeModel):
    def process_request(self,
                        session_context:SessionContext,
                        plant_code:uuid,
                        response:PlantUserDetailsInitReportGetInitModelResponse) -> PlantUserDetailsInitReportGetInitModelResponse:
        try:
            logging.debug("loading model...")
            plant = Plant.objects.get(code=plant_code)
            logging.debug("process request...")
            flow = FlowPlantUserDetailsInitReport(session_context)
            flowResponse = flow.process(
                plant
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

