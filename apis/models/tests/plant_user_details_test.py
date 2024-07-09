# apis/models/tests/plant_user_details_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods

"""
This module contains unit tests for the
PlantUserDetailsGetModelRequestFactoryAsync
class.
"""

import math  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.plant import PlantFactory

from ..factory.plant_user_details import (
    PlantUserDetailsGetModelRequestFactory)
from ..plant_user_details import (
    PlantUserDetailsGetModelRequest,
    PlantUserDetailsGetModelResponse,
    PlantUserDetailsGetModelResponseItem)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"

PATCH_API_MODEL_LANT__LIST_REPORT_MANAGER = (
    "apis.models.plant_user_details"
    ".ReportManagerPlantUserDetails"
)


class TestPlantUserDetailsGetModelRequest():
    """
    This class contains unit tests for the
    PlantUserDetailsGetModelRequest class.
    """

    def test_default_values(self):
        """
        Test the default values of the
        PlantUserDetailsGetModelRequest class.
        """
        model = PlantUserDetailsGetModelRequest()
        assert model.page_number == 0
        assert model.item_count_per_page == 0
        assert model.order_by_column_name == ""
        assert model.order_by_descending is False
        assert model.force_error_message == ""


    def test_to_dict_snake(self):
        """
        Test the to_dict_snake method of the
        PlantUserDetailsGetModelRequest class.
        """
        model = PlantUserDetailsGetModelRequest(
            page_number=1,
            item_count_per_page=10,
            order_by_column_name="name",
            order_by_descending=True,
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122

# endset  # noqa: E122
        )

        snake_case_dict = model.to_dict_snake()
        assert snake_case_dict['page_number'] == 1
        assert snake_case_dict['item_count_per_page'] == 10
        assert snake_case_dict['order_by_column_name'] == "name"
        assert snake_case_dict['order_by_descending'] is True
        assert snake_case_dict['force_error_message'] == TEST_ERROR_TEXT
# endset  # noqa: E122


    def test_to_dict_camel(self):
        """
        Test the to_dict_camel method of the
        PlantUserDetailsGetModelRequest class.
        """
        model = PlantUserDetailsGetModelRequest(
            page_number=1,
            item_count_per_page=10,
            order_by_column_name="name",
            order_by_descending=True,
            force_error_message=TEST_ERROR_TEXT,
# endset  # noqa: E122

# endset  # noqa: E122
        )

        camel_case_dict = model.to_dict_camel()
        assert camel_case_dict['pageNumber'] == 1
        assert camel_case_dict['itemCountPerPage'] == 10
        assert camel_case_dict['orderByColumnName'] == "name"
        assert camel_case_dict['orderByDescending'] is True
        assert camel_case_dict['forceErrorMessage'] == TEST_ERROR_TEXT


class PlantUserDetailsGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PlantUserDetailsGetModelRequestFactory class.
    """

    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PlantUserDetailsGetModelRequestFactory class.

        Args:
            session: The database session.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """

        model_instance = await (
            PlantUserDetailsGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(
            model_instance,
            PlantUserDetailsGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)


class MockReportItemPlantUserDetails:  # pylint: disable=too-few-public-methods
    """
    This class contains mock report items for the
    PlantUserDetailsGetModelResponse class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.flavor_name = \
            "Some N Var Char"
        self.is_delete_allowed = True
        self.is_edit_allowed = True
        self.other_flavor = \
            "Some N Var Char"
        self.some_big_int_val = 1000000
        self.some_bit_val = True
        self.some_date_val = date.today()
        self.some_decimal_val = Decimal('10.99')
        self.some_email_address = TEST_EMAIL
        self.some_float_val = 1.23
        self.some_int_val = 1
        self.some_money_val = Decimal('100.00')
        self.some_n_var_char_val = \
            "Some N Var Char"
        self.some_phone_number = TEST_PHONE
        self.some_text_val = \
            "Some Text"
        self.some_uniqueidentifier_val = uuid.uuid4()
        self.some_utc_date_time_val = datetime.now(timezone.utc)
        self.some_var_char_val = \
            "Some Var Char"
        self.phone_num_conditional_on_is_editable = \
            "Some Var Char"
        self.n_var_char_as_url = \
            "https://example.com"
        self.update_button_text_link_plant_code = uuid.uuid4()
        self.random_property_updates_link_plant_code = uuid.uuid4()
        self.back_to_dashboard_link_tac_code = uuid.uuid4()


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
    return PlantUserDetailsGetModelRequest()


@pytest.fixture
def report_items():
    """
    Return a list of mock report items.
    """
    return [MockReportItemPlantUserDetails() for _ in range(3)]


@pytest.mark.asyncio
async def test_process_request(session_context, report_request, report_items):
    """
    Test the process_request method of the
    PlantUserDetailsGetModelResponse class.
    """
    with patch(
        PATCH_API_MODEL_LANT__LIST_REPORT_MANAGER,
        autospec=True
    ) as mock_report_manager:
        mock_report_manager_instance = \
            mock_report_manager.return_value
        mock_report_manager_instance.generate = AsyncMock(
            return_value=report_items)

        response = PlantUserDetailsGetModelResponse()
        plant_code = uuid.uuid4()

        await response.process_request(
            session_context, plant_code, report_request)

        assert response.success is True
        assert response.message == "Success."
        assert len(response.items) == len(report_items)

        for response_item, report_item in zip(response.items, report_items):
            assert isinstance(
                response_item,
                PlantUserDetailsGetModelResponseItem
            )
            assert response_item.flavor_name == \
                report_item.flavor_name
            assert response_item.is_delete_allowed == \
                report_item.is_delete_allowed
            assert response_item.is_edit_allowed == \
                report_item.is_edit_allowed
            assert response_item.other_flavor == \
                report_item.other_flavor
            assert response_item.some_big_int_val == \
                report_item.some_big_int_val
            assert response_item.some_bit_val == \
                report_item.some_bit_val
            assert response_item.some_date_val == \
                report_item.some_date_val
            assert response_item.some_decimal_val == \
                report_item.some_decimal_val
            assert response_item.some_email_address == \
                report_item.some_email_address
            assert response_item.some_float_val == \
                report_item.some_float_val
            assert response_item.some_int_val == \
                report_item.some_int_val
            assert response_item.some_money_val == \
                report_item.some_money_val
            assert response_item.some_n_var_char_val == \
                report_item.some_n_var_char_val
            assert response_item.some_phone_number == \
                report_item.some_phone_number
            assert response_item.some_text_val == \
                report_item.some_text_val
            assert response_item.some_uniqueidentifier_val == \
                report_item.some_uniqueidentifier_val
            assert response_item.some_utc_date_time_val == \
                report_item.some_utc_date_time_val
            assert response_item.some_var_char_val == \
                report_item.some_var_char_val
            assert response_item.phone_num_conditional_on_is_editable == \
                report_item.phone_num_conditional_on_is_editable
            assert response_item.n_var_char_as_url == \
                report_item.n_var_char_as_url
            assert response_item.update_button_text_link_plant_code == \
                report_item.update_button_text_link_plant_code
            assert response_item.random_property_updates_link_plant_code == \
                report_item.random_property_updates_link_plant_code
            assert response_item.back_to_dashboard_link_tac_code == \
                report_item.back_to_dashboard_link_tac_code
