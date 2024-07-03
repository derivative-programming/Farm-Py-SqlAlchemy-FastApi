# flows/base/tests/pac_user_tri_state_filter_list_init_report_test.py
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains the unit tests for the
`BaseFlowPacUserTriStateFilterListInitReport` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.pac_user_tri_state_filter_list_init_report \
    as FlowConstants  # noqa: F401
from flows.base.pac_user_tri_state_filter_list_init_report import (
    BaseFlowPacUserTriStateFilterListInitReport)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.pac import PacFactory


class TestBaseFlowPacUserTriStateFilterListInitReport():
    """
    This class contains unit tests for the
    `BaseFlowPacUserTriStateFilterListInitReport` class.
    """

    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowPacUserTriStateFilterListInitReport class.

        This method tests the validation rules for the request
        parameters of the
        pac  flow.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowPacUserTriStateFilterListInitReport(
            session_context)
        pac = await \
            PacFactory.create_async(session)

        # Call the method being tested
        await flow._process_validation_rules(
            pac,

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
        BaseFlowPacUserTriStateFilterListInitReport.

        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a pac
        object, and a
        BaseFlowPacUserTriStateFilterListInitReport object.
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
        pac = await \
            PacFactory.create_async(session)
        flow = BaseFlowPacUserTriStateFilterListInitReport(
            session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(pac)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
