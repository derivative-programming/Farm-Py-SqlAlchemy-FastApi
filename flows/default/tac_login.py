# flows/default/tac_login.py
"""
    #TODO add comment
"""
import uuid
import json
from datetime import date, datetime
from decimal import Decimal
from flows.base.tac_login import BaseFlowTacLogin
from flows.base import LogSeverity
from business.tac import TacBusObj
from helpers import SessionContext
from helpers import TypeConversion
class FlowTacLoginResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    customer_code: uuid.UUID = uuid.UUID(int=0)
    email: str = ""
    user_code_value: uuid.UUID = uuid.UUID(int=0)
    utc_offset_in_minutes: int = 0
    role_name_csv_list: str = ""
    api_key: str = ""
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
            'customer_code': str(self.customer_code),
            'email': self.email,
            'user_code_value': str(self.user_code_value),
            'utc_offset_in_minutes': self.utc_offset_in_minutes,
            'role_name_csv_list': self.role_name_csv_list,
            'api_key': self.api_key,
# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowTacLogin(BaseFlowTacLogin):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowTacLogin, self).__init__(session_context)
    async def process(
        self,
        tac_bus_obj: TacBusObj,
        email: str = "",
        password: str = "",
# endset  # noqa: E122
    ) -> FlowTacLoginResult:
        """
            #TODO add comment
        """
        super()._log_message_and_severity(
            LogSeverity.information_high_detail,
            "Start"
        )
        super()._log_message_and_severity(
            LogSeverity.information_high_detail,
            "Code::" + str(tac_bus_obj.code)
        )
        await super()._process_validation_rules(
            tac_bus_obj,
            email,
            password,
# endset  # noqa: E122
        )
        super()._throw_queued_validation_errors()
        customer_code_output: uuid.UUID = uuid.UUID(int=0)
        email_output: str = ""
        user_code_value_output: uuid.UUID = uuid.UUID(int=0)
        utc_offset_in_minutes_output: int = 0
        role_name_csv_list_output: str = ""
        api_key_output: str = ""
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(
            LogSeverity.information_high_detail,
            "Building result")
        result = FlowTacLoginResult()
        result.context_object_code = tac_bus_obj.code
        result.customer_code = (
            customer_code_output)
        result.email = (
            email_output)
        result.user_code_value = (
            user_code_value_output)
        result.utc_offset_in_minutes = (
            utc_offset_in_minutes_output)
        result.role_name_csv_list = (
            role_name_csv_list_output)
        result.api_key = (
            api_key_output)
# endset
        super()._log_message_and_severity(
            LogSeverity.information_high_detail,
            "Result:" + result.to_json())
        super()._log_message_and_severity(
            LogSeverity.information_high_detail,
            "End")
        return result
