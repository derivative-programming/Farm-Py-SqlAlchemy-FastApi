# models/factory/tests/tri_state_filter_async_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the asynchronous
operations of the TriStateFilterFactory class.
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
from models import Base, TriStateFilter
from models.factory import TriStateFilterFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestTriStateFilterFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the TriStateFilterFactory class.
    """
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
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
    async def test_tri_state_filter_creation(self, session):
        """
        Test case for creating a tri_state_filter asynchronously.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the tri_state_filter ID is None after creation.
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert tri_state_filter.tri_state_filter_id is not None
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
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert isinstance(tri_state_filter.code, uuid.UUID)
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
        tri_state_filter: TriStateFilter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.last_change_code == 0
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
        tri_state_filter: TriStateFilter = await TriStateFilterFactory.create_async(session=session)
        assert tri_state_filter.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the tri_state_filter.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        initial_code = tri_state_filter.last_change_code
        tri_state_filter.code = uuid.uuid4()
        await session.commit()
        assert tri_state_filter.last_change_code != initial_code
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
        tri_state_filter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
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
        tri_state_filter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tri_state_filter.code = uuid.uuid4()
        session.add(tri_state_filter)
        await session.commit()
        assert tri_state_filter.insert_utc_date_time > initial_time
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
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert tri_state_filter.insert_utc_date_time is not None
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        initial_time = tri_state_filter.insert_utc_date_time
        tri_state_filter.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert tri_state_filter.insert_utc_date_time == initial_time
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
        tri_state_filter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
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
        tri_state_filter = await TriStateFilterFactory.build_async(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tri_state_filter.code = uuid.uuid4()
        session.add(tri_state_filter)
        await session.commit()
        assert tri_state_filter.last_update_utc_date_time > initial_time
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
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert tri_state_filter.last_update_utc_date_time is not None
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
        initial_time = tri_state_filter.last_update_utc_date_time
        tri_state_filter.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert tri_state_filter.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a tri_state_filter from the database.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the deleted tri_state_filter is still
            found in the database.
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        await session.delete(tri_state_filter)
        await session.commit()
        # Construct the select statement
        stmt = select(TriStateFilter).where(
            TriStateFilter._tri_state_filter_id == tri_state_filter.tri_state_filter_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_tri_state_filter = result.scalars().first()
        assert deleted_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of the tri_state_filter attributes.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        assert isinstance(tri_state_filter.tri_state_filter_id, int)
        assert isinstance(tri_state_filter.code, uuid.UUID)
        assert isinstance(tri_state_filter.last_change_code, int)
        assert isinstance(tri_state_filter.insert_user_id, uuid.UUID)
        assert isinstance(tri_state_filter.last_update_user_id, uuid.UUID)
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
        assert isinstance(tri_state_filter.pac_code_peek, uuid.UUID)
        # stateIntValue,
# endset
        assert isinstance(tri_state_filter.insert_utc_date_time, datetime)
        assert isinstance(tri_state_filter.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint for tri_state_filters.
        This test creates two tri_state_filter instances using
        the TriStateFilterFactoryand assigns the same code to both tri_state_filters.
        Then it adds both tri_state_filters to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.
        Note: This test assumes that the
        TriStateFilterFactory.create_async() method creates unique codes for each tri_state_filter.
        """
        tri_state_filter_1 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter_2 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter_2.code = tri_state_filter_1.code
        session.add_all([tri_state_filter_1, tri_state_filter_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the TriStateFilter model.
        This test case checks that the default values
        of various fields in the TriStateFilter model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """
        tri_state_filter = TriStateFilter()
        assert tri_state_filter.code is not None
        assert tri_state_filter.last_change_code is not None
        assert tri_state_filter.insert_user_id is not None
        assert tri_state_filter.last_update_user_id is not None
        assert tri_state_filter.insert_utc_date_time is not None
        assert tri_state_filter.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(tri_state_filter.pac_code_peek, uuid.UUID)
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
        Test the concurrency of last_change_code in the TriStateFilter model.
        This test verifies that the last_change_code
        attribute of a TriStateFilter object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.
        Steps:
        1. Create a new TriStateFilter object using the TriStateFilterFactory.
        2. Get the original value of the last_change_code attribute.
        3. Query the database for the TriStateFilter object using the tri_state_filter_id.
        4. Modify the code attribute of the retrieved TriStateFilter object.
        5. Commit the changes to the database.
        6. Query the database again for the TriStateFilter object using the tri_state_filter_id.
        7. Get the modified TriStateFilter object.
        8. Verify that the last_change_code attribute
            of the modified TriStateFilter object
            is different from the original value.
        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified TriStateFilter
                            object is the same as the original value.
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        original_last_change_code = tri_state_filter.last_change_code
        stmt = select(TriStateFilter).where(
            TriStateFilter._tri_state_filter_id == tri_state_filter.tri_state_filter_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        tri_state_filter_1 = result.scalars().first()
        # tri_state_filter_1 = await session.query(TriStateFilter).filter_by(
        # tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        tri_state_filter_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(TriStateFilter).where(
            TriStateFilter._tri_state_filter_id == tri_state_filter.tri_state_filter_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        tri_state_filter_2 = result.scalars().first()
        # tri_state_filter_2 = await session.query(TriStateFilter).filter_by(
        # tri_state_filter_id=tri_state_filter.tri_state_filter_id).first()
        tri_state_filter_2.code = uuid.uuid4()
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
        Test case for handling an invalid pac ID.
        This test case creates a tri_state_filter using the
        TriStateFilterFactory and sets an invalid pac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.
        Args:
            session: The SQLAlchemy session object.
        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # stateIntValue,
# endset
