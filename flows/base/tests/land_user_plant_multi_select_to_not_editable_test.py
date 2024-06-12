# flows/base/tests/land_user_plant_multi_select_to_not_editable_test.py
"""
    #TODO add comment
"""
from decimal import Decimal
import uuid
import pytest
from decimal import Decimal
from datetime import datetime, date
from flows.base.land_user_plant_multi_select_to_not_editable import BaseFlowLandUserPlantMultiSelectToNotEditable
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.land import LandFactory
from services.db_config import DB_DIALECT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT
from sqlalchemy import String
import flows.constants.land_user_plant_multi_select_to_not_editable as FlowConstants
DB_DIALECT = "sqlite"
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestBaseFlowLandUserPlantMultiSelectToNotEditable():
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        session_context = SessionContext(dict(), session)
        flow = BaseFlowLandUserPlantMultiSelectToNotEditable(session_context)
        land = await LandFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)
        plant_code_list_csv: str = ""
        # Call the method being tested
        await flow._process_validation_rules(
            land,
            plant_code_list_csv,
            )
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed
        if FlowConstants.param_plant_code_list_csv_isRequired is True:
            assert 'plantCodeListCsv' in flow.queued_validation_errors and flow.queued_validation_errors['plantCodeListCsv'] == 'Please enter a plant Code List Csv'
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        session_context = SessionContext(dict(), session)
        land = await LandFactory.create_async(session)
        flow = BaseFlowLandUserPlantMultiSelectToNotEditable(session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(land)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
