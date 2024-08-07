# models/managers/tests/date_greater_than_filter_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DateGreaterThanFilterManager` class.
"""

import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import pytest
from helpers.session_context import SessionContext
from managers.date_greater_than_filter import DateGreaterThanFilterManager
from models import DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory


class TestDateGreaterThanFilterGetByManager:
    """
    This class contains unit tests for the
    `DateGreaterThanFilterManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DateGreaterThanFilterManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DateGreaterThanFilterManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `build` method of
        `DateGreaterThanFilterManager`.
        """
        # Define mock data for our date_greater_than_filter
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        date_greater_than_filter = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of
        # DateGreaterThanFilter
        assert isinstance(
            date_greater_than_filter,
            DateGreaterThanFilter)

        # Assert that the attributes of the
        # date_greater_than_filter match our mock data
        assert date_greater_than_filter.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `DateGreaterThanFilterManager`.
        """
        new_obj = await \
            DateGreaterThanFilterFactory.create_async(
                session)

        date_greater_than_filter = await \
            obj_manager.get_by_id(
                new_obj.date_greater_than_filter_id)

        assert isinstance(
            date_greater_than_filter,
            DateGreaterThanFilter)

        assert new_obj.date_greater_than_filter_id == \
            date_greater_than_filter.date_greater_than_filter_id
        assert new_obj.code == \
            date_greater_than_filter.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `get_by_id` method of
        `DateGreaterThanFilterManager` when the
        date_greater_than_filter is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_date_greater_than_filter = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_date_greater_than_filter is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_date_greater_than_filter(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `DateGreaterThanFilterManager` that checks if
        a date_greater_than_filter is
        returned by its code.
        """

        new_obj = await \
            DateGreaterThanFilterFactory.create_async(
                session)

        date_greater_than_filter = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            date_greater_than_filter,
            DateGreaterThanFilter)

        assert new_obj.date_greater_than_filter_id == \
            date_greater_than_filter.date_greater_than_filter_id
        assert new_obj.code == \
            date_greater_than_filter.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `get_by_code` method of
        `DateGreaterThanFilterManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any DateGreaterThanFilter in the database
        random_code = uuid.uuid4()

        date_greater_than_filter = await \
            obj_manager.get_by_code(
                random_code)

        assert date_greater_than_filter is None

    # dayCount
    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a date_greater_than_filter with
        a specific pac_id exists.

        Steps:
        1. Create a date_greater_than_filter using the
            DateGreaterThanFilterFactory.
        2. Fetch the date_greater_than_filter using the
            `get_by_pac_id` method of the obj_manager.
        3. Assert that the fetched date_greater_than_filters list contains
            only one date_greater_than_filter.
        4. Assert that the fetched date_greater_than_filter
            is an instance
            of the DateGreaterThanFilter class.
        5. Assert that the code of the fetched date_greater_than_filter
            matches the code of the created date_greater_than_filter.
        6. Fetch the corresponding pac object
            using the pac_id of the created date_greater_than_filter.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            date_greater_than_filter matches the
            code of the fetched pac.

        """
        # Add a date_greater_than_filter with a specific
        # pac_id
        obj_1 = await DateGreaterThanFilterFactory.create_async(
            session=session)

        # Fetch the date_greater_than_filter using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                obj_1.pac_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          DateGreaterThanFilter)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Pac).where(
            models.Pac._pac_id == obj_1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()

        assert isinstance(pac, models.Pac)

        assert fetched_objs[0].pac_code_peek == pac.code

    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        obj_manager: DateGreaterThanFilterManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.

        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_pac_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        obj_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.

        Args:
            obj_manager (DateGreaterThanFilterManager): An
                instance of the DateGreaterThanFilterManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.

        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_pac_id` method.

        Returns:
            None
        """

        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_pac_id(
                invalid_id)  # type: ignore

        await session.rollback()
