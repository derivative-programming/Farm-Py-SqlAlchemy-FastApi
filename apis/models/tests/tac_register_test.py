# apis/models/tests/tac_register_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains unit tests for the
TacRegisterPostModelResponse class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch

import pytest

from business.tac import TacBusObj
from flows.tac_register import (
    FlowTacRegister,
    FlowTacRegisterResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.tac import TacFactory

from ...models.tac_register import (
    TacRegisterPostModelResponse,
    TacRegisterPostModelRequest)
from ..factory.tac_register import (
    TacRegisterPostModelRequestFactory)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


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
        assert model.email == ""
        assert model.password == ""
        assert model.confirm_password == ""
        assert model.first_name == ""
        assert model.last_name == ""

    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        TacRegisterPostModelRequest class.
        """
        model = TacRegisterPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            email=TEST_EMAIL,
            password="varchar",
            confirm_password="varchar",
            first_name="nvarchar",
            last_name="nvarchar",
# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT
        assert snake_case_dict['email'] == \
            model.email
        assert snake_case_dict['password'] == \
            model.password
        assert snake_case_dict['confirm_password'] == \
            model.confirm_password
        assert snake_case_dict['first_name'] == \
            model.first_name
        assert snake_case_dict['last_name'] == \
            model.last_name

    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        TacRegisterPostModelRequest class.
        """
        model = TacRegisterPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            email=TEST_EMAIL,
            password="varchar",
            confirm_password="varchar",
            first_name="nvarchar",
            last_name="nvarchar",
# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT
        assert camel_case_dict['email'] == \
            model.email
        assert camel_case_dict['password'] == \
            model.password
        assert camel_case_dict['confirmPassword'] == \
            model.confirm_password
        assert camel_case_dict['firstName'] == \
            model.first_name
        assert camel_case_dict['lastName'] == \
            model.last_name

    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        TacRegisterPostModelRequest class.
        """
        # Create an instance of the
        # TacRegisterPostModelRequest class
        request = TacRegisterPostModelRequest(
            force_error_message="Test Error Message",
# endset  # noqa: E122
            email=TEST_EMAIL,
            password="Test VarChar",
            confirm_password="Test VarChar",
            first_name="Test NVarChar",
            last_name="Test NVarChar",
# endset  # noqa: E122
        )

        # Convert the model to a dictionary with snake_case
        # keys and serialized values
        data = request.to_dict_snake_serialized()

        # Define the expected dictionary
        expected_data = {
            "force_error_message": "Test Error Message",
# endset  # noqa: E122
            "email": TEST_EMAIL,
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
            email=TEST_EMAIL,
            password="Test Var Char",
            confirm_password="Test Var Char",
            first_name="Test N Var Char",
            last_name="Test N Var Char",
        )

        expected_data = {
            "forceErrorMessage": "Test Error Message",
            "email": TEST_EMAIL,
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
        It mocks the process method of
        FlowTacRegister
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
            response_instance = \
                TacRegisterPostModelResponse()
            session_context = SessionContext({}, session)

            tac = await TacFactory.create_async(session)

            await response_instance.process_request(
                session_context=session_context,
                tac_code=tac.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()
