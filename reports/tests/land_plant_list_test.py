from decimal import Decimal
import pytest 
from decimal import Decimal
from datetime import datetime, date 
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion 
from models.factory.land import LandFactory
from reports.land_plant_list import ReportManagerLandPlantList
from reports.report_request_validation_error import ReportRequestValidationError 
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String 
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
class TestReportManagerLandPlantList: 

    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        session_context = SessionContext(dict())
        report_generator = ReportManagerLandPlantList(session, session_context) 
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
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
        
        assert isinstance(results, list), "Results should be a list" 
    
    @pytest.mark.asyncio
    async def test_generate_invalid_item_count_per_page(self, session): 
        session_context = SessionContext(dict())
        report_generator = ReportManagerLandPlantList(session, session_context) 
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
                page_number,
                0,
                order_by_column_name,
                order_by_descending
            )

    @pytest.mark.asyncio
    async def test_generate_invalid_page_number(self, session):  
        session_context = SessionContext(dict())
        report_generator = ReportManagerLandPlantList(session, session_context) 
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
                0,
                item_count_per_page,
                order_by_column_name,
                order_by_descending
            )


# from unittest import TestCase
# from unittest.mock import patch, MagicMock
# from reports import ReportManagerLandPlantList, ReportRequestValidationError
# from reports.row_models import ReportItemLandPlantList
# from datetime import date, datetime
# import uuid
# from decimal import Decimal 
# from helpers import SessionContext,TypeConversion
# from models.factory import LandFactory
# from models import CurrentRuntime

# class ReportTestLandPlantList(TestCase):

#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.land = LandFactory.create()
#         self.land_code = self.land.code
        
#         self.some_int_val: int = 0
#         self.some_big_int_val: int = 0
#         self.some_bit_val: bool = False
#         self.is_edit_allowed: bool = False
#         self.is_delete_allowed: bool = False
#         self.some_float_val: float = 0
#         self.some_decimal_val: Decimal = Decimal(0)
#         self.some_min_utc_date_time_val: datetime = TypeConversion.get_default_date_time()
#         self.some_min_date_val: date  = TypeConversion.get_default_date()
#         self.some_money_val: Decimal = Decimal(0)
#         self.some_n_var_char_val: str = ""
#         self.some_var_char_val: str = ""
#         self.some_text_val: str = ""
#         self.some_phone_number: str = ""
#         self.some_email_address: str = ""
#         self.flavor_code: uuid = uuid.UUID(int=0) 

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = "code" 
#         self.order_by_descending = False
#         self.report = ReportManagerLandPlantList(session_context)

    # @patch('farm.reports.providers.land_plant_list.ReportProviderLandPlantList')
    # def test_generate(self, MockProvider):
    #     mock_provider = MockProvider.return_value
    #     mock_provider.generate_list.return_value = [ 
    #         {
    #             "plant_code": uuid.UUID(self.plant_code),
    #             "some_int_val": int(self.some_int_val),
    #             "some_big_int_val": int(self.some_big_int_val),
    #             "some_bit_val": bool(self.some_bit_val),
    #             "is_edit_allowed": bool(self.is_edit_allowed),
    #             "is_delete_allowed": bool(self.is_delete_allowed),
    #             "some_float_val": float(self.some_float_val),
    #             "some_decimal_val": Decimal(self.some_decimal_val),
    #             "some_utc_date_time_val": datetime(self.some_utc_date_time_val),
    #             "some_date_val": date(self.some_date_val),
    #             "some_money_val": Decimal(self.some_money_val),
    #             "some_n_var_char_val": str(self.some_n_var_char_val),
    #             "some_var_char_val": str(self.some_var_char_val),
    #             "some_text_val": str(self.some_text_val),
    #             "some_phone_number": str(self.some_phone_number),
    #             "some_email_address": str(self.some_email_address),
    #             "flavor_name": str(self.flavor_name),
    #             "flavor_code": uuid.UUID(self.flavor_code),
    #             "some_int_conditional_on_deletable": int(self.some_int_conditional_on_deletable),
    #             "n_var_char_as_url": str(self.n_var_char_as_url),
    #             "update_link_plant_code": uuid.UUID(self.update_link_plant_code),
    #             "delete_async_button_link_plant_code": uuid.UUID(self.delete_async_button_link_plant_code),
    #             "details_link_plant_code": uuid.UUID(self.details_link_plant_code)
    #         }
    #     ]

    #     result = self.report.generate(
    #         self.land_code, 
    #         self.page_number,
    #         self.item_count_per_page,
    #         self.order_by_column_name,
    #         self.order_by_descending
    #     )

    #     self.assertIsInstance(result, list)
    #     for item in result:
    #         self.assertIsInstance(item, ReportItemLandPlantList)
    #         self.assertEqual(item.field_one_plant_list_link_land_code, self.land_code)
    #         self.assertEqual(item.conditional_btn_example_link_land_code, self.land_code)
    #         self.assertEqual(item.is_conditional_btn_available, self.land_code)

    # def test_generate_invalid_item_count_per_page(self):
    #     with self.assertRaises(ReportRequestValidationError):
    #         self.report.generate(
    #             self.land_code, 
    #             self.some_int_val, 
    #             self.some_big_int_val,
    #             self.some_bit_val,
    #             self.is_edit_allowed,
    #             self.is_delete_allowed,
    #             self.some_float_val,
    #             self.some_decimal_val, 
    #             self.some_min_utc_date_time_val,
    #             self.some_min_date_val,
    #             self.some_money_val, 
    #             self.some_n_var_char_val,
    #             self.some_var_char_val,
    #             self.some_text_val,
    #             self.some_phone_number,
    #             self.some_email_address,
    #             self.flavor_code, 
    #             self.page_number,
    #             0,
    #             self.order_by_column_name,
    #             self.order_by_descending
    #         )

    # def test_generate_invalid_page_number(self):
    #     with self.assertRaises(ReportRequestValidationError):
    #         self.report.generate(
    #             self.land_code, 
    #             self.some_int_val, 
    #             self.some_big_int_val,
    #             self.some_bit_val,
    #             self.is_edit_allowed,
    #             self.is_delete_allowed,
    #             self.some_float_val,
    #             self.some_decimal_val, 
    #             self.some_min_utc_date_time_val,
    #             self.some_min_date_val,
    #             self.some_money_val, 
    #             self.some_n_var_char_val,
    #             self.some_var_char_val,
    #             self.some_text_val,
    #             self.some_phone_number,
    #             self.some_email_address,
    #             self.flavor_code, 
    #             0,
    #             self.item_count_per_page,
    #             self.order_by_column_name,
    #             self.order_by_descending
    #         )
