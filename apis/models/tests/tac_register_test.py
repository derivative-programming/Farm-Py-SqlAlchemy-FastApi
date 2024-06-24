# apis/models/tests/tac_register_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
TacRegisterPostModelResponse class.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.tac import TacBusObj
from flows.tac_register import FlowTacRegister, FlowTacRegisterResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
from ...models.tac_register import (
    TacRegisterPostModelResponse,
    TacRegisterPostModelRequest)
from ..factory.tac_register import TacRegisterPostModelRequestFactory
class TestTacRegisterPostModelRequest:
    """
    This class contains unit tests for the
    TacRegisterPostModelRequest class.
    """
    def test_default_values(self):
        """
        This method tests the default values of the
        TacRegisterPostModelRequest class.
        """
        model = TacRegisterPostModelRequest()
        assert model.force_error_message == ""
# endset
        assert model.email == ""
        assert model.password == ""
        assert model.confirm_password == ""
        assert model.first_name == ""
        assert model.last_name == ""
# endset
    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        TacRegisterPostModelRequest class.
        """
        model = TacRegisterPostModelRequest(
            force_error_message="Test Error",
# endset  # noqa: E122
            email="test@example.com",
            password="varchar",
            confirm_password="varchar",
            first_name="nvarchar",
            last_name="nvarchar",
# endset  # noqa: E122
        )
        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == "Test Error"
# endset
        assert snake_case_dict['email'] == "test@example.com"
        assert snake_case_dict['password'] == "varchar"
        assert snake_case_dict['confirm_password'] == "varchar"
        assert snake_case_dict['first_name'] == "nvarchar"
        assert snake_case_dict['last_name'] == "nvarchar"
# endset
    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        TacRegisterPostModelRequest class.
        """
        model = TacRegisterPostModelRequest(
            force_error_message="Test Error",
# endset  # noqa: E122
            email="test@example.com",
            password="varchar",
            confirm_password="varchar",
            first_name="nvarchar",
            last_name="nvarchar",
# endset  # noqa: E122
        )
        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == "Test Error"
# endset
        assert camel_case_dict['email'] == "test@example.com"
        assert camel_case_dict['password'] == "varchar"
        assert camel_case_dict['confirmPassword'] == "varchar"
        assert camel_case_dict['firstName'] == "nvarchar"
        assert camel_case_dict['lastName'] == "nvarchar"
# endset
    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        TacRegisterPostModelRequest class.
        """
        # Create an instance of the TacRegisterPostModelRequest class
        request = TacRegisterPostModelRequest(
            force_error_message="Test Error Message",
# endset  # noqa: E122
            email="test@example.com",
            password="Test VarChar",
            confirm_password="Test VarChar",
            first_name="Test NVarChar",
            last_name="Test NVarChar",
# endset  # noqa: E122
        )
        # Convert the model to a dictionary with snake_case keys and serialized values
        data = request.to_dict_snake_serialized()
        # Define the expected dictionary
        expected_data = {
            "force_error_message": "Test Error Message",
# endset  # noqa: E122
            "email": "test@example.com",
            "password": "Test VarChar",
            "confirm_password": "Test VarChar",
            "first_name": "Test NVarChar",
            "last_name": "Test NVarChar",
# endset  # noqa: E122
        }
        # Compare the actual and expected dictionaries
        assert data == expected_data
    def test_to_dict_camel_serialized(self):
        """
        This method tests the to_dict_camel_serialized method of the
        TacRegisterPostModelRequest class.
        """
        request = TacRegisterPostModelRequest(
            force_error_message="Test Error Message",
            email="test@example.com",
            password="Test Var Char",
            confirm_password="Test Var Char",
            first_name="Test N Var Char",
            last_name="Test N Var Char",
        )
        expected_data = {
            "forceErrorMessage": "Test Error Message",
            "email": "test@example.com",
            "password": "Test Var Char",
            "confirmPassword": "Test Var Char",
            "firstName": "Test N Var Char",
            "lastName": "Test N Var Char",
        }
        data = request.to_dict_camel_serialized()
        assert data == expected_data
class TestTacRegisterPostModelResponse:
    """
    This class contains unit tests for the
    TacRegisterPostModelResponse class.
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a customer to a tac.
        It mocks the process method of FlowTacRegister
        and asserts that the response is successful.
        """
        async def mock_process(
            tac_bus_obj: TacBusObj,
            email: str = "",
            password: str = "",
            confirm_password: str = "",
            first_name: str = "",
            last_name: str = "",
        ):
            return FlowTacRegisterResult()
        with patch.object(
            FlowTacRegister,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await (
                TacRegisterPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
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

