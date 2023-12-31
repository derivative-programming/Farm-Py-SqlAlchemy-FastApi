import json
from business.tac import TacBusObj
from datetime import date, datetime
import uuid
from flows.base.tac_register import BaseFlowTacRegister
from models import Tac
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
class FlowTacRegisterResult():
    context_object_code:uuid.UUID =  uuid.UUID(int=0)
    customer_code:uuid.UUID =  uuid.UUID(int=0)
    email:str = ""
    user_code_value:uuid.UUID =  uuid.UUID(int=0)
    utc_offset_in_minutes:int = 0
    role_name_csv_list:str = ""
    api_key:str = ""

    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'customer_code': str(self.customer_code),
            'email': self.email,
            'user_code_value': str(self.user_code_value),
            'utc_offset_in_minutes': self.utc_offset_in_minutes,
            'role_name_csv_list': self.role_name_csv_list,
            'api_key': self.api_key,

        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowTacRegister(BaseFlowTacRegister):
    def __init__(self, session_context:SessionContext):
        super(FlowTacRegister, self).__init__(session_context)
    async def process(self,
        tac_bus_obj: TacBusObj,
        email:str = "",
        password:str = "",
        confirm_password:str = "",
        first_name:str = "",
        last_name:str = "",

        ) -> FlowTacRegisterResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac_bus_obj.code))
        await super()._process_validation_rules(
            tac_bus_obj,
            email,
            password,
            confirm_password,
            first_name,
            last_name,

        )
        super()._throw_queued_validation_errors()
        customer_code_output:uuid = uuid.UUID(int=0)
        email_output:str = ""
        user_code_value_output:uuid = uuid.UUID(int=0)
        utc_offset_in_minutes_output:int = 0
        role_name_csv_list_output:str = ""
        api_key_output:str = ""

        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacRegisterResult()
        result.context_object_code = tac_bus_obj.code
        result.customer_code = customer_code_output
        result.email = email_output
        result.user_code_value = user_code_value_output
        result.utc_offset_in_minutes = utc_offset_in_minutes_output
        result.role_name_csv_list = role_name_csv_list_output
        result.api_key = api_key_output

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
