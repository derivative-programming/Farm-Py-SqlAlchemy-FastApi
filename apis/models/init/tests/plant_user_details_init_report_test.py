# apis/models/init/tests/plant_user_details_init_report_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains the unit tests for the
plant_user_details_init_report module.
"""
import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest

from helpers import SessionContext, TypeConversion

from models.factory.plant import PlantFactory
from ..plant_user_details_init_report import (
    PlantUserDetailsInitReportGetInitModelRequest,
    PlantUserDetailsInitReportGetInitModelResponse)


class MockFlowPlantUserDetailsInitReportResult:
    """
    A mock object for the
    FlowPlantUserDetailsInitReportResult
    class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.land_code = uuid.uuid4()
        self.tac_code = uuid.uuid4()


@pytest.fixture
def flow_response():
    """
    Return a mock
    FlowPlantUserDetailsInitReportResult
    object.
    """
    return MockFlowPlantUserDetailsInitReportResult()


def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = PlantUserDetailsInitReportGetInitModelResponse()
    response.load_flow_response(flow_response)

    assert response.land_code == \
        flow_response.land_code
    assert response.tac_code == \
        flow_response.tac_code


def test_to_json():
    """
    Test the to_json method.
    """
    response = PlantUserDetailsInitReportGetInitModelResponse(
        success=True,
        message="Test Message",
        validation_errors=[],
# endset  # noqa: E122
        land_code=uuid.uuid4(),
        tac_code=uuid.uuid4(),
# endset  # noqa: E122
    )
    json_response = response.to_json()
    assert isinstance(json_response, str)

    json_data = json.loads(json_response)

    assert json_data["success"] == response.success
    assert json_data["message"] == response.message
    assert json_data["land_code"] == str(response.land_code)
    assert json_data["tac_code"] == str(response.tac_code)


@pytest.mark.asyncio
async def test_process_request(flow_response, session):
    """
    Test the process_request method.
    """
    session_context = SessionContext({}, session)
    mock_flow = patch(
        "apis.models.init.plant_user_details_init_report."
        "FlowPlantUserDetailsInitReport",
        autospec=True).start()
    mock_flow_instance = \
        mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)

    request = PlantUserDetailsInitReportGetInitModelRequest()
    response = PlantUserDetailsInitReportGetInitModelResponse()

    plant = await PlantFactory.create_async(session)

    result = await request.process_request(
        session_context,
        plant.code,
        response)

    assert result.success is True
    assert result.message == "Success."
    mock_flow_instance.process.assert_called_once()

    patch.stopall()
