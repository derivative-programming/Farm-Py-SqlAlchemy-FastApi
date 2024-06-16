# models/factory/tests/organization_async_test.py
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
from models import Base, Organization
from models.factory import OrganizationFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
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
        assert isinstance(organization.code, uuid.UUID)
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
        organization.code = uuid.uuid4()
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
        organization.code = uuid.uuid4()
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
        organization.code = uuid.uuid4()
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
        organization.code = uuid.uuid4()
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
        organization.code = uuid.uuid4()
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
        assert isinstance(organization.code, uuid.UUID)
        assert isinstance(organization.last_change_code, int)
        assert isinstance(organization.insert_user_id, uuid.UUID)
        assert isinstance(organization.last_update_user_id, uuid.UUID)
        assert organization.name == "" or isinstance(organization.name, str)
        assert isinstance(organization.tac_id, int)
        # Check for the peek values
# endset
        # name,
        # tacID
        assert isinstance(organization.tac_code_peek, uuid.UUID)
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
    async def test_fields_default(self):
        """
        #TODO add comment
        """
        organization = Organization()
        assert organization.code is not None
        assert organization.last_change_code is not None
        assert organization.insert_user_id is not None
        assert organization.last_update_user_id is not None
        assert organization.insert_utc_date_time is not None
        assert organization.last_update_utc_date_time is not None
# endset
        # name,
        # TacID
        assert isinstance(organization.tac_code_peek, uuid.UUID)
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
        organization_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Organization).where(Organization.organization_id == organization.organization_id)
        result = await session.execute(stmt)
        organization_2 = result.scalars().first()
        # organization_2 = await session.query(Organization).filter_by(
        # organization_id=organization.organization_id).first()
        organization_2.code = uuid.uuid4()
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
