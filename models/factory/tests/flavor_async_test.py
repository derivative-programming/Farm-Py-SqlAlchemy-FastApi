# models/factory/tests/flavor_async_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the asynchronous
operations of the FlavorFactory class.
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
from models import Base, Flavor
from models.factory import FlavorFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestFlavorFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the FlavorFactory class.
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
    async def test_flavor_creation(self, session):
        """
        Test case for creating a flavor asynchronously.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the flavor ID is None after creation.
        """
        flavor = await FlavorFactory.create_async(session=session)
        assert flavor.flavor_id is not None
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
        flavor = await FlavorFactory.create_async(session=session)
        assert isinstance(flavor.code, uuid.UUID)
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
        flavor: Flavor = await FlavorFactory.build_async(session=session)
        assert flavor.last_change_code == 0
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
        flavor: Flavor = await FlavorFactory.create_async(session=session)
        assert flavor.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the flavor.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        flavor = await FlavorFactory.create_async(session=session)
        initial_code = flavor.last_change_code
        flavor.code = uuid.uuid4()
        await session.commit()
        assert flavor.last_change_code != initial_code
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
        flavor = await FlavorFactory.build_async(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
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
        flavor = await FlavorFactory.build_async(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        flavor.code = uuid.uuid4()
        session.add(flavor)
        await session.commit()
        assert flavor.insert_utc_date_time > initial_time
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
        flavor = await FlavorFactory.create_async(session=session)
        assert flavor.insert_utc_date_time is not None
        assert isinstance(flavor.insert_utc_date_time, datetime)
        initial_time = flavor.insert_utc_date_time
        flavor.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert flavor.insert_utc_date_time == initial_time
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
        flavor = await FlavorFactory.build_async(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
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
        flavor = await FlavorFactory.build_async(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        flavor.code = uuid.uuid4()
        session.add(flavor)
        await session.commit()
        assert flavor.last_update_utc_date_time > initial_time
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
        flavor = await FlavorFactory.create_async(session=session)
        assert flavor.last_update_utc_date_time is not None
        assert isinstance(flavor.last_update_utc_date_time, datetime)
        initial_time = flavor.last_update_utc_date_time
        flavor.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert flavor.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a flavor from the database.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the deleted flavor is still
            found in the database.
        """
        flavor = await FlavorFactory.create_async(session=session)
        await session.delete(flavor)
        await session.commit()
        # Construct the select statement
        stmt = select(Flavor).where(
            Flavor._flavor_id == flavor.flavor_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_flavor = result.scalars().first()
        assert deleted_flavor is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of the flavor attributes.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        flavor = await FlavorFactory.create_async(session=session)
        assert isinstance(flavor.flavor_id, int)
        assert isinstance(flavor.code, uuid.UUID)
        assert isinstance(flavor.last_change_code, int)
        assert isinstance(flavor.insert_user_id, uuid.UUID)
        assert isinstance(flavor.last_update_user_id, uuid.UUID)
        assert flavor.description == "" or isinstance(flavor.description, str)
        assert isinstance(flavor.display_order, int)
        assert isinstance(flavor.is_active, bool)
        assert flavor.lookup_enum_name == "" or isinstance(flavor.lookup_enum_name, str)
        assert flavor.name == "" or isinstance(flavor.name, str)
        assert isinstance(flavor.pac_id, int)
        # Check for the peek values
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        assert isinstance(flavor.pac_code_peek, uuid.UUID)
# endset
        assert isinstance(flavor.insert_utc_date_time, datetime)
        assert isinstance(flavor.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint for flavors.
        This test creates two flavor instances using
        the FlavorFactoryand assigns the same code to both flavors.
        Then it adds both flavors to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.
        Note: This test assumes that the
        FlavorFactory.create_async() method creates unique codes for each flavor.
        """
        flavor_1 = await FlavorFactory.create_async(session=session)
        flavor_2 = await FlavorFactory.create_async(session=session)
        flavor_2.code = flavor_1.code
        session.add_all([flavor_1, flavor_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the Flavor model.
        This test case checks that the default values
        of various fields in the Flavor model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """
        flavor = Flavor()
        assert flavor.code is not None
        assert flavor.last_change_code is not None
        assert flavor.insert_user_id is not None
        assert flavor.last_update_user_id is not None
        assert flavor.insert_utc_date_time is not None
        assert flavor.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(flavor.pac_code_peek, uuid.UUID)
# endset
        assert flavor.description == ""
        assert flavor.display_order == 0
        assert flavor.is_active is False
        assert flavor.lookup_enum_name == ""
        assert flavor.name == ""
        assert flavor.pac_id == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code in the Flavor model.
        This test verifies that the last_change_code
        attribute of a Flavor object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.
        Steps:
        1. Create a new Flavor object using the FlavorFactory.
        2. Get the original value of the last_change_code attribute.
        3. Query the database for the Flavor object using the flavor_id.
        4. Modify the code attribute of the retrieved Flavor object.
        5. Commit the changes to the database.
        6. Query the database again for the Flavor object using the flavor_id.
        7. Get the modified Flavor object.
        8. Verify that the last_change_code attribute
            of the modified Flavor object
            is different from the original value.
        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified Flavor
                            object is the same as the original value.
        """
        flavor = await FlavorFactory.create_async(session=session)
        original_last_change_code = flavor.last_change_code
        stmt = select(Flavor).where(
            Flavor._flavor_id == flavor.flavor_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        flavor_1 = result.scalars().first()
        # flavor_1 = await session.query(Flavor).filter_by(
        # flavor_id=flavor.flavor_id).first()
        flavor_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Flavor).where(
            Flavor._flavor_id == flavor.flavor_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        flavor_2 = result.scalars().first()
        # flavor_2 = await session.query(Flavor).filter_by(
        # flavor_id=flavor.flavor_id).first()
        flavor_2.code = uuid.uuid4()
        await session.commit()
        assert flavor_2.last_change_code != original_last_change_code
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
        This test case creates a flavor using the
        FlavorFactory and sets an invalid pac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.
        Args:
            session: The SQLAlchemy session object.
        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        flavor = await FlavorFactory.create_async(session=session)
        flavor.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
# endset
