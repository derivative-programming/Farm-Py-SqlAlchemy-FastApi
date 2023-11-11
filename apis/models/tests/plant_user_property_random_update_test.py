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
from flows.base.flow_validation_error import FlowValidationError
from helpers.session_context import SessionContext
from models.factory.plant import PlantFactory
from ...models.plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequest,PlantUserPropertyRandomUpdatePostModelResponse
from models import Base
from ..factory.plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequestFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field,UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants

db_dialect = "sqlite"

# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)

class TestPlantUserPropertyRandomUpdatePostModelResponse:

    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        request_instance = await PlantUserPropertyRandomUpdatePostModelRequestFactory.create_async(session=session)
        response_instance = PlantUserPropertyRandomUpdatePostModelResponse()
        session_context = SessionContext(dict())

        plant = await PlantFactory.create_async(session)

        role_required = "User"

        if len(role_required) > 0:
            await response_instance.process_request(
                session=session,
                session_context=session_context,
                plant_code=plant.code,
                request=request_instance
            )
            assert response_instance.success == False
            assert len(response_instance.validation_errors) == 1
            assert response_instance.validation_errors[0].message == "Unautorized access. " + role_required + " role not found."

        session_context.role_name_csv = role_required

        customerCodeMatchRequired = False
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed == True:
            customerCodeMatchRequired = True

        if customerCodeMatchRequired == True:
            await response_instance.process_request(
                session=session,
                session_context=session_context,
                plant_code=plant.code,
                request=request_instance
            )
            assert response_instance.success == False
            assert len(response_instance.validation_errors) == 1
            assert response_instance.validation_errors[0].message == "Unautorized access.  Invalid User."

        session_context.role_name_csv = role_required

        await response_instance.process_request(
            session=session,
            session_context=session_context,
            plant_code=plant.code,
            request=request_instance
            )

