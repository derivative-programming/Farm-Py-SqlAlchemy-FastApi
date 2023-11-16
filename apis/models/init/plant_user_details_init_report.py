from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from apis.models import validation_error
from helpers import TypeConversion
from flows.plant_user_details_init_report import FlowPlantUserDetailsInitReportResult, FlowPlantUserDetailsInitReport
from helpers import SessionContext
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class PlantUserDetailsInitReportGetInitModelResponse(CamelModel):
    success:bool = Field(default=False, description="Success")
    message:str = Field(default="", description="Message")
    validation_errors:List[ValidationErrorItem] = Field(default_factory=list)
    land_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'),
                                      description="Land Code")
    tac_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'),
                                      description="Tac Code")

    def load_flow_response(self,data:FlowPlantUserDetailsInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.land_code = data.land_code
        self.tac_code = data.tac_code
    def to_json(self):
        return self.model_dump_json()
class PlantUserDetailsInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session_context:SessionContext,
                        plant_code:uuid,
                        response:PlantUserDetailsInitReportGetInitModelResponse) -> PlantUserDetailsInitReportGetInitModelResponse:
        try:
            logging.info("loading model...PlantUserDetailsInitReportGetInitModelRequest")
            plant_bus_obj = PlantBusObj(session_context)
            await plant_bus_obj.load(code=plant_code)
            if(plant_bus_obj.get_plant_obj() is None):
                logging.info("Invalid plant_code")
                raise ValueError("Invalid plant_code")
            flow = FlowPlantUserDetailsInitReport(session_context)
            logging.info("process request...PlantUserDetailsInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                plant_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...PlantUserDetailsInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(validation_error(key,ve.error_dict[key]))
        return response

