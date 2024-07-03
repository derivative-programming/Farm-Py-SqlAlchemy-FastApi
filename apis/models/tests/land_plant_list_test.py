# apis/models/tests/land_plant_list_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

"""
This module contains unit tests for the
LandPlantListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
import math  # noqa: F401

from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch, Mock

import pytest

from helpers.type_conversion import TypeConversion  # noqa: F401
from helpers.session_context import SessionContext

from ..factory.land_plant_list import (
    LandPlantListGetModelRequestFactory)
from ..land_plant_list import (
    LandPlantListGetModelRequest,
    LandPlantListGetModelResponse,
    LandPlantListGetModelResponseItem)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestLandPlantListGetModelRequest():
    """
    This class contains unit tests for the
    LandPlantListGetModelRequest class.
    """

    def test_default_values(self):
        """
        Test the default values of the
        LandPlantListGetModelRequest class.
        """
        model = LandPlantListGetModelRequest()
        assert model.page_number == 0
        assert model.item_count_per_page == 0
        assert model.order_by_column_name == ""
        assert model.order_by_descending is False
        assert model.force_error_message == ""
# endset
        assert model.flavor_code == \
            uuid.UUID('00000000-0000-0000-0000-000000000000')
        assert model.some_int_val == 0
        assert model.some_big_int_val == 0
        assert math.isclose(model.some_float_val, 0.0)
        assert model.some_bit_val is False
        assert model.is_edit_allowed is False
        assert model.is_delete_allowed is False
        assert model.some_decimal_val == \
            Decimal(0)
        assert model.some_min_utc_date_time_val == \
            TypeConversion.get_default_date_time()
        assert model.some_min_date_val == \
            TypeConversion.get_default_date()
        assert model.some_money_val == \
            Decimal(0)
        assert model.some_n_var_char_val == ""
        assert model.some_var_char_val == ""
        assert model.some_text_val == ""
        assert model.some_phone_number == ""
        assert model.some_email_address == ""
# endset

    def test_to_dict_snake(self):
        """
        Test the to_dict_snake method of the
        LandPlantListGetModelRequest class.
        """
        model = LandPlantListGetModelRequest(
            page_number=1,
            item_count_per_page=10,
            order_by_column_name="name",
            order_by_descending=True,
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            flavor_code=uuid.uuid4(),
            some_int_val=42,
            some_big_int_val=123456789,
            some_float_val=3.14,
            some_bit_val=True,
            is_edit_allowed=True,
            is_delete_allowed=True,
            some_decimal_val=Decimal('99.99'),
            some_min_utc_date_time_val=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            some_min_date_val=date(2023, 1, 1),
            some_money_val=Decimal('100.00'),
            some_n_var_char_val="nvarchar",
            some_var_char_val="varchar",
            some_text_val="text",
            some_phone_number=TEST_PHONE,
            some_email_address=TEST_EMAIL
# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['page_number'] == 1
        assert snake_case_dict['item_count_per_page'] == 10
        assert snake_case_dict['order_by_column_name'] == "name"
        assert snake_case_dict['order_by_descending'] is True
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT
# endset  # noqa: E122
        assert snake_case_dict['flavor_code'] == model.flavor_code
        assert snake_case_dict['some_int_val'] == 42
        assert snake_case_dict['some_big_int_val'] == 123456789
        assert math.isclose(snake_case_dict['some_float_val'], 3.14)
        assert snake_case_dict['some_bit_val'] is True
        assert snake_case_dict['is_edit_allowed'] is True
        assert snake_case_dict['is_delete_allowed'] is True
        assert snake_case_dict['some_decimal_val'] == \
            Decimal('99.99')
        assert snake_case_dict['some_min_utc_date_time_val'] == \
            datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        assert snake_case_dict['some_min_date_val'] == \
            date(2023, 1, 1)
        assert snake_case_dict['some_money_val'] == \
            Decimal('100.00')
        assert snake_case_dict['some_n_var_char_val'] == "nvarchar"
        assert snake_case_dict['some_var_char_val'] == "varchar"
        assert snake_case_dict['some_text_val'] == "text"
        assert snake_case_dict['some_phone_number'] == TEST_PHONE
        assert snake_case_dict['some_email_address'] == TEST_EMAIL
# endset

    def test_to_dict_camel(self):
        """
        Test the to_dict_camel method of the
        LandPlantListGetModelRequest class.
        """
        model = LandPlantListGetModelRequest(
            page_number=1,
            item_count_per_page=10,
            order_by_column_name="name",
            order_by_descending=True,
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122
            flavor_code=uuid.uuid4(),
            some_int_val=42,
            some_big_int_val=123456789,
            some_float_val=3.14,
            some_bit_val=True,
            is_edit_allowed=True,
            is_delete_allowed=True,
            some_decimal_val=Decimal('99.99'),
            some_min_utc_date_time_val=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            some_min_date_val=date(2023, 1, 1),
            some_money_val=Decimal('100.00'),
            some_n_var_char_val="nvarchar",
            some_var_char_val="varchar",
            some_text_val="text",
            some_phone_number=TEST_PHONE,
            some_email_address=TEST_EMAIL
# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['pageNumber'] == 1
        assert camel_case_dict['itemCountPerPage'] == 10
        assert camel_case_dict['orderByColumnName'] == "name"
        assert camel_case_dict['orderByDescending'] is True
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT
# endset
        assert camel_case_dict['flavorCode'] == model.flavor_code
        assert camel_case_dict['someIntVal'] == 42
        assert camel_case_dict['someBigIntVal'] == 123456789
        assert math.isclose(camel_case_dict['someFloatVal'], 3.14)
        assert camel_case_dict['someBitVal'] is True
        assert camel_case_dict['isEditAllowed'] is True
        assert camel_case_dict['isDeleteAllowed'] is True
        assert camel_case_dict['someDecimalVal'] == Decimal('99.99')
        assert camel_case_dict['someMinUTCDateTimeVal'] == datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)  # .isoformat()  # Convert to ISO format
        assert camel_case_dict['someMinDateVal'] == date(2023, 1, 1)  # .isoformat()  # Convert to ISO format
        assert camel_case_dict['someMoneyVal'] == Decimal('100.00')
        assert camel_case_dict['someNVarCharVal'] == "nvarchar"
        assert camel_case_dict['someVarCharVal'] == "varchar"
        assert camel_case_dict['someTextVal'] == "text"
        assert camel_case_dict['somePhoneNumber'] == TEST_PHONE
        assert camel_case_dict['someEmailAddress'] == TEST_EMAIL
# endset


class LandPlantListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    LandPlantListGetModelRequestFactory class.
    """

    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        LandPlantListGetModelRequestFactory class.

        Args:
            session: The database session.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """

        model_instance = await (
            LandPlantListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(
            model_instance,
            LandPlantListGetModelRequest)
        assert isinstance(model_instance.flavor_code, uuid.UUID)
        assert isinstance(model_instance.some_int_val, int)
        assert isinstance(model_instance.some_big_int_val, int)
        assert isinstance(model_instance.some_float_val, float)
        assert isinstance(model_instance.some_bit_val, bool)
        assert isinstance(model_instance.is_edit_allowed, bool)
        assert isinstance(model_instance.is_delete_allowed, bool)
        assert isinstance(model_instance.some_decimal_val, Decimal)
        assert isinstance(model_instance.some_min_utc_date_time_val, datetime)
        assert isinstance(model_instance.some_min_date_val, date)
        assert isinstance(model_instance.some_money_val, Decimal)
        assert isinstance(model_instance.some_n_var_char_val, str)
        assert isinstance(model_instance.some_var_char_val, str)
        assert isinstance(model_instance.some_text_val, str)
        assert isinstance(model_instance.some_phone_number, str)
        assert isinstance(model_instance.some_email_address, str)
        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)


class MockReportItemLandPlantList:
    """
    This class contains mock report items for the
    LandPlantListGetModelResponse class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.plant_code = uuid.uuid4()
        self.some_int_val = 1
        self.some_big_int_val = 1000000
        self.some_bit_val = True
        self.is_edit_allowed = True
        self.is_delete_allowed = True
        self.some_float_val = 1.23
        self.some_decimal_val = Decimal('10.99')
        self.some_utc_date_time_val = datetime.now(timezone.utc)
        self.some_date_val = date.today()
        self.some_money_val = Decimal('100.00')
        self.some_n_var_char_val = \
            "Some N Var Char"
        self.some_var_char_val = \
            "Some Var Char"
        self.some_text_val = \
            "Some Text"
        self.some_phone_number = TEST_PHONE
        self.some_email_address = TEST_EMAIL
        self.flavor_name = \
            "Flavor Name"
        self.flavor_code = uuid.uuid4()
        self.some_int_conditional_on_deletable = 2
        self.n_var_char_as_url = \
            "http://example.com"
        self.update_link_plant_code = uuid.uuid4()
        self.delete_async_button_link_plant_code = uuid.uuid4()
        self.details_link_plant_code = uuid.uuid4()
