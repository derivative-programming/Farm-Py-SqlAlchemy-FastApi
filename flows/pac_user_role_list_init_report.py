from dataclasses import dataclass, field
from dataclasses_json import dataclass_json,LetterCase, config
from datetime import date, datetime
import uuid
from flows.base import BaseFlowPacUserRoleListInitReport
from models import Pac
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
class FlowPacUserRoleListInitReportResult():
    context_object_code:uuid = uuid.UUID(int=0)

class FlowPacUserRoleListInitReport(BaseFlowPacUserRoleListInitReport):
    def __init__(self, session_context:SessionContext):
        super(FlowPacUserRoleListInitReport, self).__init__(session_context)
    def process(self,
        pac: Pac,

        ) -> FlowPacUserRoleListInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(pac.code))
        super()._process_validation_rules(
            pac,

        )
        super()._throw_queued_validation_errors()

        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowPacUserRoleListInitReportResult()
        result.context_object_code = pac.code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
