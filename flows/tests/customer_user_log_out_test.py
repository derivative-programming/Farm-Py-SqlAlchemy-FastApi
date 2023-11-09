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
from business.customer import CustomerBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.customer_user_log_out import FlowCustomerUserLogOut, FlowCustomerUserLogOutResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.customer import CustomerFactory
from models import Base
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import Field,UUID4
import flows.constants.error_log_config_resolve_error_log as FlowConstants
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestCustomerUserLogOutPostModelResponse:
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=True)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self,engine) -> AsyncGenerator[AsyncSession, None]:
        @event.listens_for(engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        async with engine.begin() as connection:
            await connection.begin_nested()
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
            TestingSessionLocal = sessionmaker(
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with TestingSessionLocal(bind=connection) as session:
                @event.listens_for(
                    session.sync_session, "after_transaction_end"
                )
                def end_savepoint(session, transaction):
                    if connection.closed:
                        return
                    if not connection.in_nested_transaction():
                        connection.sync_connection.begin_nested()
                yield session
                await session.flush()
                await session.rollback()
    #todo finish test
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        session_context = SessionContext(dict())
        flow = FlowCustomerUserLogOut(session_context)
        customer = await CustomerFactory.create_async(session)
        customer_bus_obj = CustomerBusObj(session)
        await customer_bus_obj.load(customer_obj_instance=customer)
        role_required = "User"

        if len(role_required) > 0:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    customer_bus_obj,

                )
            # assert isinstance(flow_result,FlowCustomerUserLogOutResult)
            # assert response_instance.success == False
            # assert len(response_instance.validation_errors) == 1
            # assert response_instance.validation_errors[0].message == "Unautorized access. " + role_required + " role not found."
        session_context.role_name_csv = role_required
        customerCodeMatchRequired = False
        if FlowConstants.calculatedIsRowLevelCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrganizationSecurityUsed == True:
            customerCodeMatchRequired = True
        if FlowConstants.calculatedIsRowLevelOrgCustomerSecurityUsed == True:
            customerCodeMatchRequired = True
        if customerCodeMatchRequired == True:
            with pytest.raises(FlowValidationError):
                flow_result = await flow.process(
                    customer_bus_obj,

                )
                # assert response_instance.success == False
                # assert len(response_instance.validation_errors) == 1
                # assert response_instance.validation_errors[0].message == "Unautorized access.  Invalid User."
        session_context.role_name_csv = role_required
        # await response_instance.process_request(
        #     session=session,
        #     session_context=session_context,
        #     customer_code=customer.code,
        #     request=request_instance
        #     )

