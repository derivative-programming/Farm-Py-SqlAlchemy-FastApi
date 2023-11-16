from datetime import date, datetime
from decimal import Decimal
import json
from typing import List
import uuid
from apis.models import validation_error
from helpers import TypeConversion
from flows.tac_farm_dashboard_init_report import FlowTacFarmDashboardInitReportResult, FlowTacFarmDashboardInitReport
from helpers import SessionContext
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class TacFarmDashboardInitReportGetInitModelResponse(CamelModel):
    success:bool = Field(default=False, description="Success")
    message:str = Field(default="", description="Message")
    validation_errors:List[ValidationErrorItem] = Field(default_factory=list)
    customer_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'),
                                      description="Customer Code")

    def load_flow_response(self,data:FlowTacFarmDashboardInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.customer_code = data.customer_code
    def to_json(self):
        return self.model_dump_json()
class TacFarmDashboardInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session_context:SessionContext,
                        tac_code:uuid,
                        response:TacFarmDashboardInitReportGetInitModelResponse) -> TacFarmDashboardInitReportGetInitModelResponse:
        try:
            logging.info("loading model...TacFarmDashboardInitReportGetInitModelRequest")
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load(code=tac_code)
            if(tac_bus_obj.get_tac_obj() is None):
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacFarmDashboardInitReport(session_context)
            logging.info("process request...TacFarmDashboardInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                tac_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...TacFarmDashboardInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(validation_error(key,ve.error_dict[key]))
        return response

