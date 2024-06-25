# apis/models/init/tests/land_plant_list_init_report_test.py
# pylint: disable=redefined-outer-name
"""
This module contains the unit tests for the
land_plant_list_init_report module.
"""
import json
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, Mock, patch

import pytest

from helpers import SessionContext

from ..land_plant_list_init_report import (
    LandPlantListInitReportGetInitModelRequest,
    LandPlantListInitReportGetInitModelResponse)


class MockFlowLandPlantListInitReportResult:
    """
    A mock object for the
    FlowLandPlantListInitReportResult
    class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.some_int_val = 1
        self.some_big_int_val = 1000000
        self.some_bit_val = True
        self.is_edit_allowed = True
        self.is_delete_allowed = True
        self.some_float_val = 1.23
        self.some_decimal_val = Decimal('10.99')
        self.some_min_utc_date_time_val = datetime.utcnow()
        self.some_min_date_val = date.today()
        self.some_money_val = Decimal('100.00')
        self.some_n_var_char_val = "Some N Var Char Val"
        self.some_var_char_val = "Some Var Char"
        self.some_text_val = "Some Text"
        self.some_phone_number = "123-456-7890"
        self.some_email_address = "Some Var Char"
        self.land_code = uuid.uuid4()
        self.tac_code = uuid.uuid4()
        self.land_name = "Land Name"


@pytest.fixture
def flow_response():
    """
    Return a mock
    FlowLandPlantListInitReportResult
    object.
    """
    return MockFlowLandPlantListInitReportResult()


def test_load_flow_response(flow_response):
    """
    Test the load_flow_response method.
    """
    response = LandPlantListInitReportGetInitModelResponse()
    response.load_flow_response(flow_response)

    assert response.some_int_val == \
        flow_response.some_int_val
    assert response.some_big_int_val == \
        flow_response.some_big_int_val
    assert response.some_bit_val == \
        flow_response.some_bit_val
    assert response.is_edit_allowed == \
        flow_response.is_edit_allowed
    assert response.is_delete_allowed == \
        flow_response.is_delete_allowed
    assert response.some_float_val == \
        flow_response.some_float_val
    assert response.some_decimal_val == \
        flow_response.some_decimal_val
    assert response.some_min_utc_date_time_val == \
        flow_response.some_min_utc_date_time_val
    assert response.some_min_date_val == \
        flow_response.some_min_date_val
    assert response.some_money_val == \
        flow_response.some_money_val
    assert response.some_n_var_char_val == \
        flow_response.some_n_var_char_val
    assert response.some_var_char_val == \
        flow_response.some_var_char_val
    assert response.some_text_val == \
        flow_response.some_text_val
    assert response.some_phone_number == \
        flow_response.some_phone_number
    assert response.some_email_address == \
        flow_response.some_email_address
    assert response.land_code == \
        flow_response.land_code
    assert response.tac_code == \
        flow_response.tac_code
    assert response.land_name == \
        flow_response.land_name


def test_to_json():
    """
    Test the to_json method.
    """
    response = LandPlantListInitReportGetInitModelResponse(
        success=True,
        message="Test Message",
        validation_errors=[],
# endset  # noqa: E122
        some_int_val=1,
        some_big_int_val=1000000,
        some_bit_val=True,
        is_edit_allowed=True,
        is_delete_allowed=True,
        some_float_val=1.23,
        some_decimal_val=Decimal('10.99'),
        some_min_utc_date_time_val=datetime.utcnow(),
        some_min_date_val=date.today(),
        some_money_val=Decimal('100.00'),
        some_n_var_char_val="Some N Var Char Val",
        some_var_char_val="Some Var Char",
        some_text_val="Some Text",
        some_phone_number="123-456-7890",
        some_email_address="Some Var Char",
        land_code=uuid.uuid4(),
        tac_code=uuid.uuid4(),
        land_name="Land Name",
# endset  # noqa: E122
    )
    json_response = response.to_json()
    assert isinstance(json_response, str)

    json_data = json.loads(json_response)

    assert json_data["success"] == response.success
    assert json_data["message"] == response.message
    assert json_data["some_int_val"] == \
        response.some_int_val
    assert json_data["some_big_int_val"] == \
        response.some_big_int_val
    assert json_data["some_bit_val"] == \
        response.some_bit_val
    assert json_data["is_edit_allowed"] == \
        response.is_edit_allowed
    assert json_data["is_delete_allowed"] == \
        response.is_delete_allowed
    assert json_data["some_float_val"] == \
        response.some_float_val
    assert json_data["some_decimal_val"] == \
        str(response.some_decimal_val)
    assert json_data["some_min_utc_date_time_val"] == \
        response.some_min_utc_date_time_val.isoformat()
    assert json_data["some_min_date_val"] == \
        response.some_min_date_val.isoformat()
    assert json_data["some_money_val"] == \
        str(response.some_money_val)
    assert json_data["some_n_var_char_val"] == \
        response.some_n_var_char_val
    assert json_data["some_var_char_val"] == \
        response.some_var_char_val
    assert json_data["some_text_val"] == \
        response.some_text_val
    assert json_data["some_phone_number"] == \
        response.some_phone_number
    assert json_data["some_email_address"] == \
        response.some_email_address
    assert json_data["land_code"] == str(response.land_code)
    assert json_data["tac_code"] == str(response.tac_code)
    assert json_data["land_name"] == response.land_name


@pytest.mark.asyncio
async def test_process_request(flow_response):
    """
    Test the process_request method.
    """
    mock_session_context = Mock(spec=SessionContext)
    mock_land_bus_obj = patch(
        'apis.models.init.land_plant_list_init_report.LandBusObj',
        autospec=True).start()
    mock_flow = patch(
        "apis.models.init.land_plant_list_init_report."
        "FlowLandPlantListInitReport",
        autospec=True).start()
    mock_flow_instance = mock_flow.return_value
    mock_flow_instance.process = AsyncMock(return_value=flow_response)

    request = LandPlantListInitReportGetInitModelRequest()
    response = LandPlantListInitReportGetInitModelResponse()

    land_code = uuid.uuid4()
    result = await request.process_request(
        mock_session_context,
        land_code,
        response)

    assert result.success is True
    assert result.message == "Success."
    mock_land_bus_obj.assert_called_once_with(mock_session_context)
    mock_flow_instance.process.assert_called_once()

    patch.stopall()

