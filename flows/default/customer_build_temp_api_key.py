# flows/default/customer_build_temp_api_key.py
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
from flows.base.customer_build_temp_api_key import BaseFlowCustomerBuildTempApiKey
from models import Customer
from flows.base import LogSeverity
from business.customer import CustomerBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
class FlowCustomerBuildTempApiKeyResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    tmp_org_api_key_code: uuid.UUID = uuid.UUID(int=0)
# endset
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'tmp_org_api_key_code': str(self.tmp_org_api_key_code),
# endset
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowCustomerBuildTempApiKey(BaseFlowCustomerBuildTempApiKey):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowCustomerBuildTempApiKey, self).__init__(session_context)
    async def process(
        self,
        customer_bus_obj: CustomerBusObj,

# endset
        ) -> FlowCustomerBuildTempApiKeyResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(customer_bus_obj.code))
        await super()._process_validation_rules(
            customer_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()
        tmp_org_api_key_code_output: uuid.UUID = uuid.UUID(int=0)
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowCustomerBuildTempApiKeyResult()
        result.context_object_code = customer_bus_obj.code
        result.tmp_org_api_key_code = tmp_org_api_key_code_output
# endset
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
