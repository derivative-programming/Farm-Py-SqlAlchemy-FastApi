# models/factory/tests/org_api_key_async_test.py
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
from models import Base, OrgApiKey
from models.factory import OrgApiKeyFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestOrgApiKeyFactoryAsync:
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
    async def test_org_api_key_creation(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert org_api_key.org_api_key_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert isinstance(org_api_key.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        #TODO add comment
        """
        org_api_key: OrgApiKey = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        #TODO add comment
        """
        org_api_key: OrgApiKey = await OrgApiKeyFactory.create_async(session=session)
        assert org_api_key.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        initial_code = org_api_key.last_change_code
        org_api_key.code = uuid.uuid4()
        await session.commit()
        assert org_api_key.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(org_api_key.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(org_api_key.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        org_api_key.code = uuid.uuid4()
        session.add(org_api_key)
        await session.commit()
        assert org_api_key.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(org_api_key.insert_utc_date_time, datetime)
        initial_time = org_api_key.insert_utc_date_time
        org_api_key.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert org_api_key.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        org_api_key.code = uuid.uuid4()
        session.add(org_api_key)
        await session.commit()
        assert org_api_key.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
        initial_time = org_api_key.last_update_utc_date_time
        org_api_key.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert org_api_key.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        await session.delete(org_api_key)
        await session.commit()
        # Construct the select statement
        stmt = select(OrgApiKey).where(
            OrgApiKey._org_api_key_id == org_api_key.org_api_key_id)  # pylint: disable=protected-access
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_org_api_key = result.scalars().first()
        # deleted_org_api_key = await session.query(OrgApiKey).filter_by(
        # org_api_key_id=org_api_key.org_api_key_id).first()
        assert deleted_org_api_key is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert isinstance(org_api_key.org_api_key_id, int)
        assert isinstance(org_api_key.code, uuid.UUID)
        assert isinstance(org_api_key.last_change_code, int)
        assert isinstance(org_api_key.insert_user_id, uuid.UUID)
        assert isinstance(org_api_key.last_update_user_id, uuid.UUID)
        assert org_api_key.api_key_value == "" or isinstance(org_api_key.api_key_value, str)
        assert org_api_key.created_by == "" or isinstance(org_api_key.created_by, str)
        assert isinstance(org_api_key.created_utc_date_time, datetime)
        assert isinstance(org_api_key.expiration_utc_date_time, datetime)
        assert isinstance(org_api_key.is_active, bool)
        assert isinstance(org_api_key.is_temp_user_key, bool)
        assert org_api_key.name == "" or isinstance(org_api_key.name, str)
        assert isinstance(org_api_key.organization_id, int)
        assert isinstance(org_api_key.org_customer_id, int)
        # Check for the peek values
# endset
        # apiKeyValue,
        # createdBy,
        # createdUTCDateTime
        # expirationUTCDateTime
        # isActive,
        # isTempUserKey,
        # name,
        # organizationID
        assert isinstance(org_api_key.organization_code_peek, uuid.UUID)
        # orgCustomerID
        assert isinstance(org_api_key.org_customer_code_peek, uuid.UUID)
# endset
        assert isinstance(org_api_key.insert_utc_date_time, datetime)
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        #TODO add comment
        """
        org_api_key_1 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key_2 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key_2.code = org_api_key_1.code
        session.add_all([org_api_key_1, org_api_key_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        #TODO add comment
        """
        org_api_key = OrgApiKey()
        assert org_api_key.code is not None
        assert org_api_key.last_change_code is not None
        assert org_api_key.insert_user_id is not None
        assert org_api_key.last_update_user_id is not None
        assert org_api_key.insert_utc_date_time is not None
        assert org_api_key.last_update_utc_date_time is not None
# endset
        # apiKeyValue,
        # createdBy,
        # createdUTCDateTime
        # expirationUTCDateTime
        # isActive,
        # isTempUserKey,
        # name,
        # OrganizationID
        assert isinstance(org_api_key.organization_code_peek, uuid.UUID)
        # OrgCustomerID
        assert isinstance(org_api_key.org_customer_code_peek, uuid.UUID)
# endset
        assert org_api_key.api_key_value == ""
        assert org_api_key.created_by == ""
        assert org_api_key.created_utc_date_time == datetime(1753, 1, 1)
        assert org_api_key.expiration_utc_date_time == datetime(1753, 1, 1)
        assert org_api_key.is_active is False
        assert org_api_key.is_temp_user_key is False
        assert org_api_key.name == ""
        assert org_api_key.organization_id == 0
        assert org_api_key.org_customer_id == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        original_last_change_code = org_api_key.last_change_code
        stmt = select(OrgApiKey).where(
            OrgApiKey._org_api_key_id == org_api_key.org_api_key_id)  # pylint: disable=protected-access
        result = await session.execute(stmt)
        org_api_key_1 = result.scalars().first()
        # org_api_key_1 = await session.query(OrgApiKey).filter_by(
        # org_api_key_id=org_api_key.org_api_key_id).first()
        org_api_key_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(OrgApiKey).where(
            OrgApiKey._org_api_key_id == org_api_key.org_api_key_id)  # pylint: disable=protected-access
        result = await session.execute(stmt)
        org_api_key_2 = result.scalars().first()
        # org_api_key_2 = await session.query(OrgApiKey).filter_by(
        # org_api_key_id=org_api_key.org_api_key_id).first()
        org_api_key_2.code = uuid.uuid4()
        await session.commit()
        assert org_api_key_2.last_change_code != original_last_change_code
# endset
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID
    @pytest.mark.asyncio
    async def test_invalid_organization_id(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        org_api_key.organization_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # OrgCustomerID
    @pytest.mark.asyncio
    async def test_invalid_org_customer_id(self, session):
        """
        #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        org_api_key.org_customer_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
# endset
