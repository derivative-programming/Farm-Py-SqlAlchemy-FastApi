# flows/base/tests/plant_user_property_random_update_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.plant_user_property_random_update as FlowConstants
from flows.base.plant_user_property_random_update import (
    BaseFlowPlantUserPropertyRandomUpdate)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.plant import PlantFactory
class TestBaseFlowPlantUserPropertyRandomUpdate():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowPlantUserPropertyRandomUpdate(session_context)
        plant = await PlantFactory.create_async(session)

# endset
        # Call the method being tested
        await flow._process_validation_rules(
            plant,

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
        plant = await PlantFactory.create_async(session)
        flow = BaseFlowPlantUserPropertyRandomUpdate(session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(plant)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                "Unautorized access. " + role_required + " role not found.")
            session_context.role_name_csv = role_required
