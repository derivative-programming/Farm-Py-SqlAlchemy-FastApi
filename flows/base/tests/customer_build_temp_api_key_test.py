# flows/base/tests/customer_build_temp_api_key_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.customer_build_temp_api_key as FlowConstants
from flows.base.customer_build_temp_api_key import (
    BaseFlowCustomerBuildTempApiKey)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.customer import CustomerFactory
class TestBaseFlowCustomerBuildTempApiKey():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowCustomerBuildTempApiKey(session_context)
        customer = await CustomerFactory.create_async(session)

# endset
        # Call the method being tested
        await flow._process_validation_rules(
            customer,

# endset  # noqa: E122
        )
        #TODO add validation checks
        # - is email
        # - is phone
        # - calculatedIsRowLevelCustomerSecurityUsed
        # - calculatedIsRowLevelOrgCustomerSecurityUsed
        # - calculatedIsRowLevelOrganizationSecurityUsed

# endset
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        customer = await CustomerFactory.create_async(session)
        flow = BaseFlowCustomerBuildTempApiKey(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(customer)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                "Unautorized access. " + role_required + " role not found.")
            session_context.role_name_csv = role_required
