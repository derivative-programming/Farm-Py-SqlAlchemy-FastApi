# plant_user_details_test.py
# pylint: disable=unused-argument
# pylint: disable=protected-access
"""
This module contains unit tests for the
`ReportManagerPlantUserDetails`
class in the `plant_user_details` module.
"""
import os
import uuid
from decimal import Decimal
from datetime import datetime, date
import sqlite3
from unittest.mock import patch, AsyncMock
import pytest
# from typing import List
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.plant import PlantFactory
from reports.plant_user_details import (
    ReportManagerPlantUserDetails)
from reports.report_request_validation_error import (
    ReportRequestValidationError)
from reports.providers.plant_user_details import (
    ReportProviderPlantUserDetails)
from reports.row_models.plant_user_details import (
    ReportItemPlantUserDetails)
# Register the adapter
sqlite3.register_adapter(Decimal, str)
class TestReportManagerPlantUserDetails:
    """
    This class contains unit tests for the
    `ReportManagerPlantUserDetails` class.
    """
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        Test case for generating a report.
        This test case verifies the functionality of generating
        a report using the
        `ReportManagerPlantUserDetails` class.
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

# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = list()
            return result
        with patch.object(
            ReportProviderPlantUserDetails,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerPlantUserDetails(
                session_context)
            plant = await PlantFactory.create_async(
                session=session)
            plant_code = plant.code
            role_required = "User"
            session_context.role_name_csv = role_required

# endset
            page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            results = await report_generator.generate(
                plant_code,

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

# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = list()
            return result
        with patch.object(
            ReportProviderPlantUserDetails,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerPlantUserDetails(
                session_context)
            plant = await PlantFactory.create_async(
                session=session)
            plant_code = plant.code
            role_required = "User"
            session_context.role_name_csv = role_required

# endset
            page_number = 1
            # item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    plant_code,

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

# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = list()
            return result
        with patch.object(
            ReportProviderPlantUserDetails,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerPlantUserDetails(
                session_context)
            plant = await PlantFactory.create_async(
                session=session)
            plant_code = plant.code
            role_required = "User"
            session_context.role_name_csv = role_required

# endset
            # page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    plant_code,

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
        ReportManagerPlantUserDetails.
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
            dict(), session)
        test_obj = ReportManagerPlantUserDetails(
            session_context)
        test_data = [ReportItemPlantUserDetails(),
                     ReportItemPlantUserDetails()]
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
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerPlantUserDetails(
            session_context)
        test_data = [ReportItemPlantUserDetails(),
                     ReportItemPlantUserDetails()]
        file_name = 'test_input.csv'
        await test_obj.build_csv(file_name, test_data)
        # Ensure 'test_input.csv' exists and contains valid data for testing
        result = await test_obj.read_csv(file_name)
        assert isinstance(result, list)
        assert all(
            isinstance(item, ReportItemPlantUserDetails) for item in result
        )
        os.remove(file_name)
        # Further checks can be added to verify the data in the objects
    def test_parse_bool(self, session):
        """
        Test the _parse_bool method of
        ReportManagerPlantUserDetails.
        This method tests the behavior of the _parse_bool method
        in the ReportManagerPlantUserDetails class.
        It verifies that the method correctly parses boolean
        values and returns the expected results.
        Args:
            session: The session object for the test.
        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerPlantUserDetails(
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

