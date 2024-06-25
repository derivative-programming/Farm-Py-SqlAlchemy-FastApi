# plant_user_details_test.py
# pylint: disable=unused-import

"""
This module contains a test case for the
ReportProviderPlantUserDetails class.
"""

import uuid  # noqa: F401
import sqlite3
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.plant import PlantFactory
from reports.providers.plant_user_details import (
    ReportProviderPlantUserDetails)
import current_runtime


# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportProviderPlantUserDetails:
    """
    This class contains test cases for the
    ReportProviderPlantUserDetails class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        This test case verifies the generation of
        a Plant Details report.

        It creates a session context, initializes
        the runtime, and generates
        a Plant Details report using
        the ReportProviderPlantUserDetails class.
        The generated report is then
        checked for the expected format.
        """

        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPlantUserDetails(
            session_context)
        plant = await PlantFactory.create_async(session=session)
        plant_code = plant.code

        # Set up test data

        # Generate the report
        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            plant_code,

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
                "flavor_name",
                "is_delete_allowed",
                "is_edit_allowed",
                "other_flavor",
                "some_big_int_val",
                "some_bit_val",
                "some_date_val",
                "some_decimal_val",
                "some_email_address",
                "some_float_val",
                "some_int_val",
                "some_money_val",
                "some_n_var_char_val",
                "some_phone_number",
                "some_text_val",
                "some_uniqueidentifier_val",
                "some_utc_date_time_val",
                "some_var_char_val",
                "phone_num_conditional_on_is_editable",
                "n_var_char_as_url",
                "update_button_text_link_plant_code"
                "random_property_updates_link_plant_code",
                "back_to_dashboard_link_tac_code"
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"

