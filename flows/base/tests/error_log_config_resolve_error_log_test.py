# flows/base/tests/error_log_config_resolve_error_log_test.py
# pylint: disable=protected-access
"""
This module contains the unit tests for the `BaseFlowErrorLogConfigResolveErrorLog` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.error_log_config_resolve_error_log as FlowConstants
from flows.base.error_log_config_resolve_error_log import (
    BaseFlowErrorLogConfigResolveErrorLog)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.error_log import ErrorLogFactory
class TestBaseFlowErrorLogConfigResolveErrorLog():
    """
    This class contains unit tests for the `BaseFlowErrorLogConfigResolveErrorLog` class.
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowErrorLogConfigResolveErrorLog class.
        This method tests the validation rules for the request
        parameters of the error_log  flow.
        Args:
            session: The session object for the test.
        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowErrorLogConfigResolveErrorLog(session_context)
        error_log = await ErrorLogFactory.create_async(session)

# endset
        # Call the method being tested
        await flow._process_validation_rules(
            error_log,

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
        Test the process_security_rules method of BaseFlowErrorLogConfigResolveErrorLog.
        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a error_log
        object, and a BaseFlowErrorLogConfigResolveErrorLog object.
        Then, it sets the role_required
        variable to "Config" and calls the
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
        error_log = await ErrorLogFactory.create_async(session)
        flow = BaseFlowErrorLogConfigResolveErrorLog(session_context)
        role_required = "Config"
        if len(role_required) > 0:
            await flow._process_security_rules(error_log)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
