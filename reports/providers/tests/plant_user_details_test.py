# plant_user_details_test.py
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
from models.factory.plant import PlantFactory
from services.db_config import DB_DIALECT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT, generate_uuid
from reports.providers.plant_user_details import ReportProviderPlantUserDetails
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
class TestReportProviderPlantUserDetails:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context)
        report_provider = ReportProviderPlantUserDetails(session_context)
        plant = await PlantFactory.create_async(session=session)
        plant_code = plant.code

# endset
        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_provider.generate_list(
            plant_code,

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
                "flavor_name",
                "is_delete_allowed",
                "is_edit_allowed",
                "other_flavor",
                "some_big_int_val",
                "some_bit_val",
                "some_date_val",
                "some_decimal_val",
                "some_email_address",
                "some_float_val",
                "some_int_val",
                "some_money_val",
                "some_n_var_char_val",
                "some_phone_number",
                "some_text_val",
                "some_uniqueidentifier_val",
                "some_utc_date_time_val",
                "some_var_char_val",
                "phone_num_conditional_on_is_editable",
                "n_var_char_as_url",
                "update_button_text_link_plant_code"
                "random_property_updates_link_plant_code",
                "back_to_dashboard_link_tac_code"
# endset
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result"

