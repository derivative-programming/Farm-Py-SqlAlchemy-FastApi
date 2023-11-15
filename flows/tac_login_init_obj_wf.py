import json
from business.tac import TacBusObj
from datetime import date, datetime
import uuid
from flows.base.tac_login_init_obj_wf import BaseFlowTacLoginInitObjWF
from models import Tac
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from decimal import Decimal
class FlowTacLoginInitObjWFResult():
    context_object_code:uuid.UUID =  uuid.UUID(int=0)
    email:str = ""
    password:str = ""
    def __init__(self):
        pass
    def to_json(self):
        # Create a dictionary representation of the instance
        data = {
            'context_object_code': str(self.context_object_code),
            'email': self.email,
            'password': self.password,
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowTacLoginInitObjWF(BaseFlowTacLoginInitObjWF):
    def __init__(self, session_context:SessionContext):
        super(FlowTacLoginInitObjWF, self).__init__(session_context)
    async def process(self,
        tac_bus_obj: TacBusObj,

        ) -> FlowTacLoginInitObjWFResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac_bus_obj.code))
        await super()._process_validation_rules(
            tac_bus_obj,

        )
        super()._throw_queued_validation_errors()
        email_output:str = ""
        password_output:str = "" 

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacLoginInitObjWFResult()
        result.context_object_code = tac_bus_obj.code
        result.email = email_output
        result.password = password_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
