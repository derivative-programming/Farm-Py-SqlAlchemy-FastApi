# apis/models/tests/tac_register_test.py
"""
    #TODO add comment
"""
import asyncio
import time
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch
import pytest
import pytest_asyncio
from pydantic import UUID4, Field
from sqlalchemy import String, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.tac import TacBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.tac_register import FlowTacRegister, FlowTacRegisterResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models import Base
from models.factory.tac import TacFactory
from ...models.tac_register import (TacRegisterPostModelRequest,
                                      TacRegisterPostModelResponse)
from ..factory.tac_register import TacRegisterPostModelRequestFactory
class TestTacRegisterPostModelResponse:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        async def mock_process(
            tac_bus_obj: TacBusObj,  # pylint: disable=unused-argument
            email: str = "",  # pylint: disable=unused-argument
            password: str = "",  # pylint: disable=unused-argument
            confirm_password: str = "",  # pylint: disable=unused-argument
            first_name: str = "",  # pylint: disable=unused-argument
            last_name: str = "",  # pylint: disable=unused-argument
        ):
            return FlowTacRegisterResult()
        with patch.object(FlowTacRegister, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await TacRegisterPostModelRequestFactory.create_async(session=session)
            response_instance = TacRegisterPostModelResponse()
            session_context = SessionContext(dict(), session)
            tac = await TacFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                tac_code=tac.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

