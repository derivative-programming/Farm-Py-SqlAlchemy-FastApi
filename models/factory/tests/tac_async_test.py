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
from models import Base, Tac
from models.factory import TacFactory
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
class TestTacFactoryAsync:
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
    async def test_tac_creation(self, session):
        tac = await TacFactory.create_async(session=session)
        assert tac.tac_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        tac = await TacFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(tac.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tac.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        tac:Tac = await TacFactory.build_async(session=session)
        assert tac.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        tac:Tac = await TacFactory.create_async(session=session)
        assert tac.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        tac = await TacFactory.create_async(session=session)
        initial_code = tac.last_change_code
        tac.code = generate_uuid()
        await session.commit()
        assert tac.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        tac = await TacFactory.build_async(session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(tac.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        tac = await TacFactory.build_async(session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(tac.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tac.code = generate_uuid()
        await session.commit()
        assert tac.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        tac = await TacFactory.create_async(session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(tac.insert_utc_date_time, datetime)
        initial_time = tac.insert_utc_date_time
        tac.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert tac.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        tac = await TacFactory.build_async(session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(tac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        tac = await TacFactory.build_async(session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(tac.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tac.code = generate_uuid()
        await session.commit()
        assert tac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        tac = await TacFactory.create_async(session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(tac.last_update_utc_date_time, datetime)
        initial_time = tac.last_update_utc_date_time
        tac.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert tac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        tac = await TacFactory.create_async(session=session)
        await session.delete(tac)
        await session.commit()
        # Construct the select statement
        stmt = select(Tac).where(Tac.tac_id==tac.tac_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_tac = result.scalars().first()
        # deleted_tac = await session.query(Tac).filter_by(tac_id=tac.tac_id).first()
        assert deleted_tac is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        tac = await TacFactory.create_async(session=session)
        assert isinstance(tac.tac_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(tac.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tac.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.code, str)
        assert isinstance(tac.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(tac.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tac.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(tac.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tac.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.last_update_user_id, str)
        assert tac.description == "" or isinstance(tac.description, str)
        assert isinstance(tac.display_order, int)
        assert isinstance(tac.is_active, bool)
        assert tac.lookup_enum_name == "" or isinstance(tac.lookup_enum_name, str)
        assert tac.name == "" or isinstance(tac.name, str)
        assert isinstance(tac.pac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(tac.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tac.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.pac_code_peek, str)

        assert isinstance(tac.insert_utc_date_time, datetime)
        assert isinstance(tac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        tac_1 = await TacFactory.create_async(session=session)
        tac_2 = await TacFactory.create_async(session=session)
        tac_2.code = tac_1.code
        session.add_all([tac_1, tac_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        tac = Tac()
        assert tac.code is not None
        assert tac.last_change_code is not None
        assert tac.insert_user_id is None
        assert tac.last_update_user_id is None
        assert tac.insert_utc_date_time is not None
        assert tac.last_update_utc_date_time is not None

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(tac.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tac.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac.pac_code_peek, str)

        assert tac.description == ""
        assert tac.display_order == 0
        assert tac.is_active == False
        assert tac.lookup_enum_name == ""
        assert tac.name == ""
        assert tac.pac_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        tac = await TacFactory.create_async(session=session)
        original_last_change_code = tac.last_change_code
        stmt = select(Tac).where(Tac.tac_id==tac.tac_id)
        result = await session.execute(stmt)
        tac_1 = result.scalars().first()
        # tac_1 = await session.query(Tac).filter_by(tac_id=tac.tac_id).first()
        tac_1.code = generate_uuid()
        await session.commit()
        stmt = select(Tac).where(Tac.tac_id==tac.tac_id)
        result = await session.execute(stmt)
        tac_2 = result.scalars().first()
        # tac_2 = await session.query(Tac).filter_by(tac_id=tac.tac_id).first()
        tac_2.code = generate_uuid()
        await session.commit()
        assert tac_2.last_change_code != original_last_change_code

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        tac = await TacFactory.create_async(session=session)
        tac.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

