# flows/base/tests/land_user_plant_multi_select_to_not_editable_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.land_user_plant_multi_select_to_not_editable as FlowConstants
from flows.base.land_user_plant_multi_select_to_not_editable import (
    BaseFlowLandUserPlantMultiSelectToNotEditable)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.land import LandFactory
class TestBaseFlowLandUserPlantMultiSelectToNotEditable():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowLandUserPlantMultiSelectToNotEditable(session_context)
        land = await LandFactory.create_async(session)
        plant_code_list_csv: str = ""
# endset
        # Call the method being tested
        await flow._process_validation_rules(
            land,
            plant_code_list_csv,
# endset  # noqa: E122
        )
        #TODO add validation checks
        # - is email
        # - is phone
        # - calculatedIsRowLevelCustomerSecurityUsed
        # - calculatedIsRowLevelOrgCustomerSecurityUsed
        # - calculatedIsRowLevelOrganizationSecurityUsed
        if FlowConstants.PARAM_PLANT_CODE_LIST_CSV_IS_REQUIRED \
                is True:
            assert 'plantCodeListCsv' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'plantCodeListCsv'] == (
                'Please enter a plant Code List Csv')
# endset
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        land = await LandFactory.create_async(session)
        flow = BaseFlowLandUserPlantMultiSelectToNotEditable(session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(land)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                "Unautorized access. " + role_required + " role not found.")
            session_context.role_name_csv = role_required
