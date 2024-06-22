# flows/default/tests/land_add_plant_test.py

"""
This module contains unit tests for the
`FlowLandAddPlantResult` and `FlowLandAddPlant` classes.
"""

import json
import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest

import flows.constants.error_log_config_resolve_error_log as FlowConstants
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_add_plant import FlowLandAddPlant, FlowLandAddPlantResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.land import LandFactory


class TestLandAddPlantPostModelResponse:
    """
    This class contains unit tests for the
    `FlowLandAddPlantResult` class.
    """

    def test_flow_land_add_plant_result_to_json(self):
        """
        Test the `to_json` method of the
        `FlowLandAddPlantResult` class.
        """

        # Create an instance and set attributes
        result = FlowLandAddPlantResult()
        result.context_object_code = uuid.uuid4()
        result.land_code = uuid.uuid4()
        result.plant_code = uuid.uuid4()
        result.output_flavor_code = uuid.uuid4()
        result.output_other_flavor = "test text"
        result.output_some_int_val = 123
        result.output_some_big_int_val = 123456789
        result.output_some_bit_val = True
        result.output_is_edit_allowed = True
        result.output_is_delete_allowed = False
        result.output_some_float_val = 12.34
        result.output_some_decimal_val = Decimal("123.45")
        result.output_some_utc_date_time_val = datetime.utcnow()
        result.output_some_date_val = date.today()
        result.output_some_money_val = Decimal("67.89")
        result.output_some_n_var_char_val = "nvarchar test"
        result.output_some_var_char_val = "varchar test"
        result.output_some_text_val = "text value"
        result.output_some_phone_number = "123-456-7890"
        result.output_some_email_address = "test@example.com"
# endset

        # Call to_json method
        json_output = result.to_json()

        # Parse JSON output
        data = json.loads(json_output)

        # Assert individual fields
        assert data["context_object_code"] == (
            str(result.context_object_code))
        assert data["land_code"] == (
            str(result.land_code))
        assert data["plant_code"] == (
            str(result.plant_code))
        assert data["output_flavor_code"] == (
            str(result.output_flavor_code))
        assert data["output_other_flavor"] == (
            result.output_other_flavor)
        assert data["output_some_int_val"] == (
            result.output_some_int_val)
        assert data["output_some_big_int_val"] == (
            result.output_some_big_int_val)
        assert data["output_some_bit_val"] == (
            result.output_some_bit_val)
        assert data["output_is_edit_allowed"] == (
            result.output_is_edit_allowed)
        assert data["output_is_delete_allowed"] == (
            result.output_is_delete_allowed)
        assert data["output_some_float_val"] == (
            result.output_some_float_val)
        assert data["output_some_decimal_val"] == (
            str(result.output_some_decimal_val))
        assert data["output_some_utc_date_time_val"] == (
            result.output_some_utc_date_time_val.isoformat())
        assert data["output_some_date_val"] == (
            result.output_some_date_val.isoformat())
        assert data["output_some_money_val"] == (
            str(result.output_some_money_val))
        assert data["output_some_n_var_char_val"] == (
            result.output_some_n_var_char_val)
        assert data["output_some_var_char_val"] == (
            result.output_some_var_char_val)
        assert data["output_some_text_val"] == (
            result.output_some_text_val)
        assert data["output_some_phone_number"] == (
            result.output_some_phone_number)
        assert data["output_some_email_address"] == (
            result.output_some_email_address)
# endsets

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        Test the `process` method of the `FlowLandAddPlant` class.
        """

        session_context = SessionContext(dict(), session)
        flow = FlowLandAddPlant(session_context)

        land = await LandFactory.create_async(session)

        land_bus_obj = LandBusObj(session_context)
        await land_bus_obj.load_from_obj_instance(land)

        role_required = "User"

        request_flavor_code: uuid.UUID = uuid.UUID(int=0)
        request_other_flavor: str = ""
        request_some_int_val: int = 0
        request_some_big_int_val: int = 0
        request_some_bit_val: bool = False
        request_is_edit_allowed: bool = False
        request_is_delete_allowed: bool = False
        request_some_float_val: float = 0
        request_some_decimal_val: Decimal = Decimal(0)
        request_some_utc_date_time_val: datetime = (
            TypeConversion.get_default_date_time())
        request_some_date_val: date = (
            TypeConversion.get_default_date())
        request_some_money_val: Decimal = Decimal(0)
        request_some_n_var_char_val: str = ""
        request_some_var_char_val: str = ""
        request_some_text_val: str = ""
        request_some_phone_number: str = ""
        request_some_email_address: str = ""
        request_sample_image_upload_file: str = ""
# endset

        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                await flow.process(
                    land_bus_obj,
                    request_flavor_code,
                    request_other_flavor,
                    request_some_int_val,
                    request_some_big_int_val,
                    request_some_bit_val,
                    request_is_edit_allowed,
                    request_is_delete_allowed,
                    request_some_float_val,
                    request_some_decimal_val,
                    request_some_utc_date_time_val,
                    request_some_date_val,
                    request_some_money_val,
                    request_some_n_var_char_val,
                    request_some_var_char_val,
                    request_some_text_val,
                    request_some_phone_number,
                    request_some_email_address,
                    request_sample_image_upload_file,
# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required

        customer_code_match_required = False
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORGANIZATION_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORG_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True

        if customer_code_match_required is True:
            with pytest.raises(FlowValidationError):

                await flow.process(
                    land_bus_obj,
                    request_flavor_code,
                    request_other_flavor,
                    request_some_int_val,
                    request_some_big_int_val,
                    request_some_bit_val,
                    request_is_edit_allowed,
                    request_is_delete_allowed,
                    request_some_float_val,
                    request_some_decimal_val,
                    request_some_utc_date_time_val,
                    request_some_date_val,
                    request_some_money_val,
                    request_some_n_var_char_val,
                    request_some_var_char_val,
                    request_some_text_val,
                    request_some_phone_number,
                    request_some_email_address,
                    request_sample_image_upload_file,
# endset  # noqa: E122
                )

        session_context.role_name_csv = role_required

        # result = await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     land_code=land.code,
        #     request=request_instance
        #     )
        # assert isinstance(result,FlowLandAddPlantResult)
