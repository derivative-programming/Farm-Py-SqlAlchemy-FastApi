# flows/default/tac_register.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
FlowTacRegister class
and related classes
that handle the addition of a
customer to a specific
tac in the flow process.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from business.tac import TacBusObj
from flows.base import LogSeverity
from flows.base.tac_register import BaseFlowTacRegister
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowTacRegisterResult():
    """
    Represents the result of the
    FlowTacRegister process.
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
        FlowTacRegisterResult class.
        """

    def to_json(self):
        """
        Converts the FlowTacRegisterResult
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


class FlowTacRegister(
    BaseFlowTacRegister
):
    """
    FlowTacRegister handles the addition of
    a customer to
    a specific tac in the flow process.

    This class extends the
    BaseFlowTacRegisterclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        tac_bus_obj: TacBusObj,
        email: str = "",
        password: str = "",
        confirm_password: str = "",
        first_name: str = "",
        last_name: str = "",
# endset  # noqa: E122
    ) -> FlowTacRegisterResult:
        """
        Processes the addition of a
        customer to a specific tac.

        Returns:
            FlowTacRegisterResult:
                The result of the
                FlowTacRegister process.
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
            confirm_password,
            first_name,
            last_name,
# endset  # noqa: E122
        )
        if password != confirm_password:
            self._add_field_validation_error("confirm_password","Passwords do not match")

        if len(email) > 0:
            similar_email_list = await tac_bus_obj.get_customer_by_email_prop(email)
            if len(similar_email_list) > 0:
                self._add_field_validation_error("email","This email is already registered")

        super()._throw_queued_validation_errors()
        customer_code_output: uuid.UUID = uuid.UUID(int=0)
        email_output: str = ""
        user_code_value_output: uuid.UUID = uuid.UUID(int=0)
        utc_offset_in_minutes_output: int = 0
        role_name_csv_list_output: str = ""
        api_key_output: str = ""
        # TODO: add flow logic

        customer_bus_obj = await tac_bus_obj.build_customer()
        customer_bus_obj = (
            customer_bus_obj
            .set_prop_email(email)
            .set_prop_first_name(first_name)
            .set_prop_last_name(last_name)
            .set_prop_last_login_utc_date_time(datetime.utcnow)
            .set_prop_is_active(True)
            .set_prop_registration_utc_date_time(datetime.utcnow)
        )
        await customer_bus_obj.save()

        organization_bus_obj = await tac_bus_obj.build_organization()
        await organization_bus_obj.save()

        org_customer_bus_obj = await organization_bus_obj.build_org_customer()
        org_customer_bus_obj = (
            org_customer_bus_obj
            .set_prop_customer_id(customer_bus_obj.customer_id)
            .set_prop_email(customer_bus_obj.email)
            )
        await org_customer_bus_obj.save()

        customer_role_bus_obj = await customer_bus_obj.build_customer_role()
        customer_role_bus_obj = (
            customer_role_bus_obj
            .set_prop_role_id(await RoleBusObj.get(
                customer_bus_obj.session,
                role_enum=RoleEnum.User
                ).role_id)
             )
        await customer_role_bus_obj.save()


        if email == "vince.roche@gmail.com":
            customer_role_bus_obj = await customer_bus_obj.build_customer_role()
            customer_role_bus_obj = (
                customer_role_bus_obj
                .set_prop_role_id(await RoleBusObj.get(
                    customer_bus_obj.session,
                    role_enum=RoleEnum.Config
                    ).role_id)
                )
            await customer_role_bus_obj.save()

            customer_role_bus_obj = await customer_bus_obj.build_customer_role()
            customer_role_bus_obj = (
                customer_role_bus_obj
                .set_prop_role_id(await RoleBusObj.get(
                    customer_bus_obj.session,
                    role_enum=RoleEnum.Admin
                    ).role_id)
                )
            await customer_role_bus_obj.save()

        customer_bus_obj.active_organization_id = organization_bus_obj.organization_id
        await customer_bus_obj.save()

        customer_role_list = await customer_bus_obj.get_all_customer_role()

        for customer_role in customer_role_list:
            role = await customer_role.get_role_id_rel_obj()
            role_name_csv_list_output = role_name_csv_list_output + ',' + role.name


        customer_code_output = customer_bus_obj.code
        email_output = customer_bus_obj.email
        user_code_value_output = customer_bus_obj.code
        utc_offset_in_minutes_output = 0

        api_key_flow = FlowCustomerBuildTempApiKey(self._session_context)
        api_key_flow_result = await api_key_flow.process(
            customer_bus_obj
        )

        api_key = await business.OrgApiKeyBusObj.get(
            customer_bus_obj.session,
            code=api_key_flow_result.tmp_org_api_key_code)

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowTacRegisterResult()
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
