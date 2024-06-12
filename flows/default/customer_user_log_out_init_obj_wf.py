# flows/default/customer_user_log_out_init_obj_wf.py
"""
    #TODO add comment
"""
import uuid
import json
from datetime import date, datetime
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from decimal import Decimal
from flows.base.customer_user_log_out_init_obj_wf import BaseFlowCustomerUserLogOutInitObjWF
from models import Customer
from flows.base import LogSeverity
from business.customer import CustomerBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
from services.db_config import DB_DIALECT, generate_uuid
class FlowCustomerUserLogOutInitObjWFResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    tac_code: uuid.UUID = uuid.UUID(int=0)
# endset
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'tac_code': str(self.tac_code),
# endset
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowCustomerUserLogOutInitObjWF(BaseFlowCustomerUserLogOutInitObjWF):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowCustomerUserLogOutInitObjWF, self).__init__(session_context)
    async def process(
        self,
        customer_bus_obj: CustomerBusObj,

# endset
        ) -> FlowCustomerUserLogOutInitObjWFResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(customer_bus_obj.code))
        await super()._process_validation_rules(
            customer_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()
        tac_code_output: uuid = uuid.UUID(int=0)
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowCustomerUserLogOutInitObjWFResult()
        result.context_object_code = customer_bus_obj.code
        result.tac_code = tac_code_output
# endset
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
