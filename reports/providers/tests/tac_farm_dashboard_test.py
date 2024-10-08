# reports/providers/tests/tac_farm_dashboard_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=too-few-public-methods

"""
This module contains a test case for the
ReportProviderTacFarmDashboard class.
"""

import uuid  # noqa: F401
import sqlite3
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
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

        session_context = SessionContext({}, session)
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
                "field_one_plant_list_link_land_code",
                "conditional_btn_example_link_land_code",
                "is_conditional_btn_available",
                "test_file_download_link_pac_code",
                "test_conditional_file_download_link_pac_code",
                "test_async_flow_req_link_pac_code",
                "test_conditional_async_flow_req_link_pac_code",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"
