# flows/default/tests/customer_user_log_out_test.py

"""
This module contains unit tests for the
`FlowCustomerUserLogOutResult` and `FlowCustomerUserLogOut` classes.
"""

import json
import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.customer_user_log_out import FlowCustomerUserLogOut, FlowCustomerUserLogOutResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.customer import CustomerFactory


class TestCustomerUserLogOutPostModelResponse:
    """
    This class contains unit tests for the
    `FlowCustomerUserLogOutResult` class.
    """

    def test_flow_customer_user_log_out_result_to_json(self):
        """
        Test the `to_json` method of the
        `FlowCustomerUserLogOutResult` class.
        """

        # Create an instance and set attributes
        result = FlowCustomerUserLogOutResult()
        result.context_object_code = uuid.uuid4()


        # Call to_json method
        json_output = result.to_json()

        # Parse JSON output
        data = json.loads(json_output)

        # Assert individual fields
        assert data["context_object_code"] == (
            str(result.context_object_code))


    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        Test the `process` method of the `FlowCustomerUserLogOut` class.
        """

        session_context = SessionContext(dict(), session)
        flow = FlowCustomerUserLogOut(session_context)

        customer = await CustomerFactory.create_async(session)

        customer_bus_obj = CustomerBusObj(session_context)
        customer_bus_obj.load_from_obj_instance(customer)

        role_required = "User"


        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                await flow.process(
                    customer_bus_obj,

# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required

        customer_code_match_required = False
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORGANIZATION_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORG_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True

        if customer_code_match_required is True:
            with pytest.raises(FlowValidationError):

                await flow.process(
                    customer_bus_obj,

# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required

        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     customer_code=customer.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowCustomerUserLogOutResult)

