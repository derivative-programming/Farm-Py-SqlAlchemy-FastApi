# pac_user_tri_state_filter_list_test.py
"""
    #TODO add comment
"""
from decimal import Decimal
import os
import uuid
import pytest
import sqlite3
from sqlalchemy import String
from typing import List
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.pac import PacFactory
from reports.pac_user_tri_state_filter_list import ReportManagerPacUserTriStateFilterList
from reports.report_request_validation_error import ReportRequestValidationError
from reports.providers.pac_user_tri_state_filter_list import ReportProviderPacUserTriStateFilterList
from reports.row_models.pac_user_tri_state_filter_list import ReportItemPacUserTriStateFilterList
from services.db_config import DB_DIALECT
from services.db_config import DB_DIALECT,generate_uuid
from unittest.mock import patch, AsyncMock
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
class TestReportManagerPacUserTriStateFilterList:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        #TODO add comment
        """
        async def mock_generate_list(
            context_code: uuid,

# endset
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
            ):
            result = list()
            return result
        with patch.object(
            ReportProviderPacUserTriStateFilterList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerPacUserTriStateFilterList(session_context)
            pac = await PacFactory.create_async(session=session)
            pac_code = pac.code
            role_required = ""
            session_context.role_name_csv = role_required

# endset
            page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            results = await report_generator.generate(
                pac_code,

# endset
                page_number,
                item_count_per_page,
                order_by_column_name,
                order_by_descending
            )
            assert isinstance(results, list), "Results should be a list"
            mock_method.assert_awaited()
    @pytest.mark.asyncio
    async def test_generate_invalid_item_count_per_page(self, session):
        """
        #TODO add comment
        """
        async def mock_generate_list(
            context_code: uuid,

# endset
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
            ):
            result = list()
            return result
        with patch.object(
            ReportProviderPacUserTriStateFilterList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerPacUserTriStateFilterList(session_context)
            pac = await PacFactory.create_async(session=session)
            pac_code = pac.code
            role_required = ""
            session_context.role_name_csv = role_required

# endset
            page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    pac_code,

# endset
                    page_number,
                    0,
                    order_by_column_name,
                    order_by_descending
                )
    @pytest.mark.asyncio
    async def test_generate_invalid_page_number(self, session):
        """
        #TODO add comment
        """
        async def mock_generate_list(
            context_code: uuid,

# endset
            page_number: int,
            item_count_per_page: int,
            order_by_column_name: str,
            order_by_descending: bool,
            ):
            result = list()
            return result
        with patch.object(
            ReportProviderPacUserTriStateFilterList,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerPacUserTriStateFilterList(session_context)
            pac = await PacFactory.create_async(session=session)
            pac_code = pac.code
            role_required = ""
            session_context.role_name_csv = role_required

# endset
            page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    pac_code,

# endset
                    0,
                    item_count_per_page,
                    order_by_column_name,
                    order_by_descending
                )
    @pytest.mark.asyncio
    async def test_build_csv(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerPacUserTriStateFilterList(session_context)
        test_data = [ReportItemPacUserTriStateFilterList(), ReportItemPacUserTriStateFilterList()]
        file_name = 'test_output.csv'
        await test_obj.build_csv(file_name, test_data)
        # Verify the file is created
        assert os.path.exists(file_name)
        os.remove(file_name)
        # Further checks can be added to verify the content of the file
    @pytest.mark.asyncio
    async def test_read_csv(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerPacUserTriStateFilterList(session_context)
        test_data = [ReportItemPacUserTriStateFilterList(), ReportItemPacUserTriStateFilterList()]
        file_name = 'test_input.csv'
        await test_obj.build_csv(file_name, test_data)
        # Ensure 'test_input.csv' exists and contains valid data for testing
        result = await test_obj.read_csv(file_name)
        assert isinstance(result, list)
        assert all(
            isinstance(item, ReportItemPacUserTriStateFilterList) for item in result
        )
        os.remove(file_name)
        # Further checks can be added to verify the data in the objects
    def test_parse_bool(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerPacUserTriStateFilterList(session_context)
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

