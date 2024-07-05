# flows/base/tests/dyna_flow_task_plant_task_two_test.py
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains the unit tests for the
`BaseFlowDynaFlowTaskPlantTaskTwo` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.dyna_flow_task_plant_task_two \
    as FlowConstants  # noqa: F401
from flows.base.dyna_flow_task_plant_task_two import (
    BaseFlowDynaFlowTaskPlantTaskTwo)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.dyna_flow_task import DynaFlowTaskFactory


class TestBaseFlowDynaFlowTaskPlantTaskTwo():
    """
    This class contains unit tests for the
    `BaseFlowDynaFlowTaskPlantTaskTwo` class.
    """

    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowDynaFlowTaskPlantTaskTwo class.

        This method tests the validation rules for the request
        parameters of the
        dyna_flow_task  flow.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext({}, session)
        flow = BaseFlowDynaFlowTaskPlantTaskTwo(
            session_context)
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(session)

        # Call the method being tested
        await flow._process_validation_rules(
            dyna_flow_task,

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
        BaseFlowDynaFlowTaskPlantTaskTwo.

        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a dyna_flow_task
        object, and a
        BaseFlowDynaFlowTaskPlantTaskTwo object.
        Then, it sets the role_required
        variable to "" and calls the
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
        dyna_flow_task = await \
            DynaFlowTaskFactory.create_async(session)
        flow = BaseFlowDynaFlowTaskPlantTaskTwo(
            session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(dyna_flow_task)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
