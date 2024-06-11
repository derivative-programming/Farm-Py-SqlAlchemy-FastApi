# models/factory/tests/pac_async_test.py
"""
    #TODO add comment
"""
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
from models import Base, Pac
from models.factory import PacFactory
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
class TestPacFactoryAsync:
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
    async def test_pac_creation(self, session):
        pac = await PacFactory.create_async(session=session)
        assert pac.pac_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        pac = await PacFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(pac.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        pac: Pac = await PacFactory.build_async(session=session)
        assert pac.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        pac: Pac = await PacFactory.create_async(session=session)
        assert pac.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        pac = await PacFactory.create_async(session=session)
        initial_code = pac.last_change_code
        pac.code = generate_uuid()
        await session.commit()
        assert pac.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        pac = await PacFactory.build_async(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        pac = await PacFactory.build_async(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        pac.code = generate_uuid()
        await session.commit()
        assert pac.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        pac = await PacFactory.create_async(session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(pac.insert_utc_date_time, datetime)
        initial_time = pac.insert_utc_date_time
        pac.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert pac.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        pac = await PacFactory.build_async(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        pac = await PacFactory.build_async(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        pac.code = generate_uuid()
        await session.commit()
        assert pac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        pac = await PacFactory.create_async(session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(pac.last_update_utc_date_time, datetime)
        initial_time = pac.last_update_utc_date_time
        pac.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert pac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        pac = await PacFactory.create_async(session=session)
        await session.delete(pac)
        await session.commit()
        # Construct the select statement
        stmt = select(Pac).where(Pac.pac_id==pac.pac_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_pac = result.scalars().first()
        # deleted_pac = await session.query(Pac).filter_by(pac_id=pac.pac_id).first()
        assert deleted_pac is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        pac = await PacFactory.create_async(session=session)
        assert isinstance(pac.pac_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(pac.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac.code, str)
        assert isinstance(pac.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(pac.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(pac.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac.last_update_user_id, str)
        assert pac.description == "" or isinstance(pac.description, str)
        assert isinstance(pac.display_order, int)
        assert isinstance(pac.is_active, bool)
        assert pac.lookup_enum_name == "" or isinstance(pac.lookup_enum_name, str)
        assert pac.name == "" or isinstance(pac.name, str)
        # Check for the peek values, assuming they are UUIDs based on your model

        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,

        assert isinstance(pac.insert_utc_date_time, datetime)
        assert isinstance(pac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        pac_1 = await PacFactory.create_async(session=session)
        pac_2 = await PacFactory.create_async(session=session)
        pac_2.code = pac_1.code
        session.add_all([pac_1, pac_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        pac = Pac()
        assert pac.code is not None
        assert pac.last_change_code is not None
        assert pac.insert_user_id is None
        assert pac.last_update_user_id is None
        assert pac.insert_utc_date_time is not None
        assert pac.last_update_utc_date_time is not None

        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,

        assert pac.description == ""
        assert pac.display_order == 0
        assert pac.is_active is False
        assert pac.lookup_enum_name == ""
        assert pac.name == ""

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        pac = await PacFactory.create_async(session=session)
        original_last_change_code = pac.last_change_code
        stmt = select(Pac).where(Pac.pac_id==pac.pac_id)
        result = await session.execute(stmt)
        pac_1 = result.scalars().first()
        # pac_1 = await session.query(Pac).filter_by(pac_id=pac.pac_id).first()
        pac_1.code = generate_uuid()
        await session.commit()
        stmt = select(Pac).where(Pac.pac_id==pac.pac_id)
        result = await session.execute(stmt)
        pac_2 = result.scalars().first()
        # pac_2 = await session.query(Pac).filter_by(pac_id=pac.pac_id).first()
        pac_2.code = generate_uuid()
        await session.commit()
        assert pac_2.last_change_code != original_last_change_code

    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,

