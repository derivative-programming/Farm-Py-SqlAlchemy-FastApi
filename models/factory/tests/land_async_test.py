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
from models import Base, Land
from models.factory import LandFactory
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
class TestLandFactoryAsync:
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
    async def test_land_creation(self, session):
        land = await LandFactory.create_async(session=session)
        assert land.land_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        land = await LandFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(land.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        land: Land = await LandFactory.build_async(session=session)
        assert land.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        land: Land = await LandFactory.create_async(session=session)
        assert land.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        land = await LandFactory.create_async(session=session)
        initial_code = land.last_change_code
        land.code = generate_uuid()
        await session.commit()
        assert land.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        land = await LandFactory.build_async(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        land = await LandFactory.build_async(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        land.code = generate_uuid()
        await session.commit()
        assert land.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        land = await LandFactory.create_async(session=session)
        assert land.insert_utc_date_time is not None
        assert isinstance(land.insert_utc_date_time, datetime)
        initial_time = land.insert_utc_date_time
        land.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert land.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        land = await LandFactory.build_async(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        land = await LandFactory.build_async(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        land.code = generate_uuid()
        await session.commit()
        assert land.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        land = await LandFactory.create_async(session=session)
        assert land.last_update_utc_date_time is not None
        assert isinstance(land.last_update_utc_date_time, datetime)
        initial_time = land.last_update_utc_date_time
        land.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert land.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        land = await LandFactory.create_async(session=session)
        await session.delete(land)
        await session.commit()
        # Construct the select statement
        stmt = select(Land).where(Land.land_id==land.land_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_land = result.scalars().first()
        # deleted_land = await session.query(Land).filter_by(land_id=land.land_id).first()
        assert deleted_land is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        land = await LandFactory.create_async(session=session)
        assert isinstance(land.land_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(land.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.code, str)
        assert isinstance(land.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(land.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(land.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.last_update_user_id, str)
        assert land.description == "" or isinstance(land.description, str)
        assert isinstance(land.display_order, int)
        assert isinstance(land.is_active, bool)
        assert land.lookup_enum_name == "" or isinstance(land.lookup_enum_name, str)
        assert land.name == "" or isinstance(land.name, str)
        assert isinstance(land.pac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #description,
        #displayOrder,
        # isActive,
        #lookupEnumName,
        #name,
         # pacID
        if db_dialect == 'postgresql':
            assert isinstance(land.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.pac_code_peek, str)

        assert isinstance(land.insert_utc_date_time, datetime)
        assert isinstance(land.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        land_1 = await LandFactory.create_async(session=session)
        land_2 = await LandFactory.create_async(session=session)
        land_2.code = land_1.code
        session.add_all([land_1, land_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        land = Land()
        assert land.code is not None
        assert land.last_change_code is not None
        assert land.insert_user_id is None
        assert land.last_update_user_id is None
        assert land.insert_utc_date_time is not None
        assert land.last_update_utc_date_time is not None

        #description,
        #displayOrder,
        # isActive,
        #lookupEnumName,
        #name,
         # PacID
        if db_dialect == 'postgresql':
            assert isinstance(land.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(land.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(land.pac_code_peek, str)

        assert land.description == ""
        assert land.display_order == 0
        assert land.is_active is False
        assert land.lookup_enum_name == ""
        assert land.name == ""
        assert land.pac_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        land = await LandFactory.create_async(session=session)
        original_last_change_code = land.last_change_code
        stmt = select(Land).where(Land.land_id==land.land_id)
        result = await session.execute(stmt)
        land_1 = result.scalars().first()
        # land_1 = await session.query(Land).filter_by(land_id=land.land_id).first()
        land_1.code = generate_uuid()
        await session.commit()
        stmt = select(Land).where(Land.land_id==land.land_id)
        result = await session.execute(stmt)
        land_2 = result.scalars().first()
        # land_2 = await session.query(Land).filter_by(land_id=land.land_id).first()
        land_2.code = generate_uuid()
        await session.commit()
        assert land_2.last_change_code != original_last_change_code

    #description,
    #displayOrder,
    # isActive,
    #lookupEnumName,
    #name,
     # PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        land = await LandFactory.create_async(session=session)
        land.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

