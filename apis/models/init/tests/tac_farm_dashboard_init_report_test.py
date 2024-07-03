# apis/models/init/tests/tac_farm_dashboard_init_report_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
This module contains the unit tests for the
tac_farm_dashboard_init_report module.
"""
import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest

from helpers import SessionContext

from ..tac_farm_dashboard_init_report import (
    TacFarmDashboardInitReportGetInitModelRequest,
    TacFarmDashboardInitReportGetInitModelResponse)


class MockFlowTacFarmDashboardInitReportResult:
    """
    A mock object for the
    FlowTacFarmDashboardInitReportResult
    class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.customer_code = uuid.uuid4()


@pytest.fixture
def flow_response():
    """
    Return a mock
    FlowTacFarmDashboardInitReportResult
    object.
    """
    return MockFlowTacFarmDashboardInitReportResult()


def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = TacFarmDashboardInitReportGetInitModelResponse()
    response.load_flow_response(flow_response)

    assert response.customer_code == \
        flow_response.customer_code


def test_to_json():
    """
    Test the to_json method.
    """
    response = TacFarmDashboardInitReportGetInitModelResponse(
        success=True,
        message="Test Message",
        validation_errors=[],
# endset  # noqa: E122
        customer_code=uuid.uuid4(),
# endset  # noqa: E122
    )
    json_response = response.to_json()
    assert isinstance(json_response, str)

    json_data = json.loads(json_response)

    assert json_data["success"] == response.success
    assert json_data["message"] == response.message
    assert json_data["customer_code"] == str(response.customer_code)


@pytest.mark.asyncio
async def test_process_request(flow_response):
    """
    Test the process_request method.
    """
    mock_session_context = Mock(spec=SessionContext)
    mock_tac_bus_obj = patch(
        "apis.models.init.tac_farm_dashboard_init_report."
        "TacBusObj",
        autospec=True).start()
    mock_flow = patch(
        "apis.models.init.tac_farm_dashboard_init_report."
        "FlowTacFarmDashboardInitReport",
        autospec=True).start()
    mock_flow_instance = \
        mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)

    request = TacFarmDashboardInitReportGetInitModelRequest()
    response = TacFarmDashboardInitReportGetInitModelResponse()

    tac_code = uuid.uuid4()
    result = await request.process_request(
        mock_session_context,
        tac_code,
        response)

    assert result.success is True
    assert result.message == "Success."
    mock_tac_bus_obj.assert_called_once_with(
        mock_session_context)
    mock_flow_instance.process.assert_called_once()

    patch.stopall()
