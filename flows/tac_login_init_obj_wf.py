# flows/default/tac_login_init_obj_wf.py
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
from flows.base.tac_login_init_obj_wf import BaseFlowTacLoginInitObjWF
from models import Tac
from flows.base import LogSeverity
from business.tac import TacBusObj
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
import business
class FlowTacLoginInitObjWFResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    email: str = ""
    password: str = ""
# endset
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'email': self.email,
            'password': self.password,
# endset
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowTacLoginInitObjWF(BaseFlowTacLoginInitObjWF):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowTacLoginInitObjWF, self).__init__(session_context)
    async def process(
        self,
        tac_bus_obj: TacBusObj,

# endset
        ) -> FlowTacLoginInitObjWFResult:
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Start")
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Code::" + str(tac_bus_obj.code))
        await super()._process_validation_rules(
            tac_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()
        email_output: str = ""
        password_output: str = ""
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Building result")
        result = FlowTacLoginInitObjWFResult()
        result.context_object_code = tac_bus_obj.code
        result.email = email_output
        result.password = password_output
# endset
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.INFORMATION_HIGH_DETAIL, "End")
        return result
