# reports/providers/tests/pac_config_dyna_flow_task_retry_run_list_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains a test case for the
ReportProviderPacConfigDynaFlowTaskRetryRunList class.
"""

import uuid  # noqa: F401
import sqlite3
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.pac import PacFactory
from reports.providers.pac_config_dyna_flow_task_retry_run_list import (
    ReportProviderPacConfigDynaFlowTaskRetryRunList)
import current_runtime


# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportProviderPacConfigDynaFlowTaskRetryRunList:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    ReportProviderPacConfigDynaFlowTaskRetryRunList class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        This test case verifies the generation of
        a Dyna Flow Task Retry Run List report.

        It creates a session context, initializes
        the runtime, and generates
        a Dyna Flow Task Retry Run List report using
        the ReportProviderPacConfigDynaFlowTaskRetryRunList class.
        The generated report is then
        checked for the expected format.
        """

        session_context = SessionContext({}, session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPacConfigDynaFlowTaskRetryRunList(
            session_context)
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
                "dyna_flow_task_code",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"
