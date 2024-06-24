# apis/models/init/tests/tac_login_init_obj_wf_test.py
"""
This module contains the unit tests for the
tac_login_init_obj_wf module.
"""
import json
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, Mock, patch
import pytest
from helpers import SessionContext
from ..tac_login_init_obj_wf import (
    TacLoginInitObjWFGetInitModelRequest,
    TacLoginInitObjWFGetInitModelResponse)
class MockFlowTacLoginInitObjWFResult:
    """
    A mock object for the FlowTacLoginInitObjWFResult class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
# endset
        self.email = "Email"
        self.password = "Password"
# endset
@pytest.fixture
def flow_response():
    """
    Return a mock FlowTacLoginInitObjWFResult object.
    """
    return MockFlowTacLoginInitObjWFResult()
def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = TacLoginInitObjWFGetInitModelResponse()
    response.load_flow_response(flow_response)
# endset
    assert response.email == \
        flow_response.email
    assert response.password == \
        flow_response.password
# endset
def test_to_json():
    """
    Test the to_json method.
    """
    response = TacLoginInitObjWFGetInitModelResponse(
        success=True,
        message="Test Message",
        validation_errors=[],
# endset  # noqa: E122
        email="Email",
        password="Password",
# endset  # noqa: E122
    )
    json_response = response.to_json()
    assert isinstance(json_response, str)
    json_data = json.loads(json_response)
    assert json_data["success"] == response.success
    assert json_data["message"] == response.message
# endset
    assert json_data["email"] == \
        response.email
    assert json_data["password"] == \
        response.password
# endset
@pytest.mark.asyncio
async def test_process_request(flow_response):
    """
    Test the process_request method.
    """
    mock_session_context = Mock(spec=SessionContext)
    mock_tac_bus_obj = patch(
        'apis.models.init.tac_login_init_obj_wf.TacBusObj',
        autospec=True).start()
    mock_flow = patch(
        'apis.models.init.tac_login_init_obj_wf.FlowTacLoginInitObjWF',
        autospec=True).start()
    mock_flow_instance = mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)
    request = TacLoginInitObjWFGetInitModelRequest()
    response = TacLoginInitObjWFGetInitModelResponse()
    tac_code = uuid.uuid4()
    result = await request.process_request(
        mock_session_context,
        tac_code,
        response)
    assert result.success is True
    assert result.message == "Success."
    mock_tac_bus_obj.assert_called_once_with(mock_session_context)
    mock_flow_instance.process.assert_called_once()
    patch.stopall()

