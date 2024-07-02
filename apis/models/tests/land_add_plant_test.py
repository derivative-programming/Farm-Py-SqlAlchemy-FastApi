# apis/models/tests/land_add_plant_test.py
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
This module contains unit tests for the
LandAddPlantPostModelResponse class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch

import pytest

from business.land import LandBusObj
from flows.land_add_plant import (
    FlowLandAddPlant,
    FlowLandAddPlantResult)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.land import LandFactory

from ...models.land_add_plant import (
    LandAddPlantPostModelResponse,
    LandAddPlantPostModelRequest)
from ..factory.land_add_plant import (
    LandAddPlantPostModelRequestFactory)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestLandAddPlantPostModelRequest:
    """
    This class contains unit tests for the
    LandAddPlantPostModelRequest class.
    """

    def test_default_values(self):
        """
        This method tests the default values of the
        LandAddPlantPostModelRequest class.
        """
        model = LandAddPlantPostModelRequest()
        assert model.force_error_message == ""
# endset
        assert model.request_flavor_code == \
            uuid.UUID('00000000-0000-0000-0000-000000000000')
        assert model.request_other_flavor == ""
        assert model.request_some_int_val == 0
        assert model.request_some_big_int_val == 0
        assert model.request_some_bit_val is False
        assert model.request_is_edit_allowed is False
        assert model.request_is_delete_allowed is False
        assert math.isclose(model.request_some_float_val, 0.0)
        assert model.request_some_decimal_val == Decimal(0)
        assert model.request_some_utc_date_time_val == \
            TypeConversion.get_default_date_time()
        assert model.request_some_date_val == \
            TypeConversion.get_default_date()
        assert model.request_some_money_val == Decimal(0)
        assert model.request_some_n_var_char_val == ""
        assert model.request_some_var_char_val == ""
        assert model.request_some_text_val == ""
        assert model.request_some_phone_number == ""
        assert model.request_some_email_address == ""
        assert model.request_sample_image_upload_file == ""
# endset

    def test_to_dict_snake(self):
        """
        This method tests the to_dict_snake method of the
        LandAddPlantPostModelRequest class.
        """
        model = LandAddPlantPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            request_flavor_code=uuid.uuid4(),
            request_other_flavor="Other Flavor",
            request_some_int_val=42,
            request_some_big_int_val=123456789,
            request_some_bit_val=True,
            request_is_edit_allowed=True,
            request_is_delete_allowed=True,
            request_some_float_val=3.14,
            request_some_decimal_val=Decimal('99.99'),
            request_some_utc_date_time_val=datetime(2023, 1, 1, 12, 0, 0),
            request_some_date_val=date(2023, 1, 1),
            request_some_money_val=Decimal('100.00'),
            request_some_n_var_char_val="nvarchar",
            request_some_var_char_val="varchar",
            request_some_text_val="text",
            request_some_phone_number=TEST_PHONE,
            request_some_email_address=TEST_EMAIL,
            request_sample_image_upload_file="image.png"
# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT
# endset
        assert snake_case_dict['request_flavor_code'] == \
            model.request_flavor_code
        assert snake_case_dict['request_other_flavor'] == \
            model.request_other_flavor
        assert snake_case_dict['request_some_int_val'] == 42
        assert snake_case_dict['request_some_big_int_val'] == 123456789
        assert snake_case_dict['request_some_bit_val'] is True
        assert snake_case_dict['request_is_edit_allowed'] is True
        assert snake_case_dict['request_is_delete_allowed'] is True
        assert math.isclose(snake_case_dict['request_some_float_val'], 3.14)
        assert snake_case_dict['request_some_decimal_val'] == \
            Decimal('99.99')
        assert snake_case_dict['request_some_utc_date_time_val'] == \
            datetime(2023, 1, 1, 12, 0, 0)
        assert snake_case_dict['request_some_date_val'] == \
            date(2023, 1, 1)
        assert snake_case_dict['request_some_money_val'] == \
            Decimal('100.00')
        assert snake_case_dict['request_some_n_var_char_val'] == \
            model.request_some_n_var_char_val
        assert snake_case_dict['request_some_var_char_val'] == \
            model.request_some_var_char_val
        assert snake_case_dict['request_some_text_val'] == \
            model.request_some_text_val
        assert snake_case_dict['request_some_phone_number'] == \
            model.request_some_phone_number
        assert snake_case_dict['request_some_email_address'] == \
            model.request_some_email_address
        assert snake_case_dict['request_sample_image_upload_file'] == \
            "image.png"
