# models/factory/tests/tac_async_test.py
# pylint: disable=unused-argument
"""
This module contains unit tests for the asynchronous
operations of the TacFactory class.
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
from models import Base, Tac
from models.factory import TacFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
class TestTacFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the TacFactory class.
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
    async def test_tac_creation(self, session):
        """
        Test case for creating a tac
        asynchronously.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the tac ID
                is None after creation.
        """
        tac = await TacFactory.create_async(
            session=session)
        assert tac.tac_id is not None
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
        tac = await TacFactory.create_async(
            session=session)
        assert isinstance(tac.code, uuid.UUID)
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
        tac: Tac = await TacFactory.build_async(
            session=session)
        assert tac.last_change_code == 0
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
        tac: Tac = await TacFactory.create_async(
            session=session)
        assert tac.last_change_code == 1
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the tac.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        tac = await TacFactory.create_async(
            session=session)
        initial_code = tac.last_change_code
        tac.code = uuid.uuid4()
        await session.commit()
        assert tac.last_change_code != initial_code
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
        tac = await TacFactory.build_async(
            session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(
            tac.insert_utc_date_time, datetime)
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
        tac = await TacFactory.build_async(
            session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(
            tac.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tac.code = uuid.uuid4()
        session.add(tac)
        await session.commit()
        assert tac.insert_utc_date_time > initial_time
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
        tac = await TacFactory.create_async(
            session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(
            tac.insert_utc_date_time, datetime)
        initial_time = tac.insert_utc_date_time
        tac.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert tac.insert_utc_date_time == initial_time
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
        tac = await TacFactory.build_async(
            session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(
            tac.last_update_utc_date_time, datetime)
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
        tac = await TacFactory.build_async(
            session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(
            tac.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tac.code = uuid.uuid4()
        session.add(tac)
        await session.commit()
        assert tac.last_update_utc_date_time > initial_time
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
        tac = await TacFactory.create_async(
            session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(
            tac.last_update_utc_date_time, datetime)
        initial_time = tac.last_update_utc_date_time
        tac.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert tac.last_update_utc_date_time > initial_time
    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a tac
        from the database.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If the deleted
            tac is still
            found in the database.
        """
        tac = await TacFactory.create_async(
            session=session)
        await session.delete(tac)
        await session.commit()
        # Construct the select statement
        stmt = select(Tac).where(
            Tac._tac_id == tac.tac_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        # Execute the statement asynchronously
        result = await session.execute(stmt)
        # Fetch all results
        deleted_tac = result.scalars().first()
        assert deleted_tac is None
    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the tac attributes.
        Args:
            session: The database session to use.
        Returns:
            None
        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        tac = await TacFactory.create_async(
            session=session)
        assert isinstance(tac.tac_id, int)
        assert isinstance(tac.code, uuid.UUID)
        assert isinstance(tac.last_change_code, int)
        assert isinstance(tac.insert_user_id, uuid.UUID)
        assert isinstance(tac.last_update_user_id, uuid.UUID)
        assert tac.description == "" or isinstance(tac.description, str)
        assert isinstance(tac.display_order, int)
        assert isinstance(tac.is_active, bool)
        assert tac.lookup_enum_name == "" or isinstance(tac.lookup_enum_name, str)
        assert tac.name == "" or isinstance(tac.name, str)
        assert isinstance(tac.pac_id, int)
        # Check for the peek values
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID
        assert isinstance(tac.pac_code_peek, uuid.UUID)
# endset
        assert isinstance(tac.insert_utc_date_time, datetime)
        assert isinstance(tac.last_update_utc_date_time, datetime)
    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint for tacs.
        This test creates two tac
        instances using
        the TacFactoryand assigns
        the same code to both tacs.
        Then it adds both tacs to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.
        Note: This test assumes that the
        TacFactory.create_async() method creates unique codes for each tac.
        """
        tac_1 = await TacFactory.create_async(
            session=session)
        tac_2 = await TacFactory.create_async(
            session=session)
        tac_2.code = tac_1.code
        session.add_all([tac_1, tac_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()
    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the Tac model.
        This test case checks that the default values
        of various fields in the Tac
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """
        tac = Tac()
        assert tac.code is not None
        assert tac.last_change_code is not None
        assert tac.insert_user_id is not None
        assert tac.last_update_user_id is not None
        assert tac.insert_utc_date_time is not None
        assert tac.last_update_utc_date_time is not None
# endset
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID
        assert isinstance(tac.pac_code_peek, uuid.UUID)
# endset
        assert tac.description == ""
        assert tac.display_order == 0
        assert tac.is_active is False
        assert tac.lookup_enum_name == ""
        assert tac.name == ""
        assert tac.pac_id == 0
# endset
    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the Tac model.
        This test verifies that the last_change_code
        attribute of a Tac object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.
        Steps:
        1. Create a new Tac object using
            the TacFactory.
        2. Get the original value of the last_change_code attribute.
        3. Query the database for the Tac
            object using the tac_id.
        4. Modify the code attribute of the
            retrieved Tac object.
        5. Commit the changes to the database.
        6. Query the database again for the
            Tac object using the tac_id.
        7. Get the modified Tac object.
        8. Verify that the last_change_code attribute
            of the modified Tac object
            is different from the original value.
        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified Tac
                            object is the same as the original value.
        """
        tac = await TacFactory.create_async(
            session=session)
        original_last_change_code = tac.last_change_code
        stmt = select(Tac).where(
            Tac._tac_id == tac.tac_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        tac_1 = result.scalars().first()
        # tac_1 = await session.query(Tac).filter_by(
        # tac_id=tac.tac_id).first()
        tac_1.code = uuid.uuid4()
        await session.commit()
        stmt = select(Tac).where(
            Tac._tac_id == tac.tac_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        tac_2 = result.scalars().first()
        # tac_2 = await session.query(Tac).filter_by(
        # tac_id=tac.tac_id).first()
        tac_2.code = uuid.uuid4()
        await session.commit()
        assert tac_2.last_change_code != original_last_change_code
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
        This test case creates a tac using the
        TacFactory and sets an invalid pac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.
        Args:
            session: The SQLAlchemy session object.
        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        tac = await TacFactory.create_async(
            session=session)
        tac.pac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
# endset
