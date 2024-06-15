# flows/default/tests/tac_login_test.py
"""
    #TODO add comment
"""
import asyncio
from decimal import Decimal
import json
import uuid
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.tac_login import FlowTacLogin, FlowTacLoginResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
from models import Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field, UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants
class TestTacLoginPostModelResponse:
    """
    #TODO add comment
    """
    def test_flow_tac_login_result_to_json(self):
        # Create an instance and set attributes
        result = FlowTacLoginResult()
        result.context_object_code = uuid.uuid4()
        result.customer_code = uuid.uuid4()
        result.email = "test flavor"
        result.user_code_value = uuid.uuid4()
        result.utc_offset_in_minutes = 123
        result.role_name_csv_list = "test flavor"
        result.api_key = "test flavor"
# endset
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
# endset
    #todo finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        session_context = SessionContext(dict(), session)
        flow = FlowTacLogin(session_context)
        tac = await TacFactory.create_async(session)
        tac_bus_obj = TacBusObj(session_context)
        await tac_bus_obj.load_from_obj_instance(tac)
        role_required = ""
        email: str = "",
        password: str = "",
# endset
        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    tac_bus_obj,
                    email,
                    password,
# endset  # noqa: E122
                )
        session_context.role_name_csv = role_required
        customerCodeMatchRequired = False
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed is True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed is True:
            customerCodeMatchRequired = True
        if customerCodeMatchRequired is True:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    tac_bus_obj,
                    email,
                    password,
# endset  # noqa: E122
                )
        session_context.role_name_csv = role_required
        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     tac_code=tac.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowTacLoginResult)

