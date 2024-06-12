# models/factory/tests/organization_async_test.py
"""
    #TODO add comment
"""
import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
import math
from typing import AsyncGenerator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from datetime import datetime, date, timedelta
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, Organization
from models.factory import OrganizationFactory
from services.db_config import DB_DIALECT, generate_uuid
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
DB_DIALECT = "sqlite"
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestOrganizationFactoryAsync:
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
    async def test_organization_creation(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        assert organization.organization_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        if DB_DIALECT == 'postgresql':
            assert isinstance(organization.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(organization.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        organization: Organization = await OrganizationFactory.build_async(session=session)
        assert organization.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        organization: Organization = await OrganizationFactory.create_async(session=session)
        assert organization.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        initial_code = organization.last_change_code
        organization.code = generate_uuid()
        await session.commit()
        assert organization.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.build_async(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.build_async(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        organization.code = generate_uuid()
        await session.commit()
        assert organization.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
        initial_time = organization.insert_utc_date_time
        organization.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert organization.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.build_async(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.build_async(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        organization.code = generate_uuid()
        await session.commit()
        assert organization.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
        initial_time = organization.last_update_utc_date_time
        organization.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert organization.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        await session.delete(organization)
        await session.commit()
        # Construct the select statement
        stmt = select(Organization).where(Organization.organization_id == organization.organization_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_organization = result.scalars().first()
        # deleted_organization = await session.query(Organization).filter_by(
        # organization_id=organization.organization_id).first()
        assert deleted_organization is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        assert isinstance(organization.organization_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(organization.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(organization.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.code, str)
        assert isinstance(organization.last_change_code, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(organization.insert_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(organization.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.insert_user_id, str)
        if DB_DIALECT == 'postgresql':
            assert isinstance(organization.last_update_user_id, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(organization.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.last_update_user_id, str)
        assert organization.name == "" or isinstance(organization.name, str)
        assert isinstance(organization.tac_id, int)
        # Check for the peek values
# endset
        # name,
        # tacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(organization.tac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(organization.tac_code_peek,
                              UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.tac_code_peek, str)
# endset
        assert isinstance(organization.insert_utc_date_time, datetime)
        assert isinstance(organization.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        organization_1 = await OrganizationFactory.create_async(session=session)
        organization_2 = await OrganizationFactory.create_async(session=session)
        organization_2.code = organization_1.code
        session.add_all([organization_1, organization_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        """
        #TODO add comment
        """
        organization = Organization()
        assert organization.code is not None
        assert organization.last_change_code is not None
        assert organization.insert_user_id is None
        assert organization.last_update_user_id is None
        assert organization.insert_utc_date_time is not None
        assert organization.last_update_utc_date_time is not None
# endset
        # name,
        # TacID
        if DB_DIALECT == 'postgresql':
            assert isinstance(organization.tac_code_peek, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(organization.tac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.tac_code_peek, str)
# endset
        assert organization.name == ""
        assert organization.tac_id == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        original_last_change_code = organization.last_change_code
        stmt = select(Organization).where(Organization.organization_id == organization.organization_id)
        result = await session.execute(stmt)
        organization_1 = result.scalars().first()
        # organization_1 = await session.query(Organization).filter_by(
        # organization_id=organization.organization_id).first()
        organization_1.code = generate_uuid()
        await session.commit()
        stmt = select(Organization).where(Organization.organization_id == organization.organization_id)
        result = await session.execute(stmt)
        organization_2 = result.scalars().first()
        # organization_2 = await session.query(Organization).filter_by(
        # organization_id=organization.organization_id).first()
        organization_2.code = generate_uuid()
        await session.commit()
        assert organization_2.last_change_code != original_last_change_code
# endset
    # name,
    # TacID
    @pytest.mark.asyncio
    async def test_invalid_tac_id(self, session):
        """
        #TODO add comment
        """
        organization = await OrganizationFactory.create_async(session=session)
        organization.tac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
# endset
