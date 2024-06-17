# flows/base/tests/error_log_config_resolve_error_log_test.py
# pylint: disable=protected-access
"""
    #TODO add comment
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
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        #TODO add comment
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
        error_log = await ErrorLogFactory.create_async(session)
        flow = BaseFlowErrorLogConfigResolveErrorLog(session_context)
        role_required = "Config"
        if len(role_required) > 0:
            await flow._process_security_rules(error_log)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                "Unautorized access. " + role_required + " role not found.")
            session_context.role_name_csv = role_required
