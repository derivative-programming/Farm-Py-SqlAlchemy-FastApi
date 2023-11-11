from decimal import Decimal
import pytest
from decimal import Decimal
from datetime import datetime, date
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.pac import PacFactory
from reports.pac_user_tac_list import ReportManagerPacUserTacList
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
class TestReportManagerPacUserTacList:
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        session_context = SessionContext(dict())
        report_generator = ReportManagerPacUserTacList(session, session_context)
        pac = await PacFactory.create_async(session=session)
        pac_code = pac.code
        role_required = ""
        session_context.role_name_csv = role_required

        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        results = await report_generator.generate(
            pac_code,

            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending
        )
        assert isinstance(results, list), "Results should be a list"
    @pytest.mark.asyncio
    async def test_generate_invalid_item_count_per_page(self, session):
        session_context = SessionContext(dict())
        report_generator = ReportManagerPacUserTacList(session, session_context)
        pac = await PacFactory.create_async(session=session)
        pac_code = pac.code
        role_required = ""
        session_context.role_name_csv = role_required

        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        with pytest.raises(ReportRequestValidationError):
            await report_generator.generate(
                pac_code,

                page_number,
                0,
                order_by_column_name,
                order_by_descending
            )
    @pytest.mark.asyncio
    async def test_generate_invalid_page_number(self, session):
        session_context = SessionContext(dict())
        report_generator = ReportManagerPacUserTacList(session, session_context)
        pac = await PacFactory.create_async(session=session)
        pac_code = pac.code
        role_required = ""
        session_context.role_name_csv = role_required

        page_number = 1
        item_count_per_page = 10
        order_by_column_name = ""
        order_by_descending = False
        with pytest.raises(ReportRequestValidationError):
            await report_generator.generate(
                pac_code,

                0,
                item_count_per_page,
                order_by_column_name,
                order_by_descending
            )
# from unittest import TestCase
# from unittest.mock import patch, MagicMock
# from reports import ReportManagerPacUserTacList, ReportRequestValidationError
# from reports.row_models import ReportItemPacUserTacList
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factory import PacFactory
# from models import CurrentRuntime
# class ReportTestPacUserTacList(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.pac = PacFactory.create()
#         self.pac_code = self.pac.code

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = "code"
#         self.order_by_descending = False
#         self.report = ReportManagerPacUserTacList(session_context)
    # @patch('farm.reports.providers.pac_user_tac_list.ReportProviderPacUserTacList')
    # def test_generate(self, MockProvider):
    #     mock_provider = MockProvider.return_value
    #     mock_provider.generate_list.return_value = [
    #         {
    #             "tac_code": uuid.UUID(self.tac_code),
    #             "tac_description": str(self.tac_description),
    #             "tac_display_order": int(self.tac_display_order),
    #             "tac_is_active": bool(self.tac_is_active),
    #             "tac_lookup_enum_name": str(self.tac_lookup_enum_name),
    #             "tac_name": str(self.tac_name),
    #             "pac_name": str(self.pac_name),
    #         }
    #     ]
    #     result = self.report.generate(
    #         self.pac_code,
    #         self.page_number,
    #         self.item_count_per_page,
    #         self.order_by_column_name,
    #         self.order_by_descending
    #     )
    #     self.assertIsInstance(result, list)
    #     for item in result:
    #         self.assertIsInstance(item, ReportItemPacUserTacList)
    #         self.assertEqual(item.field_one_tac_list_link_pac_code, self.pac_code)
    #         self.assertEqual(item.conditional_btn_example_link_pac_code, self.pac_code)
    #         self.assertEqual(item.is_conditional_btn_available, self.pac_code)
    # def test_generate_invalid_item_count_per_page(self):
    #     with self.assertRaises(ReportRequestValidationError):
    #         self.report.generate(
    #             self.pac_code,

    #             self.page_number,
    #             0,
    #             self.order_by_column_name,
    #             self.order_by_descending
    #         )
    # def test_generate_invalid_page_number(self):
    #     with self.assertRaises(ReportRequestValidationError):
    #         self.report.generate(
    #             self.pac_code,

    #             0,
    #             self.item_count_per_page,
    #             self.order_by_column_name,
    #             self.order_by_descending
    #         )

