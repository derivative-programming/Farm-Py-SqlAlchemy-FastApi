# apis/models/tests/process_all_dyna_flow_type_schedule_task_test.py
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
This module contains unit tests for the
ProcessAllDynaFlowTypeScheduleTaskPostModelResponse class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch

import pytest

from business.dyna_flow_task import DynaFlowTaskBusObj
from flows.process_all_dyna_flow_type_schedule_task import (
    FlowProcessAllDynaFlowTypeScheduleTask,
    FlowProcessAllDynaFlowTypeScheduleTaskResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.dyna_flow_task import DynaFlowTaskFactory

from ...models.process_all_dyna_flow_type_schedule_task import (
    ProcessAllDynaFlowTypeScheduleTaskPostModelResponse,
    ProcessAllDynaFlowTypeScheduleTaskPostModelRequest)
from ..factory.process_all_dyna_flow_type_schedule_task import (
    ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactory)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestProcessAllDynaFlowTypeScheduleTaskPostModelRequest:
    """
    This class contains unit tests for the
    ProcessAllDynaFlowTypeScheduleTaskPostModelRequest class.
    """

    def test_default_values(self):
        """
        This method tests the default values of the
        ProcessAllDynaFlowTypeScheduleTaskPostModelRequest class.
        """
        model = ProcessAllDynaFlowTypeScheduleTaskPostModelRequest()
        assert model.force_error_message == ""


    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        ProcessAllDynaFlowTypeScheduleTaskPostModelRequest class.
        """
        model = ProcessAllDynaFlowTypeScheduleTaskPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122

# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT


    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        ProcessAllDynaFlowTypeScheduleTaskPostModelRequest class.
        """
        model = ProcessAllDynaFlowTypeScheduleTaskPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122

# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT


    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        ProcessAllDynaFlowTypeScheduleTaskPostModelRequest class.
        """
        # Create an instance of the
        # ProcessAllDynaFlowTypeScheduleTaskPostModelRequest class
        request = ProcessAllDynaFlowTypeScheduleTaskPostModelRequest(
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
        ProcessAllDynaFlowTypeScheduleTaskPostModelRequest class.
        """
        request = ProcessAllDynaFlowTypeScheduleTaskPostModelRequest(
            force_error_message="Test Error Message",

        )

        expected_data = {
            "forceErrorMessage": "Test Error Message",

        }

        data = request.to_dict_camel_serialized()

        assert data == expected_data


class TestProcessAllDynaFlowTypeScheduleTaskPostModelResponse:
    """
    This class contains unit tests for the
    ProcessAllDynaFlowTypeScheduleTaskPostModelResponse class.
    """

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a  to a dyna_flow_task.
        It mocks the process method of
        FlowProcessAllDynaFlowTypeScheduleTask
        and asserts that the response is successful.
        """

        async def mock_process(
            dyna_flow_task_bus_obj: DynaFlowTaskBusObj,

        ):
            return FlowProcessAllDynaFlowTypeScheduleTaskResult()
        with patch.object(
            FlowProcessAllDynaFlowTypeScheduleTask,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process

            request_instance = await (
                ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = \
                ProcessAllDynaFlowTypeScheduleTaskPostModelResponse()
            session_context = SessionContext(dict(), session)

            dyna_flow_task = await DynaFlowTaskFactory.create_async(session)

            await response_instance.process_request(
                session_context=session_context,
                dyna_flow_task_code=dyna_flow_task.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()
