# flows/base/tests/tac_register_init_obj_wf_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
import flows.constants.tac_register_init_obj_wf as FlowConstants
from flows.base.tac_register_init_obj_wf import BaseFlowTacRegisterInitObjWF
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.tac import TacFactory
class TestBaseFlowTacRegisterInitObjWF():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowTacRegisterInitObjWF(session_context)
        tac = await TacFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)

        # Call the method being tested
        await flow._process_validation_rules(
            tac,

            )
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        tac = await TacFactory.create_async(session)
        flow = BaseFlowTacRegisterInitObjWF(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(tac)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
