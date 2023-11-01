import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, Role
from models.factory import RoleFactory
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
class TestRoleFactoryAsync:
    @pytest.fixture(scope="session")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="session")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=True)
        yield engine
        engine.sync_engine.dispose()
    # @pytest_asyncio.fixture(scope="session")
    # async def prepare_db(self):
    #     create_db_engine = create_async_engine(
    #         DATABASE_URL,
    #         isolation_level="AUTOCOMMIT",
    #     )
    #     async with create_db_engine.begin() as connection:
    #         await connection.execute(
    #             text(
    #                 "drop database if exists {name};".format(
    #                     name="test_db"
    #                 )
    #             ),
    #         )
    #         await connection.execute(
    #             text("create database {name};".format(name="test_db")),
    #         )
    @pytest_asyncio.fixture(scope="session")
    async def session(self,engine) -> AsyncSession:
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
    async def test_role_creation(self, session):
        role = await RoleFactory.create_async(session=session)
        assert role.role_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        role = await RoleFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(role.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        role:Role = await RoleFactory.build_async(session=session)
        assert role.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        role:Role = await RoleFactory.create_async(session=session)
        assert role.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        role = await RoleFactory.create_async(session=session)
        initial_code = role.last_change_code
        role.code = generate_uuid()
        await session.commit()
        assert role.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        role = await RoleFactory.build_async(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        role = await RoleFactory.build_async(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
        initial_time = role.insert_utc_date_time
        role.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert role.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        role = await RoleFactory.create_async(session=session)
        assert role.insert_utc_date_time is not None
        assert isinstance(role.insert_utc_date_time, datetime)
        initial_time = role.insert_utc_date_time
        role.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert role.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        role = await RoleFactory.build_async(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        role = await RoleFactory.build_async(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
        initial_time = role.last_update_utc_date_time
        role.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert role.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        role = await RoleFactory.create_async(session=session)
        assert role.last_update_utc_date_time is not None
        assert isinstance(role.last_update_utc_date_time, datetime)
        initial_time = role.last_update_utc_date_time
        role.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert role.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        role = await RoleFactory.create_async(session=session)
        await session.delete(role)
        await session.commit()
        # Construct the select statement
        stmt = select(Role).where(Role.role_id==role.role_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_role = result.scalars().first()
        # deleted_role = await session.query(Role).filter_by(role_id=role.role_id).first()
        assert deleted_role is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        role = await RoleFactory.create_async(session=session)
        assert isinstance(role.role_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(role.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.code, str)
        assert isinstance(role.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(role.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(role.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.last_update_user_id, str)
        assert role.description == "" or isinstance(role.description, str)
        assert isinstance(role.display_order, int)
        assert isinstance(role.is_active, bool)
        assert role.lookup_enum_name == "" or isinstance(role.lookup_enum_name, str)
        assert role.name == "" or isinstance(role.name, str)
        assert isinstance(role.pac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #pacID
        if db_dialect == 'postgresql':
            assert isinstance(role.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.pac_code_peek, str)

        assert isinstance(role.insert_utc_date_time, datetime)
        assert isinstance(role.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        role_1 = await RoleFactory.create_async(session=session)
        role_2 = await RoleFactory.create_async(session=session)
        role_2.code = role_1.code
        session.add_all([role_1, role_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        role = Role()
        assert role.code is not None
        assert role.last_change_code is not None
        assert role.insert_user_id is None
        assert role.last_update_user_id is None
        assert role.insert_utc_date_time is not None
        assert role.last_update_utc_date_time is not None

        #description,
        #displayOrder,
        #isActive,
        #lookupEnumName,
        #name,
        #PacID
        if db_dialect == 'postgresql':
            assert isinstance(role.pac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(role.pac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(role.pac_code_peek, str)

        assert role.description == ""
        assert role.display_order == 0
        assert role.is_active == False
        assert role.lookup_enum_name == ""
        assert role.name == ""
        assert role.pac_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        role = await RoleFactory.create_async(session=session)
        original_last_change_code = role.last_change_code
        stmt = select(Role).where(Role.role_id==role.role_id)
        result = await session.execute(stmt)
        role_1 = result.scalars().first()
        # role_1 = await session.query(Role).filter_by(role_id=role.role_id).first()
        role_1.code = generate_uuid()
        await session.commit()
        stmt = select(Role).where(Role.role_id==role.role_id)
        result = await session.execute(stmt)
        role_2 = result.scalars().first()
        # role_2 = await session.query(Role).filter_by(role_id=role.role_id).first()
        role_2.code = generate_uuid()
        await session.commit()
        assert role_2.last_change_code != original_last_change_code

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @pytest.mark.asyncio
    async def test_invalid_pac_id(self, session):
        role = await RoleFactory.create_async(session=session)
        role.pac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

