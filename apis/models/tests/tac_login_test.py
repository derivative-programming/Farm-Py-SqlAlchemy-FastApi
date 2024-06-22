# apis/models/tests/tac_login_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
TacLoginPostModelResponse class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.tac import TacBusObj
from flows.tac_login import FlowTacLogin, FlowTacLoginResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
from ...models.tac_login import (
    TacLoginPostModelResponse,
    TacLoginPostModelRequest)
from ..factory.tac_login import TacLoginPostModelRequestFactory
class TestTacLoginPostModelRequest:
    def test_default_values(self):
        model = TacLoginPostModelRequest()
        assert model.force_error_message == ""
# endset
        assert model.email == ""
        assert model.password == ""
# endset
    def test_to_dict_snake(self):
        model = TacLoginPostModelRequest(
            force_error_message="Test Error",
# endset
            email="test@example.com",
            password="varchar",
# endset
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset
        assert snake_case_dict['email'] == "test@example.com"
        assert snake_case_dict['password'] == "varchar"
# endset
    def test_to_dict_camel(self):
        model = TacLoginPostModelRequest(
            force_error_message="Test Error",
# endset
            email="test@example.com",
            password="varchar",
# endset
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset
        assert camel_case_dict['email'] == "test@example.com"
        assert camel_case_dict['password'] == "varchar"
# endset
class TestTacLoginPostModelResponse:
    """
    This class contains unit tests for the
    TacLoginPostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a tac.
        It mocks the process method of FlowTacLogin
        and asserts that the response is successful.
        """
        async def mock_process(
            tac_bus_obj: TacBusObj,
            email: str = "",
            password: str = "",
        ):
            return FlowTacLoginResult()
        with patch.object(
            FlowTacLogin,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                TacLoginPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = TacLoginPostModelResponse()
            session_context = SessionContext(dict(), session)
            tac = await TacFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                tac_code=tac.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

