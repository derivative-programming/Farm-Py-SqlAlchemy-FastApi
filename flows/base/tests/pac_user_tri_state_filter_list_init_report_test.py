# flows/base/tests/pac_user_tri_state_filter_list_init_report_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.pac_user_tri_state_filter_list_init_report as FlowConstants
from flows.base.pac_user_tri_state_filter_list_init_report import (
    BaseFlowPacUserTriStateFilterListInitReport)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.pac import PacFactory
class TestBaseFlowPacUserTriStateFilterListInitReport():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowPacUserTriStateFilterListInitReport(session_context)
        pac = await PacFactory.create_async(session)

# endset
        # Call the method being tested
        await flow._process_validation_rules(
            pac,

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
        pac = await PacFactory.create_async(session)
        flow = BaseFlowPacUserTriStateFilterListInitReport(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(pac)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                "Unautorized access. " + role_required + " role not found.")
            session_context.role_name_csv = role_required
