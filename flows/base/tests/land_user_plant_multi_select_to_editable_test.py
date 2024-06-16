# flows/base/tests/land_user_plant_multi_select_to_editable_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
import flows.constants.land_user_plant_multi_select_to_editable as FlowConstants
from flows.base.land_user_plant_multi_select_to_editable import BaseFlowLandUserPlantMultiSelectToEditable
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.land import LandFactory
class TestBaseFlowLandUserPlantMultiSelectToEditable():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowLandUserPlantMultiSelectToEditable(session_context)
        land = await LandFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)
        plant_code_list_csv: str = ""
# endset
        # Call the method being tested
        await flow._process_validation_rules(
            land,
            plant_code_list_csv,
# endset  # noqa: E122
        )
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed
        if FlowConstants.param_plant_code_list_csv_isRequired is True:
            assert 'plantCodeListCsv' in flow.queued_validation_errors and flow.queued_validation_errors['plantCodeListCsv'] == 'Please enter a plant Code List Csv'
# endset
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        land = await LandFactory.create_async(session)
        flow = BaseFlowLandUserPlantMultiSelectToEditable(session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(land)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
