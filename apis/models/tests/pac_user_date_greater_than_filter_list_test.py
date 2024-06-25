# apis/models/tests/pac_user_date_greater_than_filter_list_test.py
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
PacUserDateGreaterThanFilterListGetModelRequestFactoryAsync class.
"""

import uuid
import math

from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch, Mock

import pytest

from helpers.type_conversion import TypeConversion
from helpers.session_context import SessionContext

from ..factory.pac_user_date_greater_than_filter_list import (
    PacUserDateGreaterThanFilterListGetModelRequestFactory)
from ..pac_user_date_greater_than_filter_list import (
    PacUserDateGreaterThanFilterListGetModelRequest,
    PacUserDateGreaterThanFilterListGetModelResponse,
    PacUserDateGreaterThanFilterListGetModelResponseItem)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestPacUserDateGreaterThanFilterListGetModelRequest():
    """
    This class contains unit tests for the
    PacUserDateGreaterThanFilterListGetModelRequest class.
    """

    def test_default_values(self):
        """
        Test the default values of the
        PacUserDateGreaterThanFilterListGetModelRequest class.
        """
        model = PacUserDateGreaterThanFilterListGetModelRequest()
        assert model.page_number == 0
        assert model.item_count_per_page == 0
        assert model.order_by_column_name == ""
        assert model.order_by_descending is False
        assert model.force_error_message == ""


    def test_to_dict_snake(self):
        """
        Test the to_dict_snake method of the
        PacUserDateGreaterThanFilterListGetModelRequest class.
        """
        model = PacUserDateGreaterThanFilterListGetModelRequest(
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
        PacUserDateGreaterThanFilterListGetModelRequest class.
        """
        model = PacUserDateGreaterThanFilterListGetModelRequest(
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


class PacUserDateGreaterThanFilterListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserDateGreaterThanFilterListGetModelRequestFactory class.
    """

    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserDateGreaterThanFilterListGetModelRequestFactory class.

        Args:
            session: The database session.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """

        model_instance = await (
            PacUserDateGreaterThanFilterListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(model_instance, PacUserDateGreaterThanFilterListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)


class MockReportItemPacUserDateGreaterThanFilterList:
    """
    This class contains mock report items for the
    PacUserDateGreaterThanFilterListGetModelResponse class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.date_greater_than_filter_code = uuid.uuid4()
        self.date_greater_than_filter_day_count = 1
        self.date_greater_than_filter_description = "Some N Var Char"
        self.date_greater_than_filter_display_order = 1
        self.date_greater_than_filter_is_active = True
        self.date_greater_than_filter_lookup_enum_name = "Some N Var Char"
        self.date_greater_than_filter_name = "Some N Var Char"
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
    return PacUserDateGreaterThanFilterListGetModelRequest()


@pytest.fixture
def report_items():
    """
    Return a list of mock report items.
    """
    return [MockReportItemPacUserDateGreaterThanFilterList() for _ in range(3)]


@pytest.mark.asyncio
async def test_process_request(session_context, report_request, report_items):
    """
    Test the process_request method of the
    PacUserDateGreaterThanFilterListGetModelResponse class.
    """
    with patch(
        'apis.models.pac_user_date_greater_than_filter_list.ReportManagerPacUserDateGreaterThanFilterList',
        autospec=True
    ) as mock_report_manager:
        mock_report_manager_instance = mock_report_manager.return_value
        mock_report_manager_instance.generate = AsyncMock(
            return_value=report_items)

        response = PacUserDateGreaterThanFilterListGetModelResponse()
        pac_code = uuid.uuid4()

        await response.process_request(
            session_context, pac_code, report_request)

        assert response.success is True
        assert response.message == "Success."
        assert len(response.items) == len(report_items)

        for response_item, report_item in zip(response.items, report_items):
            assert isinstance(response_item, PacUserDateGreaterThanFilterListGetModelResponseItem)
            assert response_item.date_greater_than_filter_code == \
                report_item.date_greater_than_filter_code
            assert response_item.date_greater_than_filter_day_count == \
                report_item.date_greater_than_filter_day_count
            assert response_item.date_greater_than_filter_description == \
                report_item.date_greater_than_filter_description
            assert response_item.date_greater_than_filter_display_order == \
                report_item.date_greater_than_filter_display_order
            assert response_item.date_greater_than_filter_is_active == \
                report_item.date_greater_than_filter_is_active
            assert response_item.date_greater_than_filter_lookup_enum_name == \
                report_item.date_greater_than_filter_lookup_enum_name
            assert response_item.date_greater_than_filter_name == \
                report_item.date_greater_than_filter_name

