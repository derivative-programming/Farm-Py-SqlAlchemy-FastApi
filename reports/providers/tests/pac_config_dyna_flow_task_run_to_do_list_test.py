# pac_config_dyna_flow_task_run_to_do_list_test.py
# pylint: disable=unused-import

"""
This module contains a test case for the
ReportProviderPacConfigDynaFlowTaskRunToDoList class.
"""

import uuid  # noqa: F401
import sqlite3
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.pac import PacFactory
from reports.providers.pac_config_dyna_flow_task_run_to_do_list import (
    ReportProviderPacConfigDynaFlowTaskRunToDoList)
import current_runtime


# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportProviderPacConfigDynaFlowTaskRunToDoList:
    """
    This class contains test cases for the
    ReportProviderPacConfigDynaFlowTaskRunToDoList class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        This test case verifies the generation of
        a Dyna Flow Task report.

        It creates a session context, initializes
        the runtime, and generates
        a Dyna Flow Task report using
        the ReportProviderPacConfigDynaFlowTaskRunToDoList class.
        The generated report is then
        checked for the expected format.
        """

        session_context = SessionContext({}, session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPacConfigDynaFlowTaskRunToDoList(
            session_context)
        pac = await PacFactory.create_async(session=session)
        pac_code = pac.code

        # Set up test data
        is_run_task_debug_required_tri_state_filter_code: uuid.UUID = (
            uuid.uuid4())  # type: ignore
        # Generate the report
        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            pac_code,
            is_run_task_debug_required_tri_state_filter_code,
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
                "is_run_task_debug_required",
                "run_order",
                "dyna_flow_priority_level",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"
