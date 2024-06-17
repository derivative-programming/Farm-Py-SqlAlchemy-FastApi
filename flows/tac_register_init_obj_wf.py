# flows/default/tac_register_init_obj_wf.py
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
from flows.base.tac_register_init_obj_wf import BaseFlowTacRegisterInitObjWF
from models import Tac
from flows.base import LogSeverity
from business.tac import TacBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
class FlowTacRegisterInitObjWFResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    first_name: str = ""
    last_name: str = ""
# endset
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'email': self.email,
            'password': self.password,
            'confirm_password': self.confirm_password,
            'first_name': self.first_name,
            'last_name': self.last_name,
# endset
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowTacRegisterInitObjWF(BaseFlowTacRegisterInitObjWF):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowTacRegisterInitObjWF, self).__init__(session_context)
    async def process(
        self,
        tac_bus_obj: TacBusObj,

# endset
        ) -> FlowTacRegisterInitObjWFResult:
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Start")
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Code::" + str(tac_bus_obj.code))
        await super()._process_validation_rules(
            tac_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()
        email_output: str = ""
        password_output: str = ""
        confirm_password_output: str = ""
        first_name_output: str = ""
        last_name_output: str = ""
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Building result")
        result = FlowTacRegisterInitObjWFResult()
        result.context_object_code = tac_bus_obj.code
        result.email = email_output
        result.password = password_output
        result.confirm_password = confirm_password_output
        result.first_name = first_name_output
        result.last_name = last_name_output
# endset
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "End")
        return result
