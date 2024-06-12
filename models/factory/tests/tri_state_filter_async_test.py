# models/factory/tests/tri_state_filter_async_test.py
"""
    #TODO add comment
"""
import asyncio
import time
import math
from decimal import Decimal
from datetime import datetime, date, timedelta
from typing import AsyncGenerator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import pytest
import pytest_asyncio
from models import Base, TriStateFilter
from models.factory import TriStateFilterFactory
from services.db_config import DB_DIALECT, generate_uuid
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
DB_DIALECT = "sqlite"  # noqa: F811
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestTriStateFilterFactoryAsync:
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
    async def test_tri_state_filter_creation(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert tri_state_filter.tri_state_filter_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        if DB_DIALECT == 'postgresql':
            assert isinstance(tri_state_filter.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tri_state_filter.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tri_state_filter.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        tri_state_filter: TriStateFilter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        tri_state_filter: TriStateFilter = await TriStateFilterFactory.create_async(session=session)
        assert tri_state_filter.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        initial_code = tri_state_filter.last_change_code
        tri_state_filter.code = generate_uuid()
        await session.commit()
        assert tri_state_filter.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tri_state_filter.code = generate_uuid()
        await session.commit()
        assert tri_state_filter.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        initial_time = tri_state_filter.insert_utc_date_time
        tri_state_filter.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert tri_state_filter.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tri_state_filter.code = generate_uuid()
        await session.commit()
        assert tri_state_filter.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
        initial_time = tri_state_filter.last_update_utc_date_time
        tri_state_filter.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert tri_state_filter.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        await session.delete(tri_state_filter)
        await session.commit()
        # Construct the select statement
        stmt = select(TriStateFilter).where(TriStateFilter.tri_state_filter_id == tri_state_filter.tri_state_filter_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_tri_state_filter = result.scalars().first()
        # deleted_tri_state_filter = await session.query(TriStateFilter).filter_by(
        # tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        assert deleted_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert isinstance(tri_state_filter.tri_state_filter_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(tri_state_filter.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tri_state_filter.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tri_state_filter.code, str)
        assert isinstance(tri_state_filter.last_change_code, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(tri_state_filter.insert_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tri_state_filter.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tri_state_filter.insert_user_id, str)
        if DB_DIALECT == 'postgresql':
            assert isinstance(tri_state_filter.last_update_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tri_state_filter.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tri_state_filter.last_update_user_id, str)
        assert tri_state_filter.description == "" or isinstance(tri_state_filter.description, str)
        assert isinstance(tri_state_filter.display_order, int)
        assert isinstance(tri_state_filter.is_active, bool)
        assert tri_state_filter.lookup_enum_name == "" or isinstance(tri_state_filter.lookup_enum_name, str)
        assert tri_state_filter.name == "" or isinstance(tri_state_filter.name, str)
        assert isinstance(tri_state_filter.pac_id, int)
        assert isinstance(tri_state_filter.state_int_value, int)
        # Check for the peek values
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(tri_state_filter.pac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tri_state_filter.pac_code_peek,
                              UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tri_state_filter.pac_code_peek, str)
        # stateIntValue,
# endset
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        tri_state_filter_1 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter_2 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter_2.code = tri_state_filter_1.code
        session.add_all([tri_state_filter_1, tri_state_filter_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = TriStateFilter()
        assert tri_state_filter.code is not None
        assert tri_state_filter.last_change_code is not None
        assert tri_state_filter.insert_user_id is None
        assert tri_state_filter.last_update_user_id is None
        assert tri_state_filter.insert_utc_date_time is not None
        assert tri_state_filter.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(tri_state_filter.pac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(tri_state_filter.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tri_state_filter.pac_code_peek, str)
        # stateIntValue,
# endset
        assert tri_state_filter.description == ""
        assert tri_state_filter.display_order == 0
        assert tri_state_filter.is_active is False
        assert tri_state_filter.lookup_enum_name == ""
        assert tri_state_filter.name == ""
        assert tri_state_filter.pac_id == 0
        assert tri_state_filter.state_int_value == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        original_last_change_code = tri_state_filter.last_change_code
        stmt = select(TriStateFilter).where(TriStateFilter.tri_state_filter_id == tri_state_filter.tri_state_filter_id)
        result = await session.execute(stmt)
        tri_state_filter_1 = result.scalars().first()
        # tri_state_filter_1 = await session.query(TriStateFilter).filter_by(
        # tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        tri_state_filter_1.code = generate_uuid()
        await session.commit()
        stmt = select(TriStateFilter).where(TriStateFilter.tri_state_filter_id == tri_state_filter.tri_state_filter_id)
        result = await session.execute(stmt)
        tri_state_filter_2 = result.scalars().first()
        # tri_state_filter_2 = await session.query(TriStateFilter).filter_by(
        # tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        tri_state_filter_2.code = generate_uuid()
        await session.commit()
        assert tri_state_filter_2.last_change_code != original_last_change_code
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
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # stateIntValue,
# endset
