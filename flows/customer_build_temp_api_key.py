import json
from business.customer import CustomerBusObj
from datetime import date, datetime, timedelta
import uuid
from flows.base.customer_build_temp_api_key import BaseFlowCustomerBuildTempApiKey
from managers.org_customer import OrgCustomerManager
from models import Customer
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import DB_DIALECT, generate_uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from decimal import Decimal
from services import encryption
class FlowCustomerBuildTempApiKeyResult():
    context_object_code: uuid.UUID =  uuid.UUID(int=0)
    tmp_org_api_key_code: uuid.UUID =  uuid.UUID(int=0)
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'tmp_org_api_key_code': str(self.tmp_org_api_key_code),
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowCustomerBuildTempApiKey(BaseFlowCustomerBuildTempApiKey):
    def __init__(self, session_context: SessionContext):
        super(FlowCustomerBuildTempApiKey, self).__init__(session_context)
    async def process(self,
        customer_bus_obj: CustomerBusObj,

        ) -> FlowCustomerBuildTempApiKeyResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(customer_bus_obj.code))
        await super()._process_validation_rules(
            customer_bus_obj,

        )
        super()._throw_queued_validation_errors()
        tmp_org_api_key_code_output:uuid = uuid.UUID(int=0)
        # TODO: add flow logic

        expiration_utc_date_time = datetime.utcnow + timedelta(days=1)

        if customer_bus_obj.active_organization_id == 0:
            raise ValueError("Active organization not set")

        org_customer_manager = OrgCustomerManager(customer_bus_obj.session)
        org_customer_list = await org_customer_manager.get_by_customer_id(customer_id=customer_bus_obj.customer_id)
        org_customer_list_active_org = []
        for org_customer in org_customer_list:
            if org_customer.organization_id == customer_bus_obj.active_organization_id:
                org_customer_list_active_org.append(org_customer)



        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowCustomerBuildTempApiKeyResult()
        result.context_object_code = customer_bus_obj.code
        result.tmp_org_api_key_code = tmp_org_api_key_code_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
