# flows/base/tests/customer_user_log_out_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
import flows.constants.customer_user_log_out as FlowConstants
from flows.base.customer_user_log_out import BaseFlowCustomerUserLogOut
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.customer import CustomerFactory
class TestBaseFlowCustomerUserLogOut():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowCustomerUserLogOut(session_context)
        customer = await CustomerFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)

# endset
        # Call the method being tested
        await flow._process_validation_rules(
            customer,

# endset  # noqa: E122
        )
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed

# endset
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        customer = await CustomerFactory.create_async(session)
        flow = BaseFlowCustomerUserLogOut(session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(customer)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
