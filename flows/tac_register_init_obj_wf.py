from business.tac import TacBusObj
from datetime import date, datetime
import uuid
from flows.base import BaseFlowTacRegisterInitObjWF
from models import Tac
from flows.base import LogSeverity
from helpers import SessionContext
from helpers import ApiToken
from helpers import TypeConversion
import models as farm_models
import managers as farm_managers
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_config import db_dialect,generate_uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from pydantic import BaseModel, Field, UUID4
from decimal import Decimal
class FlowTacRegisterInitObjWFResult(BaseModel):
    context_object_code:UUID4 =  uuid.UUID(int=0)
    email:str = ""
    password:str = ""
    confirm_password:str = ""
    first_name:str = ""
    last_name:str = ""
    def __init__(self):
        pass
class FlowTacRegisterInitObjWF(BaseFlowTacRegisterInitObjWF):
    def __init__(self, session_context:SessionContext):
        super(FlowTacRegisterInitObjWF, self).__init__(session_context)
    async def process(self,
        tac_bus_obj: TacBusObj,

        ) -> FlowTacRegisterInitObjWFResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac_bus_obj.code))
        await super()._process_validation_rules(
            tac_bus_obj,

        )
        super()._throw_queued_validation_errors()
        email_output:str = ""
        password_output:str = ""
        confirm_password_output:str = ""
        first_name_output:str = ""
        last_name_output:str = ""
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacRegisterInitObjWFResult()
        result.context_object_code = tac_bus_obj.code
        result.email = email_output
        result.password = password_output
        result.confirm_password = confirm_password_output
        result.first_name = first_name_output
        result.last_name = last_name_output
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
