# reports/providers/tests/land_plant_list_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=too-few-public-methods

"""
This module contains a test case for the
ReportProviderLandPlantList class.
"""

import uuid  # noqa: F401
import sqlite3
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.land import LandFactory
from reports.providers.land_plant_list import (
    ReportProviderLandPlantList)
import current_runtime


# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportProviderLandPlantList:
    """
    This class contains test cases for the
    ReportProviderLandPlantList class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        This test case verifies the generation of
        a plant list report.

        It creates a session context, initializes
        the runtime, and generates
        a plant list report using
        the ReportProviderLandPlantList class.
        The generated report is then
        checked for the expected format.
        """

        session_context = SessionContext({}, session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderLandPlantList(
            session_context)
        land = await LandFactory.create_async(session=session)
        land_code = land.code

        # Set up test data
        some_int_val: int = 0
        some_big_int_val: int = 0
        some_bit_val: bool = False
        is_edit_allowed: bool = False
        is_delete_allowed: bool = False
        some_float_val: float = 0
        some_decimal_val: Decimal = Decimal(0)
        some_min_utc_date_time_val: datetime = (
            TypeConversion.get_default_date_time())
        some_min_date_val: date = (
            TypeConversion.get_default_date())
        some_money_val: Decimal = Decimal(0)
        some_n_var_char_val: str = ""
        some_var_char_val: str = ""
        some_text_val: str = ""
        some_phone_number: str = ""
        some_email_address: str = ""
        flavor_code: uuid.UUID = (
            uuid.uuid4())  # type: ignore

        # Generate the report
        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            land_code,
            flavor_code,
            some_int_val,
            some_big_int_val,
            some_float_val,
            some_bit_val,
            is_edit_allowed,
            is_delete_allowed,
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

        for result in results:
            assert isinstance(result, dict), (
                "Each result should be a dictionary")
            expected_keys = [
                "plant_code",
                "some_int_val",
                "some_big_int_val",
                "some_bit_val",
                "is_edit_allowed",
                "is_delete_allowed",
                "some_float_val",
                "some_decimal_val",
                "some_utc_date_time_val",
                "some_date_val",
                "some_money_val",
                "some_n_var_char_val",
                "some_var_char_val",
                "some_text_val",
                "some_phone_number",
                "some_email_address",
                "flavor_name",
                "flavor_code",
                "some_int_conditional_on_deletable",
                "n_var_char_as_url",
                "update_link_plant_code",
                "delete_async_button_link_plant_code",
                "details_link_plant_code",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"
