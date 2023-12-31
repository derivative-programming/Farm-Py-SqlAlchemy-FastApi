from decimal import Decimal
import uuid
import pytest
from decimal import Decimal
from datetime import datetime, date
from flows.base.tac_register import BaseFlowTacRegister
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.flavor import FlavorFactory
from models.factory.tac import TacFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect
from sqlalchemy import String
import flows.constants.tac_register as FlowConstants
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestBaseFlowTacRegister():
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        session_context = SessionContext(dict(), session)
        flow = BaseFlowTacRegister(session_context)
        tac = await TacFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)
        email:str = ""
        password:str = ""
        confirm_password:str = ""
        first_name:str = ""
        last_name:str = ""
        # Call the method being tested
        await flow._process_validation_rules(
            tac,
            email,
            password,
            confirm_password,
            first_name,
            last_name,
            )
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed
        if FlowConstants.param_email_isRequired == True:
            assert 'email' in flow.queued_validation_errors and flow.queued_validation_errors['email'] == 'Please enter a Email'
        if FlowConstants.param_password_isRequired == True:
            assert 'password' in flow.queued_validation_errors and flow.queued_validation_errors['password'] == 'Please enter a Password'
        if FlowConstants.param_confirm_password_isRequired == True:
            assert 'confirmPassword' in flow.queued_validation_errors and flow.queued_validation_errors['confirmPassword'] == 'Please enter a '
        if FlowConstants.param_first_name_isRequired == True:
            assert 'firstName' in flow.queued_validation_errors and flow.queued_validation_errors['firstName'] == 'Please enter a First Name'
        if FlowConstants.param_last_name_isRequired == True:
            assert 'lastName' in flow.queued_validation_errors and flow.queued_validation_errors['lastName'] == 'Please enter a Last Name'
    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        session_context = SessionContext(dict(), session)
        tac = await TacFactory.create_async(session)
        flow = BaseFlowTacRegister(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(tac)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
