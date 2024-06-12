# tac_farm_dashboard_test.py
"""
    #TODO add comment
"""
import os
import uuid
from decimal import Decimal
from datetime import datetime, date
import sqlite3
from unittest.mock import patch, AsyncMock
import pytest
# from sqlalchemy import String
# from typing import List
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
from reports.tac_farm_dashboard import ReportManagerTacFarmDashboard
from reports.report_request_validation_error import ReportRequestValidationError
from reports.providers.tac_farm_dashboard import ReportProviderTacFarmDashboard
from reports.row_models.tac_farm_dashboard import ReportItemTacFarmDashboard
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
# Register the adapter
sqlite3.register_adapter(Decimal, str)
DB_DIALECT = "sqlite"  # noqa: F811
UUIDType = get_uuid_type(DB_DIALECT)
class TestReportManagerTacFarmDashboard:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_report_creation(self, session):
        """
        #TODO add comment
        """
        async def mock_generate_list(
            context_code: uuid.UUID,  # pylint: disable=unused-argument

# endset  # noqa: E122
            page_number: int,  # pylint: disable=unused-argument
            item_count_per_page: int,  # pylint: disable=unused-argument
            order_by_column_name: str,  # pylint: disable=unused-argument
            order_by_descending: bool,  # pylint: disable=unused-argument
        ):
            result = list()
            return result
        with patch.object(
            ReportProviderTacFarmDashboard,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerTacFarmDashboard(session_context)
            tac = await TacFactory.create_async(session=session)
            tac_code = tac.code
            role_required = ""
            session_context.role_name_csv = role_required

# endset
            page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            results = await report_generator.generate(
                tac_code,

# endset  # noqa: E122
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
            context_code: uuid.UUID,  # pylint: disable=unused-argument

# endset  # noqa: E122
            page_number: int,  # pylint: disable=unused-argument
            item_count_per_page: int,  # pylint: disable=unused-argument
            order_by_column_name: str,  # pylint: disable=unused-argument
            order_by_descending: bool,  # pylint: disable=unused-argument
        ):
            result = list()
            return result
        with patch.object(
            ReportProviderTacFarmDashboard,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerTacFarmDashboard(session_context)
            tac = await TacFactory.create_async(session=session)
            tac_code = tac.code
            role_required = ""
            session_context.role_name_csv = role_required

# endset
            page_number = 1
            # item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    tac_code,

# endset  # noqa: E122
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
            context_code: uuid.UUID,  # pylint: disable=unused-argument

# endset  # noqa: E122
            page_number: int,  # pylint: disable=unused-argument
            item_count_per_page: int,  # pylint: disable=unused-argument
            order_by_column_name: str,  # pylint: disable=unused-argument
            order_by_descending: bool,  # pylint: disable=unused-argument
        ):
            result = list()
            return result
        with patch.object(
            ReportProviderTacFarmDashboard,
            'generate_list',
            new_callable=AsyncMock
        ) as mock_method:
            mock_method.side_effect = mock_generate_list
            session_context = SessionContext(dict(), session)
            report_generator = ReportManagerTacFarmDashboard(session_context)
            tac = await TacFactory.create_async(session=session)
            tac_code = tac.code
            role_required = ""
            session_context.role_name_csv = role_required

# endset
            # page_number = 1
            item_count_per_page = 10
            order_by_column_name = ""
            order_by_descending = False
            with pytest.raises(ReportRequestValidationError):
                await report_generator.generate(
                    tac_code,

# endset  # noqa: E122
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
        test_obj = ReportManagerTacFarmDashboard(session_context)
        test_data = [ReportItemTacFarmDashboard(), ReportItemTacFarmDashboard()]
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
        test_obj = ReportManagerTacFarmDashboard(session_context)
        test_data = [ReportItemTacFarmDashboard(), ReportItemTacFarmDashboard()]
        file_name = 'test_input.csv'
        await test_obj.build_csv(file_name, test_data)
        # Ensure 'test_input.csv' exists and contains valid data for testing
        result = await test_obj.read_csv(file_name)
        assert isinstance(result, list)
        assert all(
            isinstance(item, ReportItemTacFarmDashboard) for item in result
        )
        os.remove(file_name)
        # Further checks can be added to verify the data in the objects
    def test_parse_bool(self, session):
        """
        #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        test_obj = ReportManagerTacFarmDashboard(session_context)
        # True values
        assert test_obj._parse_bool('true')  # pylint: disable=protected-access
        assert test_obj._parse_bool('1')  # pylint: disable=protected-access
        assert test_obj._parse_bool('yes')  # pylint: disable=protected-access
        # False values
        assert not test_obj._parse_bool('false')  # pylint: disable=protected-access
        assert not test_obj._parse_bool('0')  # pylint: disable=protected-access
        assert not test_obj._parse_bool('no')  # pylint: disable=protected-access
        # Case insensitivity
        assert test_obj._parse_bool('True')  # pylint: disable=protected-access
        assert test_obj._parse_bool('YeS')  # pylint: disable=protected-access

