# apis/models/tests/pac_user_tac_list_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods

"""
This module contains unit tests for the
PacUserTacListGetModelRequestFactoryAsync
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
from models.factory.pac import PacFactory

from ..factory.pac_user_tac_list import (
    PacUserTacListGetModelRequestFactory)
from ..pac_user_tac_list import (
    PacUserTacListGetModelRequest,
    PacUserTacListGetModelResponse,
    PacUserTacListGetModelResponseItem)

TEST_ERROR_TEXT = "Test Error"

TEST_EMAIL = "test@example.com"

TEST_PHONE = "123-456-7890"

PATCH_API_MODEL_LANT_TAC_LIST_REPORT_MANAGER = (
    "apis.models.pac_user_tac_list"
    ".ReportManagerPacUserTacList"
)


class TestPacUserTacListGetModelRequest():
    """
    This class contains unit tests for the
    PacUserTacListGetModelRequest class.
    """

    def test_default_values(self):
        """
        Test the default values of the
        PacUserTacListGetModelRequest class.
        """
        model = PacUserTacListGetModelRequest()
        assert model.page_number == 0
        assert model.item_count_per_page == 0
        assert model.order_by_column_name == ""
        assert model.order_by_descending is False
        assert model.force_error_message == ""


    def test_to_dict_snake(self):
        """
        Test the to_dict_snake method of the
        PacUserTacListGetModelRequest class.
        """
        model = PacUserTacListGetModelRequest(
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
        PacUserTacListGetModelRequest class.
        """
        model = PacUserTacListGetModelRequest(
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


class PacUserTacListGetModelRequestFactoryAsync:
    """
    This class contains asynchronous unit tests for the
    PacUserTacListGetModelRequestFactory class.
    """

    @pytest.mark.asyncio
    async def test_report_generation(self, session):
        """
        Test the generation of a report using the
        PacUserTacListGetModelRequestFactory class.

        Args:
            session: The database session.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """

        model_instance = await (
            PacUserTacListGetModelRequestFactory
            .create_async(session=session)
        )
        assert isinstance(
            model_instance,
            PacUserTacListGetModelRequest)

        assert isinstance(model_instance.page_number, int)
        assert isinstance(model_instance.item_count_per_page, int)


class MockReportItemPacUserTacList:  # pylint: disable=too-few-public-methods
    """
    This class contains mock report items for the
    PacUserTacListGetModelResponse class.
    """
    def __init__(self):
        """
        Initialize the mock object with default values.
        """
        self.tac_code = uuid.uuid4()
        self.tac_description = \
            "Some N Var Char"
        self.tac_display_order = 1
        self.tac_is_active = True
        self.tac_lookup_enum_name = \
            "Some N Var Char"
        self.tac_name = \
            "Some N Var Char"
        self.pac_name = \
            "Some N Var Char"


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
    return PacUserTacListGetModelRequest()


@pytest.fixture
def report_items():
    """
    Return a list of mock report items.
    """
    return [MockReportItemPacUserTacList() for _ in range(3)]


@pytest.mark.asyncio
async def test_process_request(session_context, report_request, report_items):
    """
    Test the process_request method of the
    PacUserTacListGetModelResponse class.
    """
    with patch(
        PATCH_API_MODEL_LANT_TAC_LIST_REPORT_MANAGER,
        autospec=True
    ) as mock_report_manager:
        mock_report_manager_instance = \
            mock_report_manager.return_value
        mock_report_manager_instance.generate = AsyncMock(
            return_value=report_items)

        response = PacUserTacListGetModelResponse()
        pac_code = uuid.uuid4()

        await response.process_request(
            session_context, pac_code, report_request)

        assert response.success is True
        assert response.message == "Success."
        assert len(response.items) == len(report_items)

        for response_item, report_item in zip(response.items, report_items):
            assert isinstance(
                response_item,
                PacUserTacListGetModelResponseItem
            )
            assert response_item.tac_code == \
                report_item.tac_code
            assert response_item.tac_description == \
                report_item.tac_description
            assert response_item.tac_display_order == \
                report_item.tac_display_order
            assert response_item.tac_is_active == \
                report_item.tac_is_active
            assert response_item.tac_lookup_enum_name == \
                report_item.tac_lookup_enum_name
            assert response_item.tac_name == \
                report_item.tac_name
            assert response_item.pac_name == \
                report_item.pac_name
