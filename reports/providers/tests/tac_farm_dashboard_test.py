from decimal import Decimal
import pytest
from decimal import Decimal
from datetime import datetime, date
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from reports.providers.tac_farm_dashboard import ReportProviderTacFarmDashboard
import current_runtime
import sqlite3
# Register the adapter
sqlite3.register_adapter(Decimal, str)
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestReportProviderTacFarmDashboard:
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        await current_runtime.initialize(session=session)
        session_context = SessionContext(dict())
        report_provider = ReportProviderTacFarmDashboard(session, session_context)
        tac = await TacFactory.create_async(session=session)
        tac_code = tac.code

        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            tac_code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
        assert isinstance(results, list), "Results should be a list"
        for result in results:
            assert isinstance(result, dict), "Each result should be a dictionary"
            expected_keys = [
                "field_one_plant_list_link_land_code"
                "conditional_btn_example_link_land_code"
                "is_conditional_btn_available",
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"

