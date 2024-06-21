# models/managers/tests/tri_state_filter_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `TriStateFilterManager` class.
"""
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from helpers.session_context import SessionContext
from managers.tri_state_filter import TriStateFilterManager
from models import TriStateFilter
from models.factory import TriStateFilterFactory
class TestTriStateFilterGetByManager:
    """
    This class contains unit tests for the
    `TriStateFilterManager` class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def tri_state_filter_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `TriStateFilterManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return TriStateFilterManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case for the `build` method of
        `TriStateFilterManager`.
        """
        # Define mock data for our tri_state_filter
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        tri_state_filter = await tri_state_filter_manager.build(
            **mock_data)
        # Assert that the returned object is an instance of TriStateFilter
        assert isinstance(
            tri_state_filter, TriStateFilter)
        # Assert that the attributes of the
        # tri_state_filter match our mock data
        assert tri_state_filter.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `TriStateFilterManager`.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(
            session)
        tri_state_filter = await tri_state_filter_manager.get_by_id(
            test_tri_state_filter.tri_state_filter_id)
        assert isinstance(
            tri_state_filter, TriStateFilter)
        assert test_tri_state_filter.tri_state_filter_id == \
            tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == \
            tri_state_filter.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case for the `get_by_id` method of
        `TriStateFilterManager` when the
        tri_state_filter is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_tri_state_filter = await tri_state_filter_manager.get_by_id(
            non_existent_id)
        assert retrieved_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `TriStateFilterManager` that checks if
        a tri_state_filter is
        returned by its code.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(
            session)
        tri_state_filter = await tri_state_filter_manager.get_by_code(
            test_tri_state_filter.code)
        assert isinstance(
            tri_state_filter, TriStateFilter)
        assert test_tri_state_filter.tri_state_filter_id == \
            tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == \
            tri_state_filter.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case for the `get_by_code` method of
        `TriStateFilterManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any TriStateFilter in the database
        random_code = uuid.uuid4()
        tri_state_filter = await tri_state_filter_manager.get_by_code(
            random_code)
        assert tri_state_filter is None
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a tri_state_filter with
        a specific pac_id exists.
        Steps:
        1. Create a tri_state_filter using the
            TriStateFilterFactory.
        2. Fetch the tri_state_filter using the
            `get_by_pac_id` method of the tri_state_filter_manager.
        3. Assert that the fetched tri_state_filters list contains
            only one tri_state_filter.
        4. Assert that the fetched tri_state_filter
            is an instance
            of the TriStateFilter class.
        5. Assert that the code of the fetched tri_state_filter
            matches the code of the created tri_state_filter.
        6. Fetch the corresponding pac object
            using the pac_id of the created tri_state_filter.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            tri_state_filter matches the
            code of the fetched pac.
        """
        # Add a tri_state_filter with a specific
        # pac_id
        tri_state_filter1 = await TriStateFilterFactory.create_async(
            session=session)
        # Fetch the tri_state_filter using
        # the manager function
        fetched_tri_state_filters = await tri_state_filter_manager.get_by_pac_id(
            tri_state_filter1.pac_id)
        assert len(fetched_tri_state_filters) == 1
        assert isinstance(fetched_tri_state_filters[0], TriStateFilter)
        assert fetched_tri_state_filters[0].code == \
            tri_state_filter1.code
        stmt = select(models.Pac).where(
            models.Pac._pac_id == tri_state_filter1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert isinstance(pac, models.Pac)
        assert fetched_tri_state_filters[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.
        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_tri_state_filters = await tri_state_filter_manager.get_by_pac_id(
            non_existent_id)
        assert len(fetched_tri_state_filters) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An
                instance of the TriStateFilterManager class.
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
            await tri_state_filter_manager.get_by_pac_id(
                invalid_id)  # type: ignore
        await session.rollback()
    # stateIntValue,
# endset
