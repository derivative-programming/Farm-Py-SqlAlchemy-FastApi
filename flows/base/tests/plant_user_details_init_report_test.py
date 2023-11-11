from decimal import Decimal
import uuid
import pytest
from decimal import Decimal
from datetime import datetime, date
from flows.base.plant_user_details_init_report import BaseFlowPlantUserDetailsInitReport
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.plant import PlantFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect
from sqlalchemy import String
import flows.constants.plant_user_details_init_report as FlowConstants
# DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestBaseFlowPlantUserDetailsInitReport():
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        session_context = SessionContext(dict())
        flow = BaseFlowPlantUserDetailsInitReport(session_context)
        plant = await PlantFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)

        # Call the method being tested
        await flow._process_validation_rules(
            plant,

            )
        # Add assertions here to validate the expected behavior
        #TODO add validation checks - is required,
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        session_context = SessionContext(dict())
        plant = await PlantFactory.create_async(session)
        flow = BaseFlowPlantUserDetailsInitReport(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(plant)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
        # Add assertions here to validate the expected behavior
