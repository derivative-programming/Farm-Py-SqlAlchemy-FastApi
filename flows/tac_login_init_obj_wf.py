from dataclasses import dataclass, field
from dataclasses_json import dataclass_json,LetterCase, config
from datetime import date, datetime
import uuid
from flows.base import BaseFlowTacLoginInitObjWF
from models import Tac
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
class FlowTacLoginInitObjWFResult():
    context_object_code:uuid = uuid.UUID(int=0)
    email:str = ""
    password:str = ""
class FlowTacLoginInitObjWF(BaseFlowTacLoginInitObjWF):
    def __init__(self, session_context:SessionContext):
        super(FlowTacLoginInitObjWF, self).__init__(session_context)
    def process(self,
        tac: Tac,

        ) -> FlowTacLoginInitObjWFResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac.code))
        super()._process_validation_rules(
            tac,

        )
        super()._throw_queued_validation_errors()
        email_output:str = ""
        password_output:str = ""
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacLoginInitObjWFResult()
        result.context_object_code = tac.code
        result.email = email_output
        result.password = password_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
