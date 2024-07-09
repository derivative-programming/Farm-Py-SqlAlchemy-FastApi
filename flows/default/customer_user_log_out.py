# flows/default/customer_user_log_out.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains the
FlowCustomerUserLogOut class
and related classes
that handle the addition of a
 to a specific
customer in the flow process.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import business  # noqa: F401
from business.customer import CustomerBusObj
from flows.base import LogSeverity
from flows.base.customer_user_log_out import (
    BaseFlowCustomerUserLogOut)
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowCustomerUserLogOutResult():
    """
    Represents the result of the
    FlowCustomerUserLogOut process.
    """

    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowCustomerUserLogOutResult class.
        """

    def to_json(self):
        """
        Converts the FlowCustomerUserLogOutResult
        instance to a JSON string.

        Returns:
            str: The JSON representation of the instance.
        """
        # Create a dictionary representation of the instance
        data = {
            'context_object_code':
                str(self.context_object_code),

# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)


class FlowCustomerUserLogOut(
    BaseFlowCustomerUserLogOut
):
    """
    FlowCustomerUserLogOut handles the addition of
    a  to
    a specific customer in the flow process.

    This class extends the
    BaseFlowCustomerUserLogOutclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        customer_bus_obj: CustomerBusObj,

# endset  # noqa: E122
    ) -> FlowCustomerUserLogOutResult:
        """
        Processes the addition of a
         to a specific customer.

        Returns:
            FlowCustomerUserLogOutResult:
                The result of the
                FlowCustomerUserLogOut process.
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

        # TODO: add flow logic


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowCustomerUserLogOutResult()
        result.context_object_code = customer_bus_obj.code

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
