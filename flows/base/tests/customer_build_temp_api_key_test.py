# flows/base/tests/customer_build_temp_api_key_test.py
# pylint: disable=protected-access
"""
This module contains the unit tests for the
`BaseFlowCustomerBuildTempApiKey` class.
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
    This class contains unit tests for the
    `BaseFlowCustomerBuildTempApiKey` class.
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowCustomerBuildTempApiKey class.
        This method tests the validation rules for the request
        parameters of the
        customer  flow.
        Args:
            session: The session object for the test.
        Returns:
            None
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
        Test the process_security_rules method of
        BaseFlowCustomerBuildTempApiKey.
        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a customer
        object, and a BaseFlowCustomerBuildTempApiKey object.
        Then, it sets the role_required
        variable to "" and calls the
        _process_security_rules method. Finally,
        it asserts that the expected validation
        errors are present in the flow's
        queued_validation_errors dictionary.
        Args:
            session: The session object for the test.
        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        customer = await CustomerFactory.create_async(session)
        flow = BaseFlowCustomerBuildTempApiKey(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(customer)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
