# apis/models/init/tests/pac_user_tri_state_filter_list_init_report_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
"""
This module contains the unit tests for the
pac_user_tri_state_filter_list_init_report module.
"""
import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest

from helpers import SessionContext, TypeConversion

from models.factory.pac import PacFactory
from ..pac_user_tri_state_filter_list_init_report import (
    PacUserTriStateFilterListInitReportGetInitModelRequest,
    PacUserTriStateFilterListInitReportGetInitModelResponse)


class MockFlowPacUserTriStateFilterListInitReportResult:  # pylint: disable=too-few-public-methods
    """
    A mock object for the
    FlowPacUserTriStateFilterListInitReportResult
    class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """


@pytest.fixture
def flow_response():
    """
    Return a mock
    FlowPacUserTriStateFilterListInitReportResult
    object.
    """
    return MockFlowPacUserTriStateFilterListInitReportResult()


def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = PacUserTriStateFilterListInitReportGetInitModelResponse()
    response.load_flow_response(flow_response)


def test_to_json():
    """
    Test the to_json method.
    """
    response = PacUserTriStateFilterListInitReportGetInitModelResponse(
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
async def test_process_request(flow_response, session):
    """
    Test the process_request method.
    """
    session_context = SessionContext({}, session)
    mock_flow = patch(
        "apis.models.init.pac_user_tri_state_filter_list_init_report."
        "FlowPacUserTriStateFilterListInitReport",
        autospec=True).start()
    mock_flow_instance = \
        mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)

    request = PacUserTriStateFilterListInitReportGetInitModelRequest()
    response = PacUserTriStateFilterListInitReportGetInitModelResponse()

    pac = await PacFactory.create_async(session)

    result = await request.process_request(
        session_context,
        pac.code,
        response)

    assert result.success is True
    assert result.message == "Success."
    mock_flow_instance.process.assert_called_once()

    patch.stopall()
