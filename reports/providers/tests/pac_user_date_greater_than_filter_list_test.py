# pac_user_date_greater_than_filter_list_test.py

"""
This module contains a test case for the
ReportProviderPacUserDateGreaterThanFilterList class.
"""

import uuid
import sqlite3
from decimal import Decimal
from datetime import datetime, date
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.pac import PacFactory
from reports.providers.pac_user_date_greater_than_filter_list import ReportProviderPacUserDateGreaterThanFilterList
import current_runtime


# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportProviderPacUserDateGreaterThanFilterList:
    """
    This class contains test cases for the
    ReportProviderPacUserDateGreaterThanFilterList class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        This test case verifies the generation of
        a Pac User Date Greater Than Filter List Report report.

        It creates a session context, initializes
        the runtime, and generates
        a Pac User Date Greater Than Filter List Report report using
        the ReportProviderPacUserDateGreaterThanFilterList class.
        The generated report is then
        checked for the expected format.
        """

        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPacUserDateGreaterThanFilterList(session_context)
        pac = await PacFactory.create_async(session=session)
        pac_code = pac.code

        # Set up test data

        # Generate the report
        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            pac_code,

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
                "date_greater_than_filter_code",
                "date_greater_than_filter_day_count",
                "date_greater_than_filter_description",
                "date_greater_than_filter_display_order",
                "date_greater_than_filter_is_active",
                "date_greater_than_filter_lookup_enum_name",
                "date_greater_than_filter_name",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"

