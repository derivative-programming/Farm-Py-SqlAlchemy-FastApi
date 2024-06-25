# flows/base/tests/tac_login_test.py
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains the unit tests for the
`BaseFlowTacLogin` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.tac_login as FlowConstants
from flows.base.tac_login import (
    BaseFlowTacLogin)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.tac import TacFactory


class TestBaseFlowTacLogin():
    """
    This class contains unit tests for the
    `BaseFlowTacLogin` class.
    """

    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowTacLogin class.

        This method tests the validation rules for the request
        parameters of the
        tac Log In flow.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowTacLogin(session_context)
        tac = await TacFactory.create_async(session)
        email: str = ""
        password: str = ""
        # Call the method being tested
        await flow._process_validation_rules(
            tac,
            email,
            password,
# endset  # noqa: E122
        )
        #TODO add validation checks
        # - is email
        # - is phone
        # - calculatedIsRowLevelCustomerSecurityUsed
        # - calculatedIsRowLevelOrgCustomerSecurityUsed
        # - calculatedIsRowLevelOrganizationSecurityUsed
        if FlowConstants.PARAM_EMAIL_IS_REQUIRED \
                is True:
            assert 'email' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'email'] == (
                'Please enter a Email')
        if FlowConstants.PARAM_PASSWORD_IS_REQUIRED \
                is True:
            assert 'password' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'password'] == (
                'Please enter a ')

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        Test the process_security_rules method of
        BaseFlowTacLogin.

        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a tac
        object, and a
        BaseFlowTacLogin object.
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
        tac = await TacFactory.create_async(session)
        flow = BaseFlowTacLogin(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(tac)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required

