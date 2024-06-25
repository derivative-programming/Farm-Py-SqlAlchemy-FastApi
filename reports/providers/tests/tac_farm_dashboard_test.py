# tac_farm_dashboard_test.py

"""
This module contains a test case for the
ReportProviderTacFarmDashboard class.
"""

import uuid
import sqlite3
from decimal import Decimal
from datetime import datetime, date
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
from reports.providers.tac_farm_dashboard import (
    ReportProviderTacFarmDashboard)
import current_runtime


# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportProviderTacFarmDashboard:
    """
    This class contains test cases for the
    ReportProviderTacFarmDashboard class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        This test case verifies the generation of
        a Farm Dashboard report.

        It creates a session context, initializes
        the runtime, and generates
        a Farm Dashboard report using
        the ReportProviderTacFarmDashboard class.
        The generated report is then
        checked for the expected format.
        """

        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderTacFarmDashboard(
            session_context)
        tac = await TacFactory.create_async(session=session)
        tac_code = tac.code

        # Set up test data

        # Generate the report
        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            tac_code,

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
                "field_one_plant_list_link_land_code"
                "conditional_btn_example_link_land_code"
                "is_conditional_btn_available",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"

