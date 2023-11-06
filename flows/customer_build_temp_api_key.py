from dataclasses import dataclass, field
from dataclasses_json import dataclass_json,LetterCase, config
from datetime import date, datetime
import uuid
from flows.base import BaseFlowCustomerBuildTempApiKey
from models import Customer
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
class FlowCustomerBuildTempApiKeyResult():
    context_object_code:uuid = uuid.UUID(int=0)
    tmp_org_api_key_code:uuid = uuid.UUID(int=0)
class FlowCustomerBuildTempApiKey(BaseFlowCustomerBuildTempApiKey):
    def __init__(self, session_context:SessionContext):
        super(FlowCustomerBuildTempApiKey, self).__init__(session_context)
    def process(self,
        customer: Customer,

        ) -> FlowCustomerBuildTempApiKeyResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(customer.code))
        super()._process_validation_rules(
            customer,

        )
        super()._throw_queued_validation_errors()
        tmp_org_api_key_code_output:uuid = uuid.UUID(int=0)
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowCustomerBuildTempApiKeyResult()
        result.context_object_code = customer.code
        result.tmp_org_api_key_code = tmp_org_api_key_code_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
