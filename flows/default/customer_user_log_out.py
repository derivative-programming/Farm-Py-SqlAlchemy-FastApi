import json
from business.customer import CustomerBusObj
from datetime import date, datetime
import uuid
from flows.base.customer_user_log_out import BaseFlowCustomerUserLogOut
from models import Customer
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from decimal import Decimal
class FlowCustomerUserLogOutResult():
    context_object_code:uuid.UUID =  uuid.UUID(int=0)

    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),

        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowCustomerUserLogOut(BaseFlowCustomerUserLogOut):
    def __init__(self, session_context:SessionContext):
        super(FlowCustomerUserLogOut, self).__init__(session_context)
    async def process(self,
        customer_bus_obj: CustomerBusObj,

        ) -> FlowCustomerUserLogOutResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(customer_bus_obj.code))
        await super()._process_validation_rules(
            customer_bus_obj,

        )
        super()._throw_queued_validation_errors()

        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowCustomerUserLogOutResult()
        result.context_object_code = customer_bus_obj.code

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result