# land_plant_list_test.py
# pylint: disable=unused-argument
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains unit tests for the
`ReportManagerLandPlantList`
class in the
`land_plant_list` module.
"""

import os
import uuid  # noqa: F401
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
import sqlite3
from unittest.mock import patch, AsyncMock
import pytest
# from typing import List
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.land import LandFactory
from reports.land_plant_list import (
    ReportManagerLandPlantList)
from reports.report_request_validation_error import (
    ReportRequestValidationError)
from reports.providers.land_plant_list import (
    ReportProviderLandPlantList)
from reports.row_models.land_plant_list import (
    ReportItemLandPlantList)

# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportManagerLandPlantList:
    """
    This class contains unit tests for the
    `ReportManagerLandPlantList` class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        Test case for generating a report.

        This test case verifies the functionality of generating
        a report using the
        `ReportManagerLandPlantList` class.
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
            flavor_code: uuid.UUID,
            some_int_val: int,
            some_big_int_val: int,
            some_float_val: float,
            some_bit_val: bool,
            is_edit_allowed: bool,
            is_delete_allowed: bool,
            some_decimal_val: Decimal,
            some_min_utc_date_time_val: datetime,
            some_min_date_val: date,
            some_money_val: Decimal,
            some_n_var_char_val: str,
            some_var_char_val: str,
            some_text_val: str,
            some_phone_number: str,
            some_email_address: str,
# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = list()
            return result

        with patch.object(
            ReportProviderLandPlantList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list

            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerLandPlantList(
                session_context)
            land = await LandFactory.create_async(
                session=session)
            land_code = land.code

            role_required = "User"

            session_context.role_name_csv = role_required

            some_int_val: int = 0
            some_big_int_val: int = 0
            some_bit_val: bool = False
            is_edit_allowed: bool = False
            is_delete_allowed: bool = False
            some_float_val: float = 0
            some_decimal_val: Decimal = Decimal(0)
            some_min_utc_date_time_val: datetime = (
                TypeConversion.get_default_date_time())
            some_min_date_val: date = TypeConversion.get_default_date()
            some_money_val: Decimal = Decimal(0)
            some_n_var_char_val: str = ""
            some_var_char_val: str = ""
            some_text_val: str = ""
            some_phone_number: str = ""
            some_email_address: str = ""
            flavor_code: uuid.UUID = uuid.uuid4()  # type: ignore
# endset
            page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            results = await report_generator.generate(
                land_code,
                flavor_code,
                some_int_val,
                some_big_int_val,
                some_bit_val,
                is_edit_allowed,
                is_delete_allowed,
                some_float_val,
                some_decimal_val,
                some_min_utc_date_time_val,
                some_min_date_val,
                some_money_val,
                some_n_var_char_val,
                some_var_char_val,
                some_text_val,
                some_phone_number,
                some_email_address,
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
            flavor_code: uuid.UUID,
            some_int_val: int,
            some_big_int_val: int,
            some_float_val: float,
            some_bit_val: bool,
            is_edit_allowed: bool,
            is_delete_allowed: bool,
            some_decimal_val: Decimal,
            some_min_utc_date_time_val: datetime,
            some_min_date_val: date,
            some_money_val: Decimal,
            some_n_var_char_val: str,
            some_var_char_val: str,
            some_text_val: str,
            some_phone_number: str,
            some_email_address: str,
# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = list()
            return result

        with patch.object(
            ReportProviderLandPlantList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list

            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerLandPlantList(
                session_context)
            land = await LandFactory.create_async(
                session=session)
            land_code = land.code

            role_required = "User"

            session_context.role_name_csv = role_required

            some_int_val: int = 0
            some_big_int_val: int = 0
            some_bit_val: bool = False
            is_edit_allowed: bool = False
            is_delete_allowed: bool = False
            some_float_val: float = 0
            some_decimal_val: Decimal = Decimal(0)
            some_min_utc_date_time_val: datetime = (
                TypeConversion.get_default_date_time())
            some_min_date_val: date = TypeConversion.get_default_date()
            some_money_val: Decimal = Decimal(0)
            some_n_var_char_val: str = ""
            some_var_char_val: str = ""
            some_text_val: str = ""
            some_phone_number: str = ""
            some_email_address: str = ""
            flavor_code: uuid.UUID = uuid.uuid4()  # type: ignore
# endset
            page_number = 1
            # item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False

            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    land_code,
                    flavor_code,
                    some_int_val,
                    some_big_int_val,
                    some_bit_val,
                    is_edit_allowed,
                    is_delete_allowed,
                    some_float_val,
                    some_decimal_val,
                    some_min_utc_date_time_val,
                    some_min_date_val,
                    some_money_val,
                    some_n_var_char_val,
                    some_var_char_val,
                    some_text_val,
                    some_phone_number,
                    some_email_address,
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
            flavor_code: uuid.UUID,
            some_int_val: int,
            some_big_int_val: int,
            some_float_val: float,
            some_bit_val: bool,
            is_edit_allowed: bool,
            is_delete_allowed: bool,
            some_decimal_val: Decimal,
            some_min_utc_date_time_val: datetime,
            some_min_date_val: date,
            some_money_val: Decimal,
            some_n_var_char_val: str,
            some_var_char_val: str,
            some_text_val: str,
            some_phone_number: str,
            some_email_address: str,
# endset  # noqa: E122
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
        ):
            result = list()
            return result

        with patch.object(
            ReportProviderLandPlantList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list

            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerLandPlantList(
                session_context)
            land = await LandFactory.create_async(
                session=session)
            land_code = land.code

            role_required = "User"

            session_context.role_name_csv = role_required

            some_int_val: int = 0
            some_big_int_val: int = 0
            some_bit_val: bool = False
            is_edit_allowed: bool = False
            is_delete_allowed: bool = False
            some_float_val: float = 0
            some_decimal_val: Decimal = Decimal(0)
            some_min_utc_date_time_val: datetime = (
                TypeConversion.get_default_date_time())
            some_min_date_val: date = TypeConversion.get_default_date()
            some_money_val: Decimal = Decimal(0)
            some_n_var_char_val: str = ""
            some_var_char_val: str = ""
            some_text_val: str = ""
            some_phone_number: str = ""
            some_email_address: str = ""
            flavor_code: uuid.UUID = uuid.uuid4()  # type: ignore
# endset
            # page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False

            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    land_code,
                    flavor_code,
                    some_int_val,
                    some_big_int_val,
                    some_bit_val,
                    is_edit_allowed,
                    is_delete_allowed,
                    some_float_val,
                    some_decimal_val,
                    some_min_utc_date_time_val,
                    some_min_date_val,
                    some_money_val,
                    some_n_var_char_val,
                    some_var_char_val,
                    some_text_val,
                    some_phone_number,
                    some_email_address,
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
        ReportManagerLandPlantList.

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
        test_obj = ReportManagerLandPlantList(
            session_context)
        test_data = [ReportItemLandPlantList(),
                     ReportItemLandPlantList()]
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
        test_obj = ReportManagerLandPlantList(
            session_context)

        test_data = [ReportItemLandPlantList(),
                     ReportItemLandPlantList()]
        file_name = 'test_input.csv'
        await test_obj.build_csv(file_name, test_data)

        # Ensure 'test_input.csv' exists and contains valid data for testing

        result = await test_obj.read_csv(file_name)
        assert isinstance(result, list)
        assert all(
            isinstance(item, ReportItemLandPlantList
                       ) for item in result
        )

        os.remove(file_name)
        # Further checks can be added to verify the data in the objects

    def test_parse_bool(self, session):
        """
        Test the _parse_bool method of
        ReportManagerLandPlantList.

        This method tests the behavior of the _parse_bool method
        in the ReportManagerLandPlantList class.
        It verifies that the method correctly parses boolean
        values and returns the expected results.

        Args:
            session: The session object for the test.

        Returns:
            None
        """

        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerLandPlantList(
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
