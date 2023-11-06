from dataclasses import dataclass, field
from dataclasses_json import dataclass_json,LetterCase, config
from datetime import date, datetime
import uuid
from flows.base import BaseFlowPlantUserDetailsInitReport
from models import Plant
from flows.base import LogSeverity
from helpers import SessionContext
from models import Customer
from django.utils import timezone
from helpers import ApiToken
from decimal import Decimal
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
@dataclass_json
@dataclass
class FlowPlantUserDetailsInitReportResult():
    context_object_code:uuid = uuid.UUID(int=0)
    land_code:uuid = uuid.UUID(int=0)
    tac_code:uuid = uuid.UUID(int=0)
class FlowPlantUserDetailsInitReport(BaseFlowPlantUserDetailsInitReport):
    def __init__(self, session_context:SessionContext):
        super(FlowPlantUserDetailsInitReport, self).__init__(session_context)
    def process(self,
        plant: Plant,

        ) -> FlowPlantUserDetailsInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(plant.code))
        super()._process_validation_rules(
            plant,

        )
        super()._throw_queued_validation_errors()
        land_code_output:uuid = uuid.UUID(int=0)
        tac_code_output:uuid = uuid.UUID(int=0)
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowPlantUserDetailsInitReportResult()
        result.context_object_code = plant.code
        result.land_code = land_code_output
        result.tac_code = tac_code_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
