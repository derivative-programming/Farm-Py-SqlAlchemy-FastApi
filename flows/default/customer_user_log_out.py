# flows/default/customer_user_log_out.py
"""
    #TODO add comment
"""
import uuid
import json
from datetime import date, datetime
from decimal import Decimal
from flows.base.customer_user_log_out import BaseFlowCustomerUserLogOut
from flows.base import LogSeverity
from business.customer import CustomerBusObj
from helpers import SessionContext
from helpers import TypeConversion
class FlowCustomerUserLogOutResult():
    """
    #TODO add comment
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)

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

# endset
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowCustomerUserLogOut(BaseFlowCustomerUserLogOut):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
        #TODO add comment
        """
        super(FlowCustomerUserLogOut, self).__init__(session_context)
    async def process(
        self,
        customer_bus_obj: CustomerBusObj,

# endset
        ) -> FlowCustomerUserLogOutResult:
        """
            #TODO add comment
        """
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(customer_bus_obj.code))
        await super()._process_validation_rules(
            customer_bus_obj,

# endset
        )
        super()._throw_queued_validation_errors()

# endset
        # TODO: add flow logic

        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowCustomerUserLogOutResult()
        result.context_object_code = customer_bus_obj.code

# endset
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result
