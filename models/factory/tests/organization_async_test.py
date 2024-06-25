# models/factory/tests/organization_async_test.py
# pylint: disable=unused-argument

"""
This module contains unit tests for the asynchronous
operations of the OrganizationFactory class.
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

from models import Base, Organization
from models.factory import OrganizationFactory

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestOrganizationFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the OrganizationFactory class.
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
    async def test_organization_creation(self, session):
        """
        Test case for creating a organization
        asynchronously.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the organization ID
                is None after creation.
        """
        organization = await OrganizationFactory.create_async(
            session=session)
        assert organization.organization_id is not None

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
        organization = await OrganizationFactory.create_async(
            session=session)
        assert isinstance(organization.code, uuid.UUID)

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
        organization: Organization = await OrganizationFactory.build_async(
            session=session)
        assert organization.last_change_code == 0

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
        organization: Organization = await OrganizationFactory.create_async(
            session=session)
        assert organization.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the organization.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        organization = await OrganizationFactory.create_async(
            session=session)
        initial_code = organization.last_change_code
        organization.code = uuid.uuid4()
        await session.commit()
        assert organization.last_change_code != initial_code

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
        organization = await OrganizationFactory.build_async(
            session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(
            organization.insert_utc_date_time, datetime)

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
        organization = await OrganizationFactory.build_async(
            session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(
            organization.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        organization.code = uuid.uuid4()
        session.add(organization)
        await session.commit()
        assert organization.insert_utc_date_time > initial_time

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
        organization = await OrganizationFactory.create_async(
            session=session)
        assert organization.insert_utc_date_time is not None
        assert isinstance(
            organization.insert_utc_date_time, datetime)
        initial_time = organization.insert_utc_date_time
        organization.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert organization.insert_utc_date_time == initial_time

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
        organization = await OrganizationFactory.build_async(
            session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(
            organization.last_update_utc_date_time, datetime)

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
        organization = await OrganizationFactory.build_async(
            session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(
            organization.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        organization.code = uuid.uuid4()
        session.add(organization)
        await session.commit()
        assert organization.last_update_utc_date_time > initial_time

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
        organization = await OrganizationFactory.create_async(
            session=session)
        assert organization.last_update_utc_date_time is not None
        assert isinstance(
            organization.last_update_utc_date_time, datetime)
        initial_time = organization.last_update_utc_date_time
        organization.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert organization.last_update_utc_date_time > initial_time

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a organization
        from the database.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the deleted
            organization is still
            found in the database.
        """
        organization = await OrganizationFactory.create_async(
            session=session)
        await session.delete(organization)
        await session.commit()

        # Construct the select statement
        stmt = select(Organization).where(
            Organization._organization_id == organization.organization_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_organization = result.scalars().first()

        assert deleted_organization is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the organization attributes.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        organization = await OrganizationFactory.create_async(
            session=session)
        assert isinstance(organization.organization_id, int)
        assert isinstance(organization.code, uuid.UUID)
        assert isinstance(organization.last_change_code, int)
        assert isinstance(organization.insert_user_id, uuid.UUID)
        assert isinstance(organization.last_update_user_id, uuid.UUID)
        assert organization.name == "" or isinstance(organization.name, str)
        assert isinstance(organization.tac_id, int)
        # Check for the peek values
        # name,
        # tacID

        assert isinstance(organization.tac_code_peek, uuid.UUID)

        assert isinstance(organization.insert_utc_date_time, datetime)
        assert isinstance(organization.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint for organizations.

        This test creates two organization
        instances using
        the OrganizationFactoryand assigns
        the same code to both organizations.
        Then it adds both organizations to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.

        Note: This test assumes that the
        OrganizationFactory.create_async() method creates unique codes for each organization.
        """

        organization_1 = await OrganizationFactory.create_async(
            session=session)
        organization_2 = await OrganizationFactory.create_async(
            session=session)
        organization_2.code = organization_1.code
        session.add_all([organization_1, organization_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()

    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the Organization model.

        This test case checks that the default values
        of various fields in the Organization
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """

        organization = Organization()
        assert organization.code is not None
        assert organization.last_change_code is not None
        assert organization.insert_user_id is not None
        assert organization.last_update_user_id is not None
        assert organization.insert_utc_date_time is not None
        assert organization.last_update_utc_date_time is not None

        # name,
        # TacID

        assert isinstance(organization.tac_code_peek, uuid.UUID)
        assert organization.name == ""
        assert organization.tac_id == 0

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the Organization model.

        This test verifies that the last_change_code
        attribute of a Organization object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.

        Steps:
        1. Create a new Organization object using
            the OrganizationFactory.
        2. Get the original value of the last_change_code attribute.
        3. Query the database for the Organization
            object using the organization_id.
        4. Modify the code attribute of the
            retrieved Organization object.
        5. Commit the changes to the database.
        6. Query the database again for the
            Organization object using the organization_id.
        7. Get the modified Organization object.
        8. Verify that the last_change_code attribute
            of the modified Organization object
            is different from the original value.

        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified Organization
                            object is the same as the original value.
        """
        organization = await OrganizationFactory.create_async(
            session=session)
        original_last_change_code = organization.last_change_code

        stmt = select(Organization).where(
            Organization._organization_id == organization.organization_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        organization_1 = result.scalars().first()

        # organization_1 = await session.query(Organization).filter_by(
        # organization_id=organization.organization_id).first()
        organization_1.code = uuid.uuid4()
        await session.commit()

        stmt = select(Organization).where(
            Organization._organization_id == organization.organization_id)  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
        result = await session.execute(stmt)
        organization_2 = result.scalars().first()

        # organization_2 = await session.query(Organization).filter_by(
        # organization_id=organization.organization_id).first()
        organization_2.code = uuid.uuid4()
        await session.commit()
        assert organization_2.last_change_code != original_last_change_code
    # name,
    # TacID

    @pytest.mark.asyncio
    async def test_invalid_tac_id(self, session):
        """
        Test case for handling an invalid tac ID.

        This test case creates a organization using the
        OrganizationFactory and sets an invalid tac ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        organization = await OrganizationFactory.create_async(
            session=session)
        organization.tac_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()

