from decimal import Decimal
import uuid
import pytest
from decimal import Decimal
from datetime import datetime, date
from flows.base.land_add_plant_init_obj_wf import BaseFlowLandAddPlantInitObjWF
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.land import LandFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect
from sqlalchemy import String
import flows.constants.land_add_plant_init_obj_wf as FlowConstants
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestBaseFlowLandAddPlantInitObjWF():
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        session_context = SessionContext(dict(), session)
        flow = BaseFlowLandAddPlantInitObjWF(session_context)
        land = await LandFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)

        # Call the method being tested
        await flow._process_validation_rules(
            land,

            )
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        session_context = SessionContext(dict(), session)
        land = await LandFactory.create_async(session)
        flow = BaseFlowLandAddPlantInitObjWF(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(land)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
