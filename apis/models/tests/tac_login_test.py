# apis/models/tests/tac_login_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the
TacLoginPostModelResponse class.
"""

import uuid
import math
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

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestTacLoginPostModelRequest:
    """
    This class contains unit tests for the
    TacLoginPostModelRequest class.
    """

    def test_default_values(self):
        """
        This method tests the default values of the
        TacLoginPostModelRequest class.
        """
        model = TacLoginPostModelRequest()
        assert model.force_error_message == ""
        assert model.email == ""
        assert model.password == ""

    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        TacLoginPostModelRequest class.
        """
        model = TacLoginPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            email=TEST_EMAIL,
            password="varchar",
# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT
        assert snake_case_dict['email'] == \
            model.email
        assert snake_case_dict['password'] == \
            model.password

    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        TacLoginPostModelRequest class.
        """
        model = TacLoginPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            email=TEST_EMAIL,
            password="varchar",
# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT
        assert camel_case_dict['email'] == \
            model.email
        assert camel_case_dict['password'] == \
            model.password

    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        TacLoginPostModelRequest class.
        """
        # Create an instance of the TacLoginPostModelRequest class
        request = TacLoginPostModelRequest(
            force_error_message="Test Error Message",
# endset  # noqa: E122
            email=TEST_EMAIL,
            password="Test VarChar",
# endset  # noqa: E122
        )

        # Convert the model to a dictionary with snake_case keys and serialized values
        data = request.to_dict_snake_serialized()

        # Define the expected dictionary
        expected_data = {
            "force_error_message": "Test Error Message",
# endset  # noqa: E122
            "email": TEST_EMAIL,
            "password": "Test VarChar",
# endset  # noqa: E122
        }

        # Compare the actual and expected dictionaries
        assert data == expected_data

    def test_to_dict_camel_serialized(self):
        """
        This method tests the to_dict_camel_serialized method of the
        TacLoginPostModelRequest class.
        """
        request = TacLoginPostModelRequest(
            force_error_message="Test Error Message",
            email=TEST_EMAIL,
            password="Test Var Char",
        )

        expected_data = {
            "forceErrorMessage": "Test Error Message",
            "email": TEST_EMAIL,
            "password": "Test Var Char",
        }

        data = request.to_dict_camel_serialized()

        assert data == expected_data


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

