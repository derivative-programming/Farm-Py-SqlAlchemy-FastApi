# apis/models/tests/pac_user_tri_state_filter_list_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

"""
This module contains unit tests for the
PacUserTriStateFilterListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
import math  # noqa: F401

from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch, Mock

import pytest

from helpers.type_conversion import TypeConversion  # noqa: F401
from helpers.session_context import SessionContext

from ..factory.pac_user_tri_state_filter_list import (
    PacUserTriStateFilterListGetModelRequestFactory)
from ..pac_user_tri_state_filter_list import (
    PacUserTriStateFilterListGetModelRequest,
    PacUserTriStateFilterListGetModelResponse,
    PacUserTriStateFilterListGetModelResponseItem)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"


class TestPacUserTriStateFilterListGetModelRequest():
    """
    This class contains unit tests for the
    PacUserTriStateFilterListGetModelRequest class.
    """

    def test_default_values(self):
        """
        Test the default values of the
        PacUserTriStateFilterListGetModelRequest class.
        """
        model = PacUserTriStateFilterListGetModelRequest()
        assert model.page_number == 0
        assert model.item_count_per_page == 0
        assert model.order_by_column_name == ""
        assert model.order_by_descending is False
        assert model.force_error_message == ""


    def test_to_dict_snake(self):
        """
        Test the to_dict_snake method of the
        PacUserTriStateFilterListGetModelRequest class.
        """
        model = PacUserTriStateFilterListGetModelRequest(
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
        PacUserTriStateFilterListGetModelRequest class.
        """
        model = PacUserTriStateFilterListGetModelRequest(
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


class PacUserTriStateFilterListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserTriStateFilterListGetModelRequestFactory class.
    """

    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserTriStateFilterListGetModelRequestFactory class.

        Args:
            session: The database session.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """

        model_instance = await (
            PacUserTriStateFilterListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(
            model_instance,
            PacUserTriStateFilterListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)


class MockReportItemPacUserTriStateFilterList:
    """
    This class contains mock report items for the
    PacUserTriStateFilterListGetModelResponse class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.tri_state_filter_code = uuid.uuid4()
        self.tri_state_filter_description = \
            "Some N Var Char"
        self.tri_state_filter_display_order = 1
        self.tri_state_filter_is_active = True
        self.tri_state_filter_lookup_enum_name = \
            "Some N Var Char"
        self.tri_state_filter_name = \
            "Some N Var Char"
        self.tri_state_filter_state_int_value = 1


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
    return PacUserTriStateFilterListGetModelRequest()


@pytest.fixture
def report_items():
    """
    Return a list of mock report items.
    """
    return [MockReportItemPacUserTriStateFilterList() for _ in range(3)]


@pytest.mark.asyncio
async def test_process_request(session_context, report_request, report_items):
    """
    Test the process_request method of the
    PacUserTriStateFilterListGetModelResponse class.
    """
    with patch(
        "apis.models.pac_user_tri_state_filter_list"
        ".ReportManagerPacUserTriStateFilterList",
        autospec=True
    ) as mock_report_manager:
        mock_report_manager_instance = \
            mock_report_manager.return_value
        mock_report_manager_instance.generate = AsyncMock(
            return_value=report_items)

        response = PacUserTriStateFilterListGetModelResponse()
        pac_code = uuid.uuid4()

        await response.process_request(
            session_context, pac_code, report_request)

        assert response.success is True
        assert response.message == "Success."
        assert len(response.items) == len(report_items)

        for response_item, report_item in zip(response.items, report_items):
            assert isinstance(
                response_item,
                PacUserTriStateFilterListGetModelResponseItem
            )
            assert response_item.tri_state_filter_code == \
                report_item.tri_state_filter_code
            assert response_item.tri_state_filter_description == \
                report_item.tri_state_filter_description
            assert response_item.tri_state_filter_display_order == \
                report_item.tri_state_filter_display_order
            assert response_item.tri_state_filter_is_active == \
                report_item.tri_state_filter_is_active
            assert response_item.tri_state_filter_lookup_enum_name == \
                report_item.tri_state_filter_lookup_enum_name
            assert response_item.tri_state_filter_name == \
                report_item.tri_state_filter_name
            assert response_item.tri_state_filter_state_int_value == \
                report_item.tri_state_filter_state_int_value