# endset

    def test_to_dict_camel(self):
        """
        This method tests the to_dict_camel method of the
        LandAddPlantPostModelRequest class.
        """
        model = LandAddPlantPostModelRequest(
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            request_flavor_code=uuid.uuid4(),
            request_other_flavor="Other Flavor",
            request_some_int_val=42,
            request_some_big_int_val=123456789,
            request_some_bit_val=True,
            request_is_edit_allowed=True,
            request_is_delete_allowed=True,
            request_some_float_val=3.14,
            request_some_decimal_val=Decimal('99.99'),
            request_some_utc_date_time_val=datetime(2023, 1, 1, 12, 0, 0),
            request_some_date_val=date(2023, 1, 1),
            request_some_money_val=Decimal('100.00'),
            request_some_n_var_char_val="nvarchar",
            request_some_var_char_val="varchar",
            request_some_text_val="text",
            request_some_phone_number=TEST_PHONE,
            request_some_email_address=TEST_EMAIL,
            request_sample_image_upload_file="image.png"
# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT
# endset
        assert camel_case_dict['requestFlavorCode'] == \
            model.request_flavor_code
        assert camel_case_dict['requestOtherFlavor'] == \
            model.request_other_flavor
        assert camel_case_dict['requestSomeIntVal'] == 42
        assert camel_case_dict['requestSomeBigIntVal'] == 123456789
        assert camel_case_dict['requestSomeBitVal'] is True
        assert camel_case_dict['requestIsEditAllowed'] is True
        assert camel_case_dict['requestIsDeleteAllowed'] is True
        assert math.isclose(camel_case_dict['requestSomeFloatVal'], 3.14)
        assert camel_case_dict['requestSomeDecimalVal'] == Decimal('99.99')
        # assert camel_case_dict['requestSomeUTCDateTimeVal'] == datetime(2023, 1, 1, 12, 0, 0).isoformat()
        # assert camel_case_dict['requestSomeDateVal'] == date(2023, 1, 1).isoformat()
        assert camel_case_dict['requestSomeMoneyVal'] == Decimal('100.00')
        assert camel_case_dict['requestSomeNVarCharVal'] == \
            model.request_some_n_var_char_val
        assert camel_case_dict['requestSomeVarCharVal'] == \
            model.request_some_var_char_val
        assert camel_case_dict['requestSomeTextVal'] == \
            model.request_some_text_val
        assert camel_case_dict['requestSomePhoneNumber'] == \
            model.request_some_phone_number
        assert camel_case_dict['requestSomeEmailAddress'] == \
            model.request_some_email_address
        assert camel_case_dict['requestSampleImageUploadFile'] == \
            "image.png"
# endset

    def test_to_dict_snake_serialized(self):
        """
        This method tests the to_dict_snake_serialized method of the
        LandAddPlantPostModelRequest class.
        """
        # Create an instance of the
        # LandAddPlantPostModelRequest class
        request = LandAddPlantPostModelRequest(
            force_error_message="Test Error Message",
# endset  # noqa: E122
            request_flavor_code=uuid.uuid4(),
            request_other_flavor="Test Text",
            request_some_int_val=123,
            request_some_big_int_val=456,
            request_some_bit_val=True,
            request_is_edit_allowed=True,
            request_is_delete_allowed=False,
            request_some_float_val=3.14,
            request_some_decimal_val=Decimal("10.5"),
            request_some_utc_date_time_val=datetime.utcnow(),
            request_some_date_val=datetime.now().date(),
            request_some_money_val=Decimal("100.50"),
            request_some_n_var_char_val="Test NVarChar",
            request_some_var_char_val="Test VarChar",
            request_some_text_val="Test Text",
            request_some_phone_number="1234567890",
            request_some_email_address=TEST_EMAIL,
            request_sample_image_upload_file="sample_image.jpg"
# endset  # noqa: E122
        )

        # Convert the model to a dictionary with snake_case
        # keys and serialized values
        data = request.to_dict_snake_serialized()

        # Define the expected dictionary
        expected_data = {
            "force_error_message": "Test Error Message",
# endset  # noqa: E122
            "request_flavor_code": str(request.request_flavor_code),
            "request_other_flavor": "Test Text",
            "request_some_int_val": 123,
            "request_some_big_int_val": 456,
            "request_some_bit_val": True,
            "request_is_edit_allowed": True,
            "request_is_delete_allowed": False,
            "request_some_float_val": 3.14,
            "request_some_decimal_val": "10.5",
            "request_some_utc_date_time_val":
                request.request_some_utc_date_time_val.isoformat(),
            "request_some_date_val":
                request.request_some_date_val.isoformat(),
            "request_some_money_val": "100.50",
            "request_some_n_var_char_val": "Test NVarChar",
            "request_some_var_char_val": "Test VarChar",
            "request_some_text_val": "Test Text",
            "request_some_phone_number": "1234567890",
            "request_some_email_address": TEST_EMAIL,
            "request_sample_image_upload_file": "sample_image.jpg"
# endset  # noqa: E122
        }

        # Compare the actual and expected dictionaries
        assert data == expected_data

    def test_to_dict_camel_serialized(self):
        """
        This method tests the to_dict_camel_serialized method of the
        LandAddPlantPostModelRequest class.
        """
        request = LandAddPlantPostModelRequest(
            force_error_message="Test Error Message",
            request_flavor_code=uuid.uuid4(),
            request_other_flavor="Test Text",
            request_some_int_val=123,
            request_some_big_int_val=456,
            request_some_bit_val=True,
            request_is_edit_allowed=True,
            request_is_delete_allowed=False,
            request_some_float_val=3.14,
            request_some_decimal_val=Decimal(2.5),
            request_some_utc_date_time_val=datetime.utcnow(),
            request_some_date_val=date.today(),
            request_some_money_val=Decimal(100.50),
            request_some_n_var_char_val="Test N Var Char",
            request_some_var_char_val="Test Var Char",
            request_some_text_val="Test Text",
            request_some_phone_number="1234567890",
            request_some_email_address=TEST_EMAIL,
            request_sample_image_upload_file="sample.jpg"
        )

        expected_data = {
            "forceErrorMessage": "Test Error Message",
            "requestFlavorCode": str(request.request_flavor_code),
            "requestOtherFlavor": "Test Text",
            "requestSomeIntVal": 123,
            "requestSomeBigIntVal": 456,
            "requestSomeBitVal": True,
            "requestIsEditAllowed": True,
            "requestIsDeleteAllowed": False,
            "requestSomeFloatVal": 3.14,
            "requestSomeDecimalVal": "2.5",
            "requestSomeUTCDateTimeVal":
                request.request_some_utc_date_time_val.isoformat(),
            "requestSomeDateVal":
                str(request.request_some_date_val),
            "requestSomeMoneyVal": "100.5",
            "requestSomeNVarCharVal": "Test N Var Char",
            "requestSomeVarCharVal": "Test Var Char",
            "requestSomeTextVal": "Test Text",
            "requestSomePhoneNumber": "1234567890",
            "requestSomeEmailAddress": TEST_EMAIL,
            "requestSampleImageUploadFile": "sample.jpg"
        }

        data = request.to_dict_camel_serialized()

        assert data == expected_data


class TestLandAddPlantPostModelResponse:
    """
    This class contains unit tests for the
    LandAddPlantPostModelResponse class.
    """

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
        This method tests the flow process request
        for adding a plant to a land.
        It mocks the process method of
        FlowLandAddPlant
        and asserts that the response is successful.
        """

        async def mock_process(
            land_bus_obj: LandBusObj,
            request_flavor_code: uuid.UUID = uuid.UUID(int=0),
            request_other_flavor: str = "",
            request_some_int_val: int = 0,
            request_some_big_int_val: int = 0,
            request_some_bit_val: bool = False,
            request_is_edit_allowed: bool = False,
            request_is_delete_allowed: bool = False,
            request_some_float_val: float = 0,
            request_some_decimal_val: Decimal = Decimal(0),
            request_some_utc_date_time_val: datetime = (
                TypeConversion.get_default_date_time()),
            request_some_date_val: date = TypeConversion.get_default_date(),
            request_some_money_val: Decimal = Decimal(0),
            request_some_n_var_char_val: str = "",
            request_some_var_char_val: str = "",
            request_some_text_val: str = "",
            request_some_phone_number: str = "",
            request_some_email_address: str = "",
            request_sample_image_upload_file: str = "",
        ):
            return FlowLandAddPlantResult()
        with patch.object(
            FlowLandAddPlant,
            'process',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_process

            request_instance = await (
                LandAddPlantPostModelRequestFactory
                .create_async(
                    session=session
                )
            )
            response_instance = \
                LandAddPlantPostModelResponse()
            session_context = SessionContext(dict(), session)

            land = await LandFactory.create_async(session)

            await response_instance.process_request(
                session_context=session_context,
                land_code=land.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()
