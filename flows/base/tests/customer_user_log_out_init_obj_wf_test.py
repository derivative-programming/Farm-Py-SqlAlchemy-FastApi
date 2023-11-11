import asyncio
from decimal import Decimal
import factory
import uuid
from factory import Faker
import pytest
import pytest_asyncio
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from flows.base.customer_user_log_out_init_obj_wf import BaseFlowCustomerUserLogOutInitObjWF
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models import Base, CustomerRole
from models.factory import CustomerRoleFactory
from managers.customer_role import CustomerRoleManager
from models.factory.flavor import FlavorFactory
from models.factory.customer import CustomerFactory
from models.serialization_schema.customer_role import CustomerRoleSchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
import flows.constants.customer_user_log_out_init_obj_wf as FlowConstants
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestBaseFlowCustomerUserLogOutInitObjWF():
    # @pytest.fixture(scope="function")
    # def event_loop(self) -> asyncio.AbstractEventLoop:
    #     loop = asyncio.get_event_loop_policy().new_event_loop()
    #     yield loop
    #     loop.close()
    # @pytest.fixture(scope="function")
    # def engine(self):
    #     engine = create_async_engine(DATABASE_URL, echo=False)
    #     yield engine
    #     engine.sync_engine.dispose()
    # @pytest_asyncio.fixture(scope="function")
    # async def session(self,engine) -> AsyncSession:
    #     @event.listens_for(engine.sync_engine, "connect")
    #     def set_sqlite_pragma(dbapi_connection, connection_record):
    #         cursor = dbapi_connection.cursor()
    #         cursor.execute("PRAGMA foreign_keys=ON")
    #         cursor.close()
    #     async with engine.begin() as connection:
    #         await connection.begin_nested()
    #         await connection.run_sync(Base.metadata.drop_all)
    #         await connection.run_sync(Base.metadata.create_all)
    #         TestingSessionLocal = sessionmaker(
    #             expire_on_commit=False,
    #             class_=AsyncSession,
    #             bind=engine,
    #         )
    #         async with TestingSessionLocal(bind=connection) as session:
    #             @event.listens_for(
    #                 session.sync_session, "after_transaction_end"
    #             )
    #             def end_savepoint(session, transaction):
    #                 if connection.closed:
    #                     return
    #                 if not connection.in_nested_transaction():
    #                     connection.sync_connection.begin_nested()
    #             yield session
    #             await session.flush()
    #             await session.rollback()
    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        session_context = SessionContext(dict())
        flow = BaseFlowCustomerUserLogOutInitObjWF(session_context)
        customer = await CustomerFactory.create_async(session)
        flavor = await FlavorFactory.create_async(session)

        # Call the method being tested
        await flow._process_validation_rules(
            customer,

            )
        # Add assertions here to validate the expected behavior
        #TODO add validation checks - is required,
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        session_context = SessionContext(dict())
        customer = await CustomerFactory.create_async(session)
        flow = BaseFlowCustomerUserLogOutInitObjWF(session_context)
        role_required = ""
        if len(role_required) > 0:
            await flow._process_security_rules(customer)
            assert '' in flow.queued_validation_errors and flow.queued_validation_errors[''] == "Unautorized access. " + role_required + " role not found."
            session_context.role_name_csv = role_required
        # Add assertions here to validate the expected behavior
