import asyncio
from decimal import Decimal
import json
import uuid
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.tac_register import FlowTacRegister, FlowTacRegisterResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
from models import Base
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field,UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestTacRegisterPostModelResponse:
    def test_flow_tac_register_result_to_json(self):
        # Create an instance and set attributes
        result = FlowTacRegisterResult()
        result.context_object_code = uuid.uuid4()
        result.customer_code = uuid.uuid4()
        result.email = "test flavor"
        result.user_code_value = uuid.uuid4()
        result.utc_offset_in_minutes = 123
        result.role_name_csv_list = "test flavor"
        result.api_key = "test flavor"

        # Call to_json method
        json_output = result.to_json()
        # Parse JSON output
        data = json.loads(json_output)
        # Assert individual fields
        assert data["context_object_code"] == str(result.context_object_code)
        assert data["customer_code"] == str(result.customer_code)
        assert data["email"] == result.email
        assert data["user_code_value"] == str(result.user_code_value)
        assert data["utc_offset_in_minutes"] == result.utc_offset_in_minutes
        assert data["role_name_csv_list"] == result.role_name_csv_list
        assert data["api_key"] == result.api_key

    #todo finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        session_context = SessionContext(dict(), session)
        flow = FlowTacRegister(session_context)
        tac = await TacFactory.create_async(session)
        tac_bus_obj = TacBusObj(session_context)
        await tac_bus_obj.load(tac_obj_instance=tac)
        role_required = ""
        email:str = "",
        password:str = "",
        confirm_password:str = "",
        first_name:str = "",
        last_name:str = "",

        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    tac_bus_obj,
                    email,
                    password,
                    confirm_password,
                    first_name,
                    last_name,

                )
        session_context.role_name_csv = role_required
        customerCodeMatchRequired = False
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        if customerCodeMatchRequired == True:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    tac_bus_obj,
                    email,
                    password,
                    confirm_password,
                    first_name,
                    last_name,

                )
        session_context.role_name_csv = role_required
        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     tac_code=tac.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowTacRegisterResult)

