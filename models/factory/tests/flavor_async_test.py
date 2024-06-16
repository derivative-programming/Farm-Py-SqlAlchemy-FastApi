# models/factory/tests/flavor_async_test.py
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
from models import Base, Flavor
from models.factory import FlavorFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestFlavorFactoryAsync:
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
    async def test_flavor_creation(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        assert flavor.flavor_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        assert isinstance(flavor.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        flavor: Flavor = await FlavorFactory.build_async(session=session)
        assert flavor.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        flavor: Flavor = await FlavorFactory.create_async(session=session)
        assert flavor.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        initial_code = flavor.last_change_code
        flavor.code = uuid.uuid4()
        await session.commit()
        assert flavor.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.build_async(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.build_async(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        flavor.code = uuid.uuid4()
        session.add(flavor)
        await session.commit()
        assert flavor.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
        initial_time = flavor.insert_utc_date_time
        flavor.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert flavor.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.build_async(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.build_async(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        flavor.code = uuid.uuid4()
        session.add(flavor)
        await session.commit()
        assert flavor.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
        initial_time = flavor.last_update_utc_date_time
        flavor.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert flavor.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        await session.delete(flavor)
        await session.commit()
        # Construct the select statement
        stmt = select(Flavor).where(Flavor.flavor_id == flavor.flavor_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_flavor = result.scalars().first()
        # deleted_flavor = await session.query(Flavor).filter_by(
        # flavor_id=flavor.flavor_id).first()
        assert deleted_flavor is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        assert isinstance(flavor.flavor_id, int)
        assert isinstance(flavor.code, uuid.UUID)
        assert isinstance(flavor.last_change_code, int)
        assert isinstance(flavor.insert_user_id, uuid.UUID)
        assert isinstance(flavor.last_update_user_id, uuid.UUID)
        assert flavor.description == "" or isinstance(flavor.description, str)
        assert isinstance(flavor.display_order, int)
        assert isinstance(flavor.is_active, bool)
        assert flavor.lookup_enum_name == "" or isinstance(flavor.lookup_enum_name, str)
        assert flavor.name == "" or isinstance(flavor.name, str)
        assert isinstance(flavor.pac_id, int)
        # Check for the peek values
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        assert isinstance(flavor.pac_code_peek, uuid.UUID)
# endset
        assert isinstance(flavor.insert_utc_date_time, datetime)
        assert isinstance(flavor.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        flavor_1 = await FlavorFactory.create_async(session=session)
        flavor_2 = await FlavorFactory.create_async(session=session)
        flavor_2.code = flavor_1.code
        session.add_all([flavor_1, flavor_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        #TODO add comment
        """
        flavor = Flavor()
        assert flavor.code is not None
        assert flavor.last_change_code is not None
        assert flavor.insert_user_id is not None
        assert flavor.last_update_user_id is not None
        assert flavor.insert_utc_date_time is not None
        assert flavor.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(flavor.pac_code_peek, uuid.UUID)
# endset
        assert flavor.description == ""
        assert flavor.display_order == 0
        assert flavor.is_active is False
        assert flavor.lookup_enum_name == ""
        assert flavor.name == ""
        assert flavor.pac_id == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        original_last_change_code = flavor.last_change_code
        stmt = select(Flavor).where(Flavor.flavor_id == flavor.flavor_id)
        result = await session.execute(stmt)
        flavor_1 = result.scalars().first()
        # flavor_1 = await session.query(Flavor).filter_by(
        # flavor_id=flavor.flavor_id).first()
        flavor_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Flavor).where(Flavor.flavor_id == flavor.flavor_id)
        result = await session.execute(stmt)
        flavor_2 = result.scalars().first()
        # flavor_2 = await session.query(Flavor).filter_by(
        # flavor_id=flavor.flavor_id).first()
        flavor_2.code = uuid.uuid4()
        await session.commit()
        assert flavor_2.last_change_code != original_last_change_code
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        """
        #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session=session)
        flavor.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
# endset
