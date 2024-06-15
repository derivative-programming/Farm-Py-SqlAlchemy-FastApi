# flows/default/tests/customer_user_log_out_test.py
"""
    #TODO add comment
"""
from decimal import Decimal
import json
import uuid
import pytest
from datetime import datetime, date
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.customer_user_log_out import FlowCustomerUserLogOut, FlowCustomerUserLogOutResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.customer import CustomerFactory
import flows.constants.error_log_config_resolve_error_log as FlowConstants
class TestCustomerUserLogOutPostModelResponse:
    """
    #TODO add comment
    """
    def test_flow_customer_user_log_out_result_to_json(self):
        """
            #TODO add comment
        """
        # Create an instance and set attributes
        result = FlowCustomerUserLogOutResult()
        result.context_object_code = uuid.uuid4()

# endset
        # Call to_json method
        json_output = result.to_json()
        # Parse JSON output
        data = json.loads(json_output)
        # Assert individual fields
        assert data["context_object_code"] == str(result.context_object_code)

# endset
    #todo finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = FlowCustomerUserLogOut(session_context)
        customer = await CustomerFactory.create_async(session)
        customer_bus_obj = CustomerBusObj(session_context)
        await customer_bus_obj.load_from_obj_instance(customer)
        role_required = "User"

# endset
        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    customer_bus_obj,

# endset  # noqa: E122
                )
        session_context.role_name_csv = role_required
        customerCodeMatchRequired = False
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if customerCodeMatchRequired is True:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
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

