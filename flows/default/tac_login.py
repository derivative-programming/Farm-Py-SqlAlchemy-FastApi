# flows/default/tac_login.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains the
FlowTacLogin class
and related classes
that handle the addition of a
 to a specific
tac in the flow process.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import business  # noqa: F401
from business.tac import TacBusObj
from flows.base import LogSeverity
from flows.base.tac_login import (
    BaseFlowTacLogin)
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowTacLoginResult():
    """
    Represents the result of the
    FlowTacLogin process.
    """
    customer_code: uuid.UUID = uuid.UUID(int=0)
    email: str = ""
    user_code_value: uuid.UUID = uuid.UUID(int=0)
    utc_offset_in_minutes: int = 0
    role_name_csv_list: str = ""
    api_key: str = ""
    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowTacLoginResult class.
        """

    def to_json(self):
        """
        Converts the FlowTacLoginResult
        instance to a JSON string.

        Returns:
            str: The JSON representation of the instance.
        """
        # Create a dictionary representation of the instance
        data = {
            'context_object_code':
                str(self.context_object_code),
            'customer_code':
                str(self.customer_code),
            'email':
                self.email,
            'user_code_value':
                str(self.user_code_value),
            'utc_offset_in_minutes':
                self.utc_offset_in_minutes,
            'role_name_csv_list':
                self.role_name_csv_list,
            'api_key':
                self.api_key,
# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)


class FlowTacLogin(
    BaseFlowTacLogin
):
    """
    FlowTacLogin handles the addition of
    a  to
    a specific tac in the flow process.

    This class extends the
    BaseFlowTacLoginclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        tac_bus_obj: TacBusObj,
        email: str = "",
        password: str = "",
# endset  # noqa: E122
    ) -> FlowTacLoginResult:
        """
        Processes the addition of a
         to a specific tac.

        Returns:
            FlowTacLoginResult:
                The result of the
                FlowTacLogin process.
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Start"
        )
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
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
        # TODO: add flow logic


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
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
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
