# apis/models/init/tests/land_add_plant_init_obj_wf_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
"""
This module contains the unit tests for the
land_add_plant_init_obj_wf module.
"""
import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest

from helpers import SessionContext, TypeConversion

from models.factory.land import LandFactory
from ..land_add_plant_init_obj_wf import (
    LandAddPlantInitObjWFGetInitModelRequest,
    LandAddPlantInitObjWFGetInitModelResponse)


class MockFlowLandAddPlantInitObjWFResult:  # pylint: disable=too-few-public-methods
    """
    A mock object for the
    FlowLandAddPlantInitObjWFResult
    class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
# endset
        self.request_flavor_code = uuid.uuid4()
        self.request_other_flavor = \
            "Other Flavor"
        self.request_some_int_val = 1
        self.request_some_big_int_val = 1000000
        self.request_some_bit_val = True
        self.request_is_delete_allowed = True
        self.request_is_edit_allowed = True
        self.request_some_float_val = 1.23
        self.request_some_decimal_val = \
            Decimal('10.99')
        self.request_some_utc_date_time_val = \
            datetime.now(timezone.utc)
        self.request_some_date_val = \
            date.today()
        self.request_some_money_val = \
            Decimal('100.00')
        self.request_some_n_var_char_val = \
            "Some N Var Char"
        self.request_some_var_char_val = \
            "Some Var Char"
        self.request_some_text_val = \
            "Some Text"
        self.request_some_phone_number = \
            "123-456-7890"
        self.request_some_email_address = \
            "test@example.com"
        self.land_name = \
            "Land Name"
        self.tac_code = uuid.uuid4()
# endset


@pytest.fixture
def flow_response():
    """
    Return a mock
    FlowLandAddPlantInitObjWFResult
    object.
    """
    return MockFlowLandAddPlantInitObjWFResult()


def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = LandAddPlantInitObjWFGetInitModelResponse()
    response.load_flow_response(flow_response)

# endset
    assert response.request_flavor_code == \
        flow_response.request_flavor_code
    assert response.request_other_flavor == \
        flow_response.request_other_flavor
    assert response.request_some_int_val == \
        flow_response.request_some_int_val
    assert response.request_some_big_int_val == \
        flow_response.request_some_big_int_val
    assert response.request_some_bit_val == \
        flow_response.request_some_bit_val
    assert response.request_is_delete_allowed == \
        flow_response.request_is_delete_allowed
    assert response.request_is_edit_allowed == \
        flow_response.request_is_edit_allowed
    assert response.request_some_float_val == \
        flow_response.request_some_float_val
    assert response.request_some_decimal_val == \
        flow_response.request_some_decimal_val
    assert response.request_some_utc_date_time_val == \
        flow_response.request_some_utc_date_time_val
    assert response.request_some_date_val == \
        flow_response.request_some_date_val
    assert response.request_some_money_val == \
        flow_response.request_some_money_val
    assert response.request_some_n_var_char_val == \
        flow_response.request_some_n_var_char_val
    assert response.request_some_var_char_val == \
        flow_response.request_some_var_char_val
    assert response.request_some_text_val == \
        flow_response.request_some_text_val
    assert response.request_some_phone_number == \
        flow_response.request_some_phone_number
    assert response.request_some_email_address == \
        flow_response.request_some_email_address
    assert response.land_name == \
        flow_response.land_name
    assert response.tac_code == \
        flow_response.tac_code
# endset


def test_to_json():
    """
    Test the to_json method.
    """
    response = LandAddPlantInitObjWFGetInitModelResponse(
        success=True,
        message="Test Message",
        validation_errors=[],
# endset  # noqa: E122
        request_flavor_code=uuid.uuid4(),
        request_other_flavor="Other Flavor",
        request_some_int_val=1,
        request_some_big_int_val=1000000,
        request_some_bit_val=True,
        request_is_edit_allowed=True,
        request_is_delete_allowed=True,
        request_some_float_val=1.23,
        request_some_decimal_val=Decimal('10.99'),
        request_some_utc_date_time_val=datetime.now(timezone.utc),
        request_some_date_val=date.today(),
        request_some_money_val=Decimal('100.00'),
        request_some_n_var_char_val="Some N Var Char",
        request_some_var_char_val="Some Var Char",
        request_some_text_val="Some Text",
        request_some_phone_number="123-456-7890",
        request_some_email_address="test@example.com",
        land_name="Land Name",
        tac_code=uuid.uuid4(),
# endset  # noqa: E122
    )
    json_response = response.to_json()
    assert isinstance(json_response, str)

    json_data = json.loads(json_response)

    assert json_data["success"] == response.success
    assert json_data["message"] == response.message
# endset
    assert json_data["request_flavor_code"] == \
        str(response.request_flavor_code)
    assert json_data["request_other_flavor"] == \
        response.request_other_flavor
    assert json_data["request_some_int_val"] == \
        response.request_some_int_val
    assert json_data["request_some_big_int_val"] == \
        response.request_some_big_int_val
    assert json_data["request_some_bit_val"] == \
        response.request_some_bit_val
    assert json_data["request_is_edit_allowed"] == \
        response.request_is_edit_allowed
    assert json_data["request_is_delete_allowed"] == \
        response.request_is_delete_allowed
    assert json_data["request_some_float_val"] == \
        response.request_some_float_val
    assert json_data["request_some_decimal_val"] == \
        str(response.request_some_decimal_val)
    assert json_data["request_some_utc_date_time_val"] == \
        TypeConversion.date_to_iso_format_z(
            response.request_some_utc_date_time_val)
    assert json_data["request_some_date_val"] == \
        response.request_some_date_val.isoformat()
    assert json_data["request_some_money_val"] == \
        str(response.request_some_money_val)
    assert json_data["request_some_n_var_char_val"] == \
        response.request_some_n_var_char_val
    assert json_data["request_some_var_char_val"] == \
        response.request_some_var_char_val
    assert json_data["request_some_text_val"] == \
        response.request_some_text_val
    assert json_data["request_some_phone_number"] == \
        response.request_some_phone_number
    assert json_data["request_some_email_address"] == \
        response.request_some_email_address
    assert json_data["land_name"] == response.land_name
    assert json_data["tac_code"] == str(response.tac_code)
# endset


@pytest.mark.asyncio
async def test_process_request(flow_response, session):
    """
    Test the process_request method.
    """
    session_context = SessionContext({}, session)
    mock_flow = patch(
        "apis.models.init.land_add_plant_init_obj_wf."
        "FlowLandAddPlantInitObjWF",
        autospec=True).start()
    mock_flow_instance = \
        mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)

    request = LandAddPlantInitObjWFGetInitModelRequest()
    response = LandAddPlantInitObjWFGetInitModelResponse()

    land = await LandFactory.create_async(session)

    result = await request.process_request(
        session_context,
        land.code,
        response)

    assert result.success is True
    assert result.message == "Success."
    mock_flow_instance.process.assert_called_once()

    patch.stopall()
