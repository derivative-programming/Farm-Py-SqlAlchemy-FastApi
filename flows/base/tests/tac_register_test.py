# flows/base/tests/tac_register_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.tac_register as FlowConstants
from flows.base.tac_register import (
    BaseFlowTacRegister)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.tac import TacFactory
class TestBaseFlowTacRegister():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowTacRegister(session_context)
        tac = await TacFactory.create_async(session)
        email: str = ""
        password: str = ""
        confirm_password: str = ""
        first_name: str = ""
        last_name: str = ""
# endset
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
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed
        if FlowConstants.param_email_isRequired is True:
            assert 'email' in flow.queued_validation_errors and flow.queued_validation_errors['email'] == 'Please enter a Email'
        if FlowConstants.param_password_isRequired is True:
            assert 'password' in flow.queued_validation_errors and flow.queued_validation_errors['password'] == 'Please enter a Password'
        if FlowConstants.param_confirm_password_isRequired is True:
            assert 'confirmPassword' in flow.queued_validation_errors and flow.queued_validation_errors['confirmPassword'] == 'Please enter a '
        if FlowConstants.param_first_name_isRequired is True:
            assert 'firstName' in flow.queued_validation_errors and flow.queued_validation_errors['firstName'] == 'Please enter a First Name'
        if FlowConstants.param_last_name_isRequired is True:
            assert 'lastName' in flow.queued_validation_errors and flow.queued_validation_errors['lastName'] == 'Please enter a Last Name'
# endset
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        tac = await TacFactory.create_async(session)
        flow = BaseFlowTacRegister(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(tac)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
