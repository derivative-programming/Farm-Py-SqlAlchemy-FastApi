# apis/models/tests/pac_process_all_dyna_flow_type_schedule_flow_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import
"""
This module contains unit tests for the
PacProcessAllDynaFlowTypeScheduleFlowPostModelResponse class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch

import pytest

from business.pac import PacBusObj
from flows.pac_process_all_dyna_flow_type_schedule_flow import (
    FlowPacProcessAllDynaFlowTypeScheduleFlow,
    FlowPacProcessAllDynaFlowTypeScheduleFlowResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.pac import PacFactory

from ...models.pac_process_all_dyna_flow_type_schedule_flow import (
    PacProcessAllDynaFlowTypeScheduleFlowPostModelResponse,
    PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest)
from ..factory.pac_process_all_dyna_flow_type_schedule_flow import (
    PacProcessAllDynaFlowTypeScheduleFlowPostModelRequestFactory)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestPacProcessAllDynaFlowTypeScheduleFlowPostModelRequest:
    """
    This class contains unit tests for the
    PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest class.
    """

    def test_default_values(self):
        """
        This method tests the default values of the
        PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest class.
        """
        model = PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest()
        assert model.force_error_message == ""


    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest class.
        """
        model = PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122

# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT


    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest class.
        """
        model = PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122

# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT


    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest class.
        """
        # Create an instance of the
        # PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest class
        request = PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest(
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
        PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest class.
        """
        request = PacProcessAllDynaFlowTypeScheduleFlowPostModelRequest(
            force_error_message="Test Error Message",

        )

        expected_data = {
            "forceErrorMessage": "Test Error Message",

        }

        data = request.to_dict_camel_serialized()

        assert data == expected_data


class TestPacProcessAllDynaFlowTypeScheduleFlowPostModelResponse:  # pylint: disable=too-few-public-methods
    """
    This class contains unit tests for the
    PacProcessAllDynaFlowTypeScheduleFlowPostModelResponse class.
    """

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a pac.
        It mocks the process method of
        FlowPacProcessAllDynaFlowTypeScheduleFlow
        and asserts that the response is successful.
        """

        async def mock_process(
            pac_bus_obj: PacBusObj,

        ):
            return FlowPacProcessAllDynaFlowTypeScheduleFlowResult()
        with patch.object(
            FlowPacProcessAllDynaFlowTypeScheduleFlow,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process

            request_instance = await (
                PacProcessAllDynaFlowTypeScheduleFlowPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = \
                PacProcessAllDynaFlowTypeScheduleFlowPostModelResponse()
            session_context = SessionContext({}, session)

            pac = await PacFactory.create_async(session)

            await response_instance.process_request(
                session_context=session_context,
                pac_code=pac.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()
