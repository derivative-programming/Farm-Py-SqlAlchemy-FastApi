# flows/base/tests/plant_user_delete_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-import
"""
This module contains the unit tests for the
`BaseFlowPlantUserDelete` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.plant_user_delete \
    as FlowConstants  # noqa: F401
from flows.base.plant_user_delete import (
    BaseFlowPlantUserDelete)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.plant import PlantFactory


class TestBaseFlowPlantUserDelete():
    """
    This class contains unit tests for the
    `BaseFlowPlantUserDelete` class.
    """

    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowPlantUserDelete class.

        This method tests the validation rules for the request
        parameters of the
        plant  flow.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext({}, session)
        flow = BaseFlowPlantUserDelete(
            session_context)
        plant = await \
            PlantFactory.create_async(session)

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


    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        Test the process_security_rules method of
        BaseFlowPlantUserDelete.

        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a plant
        object, and a
        BaseFlowPlantUserDelete object.
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
        session_context = SessionContext({}, session)
        plant = await \
            PlantFactory.create_async(session)
        flow = BaseFlowPlantUserDelete(
            session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(plant)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
