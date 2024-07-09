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

from business.tac import TacBusObj
from flows.base import LogSeverity
from flows.base.tac_login import BaseFlowTacLogin
from flows.customer_build_temp_api_key import (
    FlowCustomerBuildTempApiKey, FlowCustomerBuildTempApiKeyResult)
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

        similar_email_list = None

        if len(email) > 0:
            similar_email_list = await tac_bus_obj.get_customer_by_email_prop(email)
            if len(similar_email_list) > 0:
                self._add_field_validation_error("email","This email is already registered")

        if similar_email_list is None or len(similar_email_list) == 0:
            self._add_field_validation_error("","Invalid email or password")

        customer_bus_obj = similar_email_list[0]

        if customer_bus_obj.password != password:
            self._add_field_validation_error("","Invalid email or password")

        if customer_bus_obj.is_active is False:
            self._add_field_validation_error("","Invalid user")

        if customer_bus_obj.is_locked is True:
            self._add_field_validation_error("","This user account has been locked.")

        super()._throw_queued_validation_errors()
        customer_code_output: uuid.UUID = uuid.UUID(int=0)
        email_output: str = ""
        user_code_value_output: uuid.UUID = uuid.UUID(int=0)
        utc_offset_in_minutes_output: int = 0
        role_name_csv_list_output: str = ""
        api_key_output: str = ""
        
        customer_bus_obj.last_login_utc_date_time = datetime.utcnow
        await customer_bus_obj.save()

        customer_code_output = customer_bus_obj.code
        email_output = customer_bus_obj.email
        user_code_value_output = customer_bus_obj.code

        customer_role_list = await customer_bus_obj.get_all_customer_role()

        for customer_role in customer_role_list:
            role = await customer_role.get_role_id_rel_obj()
            role_name_csv_list_output = role_name_csv_list_output + ',' + role.name


        api_key_flow = FlowCustomerBuildTempApiKey(self._session_context)
        api_key_flow_result = await api_key_flow.process(
            customer_bus_obj
        )

        api_key = await business.OrgApiKeyBusObj.get(
            customer_bus_obj.session,
            code=api_key_flow_result.tmp_org_api_key_code)

        api_key_output = api_key.api_key_value



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
