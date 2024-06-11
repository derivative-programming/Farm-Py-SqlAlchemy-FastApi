import pytest
import pytest_asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
    AsyncConnection,
)
from models import Base
from models.factory import PacFactory
from models.pac import Pac
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect
from sqlalchemy import String, event, create_engine
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestPacFactoryAsync:

    async_engine = create_async_engine(
        DATABASE_URL, echo=False
    )

    # Synchronous engine for table creation
    sync_engine = create_engine(DATABASE_URL, echo=False)

    TestingAsyncSessionLocal = sessionmaker(
        async_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    )

    @pytest_asyncio.fixture(scope="function", autouse=True)
    async def setup_and_teardown_db(self):
        # Setup: Create tables
        async with self.async_engine.begin() as conn:
            await conn.run(Base.metadata.create_all(self.async_engine))

        # Setup: Create tables
        Base.metadata.create_all(bind=self.sync_engine)

        yield  # This will run the test

        # Teardown: Drop tables
        Base.metadata.drop_all(bind=self.sync_engine)

    @pytest_asyncio.fixture(scope="function")
    async def async_db_session(self):
        """The expectation with async_sessions is that the
        transactions be called on the connection object instead of the
        session object.
        Detailed explanation of async transactional tests
        <https://github.com/sqlalchemy/sqlalchemy/issues/5811>
        """

        connection = await self.async_engine.connect()

        trans = await connection.begin()
        async_session = self.TestingAsyncSessionLocal(bind=connection)
        nested = await connection.begin_nested()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            nonlocal nested

            if not nested.is_active:
                nested = connection.sync_connection.begin_nested()

        yield async_session

        await trans.rollback()
        await async_session.close()
        await connection.close()

    @pytest.mark.asyncio
    async def test_pac_creation(self,async_db_session: AsyncSession):
        await async_db_session.begin()
        async_db_session.add(Pac())
        pac = await PacFactory.create_async(session=async_db_session)
        assert pac.pac_id is not None
    # @pytest.mark.asyncio
    # async def test_code_default(self, session):
    #     pac = await PacFactory.create_async(session=session)
    #     if db_dialect == 'postgresql':
    #         assert isinstance(pac.code, UUID)
    #     elif db_dialect == 'mssql':
    #         assert isinstance(pac.code, UNIQUEIDENTIFIER)
    #     else:  # This will cover SQLite, MySQL, and other databases
    #         assert isinstance(pac.code, str)
    # @pytest.mark.asyncio
    # async def test_last_change_code_default_on_build(self, session):
    #     pac: Pac = await PacFactory.build_async(session=session)
    #     assert pac.last_change_code == 0
    # @pytest.mark.asyncio
    # async def test_last_change_code_default_on_creation(self, session):
    #     pac: Pac = await PacFactory.create_async(session=session)
    #     assert pac.last_change_code == 1
    # @pytest.mark.asyncio
    # async def test_last_change_code_default_on_update(self, session):
    #     pac = await PacFactory.create_async(session=session)
    #     initial_code = pac.last_change_code
    #     pac.code = generate_uuid()
    #     await session.commit()
    #     assert pac.last_change_code != initial_code
    # @pytest.mark.asyncio
    # async def test_date_inserted_on_build(self, session):
    #     pac = await PacFactory.build_async(session=session)
    #     assert pac.insert_utc_date_time is not None
    #     assert isinstance(pac.insert_utc_date_time, datetime)
    # @pytest.mark.asyncio
    # async def test_date_inserted_on_initial_save(self, session):
    #     pac = await PacFactory.build_async(session=session)
    #     assert pac.insert_utc_date_time is not None
    #     assert isinstance(pac.insert_utc_date_time, datetime)
    #     initial_time = pac.insert_utc_date_time
    #     pac.code = generate_uuid()
    #     time.sleep(1)
    #     await session.commit()
    #     assert pac.insert_utc_date_time > initial_time
    # @pytest.mark.asyncio
    # async def test_date_inserted_on_second_save(self, session):
    #     pac = await PacFactory.create_async(session=session)
    #     assert pac.insert_utc_date_time is not None
    #     assert isinstance(pac.insert_utc_date_time, datetime)
    #     initial_time = pac.insert_utc_date_time
    #     pac.code = generate_uuid()
    #     time.sleep(1)
    #     await session.commit()
    #     assert pac.insert_utc_date_time == initial_time
    # @pytest.mark.asyncio
    # async def test_date_updated_on_build(self, session):
    #     pac = await PacFactory.build_async(session=session)
    #     assert pac.last_update_utc_date_time is not None
    #     assert isinstance(pac.last_update_utc_date_time, datetime)
    # @pytest.mark.asyncio
    # async def test_date_updated_on_initial_save(self, session):
    #     pac = await PacFactory.build_async(session=session)
    #     assert pac.last_update_utc_date_time is not None
    #     assert isinstance(pac.last_update_utc_date_time, datetime)
    #     initial_time = pac.last_update_utc_date_time
    #     pac.code = generate_uuid()
    #     time.sleep(1)
    #     await session.commit()
    #     assert pac.last_update_utc_date_time > initial_time
    # @pytest.mark.asyncio
    # async def test_date_updated_on_second_save(self, session):
    #     pac = await PacFactory.create_async(session=session)
    #     assert pac.last_update_utc_date_time is not None
    #     assert isinstance(pac.last_update_utc_date_time, datetime)
    #     initial_time = pac.last_update_utc_date_time
    #     pac.code = generate_uuid()
    #     time.sleep(1)
    #     await session.commit()
    #     assert pac.last_update_utc_date_time > initial_time
    # @pytest.mark.asyncio
    # async def test_model_deletion(self, session):
    #     pac = await PacFactory.create_async(session=session)
    #     await session.delete(pac)
    #     await session.commit()
    #     deleted_pac = await session.query(Pac).filter_by(pac_id=pac.pac_id).first()
    #     assert deleted_pac is None
    # @pytest.mark.asyncio
    # async def test_data_types(self, session):
    #     pac = await PacFactory.create_async(session=session)
    #     assert isinstance(pac.pac_id, int)
    #     if db_dialect == 'postgresql':
    #         assert isinstance(pac.code, UUID)
    #     elif db_dialect == 'mssql':
    #         assert isinstance(pac.code, UNIQUEIDENTIFIER)
    #     else:  # This will cover SQLite, MySQL, and other databases
    #         assert isinstance(pac.code, str)
    #     assert isinstance(pac.last_change_code, int)
    #     if db_dialect == 'postgresql':
    #         assert isinstance(pac.insert_user_id, UUID)
    #     elif db_dialect == 'mssql':
    #         assert isinstance(pac.insert_user_id, UNIQUEIDENTIFIER)
    #     else:  # This will cover SQLite, MySQL, and other databases
    #         assert isinstance(pac.insert_user_id, str)
    #     if db_dialect == 'postgresql':
    #         assert isinstance(pac.last_update_user_id, UUID)
    #     elif db_dialect == 'mssql':
    #         assert isinstance(pac.last_update_user_id, UNIQUEIDENTIFIER)
    #     else:  # This will cover SQLite, MySQL, and other databases
    #         assert isinstance(pac.last_update_user_id, str)
    #     assert pac.description == "" or isinstance(pac.description, str)
    #     assert isinstance(pac.display_order, int)
    #     assert isinstance(pac.is_active, bool)
    #     assert pac.lookup_enum_name == "" or isinstance(pac.lookup_enum_name, str)
    #     assert pac.name == "" or isinstance(pac.name, str)
    #     # Check for the peek values, assuming they are UUIDs based on your model

    #     #description,
    #     #displayOrder,
    #     # isActive,
    #     #lookupEnumName,
    #     #name,

    #     assert isinstance(pac.insert_utc_date_time, datetime)
    #     assert isinstance(pac.last_update_utc_date_time, datetime)
    # @pytest.mark.asyncio
    # async def test_unique_code_constraint(self, session):
    #     pac_1 = await PacFactory.create_async(session=session)
    #     pac_2 = await PacFactory.create_async(session=session)
    #     pac_2.code = pac_1.code
    #     await session.add_all([pac_1, pac_2])
    #     with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
    #         await session.commit()
    # @pytest.mark.asyncio
    # async def test_fields_default(self, session):
    #     pac = Pac()
    #     assert pac.code is not None
    #     assert pac.last_change_code is not None
    #     assert pac.insert_user_id is None
    #     assert pac.last_update_user_id is None
    #     assert pac.insert_utc_date_time is not None
    #     assert pac.last_update_utc_date_time is not None

    #     #description,
    #     #displayOrder,
    #     # isActive,
    #     #lookupEnumName,
    #     #name,

    #     assert pac.description == ""
    #     assert pac.display_order == 0
    #     assert pac.is_active is False
    #     assert pac.lookup_enum_name == ""
    #     assert pac.name == ""

    # @pytest.mark.asyncio
    # async def test_last_change_code_concurrency(self, session):
    #     pac = await PacFactory.create_async(session=session)
    #     original_last_change_code = pac.last_change_code
    #     pac_1 = await session.query(Pac).filter_by(pac_id=pac.pac_id).first()
    #     pac_1.code = generate_uuid()
    #     await session.commit()
    #     pac_2 = await session.query(Pac).filter_by(pac_id=pac.pac_id).first()
    #     pac_2.code = generate_uuid()
    #     await session.commit()
    #     assert pac_2.last_change_code != original_last_change_code

    # #description,
    # #displayOrder,
    # # isActive,
    # #lookupEnumName,
    # #name,

