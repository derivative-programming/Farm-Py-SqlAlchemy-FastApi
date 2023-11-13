from decimal import Decimal
import pytest
import uuid
from typing import List
from decimal import Decimal
from datetime import datetime, date
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.plant import PlantFactory
from reports.plant_user_details import ReportManagerPlantUserDetails
from reports.report_request_validation_error import ReportRequestValidationError
from reports.providers.plant_user_details import ReportProviderPlantUserDetails
from reports.row_models.plant_user_details import ReportItemPlantUserDetails
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
class TestReportManagerPlantUserDetails:
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
        with patch.object(ReportProviderPlantUserDetails, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
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
        with patch.object(ReportProviderPlantUserDetails, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
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
        async def mock_generate_list(
			context_code:uuid,

			page_number:int,
			item_count_per_page:int,
			order_by_column_name:str,
			order_by_descending:bool,
            ):
            result = list()
            return result
        with patch.object(ReportProviderPlantUserDetails, 'generate_list', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_generate_list
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

