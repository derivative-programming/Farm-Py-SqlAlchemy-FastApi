# pac_user_flavor_list_test.py
"""
    #TODO add comment
"""
import uuid
import sqlite3
from decimal import Decimal
from datetime import datetime, date
import pytest
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.pac import PacFactory
from reports.providers.pac_user_flavor_list import ReportProviderPacUserFlavorList
import current_runtime
# Register the adapter
sqlite3.register_adapter(Decimal, str)
class TestReportProviderPacUserFlavorList:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPacUserFlavorList(session_context)
        pac = await PacFactory.create_async(session=session)
        pac_code = pac.code

# endset
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
                "flavor_code",
                "flavor_description",
                "flavor_display_order",
                "flavor_is_active",
                "flavor_lookup_enum_name",
                "flavor_name",
                "pac_name",
# endset  # noqa: E122
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"

