# reports/tests/pac_config_dyna_flow_task_run_to_do_list_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains unit tests for the
`ReportManagerPacConfigDynaFlowTaskRunToDoList`
class in the
`pac_config_dyna_flow_task_run_to_do_list` module.
"""

import os
import sqlite3
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, patch

import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.pac import PacFactory
from reports.pac_config_dyna_flow_task_run_to_do_list import ReportManagerPacConfigDynaFlowTaskRunToDoList
from reports.providers.pac_config_dyna_flow_task_run_to_do_list import ReportProviderPacConfigDynaFlowTaskRunToDoList
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_config_dyna_flow_task_run_to_do_list import ReportItemPacConfigDynaFlowTaskRunToDoList

# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportManagerPacConfigDynaFlowTaskRunToDoList:
    """
    This class contains unit tests for the
    `ReportManagerPacConfigDynaFlowTaskRunToDoList` class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        Test case for generating a report.

        This test case verifies the functionality of generating
        a report using the
        `ReportManagerPacConfigDynaFlowTaskRunToDoList` class.
        It mocks the `generate_list` method and asserts that the
        results returned are of type list.
        The test also ensures that the `generate_list` method is awaited.

        Args:
            session: The session object for the test.

        Returns:
            None
        """

        async def mock_generate_list(
            context_code: uuid.UUID,
            is_run_task_debug_required_tri_state_filter_code: uuid.UUID,
# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = []
            return result

        with patch.object(
            ReportProviderPacConfigDynaFlowTaskRunToDoList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list

            session_context = SessionContext({}, session)
            report_generator = ReportManagerPacConfigDynaFlowTaskRunToDoList(
                session_context)
            pac = await PacFactory.create_async(
                session=session)
            pac_code = pac.code

            role_required = "Config"

            session_context.role_name_csv = role_required
            is_run_task_debug_required_tri_state_filter_code: uuid.UUID = uuid.uuid4()  # type: ignore
            page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            results = await report_generator.generate(
                pac_code,
                is_run_task_debug_required_tri_state_filter_code,
# endset  # noqa: E122
                page_number,
                item_count_per_page,
                order_by_column_name,
                order_by_descending
            )

            assert isinstance(results, list), "Results should be a list"
            mock_method.assert_awaited()

    @pytest.mark.asyncio
    async def test_generate_invalid_item_count_per_page(self, session):
        """
        Test case to verify that an exception is raised when an
        invalid item count per page is provided.

        Args:
            session: The session object.

        Raises:
            ReportRequestValidationError: If an invalid item
                count per page is provided.
        """

        async def mock_generate_list(
            context_code: uuid.UUID,
            is_run_task_debug_required_tri_state_filter_code: uuid.UUID,
# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = []
            return result

        with patch.object(
            ReportProviderPacConfigDynaFlowTaskRunToDoList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list

            session_context = SessionContext({}, session)
            report_generator = ReportManagerPacConfigDynaFlowTaskRunToDoList(
                session_context)
            pac = await PacFactory.create_async(
                session=session)
            pac_code = pac.code

            role_required = "Config"

            session_context.role_name_csv = role_required
            is_run_task_debug_required_tri_state_filter_code: uuid.UUID = uuid.uuid4()  # type: ignore
            page_number = 1
            order_by_column_name = ""
            order_by_descending = False

            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    pac_code,
                    is_run_task_debug_required_tri_state_filter_code,
# endset  # noqa: E122
                    page_number,
                    0,
                    order_by_column_name,
                    order_by_descending
                )

    @pytest.mark.asyncio
    async def test_generate_invalid_page_number(self, session):
        """
        Test case for generating a report with an invalid page number.

        Args:
            session: The session object.

        Raises:
            ReportRequestValidationError: If the report request
                validation fails.
        """

        async def mock_generate_list(
            context_code: uuid.UUID,
            is_run_task_debug_required_tri_state_filter_code: uuid.UUID,
# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = []
            return result

        with patch.object(
            ReportProviderPacConfigDynaFlowTaskRunToDoList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list

            session_context = SessionContext({}, session)
            report_generator = ReportManagerPacConfigDynaFlowTaskRunToDoList(
                session_context)
            pac = await PacFactory.create_async(
                session=session)
            pac_code = pac.code

            role_required = "Config"

            session_context.role_name_csv = role_required
            is_run_task_debug_required_tri_state_filter_code: uuid.UUID = uuid.uuid4()  # type: ignore
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False

            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    pac_code,
                    is_run_task_debug_required_tri_state_filter_code,
# endset  # noqa: E122
                    0,
                    item_count_per_page,
                    order_by_column_name,
                    order_by_descending
                )

    @pytest.mark.asyncio
    async def test_build_csv(self, session):
        """
        Test case for the build_csv method of
        ReportManagerPacConfigDynaFlowTaskRunToDoList.

            This method tests the functionality of the build_csv
            method by creating a test CSV file
            using the provided session and test data. It then
            verifies that the file is created
            and removes it after the test is complete.

            Args:
                session: The session object used for testing.

            Returns:
                None
        """

        session_context = SessionContext(
            {}, session)
        test_obj = ReportManagerPacConfigDynaFlowTaskRunToDoList(
            session_context)
        test_data = [ReportItemPacConfigDynaFlowTaskRunToDoList(),
                     ReportItemPacConfigDynaFlowTaskRunToDoList()]
        file_name = 'test_output.csv'
        await test_obj.build_csv(file_name, test_data)

        # Verify the file is created
        assert os.path.exists(file_name)

        os.remove(file_name)

    @pytest.mark.asyncio
    async def test_read_csv(self, session):
        """
            Test case for reading a CSV file and verifying the data.

            Args:
                session: The session object for database operations.

            Returns:
                None

            Raises:
                AssertionError: If the data read from the CSV
                    file is not as expected.
        """

        session_context = SessionContext({}, session)
        test_obj = ReportManagerPacConfigDynaFlowTaskRunToDoList(
            session_context)

        test_data = [ReportItemPacConfigDynaFlowTaskRunToDoList(),
                     ReportItemPacConfigDynaFlowTaskRunToDoList()]
        file_name = 'test_input.csv'
        await test_obj.build_csv(file_name, test_data)

        # Ensure 'test_input.csv' exists and contains valid data for testing

        result = await test_obj.read_csv(file_name)
        assert isinstance(result, list)
        assert all(
            isinstance(item, ReportItemPacConfigDynaFlowTaskRunToDoList
                       ) for item in result
        )

        os.remove(file_name)
        # Further checks can be added to verify the data in the objects

    def test_parse_bool(self, session):
        """
        Test the _parse_bool method of
        ReportManagerPacConfigDynaFlowTaskRunToDoList.

        This method tests the behavior of the _parse_bool method
        in the ReportManagerPacConfigDynaFlowTaskRunToDoList class.
        It verifies that the method correctly parses boolean
        values and returns the expected results.

        Args:
            session: The session object for the test.

        Returns:
            None
        """

        session_context = SessionContext({}, session)
        test_obj = ReportManagerPacConfigDynaFlowTaskRunToDoList(
            session_context)

        # True values
        assert test_obj._parse_bool('true')
        assert test_obj._parse_bool('1')
        assert test_obj._parse_bool('yes')

        # False values
        assert not test_obj._parse_bool('false')
        assert not test_obj._parse_bool('0')
        assert not test_obj._parse_bool('no')

        # Case insensitivity
        assert test_obj._parse_bool('True')
        assert test_obj._parse_bool('YeS')
