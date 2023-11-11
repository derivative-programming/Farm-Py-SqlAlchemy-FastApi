import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models import Base
from models.factory.plant import PlantFactory
from reports.plant_user_details import ReportManagerPlantUserDetails
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
class TestReportManagerPlantUserDetails:
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        session_context = SessionContext(dict())
        report_generator = ReportManagerPlantUserDetails(session, session_context)
        plant = await PlantFactory.create_async(session=session)
        plant_code = plant.code
        role_required = "User"
        session_context.role_name_csv = role_required

        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_generator.generate(
            plant_code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
        assert isinstance(results, list), "Results should be a list"
    @pytest.mark.asyncio
    async def test_generate_invalid_item_count_per_page(self, session):
        session_context = SessionContext(dict())
        report_generator = ReportManagerPlantUserDetails(session, session_context)
        plant = await PlantFactory.create_async(session=session)
        plant_code = plant.code
        role_required = "User"
        session_context.role_name_csv = role_required

        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        with pytest.raises(ReportRequestValidationError):
            await report_generator.generate(
                plant_code,

                page_number,
                0,
                order_by_column_name,
                order_by_descending
            )
    @pytest.mark.asyncio
    async def test_generate_invalid_page_number(self, session):
        session_context = SessionContext(dict())
        report_generator = ReportManagerPlantUserDetails(session, session_context)
        plant = await PlantFactory.create_async(session=session)
        plant_code = plant.code
        role_required = "User"
        session_context.role_name_csv = role_required

        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        with pytest.raises(ReportRequestValidationError):
            await report_generator.generate(
                plant_code,

                0,
                item_count_per_page,
                order_by_column_name,
                order_by_descending
            )
# from unittest import TestCase
# from unittest.mock import patch, MagicMock
# from reports import ReportManagerPlantUserDetails, ReportRequestValidationError
# from reports.row_models import ReportItemPlantUserDetails
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factory import PlantFactory
# from models import CurrentRuntime
# class ReportTestPlantUserDetails(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.plant = PlantFactory.create()
#         self.plant_code = self.plant.code

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = "code"
#         self.order_by_descending = False
#         self.report = ReportManagerPlantUserDetails(session_context)
    # @patch('farm.reports.providers.plant_user_details.ReportProviderPlantUserDetails')
    # def test_generate(self, MockProvider):
    #     mock_provider = MockProvider.return_value
    #     mock_provider.generate_list.return_value = [
    #         {
    #             "flavor_name": str(self.flavor_name),
    #             "is_delete_allowed": bool(self.is_delete_allowed),
    #             "is_edit_allowed": bool(self.is_edit_allowed),
    #             "other_flavor": str(self.other_flavor),
    #             "some_big_int_val": int(self.some_big_int_val),
    #             "some_bit_val": bool(self.some_bit_val),
    #             "some_date_val": date(self.some_date_val),
    #             "some_decimal_val": Decimal(self.some_decimal_val),
    #             "some_email_address": str(self.some_email_address),
    #             "some_float_val": float(self.some_float_val),
    #             "some_int_val": int(self.some_int_val),
    #             "some_money_val": Decimal(self.some_money_val),
    #             "some_n_var_char_val": str(self.some_n_var_char_val),
    #             "some_phone_number": str(self.some_phone_number),
    #             "some_text_val": str(self.some_text_val),
    #             "some_uniqueidentifier_val": uuid.UUID(self.some_uniqueidentifier_val),
    #             "some_utc_date_time_val": datetime(self.some_utc_date_time_val),
    #             "some_var_char_val": str(self.some_var_char_val),
    #             "phone_num_conditional_on_is_editable": str(self.phone_num_conditional_on_is_editable),
    #             "n_var_char_as_url": str(self.n_var_char_as_url),
    #             "update_button_text_link_plant_code": uuid.UUID(self.update_button_text_link_plant_code)
    #             "random_property_updates_link_plant_code": uuid.UUID(self.random_property_updates_link_plant_code),
    #             "back_to_dashboard_link_tac_code": uuid.UUID(self.back_to_dashboard_link_tac_code)
    #         }
    #     ]
    #     result = self.report.generate(
    #         self.plant_code,
    #         self.page_number,
    #         self.item_count_per_page,
    #         self.order_by_column_name,
    #         self.order_by_descending
    #     )
    #     self.assertIsInstance(result, list)
    #     for item in result:
    #         self.assertIsInstance(item, ReportItemPlantUserDetails)
    #         self.assertEqual(item.field_one__list_link_plant_code, self.plant_code)
    #         self.assertEqual(item.conditional_btn_example_link_plant_code, self.plant_code)
    #         self.assertEqual(item.is_conditional_btn_available, self.plant_code)
    # def test_generate_invalid_item_count_per_page(self):
    #     with self.assertRaises(ReportRequestValidationError):
    #         self.report.generate(
    #             self.plant_code,

    #             self.page_number,
    #             0,
    #             self.order_by_column_name,
    #             self.order_by_descending
    #         )
    # def test_generate_invalid_page_number(self):
    #     with self.assertRaises(ReportRequestValidationError):
    #         self.report.generate(
    #             self.plant_code,

    #             0,
    #             self.item_count_per_page,
    #             self.order_by_column_name,
    #             self.order_by_descending
    #         )

