# flows/base/tests/land_user_plant_multi_select_to_editable_test.py
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains the unit tests for the
`BaseFlowLandUserPlantMultiSelectToEditable` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.land_user_plant_multi_select_to_editable \
    as FlowConstants  # noqa: F401
from flows.base.land_user_plant_multi_select_to_editable import (
    BaseFlowLandUserPlantMultiSelectToEditable)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.land import LandFactory


class TestBaseFlowLandUserPlantMultiSelectToEditable():
    """
    This class contains unit tests for the
    `BaseFlowLandUserPlantMultiSelectToEditable` class.
    """

    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowLandUserPlantMultiSelectToEditable class.

        This method tests the validation rules for the request
        parameters of the
        land  flow.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowLandUserPlantMultiSelectToEditable(
            session_context)
        land = await \
            LandFactory.create_async(session)
        plant_code_list_csv: str = ""
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

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        Test the process_security_rules method of
        BaseFlowLandUserPlantMultiSelectToEditable.

        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a land
        object, and a
        BaseFlowLandUserPlantMultiSelectToEditable object.
        Then, it sets the role_required
        variable to "User" and calls the
        _process_security_rules method. Finally,
        it asserts that the expected validation
        errors are present in the flow's
        queued_validation_errors dictionary.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        land = await \
            LandFactory.create_async(session)
        flow = BaseFlowLandUserPlantMultiSelectToEditable(
            session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(land)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
