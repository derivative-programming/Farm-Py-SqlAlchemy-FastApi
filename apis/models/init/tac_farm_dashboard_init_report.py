from datetime import date, datetime
from decimal import Decimal
from typing import List
import uuid
from helpers import TypeConversion
from flows.tac_farm_dashboard_init_report import FlowTacFarmDashboardInitReportResult, FlowTacFarmDashboardInitReport
from helpers import SessionContext
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from apis.models.validation_error import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
class TacFarmDashboardInitReportGetInitModelResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)
    customer_code:uuid.UUID = Field(default_factory=lambda: uuid.UUID('00000000-0000-0000-0000-000000000000'))

    def load_flow_response(self,data:FlowTacFarmDashboardInitReportResult):
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.customer_code = data.customer_code
class TacFarmDashboardInitReportGetInitModelRequest(SnakeModel):
    async def process_request(self,
                        session:AsyncSession,
                        session_context:SessionContext,
                        tac_code:uuid,
                        response:TacFarmDashboardInitReportGetInitModelResponse) -> TacFarmDashboardInitReportGetInitModelResponse:
        try:
            logging.debug("loading model...TacFarmDashboardInitReportGetInitModelRequest")
            tac_bus_obj = TacBusObj(session=session)
            await tac_bus_obj.load(code=tac_code)
            flow = FlowTacFarmDashboardInitReport(session_context)
            logging.debug("process request...TacFarmDashboardInitReportGetInitModelRequest")
            flowResponse = await flow.process(
                tac_bus_obj
            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.debug("error...TacFarmDashboardInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(ValidationError(key,ve.error_dict[key]))
        return response

