from decimal import Decimal
import pytest  
from decimal import Decimal
from datetime import datetime, date 
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion 
from models.factory.land import LandFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String 
from reports.providers.land_plant_list import ReportProviderLandPlantList
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
class TestReportProviderLandPlantList: 
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        await current_runtime.initialize(session=session)
        session_context = SessionContext(dict())
        report_provider = ReportProviderLandPlantList(session, session_context) 
        land = await LandFactory.create_async(session=session)
        land_code = land.code  

        some_int_val: int = 0
        some_big_int_val: int = 0
        some_bit_val: bool = False
        is_edit_allowed: bool = False
        is_delete_allowed: bool = False
        some_float_val: float = 0
        some_decimal_val: Decimal = Decimal(0)
        some_min_utc_date_time_val: datetime = TypeConversion.get_default_date_time()
        some_min_date_val: date  = TypeConversion.get_default_date()
        some_money_val: Decimal = Decimal(0)
        some_n_var_char_val: str = ""
        some_var_char_val: str = ""
        some_text_val: str = ""
        some_phone_number: str = ""
        some_email_address: str = ""
        flavor_code: UUIDType = generate_uuid()

        page_number = 1
        item_count_per_page = 10
        order_by_column_name = "" 
        order_by_descending = False
        results = await report_provider.generate_list(
            land_code,  
            some_int_val, 
            some_big_int_val,
            some_bit_val,
            is_edit_allowed,
            is_delete_allowed,
            some_float_val,
            some_decimal_val, 
            some_min_utc_date_time_val,
            some_min_date_val,
            some_money_val, 
            some_n_var_char_val,
            some_var_char_val,
            some_text_val,
            some_phone_number,
            some_email_address,
            flavor_code, 
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
        
        assert isinstance(results, list), "Results should be a list"
        
        for result in results:
            assert isinstance(result, dict), "Each result should be a dictionary"
            expected_keys = [
                "plant_code", 
                "some_int_val", 
                "some_big_int_val", 
                "some_bit_val",
                "is_edit_allowed", 
                "is_delete_allowed", 
                "some_float_val", 
                "some_decimal_val",
                "some_utc_date_time_val", 
                "some_date_val", 
                "some_money_val", 
                "some_n_var_char_val",
                "some_var_char_val", 
                "some_text_val", 
                "some_phone_number", 
                "some_email_address",
                "flavor_name", 
                "flavor_code", 
                "some_int_conditional_on_deletable",
                "n_var_char_as_url", 
                "update_link_plant_code", 
                "delete_async_button_link_plant_code",
                "details_link_plant_code"
            ]
            for key in expected_keys:
                assert key in result, f"Key {key} not found in result" 