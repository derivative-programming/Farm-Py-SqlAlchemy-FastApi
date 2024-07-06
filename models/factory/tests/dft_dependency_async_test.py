# models/factory/tests/dft_dependency_async_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains unit tests for the asynchronous
operations of the DFTDependencyFactory class.
"""

import asyncio
import math  # noqa: F401
import time
import uuid  # noqa: F401
from datetime import date, datetime, timedelta, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import AsyncGenerator, Generator

import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

import pytest
from models import Base, DFTDependency
from models.factory import DFTDependencyFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestDFTDependencyFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the DFTDependencyFactory class.
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
        engine = create_async_engine(TEST_DATABASE_URL, echo=False)
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
    async def test_dft_dependency_creation(self, session):
        """
        Test case for creating a dft_dependency
        asynchronously.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the dft_dependency ID
                is None after creation.
        """
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        assert dft_dependency.dft_dependency_id is not None

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
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        assert isinstance(dft_dependency.code, uuid.UUID)

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
        dft_dependency: DFTDependency = await \
            DFTDependencyFactory.build_async(
                session=session)
        assert dft_dependency.last_change_code == 0

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
        dft_dependency: DFTDependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        assert dft_dependency.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the dft_dependency.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        initial_code = dft_dependency.last_change_code
        dft_dependency.code = uuid.uuid4()
        await session.commit()
        assert dft_dependency.last_change_code != initial_code

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
        dft_dependency = await \
            DFTDependencyFactory.build_async(
                session=session)
        assert dft_dependency.insert_utc_date_time is not None
        assert isinstance(
            dft_dependency.insert_utc_date_time, datetime)

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
        dft_dependency = await \
            DFTDependencyFactory.build_async(
                session=session)
        assert dft_dependency.insert_utc_date_time is not None
        assert isinstance(
            dft_dependency.insert_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        dft_dependency.code = uuid.uuid4()
        session.add(dft_dependency)
        await session.commit()
        assert dft_dependency.insert_utc_date_time > \
            initial_time

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
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        assert dft_dependency.insert_utc_date_time is not None
        assert isinstance(
            dft_dependency.insert_utc_date_time, datetime)
        initial_time = dft_dependency.insert_utc_date_time
        dft_dependency.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert dft_dependency.insert_utc_date_time == \
            initial_time

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
        dft_dependency = await \
            DFTDependencyFactory.build_async(
                session=session)
        assert dft_dependency.last_update_utc_date_time is not None
        assert isinstance(
            dft_dependency.last_update_utc_date_time, datetime)

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
        dft_dependency = await \
            DFTDependencyFactory.build_async(
                session=session)
        assert dft_dependency.last_update_utc_date_time is not None
        assert isinstance(
            dft_dependency.last_update_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        dft_dependency.code = uuid.uuid4()
        session.add(dft_dependency)
        await session.commit()
        assert dft_dependency.last_update_utc_date_time > \
            initial_time

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
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        assert dft_dependency.last_update_utc_date_time is not None
        assert isinstance(
            dft_dependency.last_update_utc_date_time, datetime)
        initial_time = dft_dependency.last_update_utc_date_time
        dft_dependency.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert dft_dependency.last_update_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a dft_dependency
        from the database.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the deleted
            dft_dependency is still
            found in the database.
        """
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        await session.delete(dft_dependency)
        await session.commit()

        # Construct the select statement
        stmt = select(DFTDependency).where(
            DFTDependency._dft_dependency_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dft_dependency.dft_dependency_id))

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_dft_dependency = result.scalars().first()

        assert deleted_dft_dependency is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the dft_dependency attributes.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        obj = await \
            DFTDependencyFactory.create_async(
                session=session)
        assert isinstance(obj.dft_dependency_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.dependency_df_task_id, int)
        assert isinstance(obj.dyna_flow_task_id, int)
        assert isinstance(obj.is_placeholder, bool)
        # Check for the peek values
        # dependencyDFTaskID,
        # dynaFlowTaskID

        assert isinstance(obj.dyna_flow_task_code_peek, uuid.UUID)
        # isPlaceholder,

        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint
        for dft_dependencys.

        This test creates two dft_dependency
        instances using
        the DFTDependencyFactoryand assigns
        the same code to both dft_dependencys.
        Then it adds both dft_dependencys to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.

        Note: This test assumes that the
        DFTDependencyFactory.create_async()
        method creates unique codes for
        each dft_dependency.
        """

        obj_1 = await DFTDependencyFactory.create_async(
            session=session)
        obj_2 = await DFTDependencyFactory.create_async(
            session=session)
        obj_2.code = obj_1.code
        session.add_all([obj_1,
                         obj_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()

    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the DFTDependency model.

        This test case checks that the default values
        of various fields in the DFTDependency
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """

        new_obj = DFTDependency()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id is not None
        assert new_obj.last_update_user_id is not None
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None

        # dependencyDFTaskID,
        # DynaFlowTaskID

        assert isinstance(new_obj.dyna_flow_task_code_peek, uuid.UUID)
        # isPlaceholder,
        assert new_obj.dependency_df_task_id == 0
        assert new_obj.dyna_flow_task_id == 0
        assert new_obj.is_placeholder is False

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the DFTDependency model.

        This test verifies that the last_change_code
        attribute of a DFTDependency object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.

        Steps:
        1. Create a new
            DFTDependency object using
            the DFTDependencyFactory.
        2. Get the original value of the
            last_change_code attribute.
        3. Query the database for the DFTDependency
            object using the
            dft_dependency_id.
        4. Modify the code attribute of the
            retrieved DFTDependency object.
        5. Commit the changes to the database.
        6. Query the database again for the
            DFTDependency object using the
            dft_dependency_id.
        7. Get the modified DFTDependency object.
        8. Verify that the last_change_code attribute
            of the modified DFTDependency object
            is different from the original value.

        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified DFTDependency
                            object is the same as the original value.
        """
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        original_last_change_code = dft_dependency.last_change_code

        stmt = select(DFTDependency).where(
            DFTDependency._dft_dependency_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dft_dependency.dft_dependency_id))
        result = await session.execute(stmt)
        obj_1 = result.scalars().first()

        # obj_1 = await session.query(DFTDependency).filter_by(
        # dft_dependency_id=dft_dependency.dft_dependency_id).first()
        obj_1.code = uuid.uuid4()
        await session.commit()

        stmt = select(DFTDependency).where(
            DFTDependency._dft_dependency_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                dft_dependency.dft_dependency_id))
        result = await session.execute(stmt)
        obj_2 = result.scalars().first()

        # obj_2 = await session.query(DFTDependency).filter_by(
        # dft_dependency_id=dft_dependency.dft_dependency_id).first()
        obj_2.code = uuid.uuid4()
        await session.commit()
        assert obj_2.last_change_code != original_last_change_code
    # dependencyDFTaskID,
    # DynaFlowTaskID

    @pytest.mark.asyncio
    async def test_invalid_dyna_flow_task_id(self, session):
        """
        Test case for handling an invalid dyna_flow_task ID.

        This test case creates a dft_dependency using the
        DFTDependencyFactory and sets an invalid dyna_flow_task ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session=session)
        dft_dependency.dyna_flow_task_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # isPlaceholder,
