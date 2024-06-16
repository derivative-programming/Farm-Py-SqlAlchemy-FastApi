# flows/base/tests/plant_user_delete_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.plant_user_delete as FlowConstants
from flows.base.plant_user_delete import (
    BaseFlowPlantUserDelete)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.plant import PlantFactory
class TestBaseFlowPlantUserDelete():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowPlantUserDelete(session_context)
        plant = await PlantFactory.create_async(session)

# endset
        # Call the method being tested
        await flow._process_validation_rules(
            plant,

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
        plant = await PlantFactory.create_async(session)
        flow = BaseFlowPlantUserDelete(session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(plant)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
