import asyncio
from decimal import Decimal
import uuid
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_user_plant_multi_select_to_not_editable import FlowLandUserPlantMultiSelectToNotEditable, FlowLandUserPlantMultiSelectToNotEditableResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.land import LandFactory
from ...models.land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditablePostModelRequest,LandUserPlantMultiSelectToNotEditablePostModelResponse
from models import Base
from ..factory.land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditablePostModelRequestFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field,UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants
from unittest.mock import patch, AsyncMock
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestLandUserPlantMultiSelectToNotEditablePostModelResponse:
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        async def mock_process(
            land_bus_obj: LandBusObj,
            plant_code_list_csv:str = "",
            ):
            return FlowLandUserPlantMultiSelectToNotEditableResult()
        with patch.object(FlowLandUserPlantMultiSelectToNotEditable, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await LandUserPlantMultiSelectToNotEditablePostModelRequestFactory.create_async(session=session)
            response_instance = LandUserPlantMultiSelectToNotEditablePostModelResponse()
            session_context = SessionContext(dict(), session)
            land = await LandFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                land_code=land.code,
                request=request_instance
                )
            assert response_instance.success == True
            mock_method.assert_awaited()

