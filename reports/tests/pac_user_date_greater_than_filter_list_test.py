from decimal import Decimal
import pytest
import uuid
from typing import List
from decimal import Decimal
from datetime import datetime, date
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.pac import PacFactory
from reports.pac_user_date_greater_than_filter_list import ReportManagerPacUserDateGreaterThanFilterList
from reports.report_request_validation_error import ReportRequestValidationError
from reports.providers.pac_user_date_greater_than_filter_list import ReportProviderPacUserDateGreaterThanFilterList
from reports.row_models.pac_user_date_greater_than_filter_list import ReportItemPacUserDateGreaterThanFilterList
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
class TestReportManagerPacUserDateGreaterThanFilterList:
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        async def mock_generate_list(
			context_code:uuid,

			page_number:int,
			item_count_per_page:int,
			order_by_column_name:str,
			order_by_descending:bool,
            ):
            result = list()
            return result
        with patch.object(ReportProviderPacUserDateGreaterThanFilterList, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict())
            report_generator = ReportManagerPacUserDateGreaterThanFilterList(session, session_context)
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
            mock_method.assert_awaited()
    @pytest.mark.asyncio
    async def test_generate_invalid_item_count_per_page(self, session):
        async def mock_generate_list(
			context_code:uuid,

			page_number:int,
			item_count_per_page:int,
			order_by_column_name:str,
			order_by_descending:bool,
            ):
            result = list()
            return result
        with patch.object(ReportProviderPacUserDateGreaterThanFilterList, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict())
            report_generator = ReportManagerPacUserDateGreaterThanFilterList(session, session_context)
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
        async def mock_generate_list(
			context_code:uuid,

			page_number:int,
			item_count_per_page:int,
			order_by_column_name:str,
			order_by_descending:bool,
            ):
            result = list()
            return result
        with patch.object(ReportProviderPacUserDateGreaterThanFilterList, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict())
            report_generator = ReportManagerPacUserDateGreaterThanFilterList(session, session_context)
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

