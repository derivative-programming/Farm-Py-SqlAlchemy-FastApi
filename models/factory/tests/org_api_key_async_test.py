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
from models import Base, OrgApiKey
from models.factory import OrgApiKeyFactory
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
class TestOrgApiKeyFactoryAsync:
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
    async def test_org_api_key_creation(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert org_api_key.org_api_key_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        org_api_key:OrgApiKey = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        org_api_key:OrgApiKey = await OrgApiKeyFactory.create_async(session=session)
        assert org_api_key.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        initial_code = org_api_key.last_change_code
        org_api_key.code = generate_uuid()
        await session.commit()
        assert org_api_key.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        org_api_key = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(org_api_key.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        org_api_key = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(org_api_key.insert_utc_date_time, datetime)
        initial_time = org_api_key.insert_utc_date_time
        org_api_key.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert org_api_key.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert org_api_key.insert_utc_date_time is not None
        assert isinstance(org_api_key.insert_utc_date_time, datetime)
        initial_time = org_api_key.insert_utc_date_time
        org_api_key.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert org_api_key.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        org_api_key = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        org_api_key = await OrgApiKeyFactory.build_async(session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
        initial_time = org_api_key.last_update_utc_date_time
        org_api_key.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert org_api_key.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert org_api_key.last_update_utc_date_time is not None
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
        initial_time = org_api_key.last_update_utc_date_time
        org_api_key.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert org_api_key.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        await session.delete(org_api_key)
        await session.commit()
        # Construct the select statement
        stmt = select(OrgApiKey).where(OrgApiKey.org_api_key_id==org_api_key.org_api_key_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_org_api_key = result.scalars().first()
        # deleted_org_api_key = await session.query(OrgApiKey).filter_by(org_api_key_id=org_api_key.org_api_key_id).first()
        assert deleted_org_api_key is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        assert isinstance(org_api_key.org_api_key_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key.code, str)
        assert isinstance(org_api_key.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key.last_update_user_id, str)
        assert org_api_key.api_key_value == "" or isinstance(org_api_key.api_key_value, str)
        assert org_api_key.created_by == "" or isinstance(org_api_key.created_by, str)
        assert isinstance(org_api_key.created_utc_date_time, datetime)
        assert isinstance(org_api_key.expiration_utc_date_time, datetime)
        assert isinstance(org_api_key.is_active, bool)
        assert isinstance(org_api_key.is_temp_user_key, bool)
        assert org_api_key.name == "" or isinstance(org_api_key.name, str)
        assert isinstance(org_api_key.organization_id, int)
        assert isinstance(org_api_key.org_customer_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #apiKeyValue,
        #createdBy,
        #createdUTCDateTime
        #expirationUTCDateTime
        #isActive,
        #isTempUserKey,
        #name,
        #organizationID
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key.organization_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key.organization_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key.organization_code_peek, str)
        #orgCustomerID
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key.org_customer_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key.org_customer_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key.org_customer_code_peek, str)

        assert isinstance(org_api_key.insert_utc_date_time, datetime)
        assert isinstance(org_api_key.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        org_api_key_1 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key_2 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key_2.code = org_api_key_1.code
        session.add_all([org_api_key_1, org_api_key_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        org_api_key = OrgApiKey()
        assert org_api_key.code is not None
        assert org_api_key.last_change_code is not None
        assert org_api_key.insert_user_id is None
        assert org_api_key.last_update_user_id is None
        assert org_api_key.insert_utc_date_time is not None
        assert org_api_key.last_update_utc_date_time is not None

        #apiKeyValue,
        #createdBy,
        #createdUTCDateTime
        #expirationUTCDateTime
        #isActive,
        #isTempUserKey,
        #name,
        #OrganizationID
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key.organization_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key.organization_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key.organization_code_peek, str)
        #OrgCustomerID
        if db_dialect == 'postgresql':
            assert isinstance(org_api_key.org_customer_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_api_key.org_customer_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_api_key.org_customer_code_peek, str)

        assert org_api_key.api_key_value == ""
        assert org_api_key.created_by == ""
        assert org_api_key.created_utc_date_time == datetime(1753, 1, 1)
        assert org_api_key.expiration_utc_date_time == datetime(1753, 1, 1)
        assert org_api_key.is_active == False
        assert org_api_key.is_temp_user_key == False
        assert org_api_key.name == ""
        assert org_api_key.organization_id == 0
        assert org_api_key.org_customer_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        original_last_change_code = org_api_key.last_change_code
        stmt = select(OrgApiKey).where(OrgApiKey.org_api_key_id==org_api_key.org_api_key_id)
        result = await session.execute(stmt)
        org_api_key_1 = result.scalars().first()
        # org_api_key_1 = await session.query(OrgApiKey).filter_by(org_api_key_id=org_api_key.org_api_key_id).first()
        org_api_key_1.code = generate_uuid()
        await session.commit()
        stmt = select(OrgApiKey).where(OrgApiKey.org_api_key_id==org_api_key.org_api_key_id)
        result = await session.execute(stmt)
        org_api_key_2 = result.scalars().first()
        # org_api_key_2 = await session.query(OrgApiKey).filter_by(org_api_key_id=org_api_key.org_api_key_id).first()
        org_api_key_2.code = generate_uuid()
        await session.commit()
        assert org_api_key_2.last_change_code != original_last_change_code

    #apiKeyValue,
    #createdBy,
    #createdUTCDateTime
    #expirationUTCDateTime
    #isActive,
    #isTempUserKey,
    #name,
    #OrganizationID
    @pytest.mark.asyncio
    async def test_invalid_organization_id(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        org_api_key.organization_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    #OrgCustomerID
    @pytest.mark.asyncio
    async def test_invalid_org_customer_id(self, session):
        org_api_key = await OrgApiKeyFactory.create_async(session=session)
        org_api_key.org_customer_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

