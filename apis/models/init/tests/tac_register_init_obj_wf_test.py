# apis/models/init/tests/tac_register_init_obj_wf_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
"""
This module contains the unit tests for the
tac_register_init_obj_wf module.
"""
import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest

from helpers import SessionContext, TypeConversion

from models.factory.tac import TacFactory
from ..tac_register_init_obj_wf import (
    TacRegisterInitObjWFGetInitModelRequest,
    TacRegisterInitObjWFGetInitModelResponse)


class MockFlowTacRegisterInitObjWFResult:
    """
    A mock object for the
    FlowTacRegisterInitObjWFResult
    class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.email = \
            "Email"
        self.password = \
            "Password"
        self.confirm_password = \
            "Confirm Password"
        self.first_name = \
            "First Name"
        self.last_name = \
            "Last Name"


@pytest.fixture
def flow_response():
    """
    Return a mock
    FlowTacRegisterInitObjWFResult
    object.
    """
    return MockFlowTacRegisterInitObjWFResult()


def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = TacRegisterInitObjWFGetInitModelResponse()
    response.load_flow_response(flow_response)

    assert response.email == \
        flow_response.email
    assert response.password == \
        flow_response.password
    assert response.confirm_password == \
        flow_response.confirm_password
    assert response.first_name == \
        flow_response.first_name
    assert response.last_name == \
        flow_response.last_name


def test_to_json():
    """
    Test the to_json method.
    """
    response = TacRegisterInitObjWFGetInitModelResponse(
        success=True,
        message="Test Message",
        validation_errors=[],
# endset  # noqa: E122
        email="Email",
        password="Password",
        confirm_password="Confirm Password",
        first_name="First Name",
        last_name="Last Name",
# endset  # noqa: E122
    )
    json_response = response.to_json()
    assert isinstance(json_response, str)

    json_data = json.loads(json_response)

    assert json_data["success"] == response.success
    assert json_data["message"] == response.message
    assert json_data["email"] == \
        response.email
    assert json_data["password"] == \
        response.password
    assert json_data["confirm_password"] == \
        response.confirm_password
    assert json_data["first_name"] == \
        response.first_name
    assert json_data["last_name"] == \
        response.last_name


@pytest.mark.asyncio
async def test_process_request(flow_response, session):
    """
    Test the process_request method.
    """
    session_context = SessionContext({}, session)
    mock_flow = patch(
        "apis.models.init.tac_register_init_obj_wf."
        "FlowTacRegisterInitObjWF",
        autospec=True).start()
    mock_flow_instance = \
        mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)

    request = TacRegisterInitObjWFGetInitModelRequest()
    response = TacRegisterInitObjWFGetInitModelResponse()

    tac = await TacFactory.create_async(session)

    result = await request.process_request(
        session_context,
        tac.code,
        response)

    assert result.success is True
    assert result.message == "Success."
    mock_flow_instance.process.assert_called_once()

    patch.stopall()
