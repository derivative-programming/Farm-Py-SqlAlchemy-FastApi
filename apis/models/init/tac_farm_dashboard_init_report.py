# apis/models/init/tac_farm_dashboard_init_report.py
"""
    #TODO add comment
"""
import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List
from pydantic import Field
from apis.models.validation_error import ValidationErrorItem
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.tac_farm_dashboard_init_report import (
    FlowTacFarmDashboardInitReport,
    FlowTacFarmDashboardInitReportResult)
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel, SnakeModel
class TacFarmDashboardInitReportGetInitModelResponse(CamelModel):
    """
    #TODO add comment
    """
    success: bool = Field(default=False, description="Success")
    message: str = Field(default="", description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list)
    customer_code: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Customer Code")
# endset
    def load_flow_response(
        self,
        data: FlowTacFarmDashboardInitReportResult
    ):
        """
            #TODO add comment
        """
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.customer_code = (
            data.customer_code)
    def to_json(self):
        """
            #TODO add comment
        """
        return self.model_dump_json()
class TacFarmDashboardInitReportGetInitModelRequest(SnakeModel):
    """
    #TODO add comment
    """
    async def process_request(
            self,
            session_context: SessionContext,
            tac_code: uuid.UUID,
            response: TacFarmDashboardInitReportGetInitModelResponse
    ) -> TacFarmDashboardInitReportGetInitModelResponse:
        """
            #TODO add comment
        """
        try:
            logging.info(
                "loading model...TacFarmDashboardInitReportGetInitModelRequest")
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load_from_code(tac_code)
            if tac_bus_obj.get_tac_obj() is None:
                logging.info("Invalid tac_code")
                raise ValueError("Invalid tac_code")
            flow = FlowTacFarmDashboardInitReport(session_context)
            logging.info(
                "process request...TacFarmDashboardInitReportGetInitModelRequest")
            flow_response = await flow.process(
                tac_bus_obj
            )
            response.load_flow_response(flow_response)
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            logging.info("error...TacFarmDashboardInitReportGetInitModelRequest")
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                val_error = ValidationErrorItem()
                val_error.property = snake_to_camel(key)
                val_error.message = ve.error_dict[key]
                response.validation_errors.append(val_error)
        return response

