from decimal import Decimal
import os
import pytest 
import uuid
from typing import List
from decimal import Decimal
from datetime import datetime, date 
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion 
from models.factory.land import LandFactory
from reports.land_plant_list import ReportManagerLandPlantList
from reports.report_request_validation_error import ReportRequestValidationError 
from reports.providers.land_plant_list import ReportProviderLandPlantList
from reports.row_models.land_plant_list import ReportItemLandPlantList
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String 
import sqlite3
from unittest.mock import patch, AsyncMock


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
class TestReportManagerLandPlantList: 
 
    @pytest.mark.asyncio
    async def test_report_creation(self, session): 
        async def mock_generate_list( 
			context_code:uuid,
			flavor_code: uuid,
			some_int_val: int,
			some_big_int_val: int,
			some_float_val: float,
			some_bit_val: bool,
			is_edit_allowed: bool,
			is_delete_allowed: bool,
			some_decimal_val: Decimal,
			some_min_utc_date_time_val: datetime,
			some_min_date_val: date,
			some_money_val: Decimal,
			some_n_var_char_val: str,
			some_var_char_val: str,
			some_text_val: str,
			some_phone_number: str,
			some_email_address: str,
#endset
			page_number:int,
			item_count_per_page:int,
			order_by_column_name:str,
			order_by_descending:bool,
            ):
            result = list()
            return result
         
        with patch.object(ReportProviderLandPlantList, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
            
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerLandPlantList(session_context) 
            land = await LandFactory.create_async(session=session)
            land_code = land.code  
            
            role_required = "User"

            session_context.role_name_csv = role_required

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
#endset

            page_number = 1
            item_count_per_page = 10
            order_by_column_name = "" 
            order_by_descending = False
            results = await report_generator.generate(
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
#endset
                page_number,
                item_count_per_page,
                order_by_column_name,
                order_by_descending
            )
            
            assert isinstance(results, list), "Results should be a list" 
            mock_method.assert_awaited()
    
    @pytest.mark.asyncio
    async def test_generate_invalid_item_count_per_page(self, session): 
        async def mock_generate_list( 
			context_code:uuid,
			flavor_code: uuid,
			some_int_val: int,
			some_big_int_val: int,
			some_float_val: float,
			some_bit_val: bool,
			is_edit_allowed: bool,
			is_delete_allowed: bool,
			some_decimal_val: Decimal,
			some_min_utc_date_time_val: datetime,
			some_min_date_val: date,
			some_money_val: Decimal,
			some_n_var_char_val: str,
			some_var_char_val: str,
			some_text_val: str,
			some_phone_number: str,
			some_email_address: str,
#endset
			page_number:int,
			item_count_per_page:int,
			order_by_column_name:str,
			order_by_descending:bool,
            ):
            result = list()
            return result
         
        with patch.object(ReportProviderLandPlantList, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
            
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerLandPlantList(session_context) 
            land = await LandFactory.create_async(session=session)
            land_code = land.code  
            
            role_required = "User"

            session_context.role_name_csv = role_required
            
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
#endset

            page_number = 1
            item_count_per_page = 10
            order_by_column_name = "" 
            order_by_descending = False

            with pytest.raises(ReportRequestValidationError):  
                await report_generator.generate(
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
#endset
                    page_number,
                    0,
                    order_by_column_name,
                    order_by_descending
                )

    @pytest.mark.asyncio
    async def test_generate_invalid_page_number(self, session):  
        async def mock_generate_list( 
			context_code:uuid,
			flavor_code: uuid,
			some_int_val: int,
			some_big_int_val: int,
			some_float_val: float,
			some_bit_val: bool,
			is_edit_allowed: bool,
			is_delete_allowed: bool,
			some_decimal_val: Decimal,
			some_min_utc_date_time_val: datetime,
			some_min_date_val: date,
			some_money_val: Decimal,
			some_n_var_char_val: str,
			some_var_char_val: str,
			some_text_val: str,
			some_phone_number: str,
			some_email_address: str,
#endset
			page_number:int,
			item_count_per_page:int,
			order_by_column_name:str,
			order_by_descending:bool,
            ):
            result = list()
            return result
         
        with patch.object(ReportProviderLandPlantList, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
            
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerLandPlantList(session_context) 
            land = await LandFactory.create_async(session=session)
            land_code = land.code  
            
            role_required = "User"

            session_context.role_name_csv = role_required
            
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
#endset

            page_number = 1
            item_count_per_page = 10
            order_by_column_name = "" 
            order_by_descending = False

            with pytest.raises(ReportRequestValidationError): 
                await report_generator.generate(
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
#endset
                    0,
                    item_count_per_page,
                    order_by_column_name,
                    order_by_descending
                )


    @pytest.mark.asyncio
    async def test_build_csv(self,session): 
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerLandPlantList(session_context) 
        test_data = [ReportItemLandPlantList(), ReportItemLandPlantList()]  # Replace with sample data
        file_name = 'test_output.csv'
        await test_obj.build_csv(file_name, test_data)

        # Verify the file is created
        assert os.path.exists(file_name) 

        os.remove(file_name)
        
        # Further checks can be added to verify the content of the file

    @pytest.mark.asyncio
    async def test_read_csv(self,session): 
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerLandPlantList(session_context) 
        
        test_data = [ReportItemLandPlantList(), ReportItemLandPlantList()]   
        file_name = 'test_input.csv'
        await test_obj.build_csv(file_name, test_data)

        # Ensure 'test_input.csv' exists and contains valid data for testing

        result = await test_obj.read_csv(file_name)
        assert isinstance(result, list)
        assert all(isinstance(item, ReportItemLandPlantList) for item in result)

        os.remove(file_name)
        # Further checks can be added to verify the data in the objects

    def test_parse_bool(self,session): 
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerLandPlantList(session_context) 

        # True values
        assert test_obj._parse_bool('true')
        assert test_obj._parse_bool('1')
        assert test_obj._parse_bool('yes')

        # False values
        assert not test_obj._parse_bool('false')
        assert not test_obj._parse_bool('0')
        assert not test_obj._parse_bool('no')

        # Case insensitivity
        assert test_obj._parse_bool('True')
        assert test_obj._parse_bool('YeS')