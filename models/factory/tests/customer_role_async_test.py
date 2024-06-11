import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date, timedelta
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, CustomerRole
from models.factory import CustomerRoleFactory
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestCustomerRoleFactoryAsync:
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=False)
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
    @pytest.mark.asyncio
    async def test_customer_role_creation(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert customer_role.customer_role_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(customer_role.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        customer_role: CustomerRole = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        customer_role: CustomerRole = await CustomerRoleFactory.create_async(session=session)
        assert customer_role.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        initial_code = customer_role.last_change_code
        customer_role.code = generate_uuid()
        await session.commit()
        assert customer_role.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        customer_role = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        customer_role = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer_role.code = generate_uuid()
        await session.commit()
        assert customer_role.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
        initial_time = customer_role.insert_utc_date_time
        customer_role.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert customer_role.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        customer_role = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        customer_role = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer_role.code = generate_uuid()
        await session.commit()
        assert customer_role.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
        initial_time = customer_role.last_update_utc_date_time
        customer_role.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert customer_role.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        await session.delete(customer_role)
        await session.commit()
        # Construct the select statement
        stmt = select(CustomerRole).where(CustomerRole.customer_role_id==customer_role.customer_role_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_customer_role = result.scalars().first()
        # deleted_customer_role = await session.query(CustomerRole).filter_by(customer_role_id=customer_role.customer_role_id).first()
        assert deleted_customer_role is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert isinstance(customer_role.customer_role_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(customer_role.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role.code, str)
        assert isinstance(customer_role.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(customer_role.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(customer_role.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role.last_update_user_id, str)
        assert isinstance(customer_role.customer_id, int)
        assert isinstance(customer_role.is_placeholder, bool)
        assert isinstance(customer_role.placeholder, bool)
        assert isinstance(customer_role.role_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #customerID
        if db_dialect == 'postgresql':
            assert isinstance(customer_role.customer_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role.customer_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role.customer_code_peek, str)
        # isPlaceholder,
        #placeholder,
        #roleID
        if db_dialect == 'postgresql':
            assert isinstance(customer_role.role_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role.role_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role.role_code_peek, str)

        assert isinstance(customer_role.insert_utc_date_time, datetime)
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        customer_role_1 = await CustomerRoleFactory.create_async(session=session)
        customer_role_2 = await CustomerRoleFactory.create_async(session=session)
        customer_role_2.code = customer_role_1.code
        session.add_all([customer_role_1, customer_role_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        customer_role = CustomerRole()
        assert customer_role.code is not None
        assert customer_role.last_change_code is not None
        assert customer_role.insert_user_id is None
        assert customer_role.last_update_user_id is None
        assert customer_role.insert_utc_date_time is not None
        assert customer_role.last_update_utc_date_time is not None

        #CustomerID
        if db_dialect == 'postgresql':
            assert isinstance(customer_role.customer_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role.customer_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role.customer_code_peek, str)
        # isPlaceholder,
        #placeholder,
        #RoleID
        if db_dialect == 'postgresql':
            assert isinstance(customer_role.role_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(customer_role.role_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(customer_role.role_code_peek, str)

        assert customer_role.customer_id == 0
        assert customer_role.is_placeholder is False
        assert customer_role.placeholder is False
        assert customer_role.role_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        original_last_change_code = customer_role.last_change_code
        stmt = select(CustomerRole).where(CustomerRole.customer_role_id==customer_role.customer_role_id)
        result = await session.execute(stmt)
        customer_role_1 = result.scalars().first()
        # customer_role_1 = await session.query(CustomerRole).filter_by(customer_role_id=customer_role.customer_role_id).first()
        customer_role_1.code = generate_uuid()
        await session.commit()
        stmt = select(CustomerRole).where(CustomerRole.customer_role_id==customer_role.customer_role_id)
        result = await session.execute(stmt)
        customer_role_2 = result.scalars().first()
        # customer_role_2 = await session.query(CustomerRole).filter_by(customer_role_id=customer_role.customer_role_id).first()
        customer_role_2.code = generate_uuid()
        await session.commit()
        assert customer_role_2.last_change_code != original_last_change_code

    #CustomerID
    @pytest.mark.asyncio
    async def test_invalid_customer_id(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        customer_role.customer_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    # isPlaceholder,
    #placeholder,
    #RoleID
    @pytest.mark.asyncio
    async def test_invalid_role_id(self, session):
        customer_role = await CustomerRoleFactory.create_async(session=session)
        customer_role.role_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

