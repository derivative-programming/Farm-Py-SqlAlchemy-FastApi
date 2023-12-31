from decimal import Decimal
import uuid
import pytest
from decimal import Decimal
from datetime import datetime, date
from flows.base.error_log_config_resolve_error_log import BaseFlowErrorLogConfigResolveErrorLog
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.error_log import ErrorLogFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect
from sqlalchemy import String
import flows.constants.error_log_config_resolve_error_log as FlowConstants
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestBaseFlowErrorLogConfigResolveErrorLog():
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        session_context = SessionContext(dict(), session)
        flow = BaseFlowErrorLogConfigResolveErrorLog(session_context)
        error_log = await ErrorLogFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)

        # Call the method being tested
        await flow._process_validation_rules(
            error_log,

            )
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        session_context = SessionContext(dict(), session)
        error_log = await ErrorLogFactory.create_async(session)
        flow = BaseFlowErrorLogConfigResolveErrorLog(session_context)
        role_required = "Config"
        if len(role_required) > 0:
            await flow._process_security_rules(error_log)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
