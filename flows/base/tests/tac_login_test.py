# flows/base/tests/tac_login_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
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
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowTacLogin(session_context)
        tac = await TacFactory.create_async(session)
        email: str = ""
        password: str = ""
# endset
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
        if FlowConstants.param_email_isRequired \
                is True:
            assert 'email' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'email'] == (
                'Please enter a Email')
        if FlowConstants.param_password_isRequired \
                is True:
            assert 'password' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'password'] == (
                'Please enter a ')
# endset
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        tac = await TacFactory.create_async(session)
        flow = BaseFlowTacLogin(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(tac)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                "Unautorized access. " + role_required + " role not found.")
            session_context.role_name_csv = role_required
