import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, OrgCustomer
from models.factory import OrgCustomerFactory
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
class TestOrgCustomerFactoryAsync:
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=True)
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
    async def test_org_customer_creation(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        assert org_customer.org_customer_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        if db_dialect == 'postgresql':
            assert isinstance(org_customer.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_customer.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.code, str)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        org_customer:OrgCustomer = await OrgCustomerFactory.build_async(session=session)
        assert org_customer.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        org_customer:OrgCustomer = await OrgCustomerFactory.create_async(session=session)
        assert org_customer.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        initial_code = org_customer.last_change_code
        org_customer.code = generate_uuid()
        await session.commit()
        assert org_customer.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        org_customer = await OrgCustomerFactory.build_async(session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(org_customer.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        org_customer = await OrgCustomerFactory.build_async(session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(org_customer.insert_utc_date_time, datetime)
        initial_time = org_customer.insert_utc_date_time
        org_customer.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert org_customer.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        assert org_customer.insert_utc_date_time is not None
        assert isinstance(org_customer.insert_utc_date_time, datetime)
        initial_time = org_customer.insert_utc_date_time
        org_customer.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert org_customer.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        org_customer = await OrgCustomerFactory.build_async(session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        org_customer = await OrgCustomerFactory.build_async(session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
        initial_time = org_customer.last_update_utc_date_time
        org_customer.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert org_customer.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        assert org_customer.last_update_utc_date_time is not None
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
        initial_time = org_customer.last_update_utc_date_time
        org_customer.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert org_customer.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        await session.delete(org_customer)
        await session.commit()
        # Construct the select statement
        stmt = select(OrgCustomer).where(OrgCustomer.org_customer_id==org_customer.org_customer_id)
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_org_customer = result.scalars().first()
        # deleted_org_customer = await session.query(OrgCustomer).filter_by(org_customer_id=org_customer.org_customer_id).first()
        assert deleted_org_customer is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        assert isinstance(org_customer.org_customer_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(org_customer.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_customer.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.code, str)
        assert isinstance(org_customer.last_change_code, int)
        if db_dialect == 'postgresql':
            assert isinstance(org_customer.insert_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_customer.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.insert_user_id, str)
        if db_dialect == 'postgresql':
            assert isinstance(org_customer.last_update_user_id, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_customer.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.last_update_user_id, str)
        assert isinstance(org_customer.customer_id, int)
        assert org_customer.email == "" or isinstance(org_customer.email, str)
        assert isinstance(org_customer.organization_id, int)
        # Check for the peek values, assuming they are UUIDs based on your model

        #customerID
        if db_dialect == 'postgresql':
            assert isinstance(org_customer.customer_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_customer.customer_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.customer_code_peek, str)
        #email,
        #organizationID
        if db_dialect == 'postgresql':
            assert isinstance(org_customer.organization_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_customer.organization_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.organization_code_peek, str)

        assert isinstance(org_customer.insert_utc_date_time, datetime)
        assert isinstance(org_customer.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        org_customer_1 = await OrgCustomerFactory.create_async(session=session)
        org_customer_2 = await OrgCustomerFactory.create_async(session=session)
        org_customer_2.code = org_customer_1.code
        session.add_all([org_customer_1, org_customer_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        org_customer = OrgCustomer()
        assert org_customer.code is not None
        assert org_customer.last_change_code is not None
        assert org_customer.insert_user_id is None
        assert org_customer.last_update_user_id is None
        assert org_customer.insert_utc_date_time is not None
        assert org_customer.last_update_utc_date_time is not None

        #CustomerID
        if db_dialect == 'postgresql':
            assert isinstance(org_customer.customer_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_customer.customer_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.customer_code_peek, str)
        #email,
        #OrganizationID
        if db_dialect == 'postgresql':
            assert isinstance(org_customer.organization_code_peek, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(org_customer.organization_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(org_customer.organization_code_peek, str)

        assert org_customer.customer_id == 0
        assert org_customer.email == ""
        assert org_customer.organization_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        original_last_change_code = org_customer.last_change_code
        stmt = select(OrgCustomer).where(OrgCustomer.org_customer_id==org_customer.org_customer_id)
        result = await session.execute(stmt)
        org_customer_1 = result.scalars().first()
        # org_customer_1 = await session.query(OrgCustomer).filter_by(org_customer_id=org_customer.org_customer_id).first()
        org_customer_1.code = generate_uuid()
        await session.commit()
        stmt = select(OrgCustomer).where(OrgCustomer.org_customer_id==org_customer.org_customer_id)
        result = await session.execute(stmt)
        org_customer_2 = result.scalars().first()
        # org_customer_2 = await session.query(OrgCustomer).filter_by(org_customer_id=org_customer.org_customer_id).first()
        org_customer_2.code = generate_uuid()
        await session.commit()
        assert org_customer_2.last_change_code != original_last_change_code

    #CustomerID
    @pytest.mark.asyncio
    async def test_invalid_customer_id(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        org_customer.customer_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    #email,
    #OrganizationID
    @pytest.mark.asyncio
    async def test_invalid_organization_id(self, session):
        org_customer = await OrgCustomerFactory.create_async(session=session)
        org_customer.organization_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

