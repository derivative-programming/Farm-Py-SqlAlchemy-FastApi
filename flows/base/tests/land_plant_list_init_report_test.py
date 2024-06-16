# flows/base/tests/land_plant_list_init_report_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
import flows.constants.land_plant_list_init_report as FlowConstants
from flows.base.land_plant_list_init_report import BaseFlowLandPlantListInitReport
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.land import LandFactory
class TestBaseFlowLandPlantListInitReport():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowLandPlantListInitReport(session_context)
        land = await LandFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)

# endset
        # Call the method being tested
        await flow._process_validation_rules(
            land,

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
        land = await LandFactory.create_async(session)
        flow = BaseFlowLandPlantListInitReport(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(land)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
