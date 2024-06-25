# apis/models/init/tests/pac_user_role_list_init_report_test.py
# pylint: disable=redefined-outer-name
"""
This module contains the unit tests for the
pac_user_role_list_init_report module.
"""
import json
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, Mock, patch

import pytest

from helpers import SessionContext

from ..pac_user_role_list_init_report import (
    PacUserRoleListInitReportGetInitModelRequest,
    PacUserRoleListInitReportGetInitModelResponse)


class MockFlowPacUserRoleListInitReportResult:
    """
    A mock object for the FlowPacUserRoleListInitReportResult class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """


@pytest.fixture
def flow_response():
    """
    Return a mock FlowPacUserRoleListInitReportResult object.
    """
    return MockFlowPacUserRoleListInitReportResult()


def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = PacUserRoleListInitReportGetInitModelResponse()
    response.load_flow_response(flow_response)


def test_to_json():
    """
    Test the to_json method.
    """
    response = PacUserRoleListInitReportGetInitModelResponse(
        success=True,
        message="Test Message",
        validation_errors=[],
# endset  # noqa: E122

# endset  # noqa: E122
    )
    json_response = response.to_json()
    assert isinstance(json_response, str)

    json_data = json.loads(json_response)

    assert json_data["success"] == response.success
    assert json_data["message"] == response.message


@pytest.mark.asyncio
async def test_process_request(flow_response):
    """
    Test the process_request method.
    """
    mock_session_context = Mock(spec=SessionContext)
    mock_pac_bus_obj = patch(
        'apis.models.init.pac_user_role_list_init_report.PacBusObj',
        autospec=True).start()
    mock_flow = patch(
        "apis.models.init.pac_user_role_list_init_report."
        "FlowPacUserRoleListInitReport",
        autospec=True).start()
    mock_flow_instance = mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)

    request = PacUserRoleListInitReportGetInitModelRequest()
    response = PacUserRoleListInitReportGetInitModelResponse()

    pac_code = uuid.uuid4()
    result = await request.process_request(
        mock_session_context,
        pac_code,
        response)

    assert result.success is True
    assert result.message == "Success."
    mock_pac_bus_obj.assert_called_once_with(mock_session_context)
    mock_flow_instance.process.assert_called_once()

    patch.stopall()

