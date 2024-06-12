# pac_user_tri_state_filter_list_test.py
"""
    #TODO add comment
"""
import pytest
import sqlite3
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import String
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.pac import PacFactory
from services.db_config import DB_DIALECT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT, generate_uuid
from reports.providers.pac_user_tri_state_filter_list import ReportProviderPacUserTriStateFilterList
import current_runtime
# Register the adapter
sqlite3.register_adapter(Decimal, str)
DB_DIALECT = "sqlite"
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestReportProviderPacUserTriStateFilterList:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPacUserTriStateFilterList(session_context)
        pac = await PacFactory.create_async(session=session)
        pac_code = pac.code

# endset
        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            pac_code,

# endset
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
                "tri_state_filter_code",
                "tri_state_filter_description",
                "tri_state_filter_display_order",
                "tri_state_filter_is_active",
                "tri_state_filter_lookup_enum_name",
                "tri_state_filter_name",
                "tri_state_filter_state_int_value",
# endset
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"

