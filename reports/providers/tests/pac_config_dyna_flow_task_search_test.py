# reports/providers/tests/pac_config_dyna_flow_task_search_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains a test case for the
ReportProviderPacConfigDynaFlowTaskSearch class.
"""

import uuid  # noqa: F401
import sqlite3
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.pac import PacFactory
from reports.providers.pac_config_dyna_flow_task_search import (
    ReportProviderPacConfigDynaFlowTaskSearch)
import current_runtime


# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportProviderPacConfigDynaFlowTaskSearch:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    ReportProviderPacConfigDynaFlowTaskSearch class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        This test case verifies the generation of
        a Dyna Flow Task Search report.

        It creates a session context, initializes
        the runtime, and generates
        a Dyna Flow Task Search report using
        the ReportProviderPacConfigDynaFlowTaskSearch class.
        The generated report is then
        checked for the expected format.
        """

        session_context = SessionContext({}, session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPacConfigDynaFlowTaskSearch(
            session_context)
        pac = await PacFactory.create_async(session=session)
        pac_code = pac.code

        # Set up test data
        started_date_greater_than_filter_code: uuid.UUID = (
            uuid.uuid4())  # type: ignore
        processor_identifier: str = ""
        is_started_tri_state_filter_code: uuid.UUID = (
            uuid.uuid4())  # type: ignore
        is_completed_tri_state_filter_code: uuid.UUID = (
            uuid.uuid4())  # type: ignore
        is_successful_tri_state_filter_code: uuid.UUID = (
            uuid.uuid4())  # type: ignore
        # Generate the report
        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            pac_code,
            started_date_greater_than_filter_code,
            processor_identifier,
            is_started_tri_state_filter_code,
            is_completed_tri_state_filter_code,
            is_successful_tri_state_filter_code,
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
                "started_utc_date_time",
                "processor_identifier",
                "is_started",
                "is_completed",
                "is_successful",
                "dyna_flow_task_code",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"
