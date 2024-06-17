# models/factory/tests/pac_async_test.py
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
from models import Base, Pac
from models.factory import PacFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestPacFactoryAsync:
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
    async def test_pac_creation(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.create_async(session=session)
        assert pac.pac_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.create_async(session=session)
        assert isinstance(pac.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        pac: Pac = await PacFactory.build_async(session=session)
        assert pac.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        pac: Pac = await PacFactory.create_async(session=session)
        assert pac.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.create_async(session=session)
        initial_code = pac.last_change_code
        pac.code = uuid.uuid4()
        await session.commit()
        assert pac.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.build_async(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.build_async(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        pac.code = uuid.uuid4()
        session.add(pac)
        await session.commit()
        assert pac.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.create_async(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
        initial_time = pac.insert_utc_date_time
        pac.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert pac.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.build_async(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.build_async(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        pac.code = uuid.uuid4()
        session.add(pac)
        await session.commit()
        assert pac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.create_async(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
        initial_time = pac.last_update_utc_date_time
        pac.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert pac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.create_async(session=session)
        await session.delete(pac)
        await session.commit()
        # Construct the select statement
        stmt = select(Pac).where(
            Pac._pac_id == pac.pac_id)  # pylint: disable=protected-access
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_pac = result.scalars().first()
        # deleted_pac = await session.query(Pac).filter_by(
        # pac_id=pac.pac_id).first()
        assert deleted_pac is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.create_async(session=session)
        assert isinstance(pac.pac_id, int)
        assert isinstance(pac.code, uuid.UUID)
        assert isinstance(pac.last_change_code, int)
        assert isinstance(pac.insert_user_id, uuid.UUID)
        assert isinstance(pac.last_update_user_id, uuid.UUID)
        assert pac.description == "" or isinstance(pac.description, str)
        assert isinstance(pac.display_order, int)
        assert isinstance(pac.is_active, bool)
        assert pac.lookup_enum_name == "" or isinstance(pac.lookup_enum_name, str)
        assert pac.name == "" or isinstance(pac.name, str)
        # Check for the peek values
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
# endset
        assert isinstance(pac.insert_utc_date_time, datetime)
        assert isinstance(pac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        pac_1 = await PacFactory.create_async(session=session)
        pac_2 = await PacFactory.create_async(session=session)
        pac_2.code = pac_1.code
        session.add_all([pac_1, pac_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        #TODO add comment
        """
        pac = Pac()
        assert pac.code is not None
        assert pac.last_change_code is not None
        assert pac.insert_user_id is not None
        assert pac.last_update_user_id is not None
        assert pac.insert_utc_date_time is not None
        assert pac.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
# endset
        assert pac.description == ""
        assert pac.display_order == 0
        assert pac.is_active is False
        assert pac.lookup_enum_name == ""
        assert pac.name == ""
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        pac = await PacFactory.create_async(session=session)
        original_last_change_code = pac.last_change_code
        stmt = select(Pac).where(
            Pac._pac_id == pac.pac_id)  # pylint: disable=protected-access
        result = await session.execute(stmt)
        pac_1 = result.scalars().first()
        # pac_1 = await session.query(Pac).filter_by(
        # pac_id=pac.pac_id).first()
        pac_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Pac).where(
            Pac._pac_id == pac.pac_id)  # pylint: disable=protected-access
        result = await session.execute(stmt)
        pac_2 = result.scalars().first()
        # pac_2 = await session.query(Pac).filter_by(
        # pac_id=pac.pac_id).first()
        pac_2.code = uuid.uuid4()
        await session.commit()
        assert pac_2.last_change_code != original_last_change_code
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
# endset
