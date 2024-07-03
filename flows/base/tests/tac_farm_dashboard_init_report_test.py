# flows/base/tests/tac_farm_dashboard_init_report_test.py
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains the unit tests for the
`BaseFlowTacFarmDashboardInitReport` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.tac_farm_dashboard_init_report \
    as FlowConstants  # noqa: F401
from flows.base.tac_farm_dashboard_init_report import (
    BaseFlowTacFarmDashboardInitReport)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.tac import TacFactory


class TestBaseFlowTacFarmDashboardInitReport():
    """
    This class contains unit tests for the
    `BaseFlowTacFarmDashboardInitReport` class.
    """

    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowTacFarmDashboardInitReport class.

        This method tests the validation rules for the request
        parameters of the
        tac  flow.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowTacFarmDashboardInitReport(
            session_context)
        tac = await \
            TacFactory.create_async(session)

        # Call the method being tested
        await flow._process_validation_rules(
            tac,

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
        BaseFlowTacFarmDashboardInitReport.

        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a tac
        object, and a
        BaseFlowTacFarmDashboardInitReport object.
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
        session_context = SessionContext(dict(), session)
        tac = await \
            TacFactory.create_async(session)
        flow = BaseFlowTacFarmDashboardInitReport(
            session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(tac)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
