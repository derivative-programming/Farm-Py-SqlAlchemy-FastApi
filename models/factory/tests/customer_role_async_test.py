# models/factory/tests/customer_role_async_test.py
"""
    #TODO add comment
"""
import uuid
import asyncio
import time
import math
from decimal import Decimal
from datetime import datetime, date, timedelta
from typing import AsyncGenerator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import pytest
import pytest_asyncio
from models import Base, CustomerRole
from models.factory import CustomerRoleFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestCustomerRoleFactoryAsync:
    """
    #TODO add comment
    """
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        """
        #TODO add comment
        """
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        """
        #TODO add comment
        """
        engine = create_async_engine(DATABASE_URL, echo=False)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self, engine) -> AsyncGenerator[AsyncSession, None]:
        """
        #TODO add comment
        """
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
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert customer_role.customer_role_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert isinstance(customer_role.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        customer_role: CustomerRole = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        customer_role: CustomerRole = await CustomerRoleFactory.create_async(session=session)
        assert customer_role.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        initial_code = customer_role.last_change_code
        customer_role.code = uuid.uuid4()
        await session.commit()
        assert customer_role.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer_role.code = uuid.uuid4()
        session.add(customer_role)
        await session.commit()
        assert customer_role.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert customer_role.insert_utc_date_time is not None
        assert isinstance(customer_role.insert_utc_date_time, datetime)
        initial_time = customer_role.insert_utc_date_time
        customer_role.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert customer_role.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.build_async(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        customer_role.code = uuid.uuid4()
        session.add(customer_role)
        await session.commit()
        assert customer_role.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert customer_role.last_update_utc_date_time is not None
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
        initial_time = customer_role.last_update_utc_date_time
        customer_role.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert customer_role.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        await session.delete(customer_role)
        await session.commit()
        # Construct the select statement
        stmt = select(CustomerRole).where(CustomerRole.customer_role_id == customer_role.customer_role_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_customer_role = result.scalars().first()
        # deleted_customer_role = await session.query(CustomerRole).filter_by(
        # customer_role_id=customer_role.customer_role_id).first()
        assert deleted_customer_role is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        assert isinstance(customer_role.customer_role_id, int)
        assert isinstance(customer_role.code, uuid.UUID)
        assert isinstance(customer_role.last_change_code, int)
        assert isinstance(customer_role.insert_user_id, uuid.UUID)
        assert isinstance(customer_role.last_update_user_id, uuid.UUID)
        assert isinstance(customer_role.customer_id, int)
        assert isinstance(customer_role.is_placeholder, bool)
        assert isinstance(customer_role.placeholder, bool)
        assert isinstance(customer_role.role_id, int)
        # Check for the peek values
# endset
        # customerID
        assert isinstance(customer_role.customer_code_peek, uuid.UUID)
        # isPlaceholder,
        # placeholder,
        # roleID
        assert isinstance(customer_role.role_code_peek, uuid.UUID)
# endset
        assert isinstance(customer_role.insert_utc_date_time, datetime)
        assert isinstance(customer_role.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        customer_role_1 = await CustomerRoleFactory.create_async(session=session)
        customer_role_2 = await CustomerRoleFactory.create_async(session=session)
        customer_role_2.code = customer_role_1.code
        session.add_all([customer_role_1, customer_role_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        #TODO add comment
        """
        customer_role = CustomerRole()
        assert customer_role.code is not None
        assert customer_role.last_change_code is not None
        assert customer_role.insert_user_id is not None
        assert customer_role.last_update_user_id is not None
        assert customer_role.insert_utc_date_time is not None
        assert customer_role.last_update_utc_date_time is not None
# endset
        # CustomerID
        assert isinstance(customer_role.customer_code_peek, uuid.UUID)
        # isPlaceholder,
        # placeholder,
        # RoleID
        assert isinstance(customer_role.role_code_peek, uuid.UUID)
# endset
        assert customer_role.customer_id == 0
        assert customer_role.is_placeholder is False
        assert customer_role.placeholder is False
        assert customer_role.role_id == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        original_last_change_code = customer_role.last_change_code
        stmt = select(CustomerRole).where(CustomerRole.customer_role_id == customer_role.customer_role_id)
        result = await session.execute(stmt)
        customer_role_1 = result.scalars().first()
        # customer_role_1 = await session.query(CustomerRole).filter_by(
        # customer_role_id=customer_role.customer_role_id).first()
        customer_role_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(CustomerRole).where(CustomerRole.customer_role_id == customer_role.customer_role_id)
        result = await session.execute(stmt)
        customer_role_2 = result.scalars().first()
        # customer_role_2 = await session.query(CustomerRole).filter_by(
        # customer_role_id=customer_role.customer_role_id).first()
        customer_role_2.code = uuid.uuid4()
        await session.commit()
        assert customer_role_2.last_change_code != original_last_change_code
# endset
    # CustomerID
    @pytest.mark.asyncio
    async def test_invalid_customer_id(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        customer_role.customer_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # isPlaceholder,
    # placeholder,
    # RoleID
    @pytest.mark.asyncio
    async def test_invalid_role_id(self, session):
        """
        #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session=session)
        customer_role.role_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
# endset
