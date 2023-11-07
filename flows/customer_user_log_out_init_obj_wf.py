from business.customer import CustomerBusObj
from datetime import date, datetime
import uuid
from flows.base import BaseFlowCustomerUserLogOutInitObjWF
from models import Customer
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from decimal import Decimal
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
# @dataclass_json
# @dataclass
class FlowCustomerUserLogOutInitObjWFResult():
    context_object_code:uuid = uuid.UUID(int=0)
    tac_code:uuid = uuid.UUID(int=0)
class FlowCustomerUserLogOutInitObjWF(BaseFlowCustomerUserLogOutInitObjWF):
    def __init__(self, session_context:SessionContext):
        super(FlowCustomerUserLogOutInitObjWF, self).__init__(session_context)
    async def process(self,
        customer_bus_obj: CustomerBusObj,

        ) -> FlowCustomerUserLogOutInitObjWFResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(customer_bus_obj.code))
        await super()._process_validation_rules(
            customer_bus_obj,

        )
        super()._throw_queued_validation_errors()
        tac_code_output:uuid = uuid.UUID(int=0)
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowCustomerUserLogOutInitObjWFResult()
        result.context_object_code = customer_bus_obj.code
        result.tac_code = tac_code_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
