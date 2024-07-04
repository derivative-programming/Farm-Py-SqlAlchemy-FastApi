# apis/models/init/tests/customer_user_log_out_init_obj_wf_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
This module contains the unit tests for the
customer_user_log_out_init_obj_wf module.
"""
import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest

from helpers import SessionContext, TypeConversion

from ..customer_user_log_out_init_obj_wf import (
    CustomerUserLogOutInitObjWFGetInitModelRequest,
    CustomerUserLogOutInitObjWFGetInitModelResponse)


class MockFlowCustomerUserLogOutInitObjWFResult:
    """
    A mock object for the
    FlowCustomerUserLogOutInitObjWFResult
    class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.tac_code = uuid.uuid4()


@pytest.fixture
def flow_response():
    """
    Return a mock
    FlowCustomerUserLogOutInitObjWFResult
    object.
    """
    return MockFlowCustomerUserLogOutInitObjWFResult()


def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = CustomerUserLogOutInitObjWFGetInitModelResponse()
    response.load_flow_response(flow_response)

    assert response.tac_code == \
        flow_response.tac_code


def test_to_json():
    """
    Test the to_json method.
    """
    response = CustomerUserLogOutInitObjWFGetInitModelResponse(
        success=True,
        message="Test Message",
        validation_errors=[],
# endset  # noqa: E122
        tac_code=uuid.uuid4(),
# endset  # noqa: E122
    )
    json_response = response.to_json()
    assert isinstance(json_response, str)

    json_data = json.loads(json_response)

    assert json_data["success"] == response.success
    assert json_data["message"] == response.message
    assert json_data["tac_code"] == str(response.tac_code)


@pytest.mark.asyncio
async def test_process_request(flow_response):
    """
    Test the process_request method.
    """
    mock_session_context = Mock(spec=SessionContext)
    mock_customer_bus_obj = patch(
        "apis.models.init.customer_user_log_out_init_obj_wf."
        "CustomerBusObj",
        autospec=True).start()
    mock_flow = patch(
        "apis.models.init.customer_user_log_out_init_obj_wf."
        "FlowCustomerUserLogOutInitObjWF",
        autospec=True).start()
    mock_flow_instance = \
        mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)

    request = CustomerUserLogOutInitObjWFGetInitModelRequest()
    response = CustomerUserLogOutInitObjWFGetInitModelResponse()

    customer_code = uuid.uuid4()
    result = await request.process_request(
        mock_session_context,
        customer_code,
        response)

    assert result.success is True
    assert result.message == "Success."
    mock_customer_bus_obj.assert_called_once_with(
        mock_session_context)
    mock_flow_instance.process.assert_called_once()

    patch.stopall()
