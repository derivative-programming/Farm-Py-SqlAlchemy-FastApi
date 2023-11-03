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
from models import Base, Organization
from models.factory import OrganizationFactory
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
class TestOrganizationFactoryAsync:
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
    async def test_organization_creation(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        assert organization.organization_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(organization.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        organization:Organization = await OrganizationFactory.build_async(session=session)
        assert organization.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        organization:Organization = await OrganizationFactory.create_async(session=session)
        assert organization.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        initial_code = organization.last_change_code
        organization.code = generate_uuid()
        await session.commit()
        assert organization.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        organization = await OrganizationFactory.build_async(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        organization = await OrganizationFactory.build_async(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
        initial_time = organization.insert_utc_date_time
        organization.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert organization.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(organization.insert_utc_date_time, datetime)
        initial_time = organization.insert_utc_date_time
        organization.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert organization.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        organization = await OrganizationFactory.build_async(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        organization = await OrganizationFactory.build_async(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
        initial_time = organization.last_update_utc_date_time
        organization.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert organization.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(organization.last_update_utc_date_time, datetime)
        initial_time = organization.last_update_utc_date_time
        organization.code = generate_uuid()
        time.sleep(2)
        await session.commit()
        assert organization.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        await session.delete(organization)
        await session.commit()
        # Construct the select statement
        stmt = select(Organization).where(Organization.organization_id==organization.organization_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_organization = result.scalars().first()
        # deleted_organization = await session.query(Organization).filter_by(organization_id=organization.organization_id).first()
        assert deleted_organization is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        assert isinstance(organization.organization_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(organization.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.code, str)
        assert isinstance(organization.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(organization.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(organization.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.last_update_user_id, str)
        assert organization.name == "" or isinstance(organization.name, str)
        assert isinstance(organization.tac_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #name,
        #tacID
        if db_dialect == 'postgresql':
            assert isinstance(organization.tac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.tac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.tac_code_peek, str)

        assert isinstance(organization.insert_utc_date_time, datetime)
        assert isinstance(organization.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        organization_1 = await OrganizationFactory.create_async(session=session)
        organization_2 = await OrganizationFactory.create_async(session=session)
        organization_2.code = organization_1.code
        session.add_all([organization_1, organization_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        organization = Organization()
        assert organization.code is not None
        assert organization.last_change_code is not None
        assert organization.insert_user_id is None
        assert organization.last_update_user_id is None
        assert organization.insert_utc_date_time is not None
        assert organization.last_update_utc_date_time is not None

        #name,
        #TacID
        if db_dialect == 'postgresql':
            assert isinstance(organization.tac_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(organization.tac_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(organization.tac_code_peek, str)

        assert organization.name == ""
        assert organization.tac_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        original_last_change_code = organization.last_change_code
        stmt = select(Organization).where(Organization.organization_id==organization.organization_id)
        result = await session.execute(stmt)
        organization_1 = result.scalars().first()
        # organization_1 = await session.query(Organization).filter_by(organization_id=organization.organization_id).first()
        organization_1.code = generate_uuid()
        await session.commit()
        stmt = select(Organization).where(Organization.organization_id==organization.organization_id)
        result = await session.execute(stmt)
        organization_2 = result.scalars().first()
        # organization_2 = await session.query(Organization).filter_by(organization_id=organization.organization_id).first()
        organization_2.code = generate_uuid()
        await session.commit()
        assert organization_2.last_change_code != original_last_change_code

    #name,
    #TacID
    @pytest.mark.asyncio
    async def test_invalid_tac_id(self, session):
        organization = await OrganizationFactory.create_async(session=session)
        organization.tac_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

