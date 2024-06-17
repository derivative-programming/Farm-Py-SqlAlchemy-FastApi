# flows/base/tests/tac_login_init_obj_wf_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.tac_login_init_obj_wf as FlowConstants
from flows.base.tac_login_init_obj_wf import (
    BaseFlowTacLoginInitObjWF)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.tac import TacFactory
class TestBaseFlowTacLoginInitObjWF():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowTacLoginInitObjWF(session_context)
        tac = await TacFactory.create_async(session)

# endset
        # Call the method being tested
        await flow._process_validation_rules(
            tac,

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
        tac = await TacFactory.create_async(session)
        flow = BaseFlowTacLoginInitObjWF(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(tac)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                "Unautorized access. " + role_required + " role not found.")
            session_context.role_name_csv = role_required
