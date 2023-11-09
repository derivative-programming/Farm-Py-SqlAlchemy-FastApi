from datetime import date, datetime
from decimal import Decimal
from typing import List
import uuid
from helpers import TypeConversion
from flows.plant_user_details_init_report import FlowPlantUserDetailsInitReportResult, FlowPlantUserDetailsInitReport
from helpers import SessionContext
from business.plant import PlantBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class PlantUserDetailsInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)
    land_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))
    tac_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))

    def load_flow_response(self,data:FlowPlantUserDetailsInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.land_code = data.land_code
        self.tac_code = data.tac_code
class PlantUserDetailsInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        plant_code:uuid,
                        response:PlantUserDetailsInitReportGetInitModelResponse) -> PlantUserDetailsInitReportGetInitModelResponse:
        try:
            logging.debug("loading model...PlantUserDetailsInitReportGetInitModelRequest")
            plant_bus_obj = PlantBusObj(session=session)
            await plant_bus_obj.load(code=plant_code)
            flow = FlowPlantUserDetailsInitReport(session_context)
            logging.debug("process request...PlantUserDetailsInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                plant_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.debug("error...PlantUserDetailsInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

