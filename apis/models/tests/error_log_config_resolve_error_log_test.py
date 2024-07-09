# apis/models/tests/error_log_config_resolve_error_log_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains unit tests for the
ErrorLogConfigResolveErrorLogPostModelResponse class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch

import pytest

from business.error_log import ErrorLogBusObj
from flows.error_log_config_resolve_error_log import (
    FlowErrorLogConfigResolveErrorLog,
    FlowErrorLogConfigResolveErrorLogResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.error_log import ErrorLogFactory

from ...models.error_log_config_resolve_error_log import (
    ErrorLogConfigResolveErrorLogPostModelResponse,
    ErrorLogConfigResolveErrorLogPostModelRequest)
from ..factory.error_log_config_resolve_error_log import (
    ErrorLogConfigResolveErrorLogPostModelRequestFactory)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestErrorLogConfigResolveErrorLogPostModelRequest:
    """
    This class contains unit tests for the
    ErrorLogConfigResolveErrorLogPostModelRequest class.
    """

    def test_default_values(self):
        """
        This method tests the default values of the
        ErrorLogConfigResolveErrorLogPostModelRequest class.
        """
        model = ErrorLogConfigResolveErrorLogPostModelRequest()
        assert model.force_error_message == ""


    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        ErrorLogConfigResolveErrorLogPostModelRequest class.
        """
        model = ErrorLogConfigResolveErrorLogPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122

# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT


    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        ErrorLogConfigResolveErrorLogPostModelRequest class.
        """
        model = ErrorLogConfigResolveErrorLogPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122

# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT


    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        ErrorLogConfigResolveErrorLogPostModelRequest class.
        """
        # Create an instance of the
        # ErrorLogConfigResolveErrorLogPostModelRequest class
        request = ErrorLogConfigResolveErrorLogPostModelRequest(
            force_error_message="Test Error Message",
# endset  # noqa: E122

# endset  # noqa: E122
        )

        # Convert the model to a dictionary with snake_case
        # keys and serialized values
        data = request.to_dict_snake_serialized()

        # Define the expected dictionary
        expected_data = {
            "force_error_message": "Test Error Message",
# endset  # noqa: E122

# endset  # noqa: E122
        }

        # Compare the actual and expected dictionaries
        assert data == expected_data

    def test_to_dict_camel_serialized(self):
        """
        This method tests the to_dict_camel_serialized method of the
        ErrorLogConfigResolveErrorLogPostModelRequest class.
        """
        request = ErrorLogConfigResolveErrorLogPostModelRequest(
            force_error_message="Test Error Message",

        )

        expected_data = {
            "forceErrorMessage": "Test Error Message",

        }

        data = request.to_dict_camel_serialized()

        assert data == expected_data


class TestErrorLogConfigResolveErrorLogPostModelResponse:
    """
    This class contains unit tests for the
    ErrorLogConfigResolveErrorLogPostModelResponse class.
    """

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a error_log.
        It mocks the process method of
        FlowErrorLogConfigResolveErrorLog
        and asserts that the response is successful.
        """

        async def mock_process(
            error_log_bus_obj: ErrorLogBusObj,

        ):
            return FlowErrorLogConfigResolveErrorLogResult()
        with patch.object(
            FlowErrorLogConfigResolveErrorLog,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process

            request_instance = await (
                ErrorLogConfigResolveErrorLogPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = \
                ErrorLogConfigResolveErrorLogPostModelResponse()
            session_context = SessionContext({}, session)

            error_log = await ErrorLogFactory.create_async(session)

            await response_instance.process_request(
                session_context=session_context,
                error_log_code=error_log.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()