# endset


@pytest.fixture
def session_context():
    """
    Return a mock session context.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def report_request():
    """
    Return a mock report request.
    """
    return LandPlantListGetModelRequest()


@pytest.fixture
def report_items():
    """
    Return a list of mock report items.
    """
    return [MockReportItemLandPlantList() for _ in range(3)]


@pytest.mark.asyncio
async def test_process_request(session_context, report_request, report_items):
    """
    Test the process_request method of the
    LandPlantListGetModelResponse class.
    """
    with patch(
        "apis.models.land_plant_list"
        ".ReportManagerLandPlantList",
        autospec=True
    ) as mock_report_manager:
        mock_report_manager_instance = \
            mock_report_manager.return_value
        mock_report_manager_instance.generate = AsyncMock(
            return_value=report_items)

        response = LandPlantListGetModelResponse()
        land_code = uuid.uuid4()

        await response.process_request(
            session_context, land_code, report_request)

        assert response.success is True
        assert response.message == "Success."
        assert len(response.items) == len(report_items)

        for response_item, report_item in zip(response.items, report_items):
            assert isinstance(
                response_item,
                LandPlantListGetModelResponseItem
            )
            assert response_item.plant_code == \
                report_item.plant_code
            assert response_item.some_int_val == \
                report_item.some_int_val
            assert response_item.some_big_int_val == \
                report_item.some_big_int_val
            assert response_item.some_bit_val == \
                report_item.some_bit_val
            assert response_item.is_edit_allowed == \
                report_item.is_edit_allowed
            assert response_item.is_delete_allowed == \
                report_item.is_delete_allowed
            assert response_item.some_float_val == \
                report_item.some_float_val
            assert response_item.some_decimal_val == \
                report_item.some_decimal_val
            assert response_item.some_utc_date_time_val == \
                report_item.some_utc_date_time_val
            assert response_item.some_date_val == \
                report_item.some_date_val
            assert response_item.some_money_val == \
                report_item.some_money_val
            assert response_item.some_n_var_char_val == \
                report_item.some_n_var_char_val
            assert response_item.some_var_char_val == \
                report_item.some_var_char_val
            assert response_item.some_text_val == \
                report_item.some_text_val
            assert response_item.some_phone_number == \
                report_item.some_phone_number
            assert response_item.some_email_address == \
                report_item.some_email_address
            assert response_item.flavor_name == \
                report_item.flavor_name
            assert response_item.flavor_code == \
                report_item.flavor_code
            assert response_item.some_int_conditional_on_deletable == \
                report_item.some_int_conditional_on_deletable
            assert response_item.n_var_char_as_url == \
                report_item.n_var_char_as_url
            assert response_item.update_link_plant_code == \
                report_item.update_link_plant_code
            assert response_item.delete_async_button_link_plant_code == \
                report_item.delete_async_button_link_plant_code
            assert response_item.details_link_plant_code == \
                report_item.details_link_plant_code
