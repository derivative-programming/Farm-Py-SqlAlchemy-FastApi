# reports/providers/tests/pac_user_dyna_flow_type_list_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=too-few-public-methods

"""
This module contains a test case for the
ReportProviderPacUserDynaFlowTypeList class.
"""

import uuid  # noqa: F401
import sqlite3
from decimal import Decimal  # noqa: F401
from datetime import datetime, date  # noqa: F401
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.pac import PacFactory
from reports.providers.pac_user_dyna_flow_type_list import (
    ReportProviderPacUserDynaFlowTypeList)
import current_runtime


# Register the adapter
sqlite3.register_adapter(Decimal, str)


class TestReportProviderPacUserDynaFlowTypeList:
    """
    This class contains test cases for the
    ReportProviderPacUserDynaFlowTypeList class.
    """

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        This test case verifies the generation of
        a Pac User Dyna Flow Type List Report report.

        It creates a session context, initializes
        the runtime, and generates
        a Pac User Dyna Flow Type List Report report using
        the ReportProviderPacUserDynaFlowTypeList class.
        The generated report is then
        checked for the expected format.
        """

        session_context = SessionContext({}, session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPacUserDynaFlowTypeList(
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
                "dyna_flow_type_code",
                "dyna_flow_type_description",
                "dyna_flow_type_display_order",
                "dyna_flow_type_is_active",
                "dyna_flow_type_lookup_enum_name",
                "dyna_flow_type_name",
                "dyna_flow_type_priority_level",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"
