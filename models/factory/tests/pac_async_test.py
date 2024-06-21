# models/factory/tests/pac_async_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the asynchronous
operations of the PacFactory class.
"""
import asyncio
import math
import time
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from models import Base, Pac
from models.factory import PacFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestPacFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the PacFactory class.
    """
    @pytest.fixture(scope="function")
    def event_loop(self) -> Generator[asyncio.AbstractEventLoop, None, None]:
        """
        Fixture that returns an asyncio event loop for the test functions.
        """
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        """
        Fixture that returns an async engine for the test functions.
        """
        engine = create_async_engine(DATABASE_URL, echo=False)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self, engine) -> AsyncGenerator[AsyncSession, None]:
        """
        Fixture that returns an async session for the test functions.
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
            TestingSessionLocal = sessionmaker(  # pylint: disable=invalid-name
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with TestingSessionLocal(bind=connection) as session:  # type: ignore # noqa: E501
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
    async def test_pac_creation(self, session):
        """
        Test case for creating a pac
        asynchronously.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the pac ID
                is None after creation.
        """
        pac = await PacFactory.create_async(
            session=session)
        assert pac.pac_id is not None
    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the code attribute is not
                an instance of uuid.UUID.
        """
        pac = await PacFactory.create_async(
            session=session)
        assert isinstance(pac.code, uuid.UUID)
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute when using the build_async method.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not 0.
        """
        pac: Pac = await PacFactory.build_async(
            session=session)
        assert pac.last_change_code == 0
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute when using the create_async method.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not 1.
        """
        pac: Pac = await PacFactory.create_async(
            session=session)
        assert pac.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the pac.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        pac = await PacFactory.create_async(
            session=session)
        initial_code = pac.last_change_code
        pac.code = uuid.uuid4()
        await session.commit()
        assert pac.last_change_code != initial_code
    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the insert_utc_date_time
        attribute when using the build_async method.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the insert_utc_date_time attribute
            is None or not an instance of datetime.
        """
        pac = await PacFactory.build_async(
            session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(
            pac.insert_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute after the initial save.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the insert_utc_date_time
            attribute is None or not an instance of datetime.
        """
        pac = await PacFactory.build_async(
            session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(
            pac.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        pac.code = uuid.uuid4()
        session.add(pac)
        await session.commit()
        assert pac.insert_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute after the second save.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the insert_utc_date_time
            attribute is not the same as the initial time.
        """
        pac = await PacFactory.create_async(
            session=session)
        assert pac.insert_utc_date_time is not None
        assert isinstance(
            pac.insert_utc_date_time, datetime)
        initial_time = pac.insert_utc_date_time
        pac.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert pac.insert_utc_date_time == initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute when using
        the build_async method.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is None or not an instance of datetime.
        """
        pac = await PacFactory.build_async(
            session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(
            pac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute after the initial save.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is None or not an instance of datetime.
        """
        pac = await PacFactory.build_async(
            session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(
            pac.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        pac.code = uuid.uuid4()
        session.add(pac)
        await session.commit()
        assert pac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute after the second save.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is not greater than the initial time.
        """
        pac = await PacFactory.create_async(
            session=session)
        assert pac.last_update_utc_date_time is not None
        assert isinstance(
            pac.last_update_utc_date_time, datetime)
        initial_time = pac.last_update_utc_date_time
        pac.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert pac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a pac
        from the database.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the deleted
            pac is still
            found in the database.
        """
        pac = await PacFactory.create_async(
            session=session)
        await session.delete(pac)
        await session.commit()
        # Construct the select statement
        stmt = select(Pac).where(
            Pac._pac_id == pac.pac_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_pac = result.scalars().first()
        assert deleted_pac is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the pac attributes.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        pac = await PacFactory.create_async(
            session=session)
        assert isinstance(pac.pac_id, int)
        assert isinstance(pac.code, uuid.UUID)
        assert isinstance(pac.last_change_code, int)
        assert isinstance(pac.insert_user_id, uuid.UUID)
        assert isinstance(pac.last_update_user_id, uuid.UUID)
        assert pac.description == "" or isinstance(pac.description, str)
        assert isinstance(pac.display_order, int)
        assert isinstance(pac.is_active, bool)
        assert pac.lookup_enum_name == "" or isinstance(pac.lookup_enum_name, str)
        assert pac.name == "" or isinstance(pac.name, str)
        # Check for the peek values
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
# endset
        assert isinstance(pac.insert_utc_date_time, datetime)
        assert isinstance(pac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint for pacs.
        This test creates two pac
        instances using
        the PacFactoryand assigns
        the same code to both pacs.
        Then it adds both pacs to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.
        Note: This test assumes that the
        PacFactory.create_async() method creates unique codes for each pac.
        """
        pac_1 = await PacFactory.create_async(
            session=session)
        pac_2 = await PacFactory.create_async(
            session=session)
        pac_2.code = pac_1.code
        session.add_all([pac_1, pac_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the Pac model.
        This test case checks that the default values
        of various fields in the Pac
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """
        pac = Pac()
        assert pac.code is not None
        assert pac.last_change_code is not None
        assert pac.insert_user_id is not None
        assert pac.last_update_user_id is not None
        assert pac.insert_utc_date_time is not None
        assert pac.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
# endset
        assert pac.description == ""
        assert pac.display_order == 0
        assert pac.is_active is False
        assert pac.lookup_enum_name == ""
        assert pac.name == ""
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the Pac model.
        This test verifies that the last_change_code
        attribute of a Pac object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.
        Steps:
        1. Create a new Pac object using
            the PacFactory.
        2. Get the original value of the last_change_code attribute.
        3. Query the database for the Pac
            object using the pac_id.
        4. Modify the code attribute of the
            retrieved Pac object.
        5. Commit the changes to the database.
        6. Query the database again for the
            Pac object using the pac_id.
        7. Get the modified Pac object.
        8. Verify that the last_change_code attribute
            of the modified Pac object
            is different from the original value.
        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified Pac
                            object is the same as the original value.
        """
        pac = await PacFactory.create_async(
            session=session)
        original_last_change_code = pac.last_change_code
        stmt = select(Pac).where(
            Pac._pac_id == pac.pac_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        pac_1 = result.scalars().first()
        # pac_1 = await session.query(Pac).filter_by(
        # pac_id=pac.pac_id).first()
        pac_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Pac).where(
            Pac._pac_id == pac.pac_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        pac_2 = result.scalars().first()
        # pac_2 = await session.query(Pac).filter_by(
        # pac_id=pac.pac_id).first()
        pac_2.code = uuid.uuid4()
        await session.commit()
        assert pac_2.last_change_code != original_last_change_code
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
# endset
