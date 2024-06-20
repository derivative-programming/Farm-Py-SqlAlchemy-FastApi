# models/managers/tests/tri_state_filter_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `TriStateFilterManager` class.
"""
# TODO file too big. split into separate test files
import logging
from typing import List
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
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
class TestTriStateFilterManager:
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
        tri_state_filter = await tri_state_filter_manager.build(**mock_data)
        # Assert that the returned object is an instance of TriStateFilter
        assert isinstance(tri_state_filter, TriStateFilter)
        # Assert that the attributes of the tri_state_filter match our mock data
        assert tri_state_filter.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `TriStateFilterManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await tri_state_filter_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_tri_state_filter_to_database(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `TriStateFilterManager` that checks if a
        tri_state_filter is correctly added to the database.
        """
        test_tri_state_filter = await TriStateFilterFactory.build_async(session)
        assert test_tri_state_filter.tri_state_filter_id == 0
        # Add the tri_state_filter using the manager's add method
        added_tri_state_filter = await tri_state_filter_manager.add(tri_state_filter=test_tri_state_filter)
        assert isinstance(added_tri_state_filter, TriStateFilter)
        assert str(added_tri_state_filter.insert_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))
        assert str(added_tri_state_filter.last_update_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))
        assert added_tri_state_filter.tri_state_filter_id > 0
        # Fetch the tri_state_filter from the database directly
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == added_tri_state_filter.tri_state_filter_id  # type: ignore
            )
        )
        fetched_tri_state_filter = result.scalars().first()
        # Assert that the fetched tri_state_filter is not None and matches the added tri_state_filter
        assert fetched_tri_state_filter is not None
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.tri_state_filter_id == added_tri_state_filter.tri_state_filter_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_tri_state_filter_object(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `TriStateFilterManager` that checks if the
        correct tri_state_filter object is returned.
        """
        # Create a test tri_state_filter using the TriStateFilterFactory
        # without persisting it to the database
        test_tri_state_filter = await TriStateFilterFactory.build_async(session)
        assert test_tri_state_filter.tri_state_filter_id == 0
        test_tri_state_filter.code = uuid.uuid4()
        # Add the tri_state_filter using the manager's add method
        added_tri_state_filter = await tri_state_filter_manager.add(tri_state_filter=test_tri_state_filter)
        assert isinstance(added_tri_state_filter, TriStateFilter)
        assert str(added_tri_state_filter.insert_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))
        assert str(added_tri_state_filter.last_update_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))
        assert added_tri_state_filter.tri_state_filter_id > 0
        # Assert that the returned tri_state_filter matches the test tri_state_filter
        assert added_tri_state_filter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id
        assert added_tri_state_filter.code == test_tri_state_filter.code
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
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        tri_state_filter = await tri_state_filter_manager.get_by_id(test_tri_state_filter.tri_state_filter_id)
        assert isinstance(tri_state_filter, TriStateFilter)
        assert test_tri_state_filter.tri_state_filter_id == tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == tri_state_filter.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case for the `get_by_id` method of
        `TriStateFilterManager` when the tri_state_filter is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_tri_state_filter = await tri_state_filter_manager.get_by_id(non_existent_id)
        assert retrieved_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `TriStateFilterManager` that checks if a tri_state_filter is
        returned by its code.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        tri_state_filter = await tri_state_filter_manager.get_by_code(test_tri_state_filter.code)
        assert isinstance(tri_state_filter, TriStateFilter)
        assert test_tri_state_filter.tri_state_filter_id == tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == tri_state_filter.code
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
        tri_state_filter = await tri_state_filter_manager.get_by_code(random_code)
        assert tri_state_filter is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `TriStateFilterManager`
        that checks if a tri_state_filter is correctly updated.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        test_tri_state_filter.code = uuid.uuid4()
        updated_tri_state_filter = await tri_state_filter_manager.update(tri_state_filter=test_tri_state_filter)
        assert isinstance(updated_tri_state_filter, TriStateFilter)
        assert str(updated_tri_state_filter.last_update_user_id) == str(
            tri_state_filter_manager._session_context.customer_code)
        assert updated_tri_state_filter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == test_tri_state_filter.code
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == test_tri_state_filter.tri_state_filter_id)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()
        assert updated_tri_state_filter.tri_state_filter_id == fetched_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == fetched_tri_state_filter.code
        assert test_tri_state_filter.tri_state_filter_id == fetched_tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == fetched_tri_state_filter.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `TriStateFilterManager`
        that checks if a tri_state_filter is correctly updated using a dictionary.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_tri_state_filter = await tri_state_filter_manager.update(
            tri_state_filter=test_tri_state_filter,
            code=new_code
        )
        assert isinstance(updated_tri_state_filter, TriStateFilter)
        assert str(updated_tri_state_filter.last_update_user_id) == str(
            tri_state_filter_manager._session_context.customer_code
        )
        assert updated_tri_state_filter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == new_code
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == test_tri_state_filter.tri_state_filter_id)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()
        assert updated_tri_state_filter.tri_state_filter_id == fetched_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == fetched_tri_state_filter.code
        assert test_tri_state_filter.tri_state_filter_id == fetched_tri_state_filter.tri_state_filter_id
        assert new_code == fetched_tri_state_filter.code
    @pytest.mark.asyncio
    async def test_update_invalid_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case for the `update` method of `TriStateFilterManager`
        with an invalid tri_state_filter.
        """
        # None tri_state_filter
        tri_state_filter = None
        new_code = uuid.uuid4()
        updated_tri_state_filter = await (
            tri_state_filter_manager.update(tri_state_filter, code=new_code))  # type: ignore
        # Assertions
        assert updated_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `TriStateFilterManager`
        with a nonexistent attribute.
        """
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await tri_state_filter_manager.update(
                tri_state_filter=test_tri_state_filter,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `TriStateFilterManager`.
        """
        tri_state_filter_data = await TriStateFilterFactory.create_async(session)
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == tri_state_filter_data.tri_state_filter_id)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.tri_state_filter_id == tri_state_filter_data.tri_state_filter_id
        await tri_state_filter_manager.delete(
            tri_state_filter_id=tri_state_filter_data.tri_state_filter_id)
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == tri_state_filter_data.tri_state_filter_id)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()
        assert fetched_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent tri_state_filter.
        This test case ensures that when the delete method
        is called with the ID of a nonexistent tri_state_filter,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.
        :param tri_state_filter_manager: The instance of the TriStateFilterManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await tri_state_filter_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a tri_state_filter
        with an invalid type.
        This test case ensures that when the `delete` method
        of the `tri_state_filter_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance of the
                `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            Exception: If the `delete` method does not raise an exception.
        """
        with pytest.raises(Exception):
            await tri_state_filter_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `TriStateFilterManager` class.
        This test verifies that the `get_list`
        method returns the correct list of tri_state_filters.
        Steps:
        1. Call the `get_list` method of the
            `tri_state_filter_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 tri_state_filter objects using the
            `TriStateFilterFactory.create_async` method.
        4. Assert that the `tri_state_filters_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `tri_state_filter_manager` instance again.
        6. Assert that the returned list contains 5 tri_state_filters.
        7. Assert that all elements in the returned list are
            instances of the `TriStateFilter` class.
        """
        tri_state_filters = await tri_state_filter_manager.get_list()
        assert len(tri_state_filters) == 0
        tri_state_filters_data = (
            [await TriStateFilterFactory.create_async(session) for _ in range(5)])
        assert isinstance(tri_state_filters_data, List)
        tri_state_filters = await tri_state_filter_manager.get_list()
        assert len(tri_state_filters) == 5
        assert all(isinstance(tri_state_filter, TriStateFilter) for tri_state_filter in tri_state_filters)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the TriStateFilterManager class.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        Raises:
            AssertionError: If the json_data is None.
        """
        tri_state_filter = await TriStateFilterFactory.build_async(session)
        json_data = tri_state_filter_manager.to_json(tri_state_filter)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the TriStateFilterManager class.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        tri_state_filter = await TriStateFilterFactory.build_async(session)
        dict_data = tri_state_filter_manager.to_dict(tri_state_filter)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `TriStateFilterManager` class.
        This method tests the functionality of the
        `from_json` method of the `TriStateFilterManager` class.
        It creates a tri_state_filter using the `TriStateFilterFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        tri_state_filter is an instance of the `TriStateFilter` class and has
        the same code as the original tri_state_filter.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance of the
                `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session)
        json_data = tri_state_filter_manager.to_json(tri_state_filter)
        deserialized_tri_state_filter = tri_state_filter_manager.from_json(json_data)
        assert isinstance(deserialized_tri_state_filter, TriStateFilter)
        assert deserialized_tri_state_filter.code == tri_state_filter.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `TriStateFilterManager` class.
        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a tri_state_filter object.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance
                of the `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        tri_state_filter = await TriStateFilterFactory.create_async(session)
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)
        assert isinstance(tri_state_filter_data, dict)
        deserialized_tri_state_filter = tri_state_filter_manager.from_dict(tri_state_filter_data)
        assert isinstance(deserialized_tri_state_filter, TriStateFilter)
        assert deserialized_tri_state_filter.code == tri_state_filter.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `TriStateFilterManager` class.
        This test case verifies that the `add_bulk`
        method correctly adds multiple tri_state_filters to the database.
        Steps:
        1. Generate a list of tri_state_filter data using the
            `TriStateFilterFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `tri_state_filter_manager` instance, passing in the generated tri_state_filter data.
        3. Verify that the number of tri_state_filters returned is
            equal to the number of tri_state_filters added.
        4. For each updated tri_state_filter, fetch the corresponding
            tri_state_filter from the database.
        5. Verify that the fetched tri_state_filter is an instance of the
            `TriStateFilter` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched tri_state_filter match the
            customer code of the session context.
        7. Verify that the tri_state_filter_id of the fetched
            tri_state_filter matches the tri_state_filter_id of the updated tri_state_filter.
        """
        tri_state_filters_data = [
            await TriStateFilterFactory.build_async(session) for _ in range(5)]
        tri_state_filters = await tri_state_filter_manager.add_bulk(tri_state_filters_data)
        assert len(tri_state_filters) == 5
        for updated_tri_state_filter in tri_state_filters:
            result = await session.execute(
                select(TriStateFilter).filter(
                    TriStateFilter._tri_state_filter_id == updated_tri_state_filter.tri_state_filter_id  # type: ignore
                )
            )
            fetched_tri_state_filter = result.scalars().first()
            assert isinstance(fetched_tri_state_filter, TriStateFilter)
            assert str(fetched_tri_state_filter.insert_user_id) == (
                str(tri_state_filter_manager._session_context.customer_code))
            assert str(fetched_tri_state_filter.last_update_user_id) == (
                str(tri_state_filter_manager._session_context.customer_code))
            assert fetched_tri_state_filter.tri_state_filter_id == updated_tri_state_filter.tri_state_filter_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of tri_state_filters.
        This test case verifies the functionality of the
        `update_bulk` method in the `TriStateFilterManager` class.
        It creates two tri_state_filter instances, updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.
        Steps:
        1. Create two tri_state_filter instances using the
            `TriStateFilterFactory.create_async` method.
        2. Generate new codes for the tri_state_filters.
        3. Update the tri_state_filters' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance of the
                `TriStateFilterManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        # Mocking tri_state_filter instances
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter2 = await TriStateFilterFactory.create_async(session=session)
        logging.info(tri_state_filter1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update tri_state_filters
        updates = [
            {
                "tri_state_filter_id": tri_state_filter1.tri_state_filter_id,
                "code": code_updated1
            },
            {
                "tri_state_filter_id": tri_state_filter2.tri_state_filter_id,
                "code": code_updated2
            }
        ]
        updated_tri_state_filters = await tri_state_filter_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_tri_state_filters) == 2
        logging.info(updated_tri_state_filters[0].__dict__)
        logging.info(updated_tri_state_filters[1].__dict__)
        logging.info('getall')
        tri_state_filters = await tri_state_filter_manager.get_list()
        logging.info(tri_state_filters[0].__dict__)
        logging.info(tri_state_filters[1].__dict__)
        assert updated_tri_state_filters[0].code == code_updated1
        assert updated_tri_state_filters[1].code == code_updated2
        assert str(updated_tri_state_filters[0].last_update_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))
        assert str(updated_tri_state_filters[1].last_update_user_id) == (
            str(tri_state_filter_manager._session_context.customer_code))
        result = await session.execute(
            select(TriStateFilter).filter(TriStateFilter._tri_state_filter_id == 1)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.code == code_updated1
        result = await session.execute(
            select(TriStateFilter).filter(TriStateFilter._tri_state_filter_id == 2)  # type: ignore
        )
        fetched_tri_state_filter = result.scalars().first()
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_tri_state_filter_id(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the tri_state_filter_id is missing.
        This test case ensures that when the tri_state_filter_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.
        Steps:
        1. Prepare the updates list with a missing tri_state_filter_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.
        """
        # No tri_state_filters to update since tri_state_filter_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await tri_state_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_tri_state_filter_not_found(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a tri_state_filter is not found.
        This test case performs the following steps:
        1. Defines a list of tri_state_filter updates, where each update
            contains a tri_state_filter_id and a code.
        2. Calls the update_bulk method of the
            tri_state_filter_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the tri_state_filter was not found.
        4. Rolls back the session to undo any changes made during the test.
        Note: This test assumes that the update_bulk method
        throws an exception when a tri_state_filter is not found.
        """
        # Update tri_state_filters
        updates = [{"tri_state_filter_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await tri_state_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        update_bulk method when invalid data types are provided.
        This test case verifies that when the update_bulk method
        is called with a list of updates containing invalid data types,
        an exception is raised. The test case also ensures
        that the session is rolled back after the test
        to maintain data integrity.
        :param tri_state_filter_manager: An instance of the TriStateFilterManager class.
        :param session: An instance of the AsyncSession class.
        """
        updates = [{"tri_state_filter_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await tri_state_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        TriStateFilterManager class.
        This test verifies that the delete_bulk method
        successfully deletes multiple tri_state_filters
        from the database.
        Steps:
        1. Create two tri_state_filter objects using the TriStateFilterFactory.
        2. Delete the tri_state_filters using the delete_bulk method
            of the tri_state_filter_manager.
        3. Verify that the delete operation was successful by
            checking if the tri_state_filters no longer exist in the database.
        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The tri_state_filters should no longer exist in the database.
        """
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter2 = await TriStateFilterFactory.create_async(session=session)
        # Delete tri_state_filters
        tri_state_filter_ids = [tri_state_filter1.tri_state_filter_id, tri_state_filter2.tri_state_filter_id]
        result = await tri_state_filter_manager.delete_bulk(tri_state_filter_ids)
        assert result is True
        for tri_state_filter_id in tri_state_filter_ids:
            execute_result = await session.execute(
                select(TriStateFilter).filter(
                    TriStateFilter._tri_state_filter_id == tri_state_filter_id)  # type: ignore
            )
            fetched_tri_state_filter = execute_result.scalars().first()
            assert fetched_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_delete_bulk_tri_state_filters_not_found(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        tri_state_filters when some tri_state_filters are not found.
        Steps:
        1. Create a tri_state_filter using the TriStateFilterFactory.
        2. Assert that the created tri_state_filter is an instance of the
            TriStateFilter class.
        3. Define a list of tri_state_filter IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk tri_state_filters.
        5. Rollback the session to undo any changes made during the test.
        This test case ensures that the delete_bulk method of the
        TriStateFilterManager raises an exception
        when some tri_state_filters with the specified IDs are
        not found in the database.
        """
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        assert isinstance(tri_state_filter1, TriStateFilter)
        # Delete tri_state_filters
        tri_state_filter_ids = [1, 2]
        with pytest.raises(Exception):
            await tri_state_filter_manager.delete_bulk(tri_state_filter_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case to verify the behavior of deleting
        tri_state_filters with an empty list.
        Args:
            tri_state_filter_manager (TriStateFilterManager): The instance of the
                TriStateFilterManager class.
        Returns:
            None
        Raises:
            AssertionError: If the result is not True.
        """
        # Delete tri_state_filters with an empty list
        tri_state_filter_ids = []
        result = await tri_state_filter_manager.delete_bulk(tri_state_filter_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid tri_state_filter IDs are provided.
        Args:
            tri_state_filter_manager (TriStateFilterManager): The instance of the
                TriStateFilterManager class.
            session (AsyncSession): The async session object.
        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.
        Returns:
            None
        """
        tri_state_filter_ids = ["1", 2]
        with pytest.raises(Exception):
            await tri_state_filter_manager.delete_bulk(tri_state_filter_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the TriStateFilterManager class.
        This test case creates 5 tri_state_filter objects using the
        TriStateFilterFactory and checks if the count method
        returns the correct count of tri_state_filters.
        Steps:
        1. Create 5 tri_state_filter objects using the TriStateFilterFactory.
        2. Call the count method of the tri_state_filter_manager.
        3. Assert that the count is equal to 5.
        """
        tri_state_filters_data = (
            [await TriStateFilterFactory.create_async(session) for _ in range(5)])
        assert isinstance(tri_state_filters_data, List)
        count = await tri_state_filter_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test the count method when the database is empty.
        This test case checks if the count method of the
        TriStateFilterManager class returns 0 when the database is empty.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance of the
                TriStateFilterManager class.
        Returns:
            None
        """
        count = await tri_state_filter_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the 'get_sorted_list' method with basic sorting.
        This test case verifies that the 'get_sorted_list'
        method returns a list of tri_state_filters
        sorted by the '_tri_state_filter_id' attribute in ascending order.
        Steps:
        1. Add tri_state_filters to the database.
        2. Call the 'get_sorted_list' method with the
            sort_by parameter set to '_tri_state_filter_id'.
        3. Verify that the returned list of tri_state_filters is
            sorted by the '_tri_state_filter_id' attribute.
        """
        # Add tri_state_filters
        tri_state_filters_data = (
            [await TriStateFilterFactory.create_async(session) for _ in range(5)])
        assert isinstance(tri_state_filters_data, List)
        sorted_tri_state_filters = await tri_state_filter_manager.get_sorted_list(
            sort_by="_tri_state_filter_id")
        assert [tri_state_filter.tri_state_filter_id for tri_state_filter in sorted_tri_state_filters] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        'get_sorted_list' method
        when sorting the list of tri_state_filters in descending order.
        Steps:
        1. Create a list of tri_state_filters using the TriStateFilterFactory.
        2. Assert that the tri_state_filters_data is of type List.
        3. Call the 'get_sorted_list' method with
            sort_by="tri_state_filter_id" and order="desc".
        4. Assert that the tri_state_filter_ids of the
            sorted_tri_state_filters are in descending order.
        """
        # Add tri_state_filters
        tri_state_filters_data = (
            [await TriStateFilterFactory.create_async(session) for _ in range(5)])
        assert isinstance(tri_state_filters_data, List)
        sorted_tri_state_filters = await tri_state_filter_manager.get_sorted_list(
            sort_by="tri_state_filter_id", order="desc")
        assert [tri_state_filter.tri_state_filter_id for tri_state_filter in sorted_tri_state_filters] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if an AttributeError is raised when
        sorting the list by an invalid attribute.
        Args:
            tri_state_filter_manager (TriStateFilterManager): The instance of the
                TriStateFilterManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            AttributeError: If an invalid attribute is used for sorting.
        Returns:
            None
        """
        with pytest.raises(AttributeError):
            await tri_state_filter_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case to verify the behavior of
        `get_sorted_list` method when the database is empty.
        This test ensures that when the database is empty, the
        `get_sorted_list` method returns an empty list.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance of the
                TriStateFilterManager class.
        Returns:
            None
        """
        sorted_tri_state_filters = await tri_state_filter_manager.get_sorted_list(sort_by="tri_state_filter_id")
        assert len(sorted_tri_state_filters) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a tri_state_filter instance.
        This test performs the following steps:
        1. Creates a tri_state_filter instance using the TriStateFilterFactory.
        2. Retrieves the tri_state_filter from the database to ensure
            it was added correctly.
        3. Updates the tri_state_filter's code and verifies the update.
        4. Refreshes the original tri_state_filter instance and checks if
            it reflects the updated code.
        Args:
            tri_state_filter_manager (TriStateFilterManager): The manager responsible
                for tri_state_filter operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a tri_state_filter
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        # Retrieve the tri_state_filter from the database
        result = await session.execute(
            select(TriStateFilter).filter(
                TriStateFilter._tri_state_filter_id == tri_state_filter1.tri_state_filter_id)  # type: ignore
        )  # type: ignore
        tri_state_filter2 = result.scalars().first()
        # Verify that the retrieved tri_state_filter matches the added tri_state_filter
        assert tri_state_filter1.code == tri_state_filter2.code
        # Update the tri_state_filter's code
        updated_code1 = uuid.uuid4()
        tri_state_filter1.code = updated_code1
        updated_tri_state_filter1 = await tri_state_filter_manager.update(tri_state_filter1)
        # Verify that the updated tri_state_filter is of type TriStateFilter
        # and has the updated code
        assert isinstance(updated_tri_state_filter1, TriStateFilter)
        assert updated_tri_state_filter1.code == updated_code1
        # Refresh the original tri_state_filter instance
        refreshed_tri_state_filter2 = await tri_state_filter_manager.refresh(tri_state_filter2)
        # Verify that the refreshed tri_state_filter reflects the updated code
        assert refreshed_tri_state_filter2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent tri_state_filter.
        Args:
            tri_state_filter_manager (TriStateFilterManager): The instance of the
                TriStateFilterManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If the tri_state_filter refresh operation raises an exception.
        Returns:
            None
        """
        tri_state_filter = TriStateFilter(tri_state_filter_id=999)
        with pytest.raises(Exception):
            await tri_state_filter_manager.refresh(tri_state_filter)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if a tri_state_filter exists using the manager function.
        Args:
            tri_state_filter_manager (TriStateFilterManager): The tri_state_filter manager instance.
            session (AsyncSession): The async session object.
        Returns:
            None
        """
        # Add a tri_state_filter
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        # Check if the tri_state_filter exists using the manager function
        assert await tri_state_filter_manager.exists(tri_state_filter1.tri_state_filter_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        TriStateFilterManager class correctly compares two tri_state_filters.
        Args:
            tri_state_filter_manager (TriStateFilterManager): An instance of the
                TriStateFilterManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        # Add a tri_state_filter
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter2 = await tri_state_filter_manager.get_by_id(tri_state_filter_id=tri_state_filter1.tri_state_filter_id)
        assert tri_state_filter_manager.is_equal(tri_state_filter1, tri_state_filter2) is True
        tri_state_filter1_dict = tri_state_filter_manager.to_dict(tri_state_filter1)
        tri_state_filter3 = tri_state_filter_manager.from_dict(tri_state_filter1_dict)
        assert tri_state_filter_manager.is_equal(tri_state_filter1, tri_state_filter3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager
    ):
        """
        Test case to check if a tri_state_filter with a
        non-existent ID exists in the database.
        Args:
            tri_state_filter_manager (TriStateFilterManager): The
                instance of the TriStateFilterManager class.
        Returns:
            bool: True if the tri_state_filter exists, False otherwise.
        """
        non_existent_id = 999
        assert await tri_state_filter_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.
        Args:
            tri_state_filter_manager (TriStateFilterManager): The instance
                of the TriStateFilterManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not raised by the exists method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await tri_state_filter_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
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
        `get_by_pac_id` method when a tri_state_filter with
        a specific pac_id exists.
        Steps:
        1. Create a tri_state_filter using the TriStateFilterFactory.
        2. Fetch the tri_state_filter using the
            `get_by_pac_id` method of the tri_state_filter_manager.
        3. Assert that the fetched tri_state_filters list contains
            only one tri_state_filter.
        4. Assert that the fetched tri_state_filter is an instance
            of the TriStateFilter class.
        5. Assert that the code of the fetched tri_state_filter
            matches the code of the created tri_state_filter.
        6. Fetch the corresponding pac object
            using the pac_id of the created tri_state_filter.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            tri_state_filter matches the code of the fetched pac.
        """
        # Add a tri_state_filter with a specific pac_id
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        # Fetch the tri_state_filter using the manager function
        fetched_tri_state_filters = await tri_state_filter_manager.get_by_pac_id(tri_state_filter1.pac_id)
        assert len(fetched_tri_state_filters) == 1
        assert isinstance(fetched_tri_state_filters[0], TriStateFilter)
        assert fetched_tri_state_filters[0].code == tri_state_filter1.code
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
        fetched_tri_state_filters = await tri_state_filter_manager.get_by_pac_id(non_existent_id)
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
            await tri_state_filter_manager.get_by_pac_id(invalid_id)  # type: ignore
        await session.rollback()
    # stateIntValue,
# endset
