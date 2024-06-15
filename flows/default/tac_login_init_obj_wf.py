# flows/default/tac_login_init_obj_wf.py
"""
    #TODO add comment
"""
import uuid
import json
from datetime import date, datetime
from decimal import Decimal
from flows.base.tac_login_init_obj_wf import BaseFlowTacLoginInitObjWF
from flows.base import LogSeverity
from business.tac import TacBusObj
from helpers import SessionContext
from helpers import TypeConversion
class FlowTacLoginInitObjWFResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    email: str = ""
    password: str = ""
# endset
    def __init__(self):
        """
            #TODO add comment
        """
    def to_json(self):
        """
            #TODO add comment
        """
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
        """
            #TODO add comment
        """
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac_bus_obj.code))
        await super()._process_validation_rules(
            tac_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()
        email_output: str = ""
        password_output: str = ""
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacLoginInitObjWFResult()
        result.context_object_code = tac_bus_obj.code
        result.email = email_output
        result.password = password_output
# endset
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
