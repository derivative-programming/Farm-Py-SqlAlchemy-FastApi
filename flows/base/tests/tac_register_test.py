# flows/base/tests/tac_register_test.py
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains the unit tests for the
`BaseFlowTacRegister` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.tac_register \
    as FlowConstants  # noqa: F401
from flows.base.tac_register import (
    BaseFlowTacRegister)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.tac import TacFactory


class TestBaseFlowTacRegister():
    """
    This class contains unit tests for the
    `BaseFlowTacRegister` class.
    """

    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowTacRegister class.

        This method tests the validation rules for the request
        parameters of the
        tac Create your account flow.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext({}, session)
        flow = BaseFlowTacRegister(
            session_context)
        tac = await \
            TacFactory.create_async(session)
        email: str = ""
        password: str = ""
        confirm_password: str = ""
        first_name: str = ""
        last_name: str = ""
        # Call the method being tested
        await flow._process_validation_rules(
            tac,
            email,
            password,
            confirm_password,
            first_name,
            last_name,
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
                'Please enter a Password')
        if FlowConstants.PARAM_CONFIRM_PASSWORD_IS_REQUIRED \
                is True:
            assert 'confirmPassword' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'confirmPassword'] == (
                'Please enter a ')
        if FlowConstants.PARAM_FIRST_NAME_IS_REQUIRED \
                is True:
            assert 'firstName' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'firstName'] == (
                'Please enter a First Name')
        if FlowConstants.PARAM_LAST_NAME_IS_REQUIRED \
                is True:
            assert 'lastName' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'lastName'] == (
                'Please enter a Last Name')

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        Test the process_security_rules method of
        BaseFlowTacRegister.

        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a tac
        object, and a
        BaseFlowTacRegister object.
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
        session_context = SessionContext({}, session)
        tac = await \
            TacFactory.create_async(session)
        flow = BaseFlowTacRegister(
            session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(tac)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
