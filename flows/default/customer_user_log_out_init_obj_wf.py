# flows/default/customer_user_log_out_init_obj_wf.py
"""
This module contains the FlowCustomerUserLogOutInitObjWF class and related classes
that handle the addition of a  to a specific customer in the flow process.
"""
import uuid
import json
from datetime import date, datetime
from decimal import Decimal
from flows.base.customer_user_log_out_init_obj_wf import BaseFlowCustomerUserLogOutInitObjWF
from flows.base import LogSeverity
from business.customer import CustomerBusObj
from helpers import SessionContext
from helpers import TypeConversion
class FlowCustomerUserLogOutInitObjWFResult():
    """
    Represents the result of the FlowCustomerUserLogOutInitObjWF process.
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    tac_code: uuid.UUID = uuid.UUID(int=0)
# endset
    def __init__(self):
        """
        Initializes a new instance of the FlowCustomerUserLogOutInitObjWFResult class.
        """
    def to_json(self):
        """
        Converts the FlowCustomerUserLogOutInitObjWFResult instance to a JSON string.
        Returns:
            str: The JSON representation of the instance.
        """
        # Create a dictionary representation of the instance
        data = {
            'context_object_code':
                str(self.context_object_code),
            'tac_code':
                str(self.tac_code),
# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowCustomerUserLogOutInitObjWF(BaseFlowCustomerUserLogOutInitObjWF):
    """
    FlowCustomerUserLogOutInitObjWF handles the addition of a  to
    a specific customer in the flow process.
    This class extends the BaseFlowCustomerUserLogOutInitObjWF class and
    initializes it with the provided session context.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the FlowCustomerUserLogOutInitObjWF class.
        Args:
            session_context (SessionContext): The session
                context to be used for this flow.
        """
        super().__init__(session_context)
    async def process(
        self,
        customer_bus_obj: CustomerBusObj,

# endset  # noqa: E122
    ) -> FlowCustomerUserLogOutInitObjWFResult:
        """
        Processes the addition of a  to a specific customer.
        Returns:
            FlowCustomerUserLogOutInitObjWFResult: The result of the FlowCustomerUserLogOutInitObjWF process.
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Start"
        )
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Code::" + str(customer_bus_obj.code)
        )
        await super()._process_validation_rules(
            customer_bus_obj,

# endset  # noqa: E122
        )
        super()._throw_queued_validation_errors()
        tac_code_output: uuid.UUID = uuid.UUID(int=0)
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowCustomerUserLogOutInitObjWFResult()
        result.context_object_code = customer_bus_obj.code
        result.tac_code = (
            tac_code_output)
# endset
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
