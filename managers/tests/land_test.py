# models/managers/tests/land_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `LandManager` class.
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
from managers.land import LandManager
from models import Land
from models.factory import LandFactory
from models.serialization_schema.land import LandSchema
class TestLandManager:
    """
    This class contains unit tests for the
    `LandManager` class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def land_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `LandManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return LandManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        land_manager: LandManager
    ):
        """
        Test case for the `build` method of
        `LandManager`.
        """
        # Define mock data for our land
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        land = await land_manager.build(**mock_data)
        # Assert that the returned object is an instance of Land
        assert isinstance(land, Land)
        # Assert that the attributes of the land match our mock data
        assert land.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `LandManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await land_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_land_to_database(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `LandManager` that checks if a
        land is correctly added to the database.
        """
        test_land = await LandFactory.build_async(session)
        assert test_land.land_id == 0
        # Add the land using the manager's add method
        added_land = await land_manager.add(land=test_land)
        assert isinstance(added_land, Land)
        assert str(added_land.insert_user_id) == (
            str(land_manager._session_context.customer_code))
        assert str(added_land.last_update_user_id) == (
            str(land_manager._session_context.customer_code))
        assert added_land.land_id > 0
        # Fetch the land from the database directly
        result = await session.execute(
            select(Land).filter(
                Land._land_id == added_land.land_id  # type: ignore
            )
        )
        fetched_land = result.scalars().first()
        # Assert that the fetched land is not None and matches the added land
        assert fetched_land is not None
        assert isinstance(fetched_land, Land)
        assert fetched_land.land_id == added_land.land_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_land_object(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `LandManager` that checks if the
        correct land object is returned.
        """
        # Create a test land using the LandFactory
        # without persisting it to the database
        test_land = await LandFactory.build_async(session)
        assert test_land.land_id == 0
        test_land.code = uuid.uuid4()
        # Add the land using the manager's add method
        added_land = await land_manager.add(land=test_land)
        assert isinstance(added_land, Land)
        assert str(added_land.insert_user_id) == (
            str(land_manager._session_context.customer_code))
        assert str(added_land.last_update_user_id) == (
            str(land_manager._session_context.customer_code))
        assert added_land.land_id > 0
        # Assert that the returned land matches the test land
        assert added_land.land_id == test_land.land_id
        assert added_land.code == test_land.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `LandManager`.
        """
        test_land = await LandFactory.create_async(session)
        land = await land_manager.get_by_id(test_land.land_id)
        assert isinstance(land, Land)
        assert test_land.land_id == land.land_id
        assert test_land.code == land.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        land_manager: LandManager
    ):
        """
        Test case for the `get_by_id` method of
        `LandManager` when the land is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_land = await land_manager.get_by_id(non_existent_id)
        assert retrieved_land is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_land(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `LandManager` that checks if a land is
        returned by its code.
        """
        test_land = await LandFactory.create_async(session)
        land = await land_manager.get_by_code(test_land.code)
        assert isinstance(land, Land)
        assert test_land.land_id == land.land_id
        assert test_land.code == land.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        land_manager: LandManager
    ):
        """
        Test case for the `get_by_code` method of
        `LandManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Land in the database
        random_code = uuid.uuid4()
        land = await land_manager.get_by_code(random_code)
        assert land is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `LandManager`
        that checks if a land is correctly updated.
        """
        test_land = await LandFactory.create_async(session)
        test_land.code = uuid.uuid4()
        updated_land = await land_manager.update(land=test_land)
        assert isinstance(updated_land, Land)
        assert str(updated_land.last_update_user_id) == str(
            land_manager._session_context.customer_code)
        assert updated_land.land_id == test_land.land_id
        assert updated_land.code == test_land.code
        result = await session.execute(
            select(Land).filter(
                Land._land_id == test_land.land_id)  # type: ignore
        )
        fetched_land = result.scalars().first()
        assert updated_land.land_id == fetched_land.land_id
        assert updated_land.code == fetched_land.code
        assert test_land.land_id == fetched_land.land_id
        assert test_land.code == fetched_land.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `LandManager`
        that checks if a land is correctly updated using a dictionary.
        """
        test_land = await LandFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_land = await land_manager.update(
            land=test_land,
            code=new_code
        )
        assert isinstance(updated_land, Land)
        assert str(updated_land.last_update_user_id) == str(
            land_manager._session_context.customer_code
        )
        assert updated_land.land_id == test_land.land_id
        assert updated_land.code == new_code
        result = await session.execute(
            select(Land).filter(
                Land._land_id == test_land.land_id)  # type: ignore
        )
        fetched_land = result.scalars().first()
        assert updated_land.land_id == fetched_land.land_id
        assert updated_land.code == fetched_land.code
        assert test_land.land_id == fetched_land.land_id
        assert new_code == fetched_land.code
    @pytest.mark.asyncio
    async def test_update_invalid_land(
        self,
        land_manager: LandManager
    ):
        """
        Test case for the `update` method of `LandManager`
        with an invalid land.
        """
        # None land
        land = None
        new_code = uuid.uuid4()
        updated_land = await (
            land_manager.update(land, code=new_code))  # type: ignore
        # Assertions
        assert updated_land is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `LandManager`
        with a nonexistent attribute.
        """
        test_land = await LandFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await land_manager.update(
                land=test_land,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `LandManager`.
        """
        land_data = await LandFactory.create_async(session)
        result = await session.execute(
            select(Land).filter(
                Land._land_id == land_data.land_id)  # type: ignore
        )
        fetched_land = result.scalars().first()
        assert isinstance(fetched_land, Land)
        assert fetched_land.land_id == land_data.land_id
        await land_manager.delete(
            land_id=land_data.land_id)
        result = await session.execute(
            select(Land).filter(
                Land._land_id == land_data.land_id)  # type: ignore
        )
        fetched_land = result.scalars().first()
        assert fetched_land is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent land.
        This test case ensures that when the delete method
        is called with the ID of a nonexistent land,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.
        :param land_manager: The instance of the LandManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await land_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a land
        with an invalid type.
        This test case ensures that when the `delete` method
        of the `land_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.
        Args:
            land_manager (LandManager): An instance of the
                `LandManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            Exception: If the `delete` method does not raise an exception.
        """
        with pytest.raises(Exception):
            await land_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `LandManager` class.
        This test verifies that the `get_list`
        method returns the correct list of lands.
        Steps:
        1. Call the `get_list` method of the
            `land_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 land objects using the
            `LandFactory.create_async` method.
        4. Assert that the `lands_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `land_manager` instance again.
        6. Assert that the returned list contains 5 lands.
        7. Assert that all elements in the returned list are
            instances of the `Land` class.
        """
        lands = await land_manager.get_list()
        assert len(lands) == 0
        lands_data = (
            [await LandFactory.create_async(session) for _ in range(5)])
        assert isinstance(lands_data, List)
        lands = await land_manager.get_list()
        assert len(lands) == 5
        assert all(isinstance(land, Land) for land in lands)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the LandManager class.
        Args:
            land_manager (LandManager): An instance of the
                LandManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        Raises:
            AssertionError: If the json_data is None.
        """
        land = await LandFactory.build_async(session)
        json_data = land_manager.to_json(land)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the LandManager class.
        Args:
            land_manager (LandManager): An instance of the
                LandManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        land = await LandFactory.build_async(session)
        dict_data = land_manager.to_dict(land)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `LandManager` class.
        This method tests the functionality of the
        `from_json` method of the `LandManager` class.
        It creates a land using the `LandFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        land is an instance of the `Land` class and has
        the same code as the original land.
        Args:
            land_manager (LandManager): An instance of the
                `LandManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        land = await LandFactory.create_async(session)
        json_data = land_manager.to_json(land)
        deserialized_land = land_manager.from_json(json_data)
        assert isinstance(deserialized_land, Land)
        assert deserialized_land.code == land.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `LandManager` class.
        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a land object.
        Args:
            land_manager (LandManager): An instance
                of the `LandManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        land = await LandFactory.create_async(session)
        schema = LandSchema()
        land_data = schema.dump(land)
        assert isinstance(land_data, dict)
        deserialized_land = land_manager.from_dict(land_data)
        assert isinstance(deserialized_land, Land)
        assert deserialized_land.code == land.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `LandManager` class.
        This test case verifies that the `add_bulk`
        method correctly adds multiple lands to the database.
        Steps:
        1. Generate a list of land data using the
            `LandFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `land_manager` instance, passing in the generated land data.
        3. Verify that the number of lands returned is
            equal to the number of lands added.
        4. For each updated land, fetch the corresponding
            land from the database.
        5. Verify that the fetched land is an instance of the
            `Land` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched land match the
            customer code of the session context.
        7. Verify that the land_id of the fetched
            land matches the land_id of the updated land.
        """
        lands_data = [
            await LandFactory.build_async(session) for _ in range(5)]
        lands = await land_manager.add_bulk(lands_data)
        assert len(lands) == 5
        for updated_land in lands:
            result = await session.execute(
                select(Land).filter(
                    Land._land_id == updated_land.land_id  # type: ignore
                )
            )
            fetched_land = result.scalars().first()
            assert isinstance(fetched_land, Land)
            assert str(fetched_land.insert_user_id) == (
                str(land_manager._session_context.customer_code))
            assert str(fetched_land.last_update_user_id) == (
                str(land_manager._session_context.customer_code))
            assert fetched_land.land_id == updated_land.land_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of lands.
        This test case verifies the functionality of the
        `update_bulk` method in the `LandManager` class.
        It creates two land instances, updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.
        Steps:
        1. Create two land instances using the
            `LandFactory.create_async` method.
        2. Generate new codes for the lands.
        3. Update the lands' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.
        Args:
            land_manager (LandManager): An instance of the
                `LandManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        # Mocking land instances
        land1 = await LandFactory.create_async(session=session)
        land2 = await LandFactory.create_async(session=session)
        logging.info(land1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update lands
        updates = [
            {
                "land_id": land1.land_id,
                "code": code_updated1
            },
            {
                "land_id": land2.land_id,
                "code": code_updated2
            }
        ]
        updated_lands = await land_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_lands) == 2
        logging.info(updated_lands[0].__dict__)
        logging.info(updated_lands[1].__dict__)
        logging.info('getall')
        lands = await land_manager.get_list()
        logging.info(lands[0].__dict__)
        logging.info(lands[1].__dict__)
        assert updated_lands[0].code == code_updated1
        assert updated_lands[1].code == code_updated2
        assert str(updated_lands[0].last_update_user_id) == (
            str(land_manager._session_context.customer_code))
        assert str(updated_lands[1].last_update_user_id) == (
            str(land_manager._session_context.customer_code))
        result = await session.execute(
            select(Land).filter(Land._land_id == 1)  # type: ignore
        )
        fetched_land = result.scalars().first()
        assert isinstance(fetched_land, Land)
        assert fetched_land.code == code_updated1
        result = await session.execute(
            select(Land).filter(Land._land_id == 2)  # type: ignore
        )
        fetched_land = result.scalars().first()
        assert isinstance(fetched_land, Land)
        assert fetched_land.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_land_id(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the land_id is missing.
        This test case ensures that when the land_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.
        Steps:
        1. Prepare the updates list with a missing land_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.
        """
        # No lands to update since land_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await land_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_land_not_found(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a land is not found.
        This test case performs the following steps:
        1. Defines a list of land updates, where each update
            contains a land_id and a code.
        2. Calls the update_bulk method of the
            land_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the land was not found.
        4. Rolls back the session to undo any changes made during the test.
        Note: This test assumes that the update_bulk method
        throws an exception when a land is not found.
        """
        # Update lands
        updates = [{"land_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await land_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        land_manager: LandManager,
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
        :param land_manager: An instance of the LandManager class.
        :param session: An instance of the AsyncSession class.
        """
        updates = [{"land_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await land_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        LandManager class.
        This test verifies that the delete_bulk method
        successfully deletes multiple lands
        from the database.
        Steps:
        1. Create two land objects using the LandFactory.
        2. Delete the lands using the delete_bulk method
            of the land_manager.
        3. Verify that the delete operation was successful by
            checking if the lands no longer exist in the database.
        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The lands should no longer exist in the database.
        """
        land1 = await LandFactory.create_async(session=session)
        land2 = await LandFactory.create_async(session=session)
        # Delete lands
        land_ids = [land1.land_id, land2.land_id]
        result = await land_manager.delete_bulk(land_ids)
        assert result is True
        for land_id in land_ids:
            execute_result = await session.execute(
                select(Land).filter(
                    Land._land_id == land_id)  # type: ignore
            )
            fetched_land = execute_result.scalars().first()
            assert fetched_land is None
    @pytest.mark.asyncio
    async def test_delete_bulk_lands_not_found(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        lands when some lands are not found.
        Steps:
        1. Create a land using the LandFactory.
        2. Assert that the created land is an instance of the
            Land class.
        3. Define a list of land IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk lands.
        5. Rollback the session to undo any changes made during the test.
        This test case ensures that the delete_bulk method of the
        LandManager raises an exception
        when some lands with the specified IDs are
        not found in the database.
        """
        land1 = await LandFactory.create_async(session=session)
        assert isinstance(land1, Land)
        # Delete lands
        land_ids = [1, 2]
        with pytest.raises(Exception):
            await land_manager.delete_bulk(land_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        land_manager: LandManager
    ):
        """
        Test case to verify the behavior of deleting
        lands with an empty list.
        Args:
            land_manager (LandManager): The instance of the
                LandManager class.
        Returns:
            None
        Raises:
            AssertionError: If the result is not True.
        """
        # Delete lands with an empty list
        land_ids = []
        result = await land_manager.delete_bulk(land_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid land IDs are provided.
        Args:
            land_manager (LandManager): The instance of the
                LandManager class.
            session (AsyncSession): The async session object.
        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.
        Returns:
            None
        """
        land_ids = ["1", 2]
        with pytest.raises(Exception):
            await land_manager.delete_bulk(land_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the LandManager class.
        This test case creates 5 land objects using the
        LandFactory and checks if the count method
        returns the correct count of lands.
        Steps:
        1. Create 5 land objects using the LandFactory.
        2. Call the count method of the land_manager.
        3. Assert that the count is equal to 5.
        """
        lands_data = (
            [await LandFactory.create_async(session) for _ in range(5)])
        assert isinstance(lands_data, List)
        count = await land_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        land_manager: LandManager
    ):
        """
        Test the count method when the database is empty.
        This test case checks if the count method of the
        LandManager class returns 0 when the database is empty.
        Args:
            land_manager (LandManager): An instance of the
                LandManager class.
        Returns:
            None
        """
        count = await land_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the 'get_sorted_list' method with basic sorting.
        This test case verifies that the 'get_sorted_list'
        method returns a list of lands
        sorted by the '_land_id' attribute in ascending order.
        Steps:
        1. Add lands to the database.
        2. Call the 'get_sorted_list' method with the
            sort_by parameter set to '_land_id'.
        3. Verify that the returned list of lands is
            sorted by the '_land_id' attribute.
        """
        # Add lands
        lands_data = (
            [await LandFactory.create_async(session) for _ in range(5)])
        assert isinstance(lands_data, List)
        sorted_lands = await land_manager.get_sorted_list(
            sort_by="_land_id")
        assert [land.land_id for land in sorted_lands] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        'get_sorted_list' method
        when sorting the list of lands in descending order.
        Steps:
        1. Create a list of lands using the LandFactory.
        2. Assert that the lands_data is of type List.
        3. Call the 'get_sorted_list' method with
            sort_by="land_id" and order="desc".
        4. Assert that the land_ids of the
            sorted_lands are in descending order.
        """
        # Add lands
        lands_data = (
            [await LandFactory.create_async(session) for _ in range(5)])
        assert isinstance(lands_data, List)
        sorted_lands = await land_manager.get_sorted_list(
            sort_by="land_id", order="desc")
        assert [land.land_id for land in sorted_lands] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to check if an AttributeError is raised when
        sorting the list by an invalid attribute.
        Args:
            land_manager (LandManager): The instance of the
                LandManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            AttributeError: If an invalid attribute is used for sorting.
        Returns:
            None
        """
        with pytest.raises(AttributeError):
            await land_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        land_manager: LandManager
    ):
        """
        Test case to verify the behavior of
        `get_sorted_list` method when the database is empty.
        This test ensures that when the database is empty, the
        `get_sorted_list` method returns an empty list.
        Args:
            land_manager (LandManager): An instance of the
                LandManager class.
        Returns:
            None
        """
        sorted_lands = await land_manager.get_sorted_list(sort_by="land_id")
        assert len(sorted_lands) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a land instance.
        This test performs the following steps:
        1. Creates a land instance using the LandFactory.
        2. Retrieves the land from the database to ensure
            it was added correctly.
        3. Updates the land's code and verifies the update.
        4. Refreshes the original land instance and checks if
            it reflects the updated code.
        Args:
            land_manager (LandManager): The manager responsible
                for land operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a land
        land1 = await LandFactory.create_async(session=session)
        # Retrieve the land from the database
        result = await session.execute(
            select(Land).filter(
                Land._land_id == land1.land_id)  # type: ignore
        )  # type: ignore
        land2 = result.scalars().first()
        # Verify that the retrieved land matches the added land
        assert land1.code == land2.code
        # Update the land's code
        updated_code1 = uuid.uuid4()
        land1.code = updated_code1
        updated_land1 = await land_manager.update(land1)
        # Verify that the updated land is of type Land
        # and has the updated code
        assert isinstance(updated_land1, Land)
        assert updated_land1.code == updated_code1
        # Refresh the original land instance
        refreshed_land2 = await land_manager.refresh(land2)
        # Verify that the refreshed land reflects the updated code
        assert refreshed_land2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_land(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent land.
        Args:
            land_manager (LandManager): The instance of the
                LandManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If the land refresh operation raises an exception.
        Returns:
            None
        """
        land = Land(land_id=999)
        with pytest.raises(Exception):
            await land_manager.refresh(land)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_land(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to check if a land exists using the manager function.
        Args:
            land_manager (LandManager): The land manager instance.
            session (AsyncSession): The async session object.
        Returns:
            None
        """
        # Add a land
        land1 = await LandFactory.create_async(session=session)
        # Check if the land exists using the manager function
        assert await land_manager.exists(land1.land_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_land(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        LandManager class correctly compares two lands.
        Args:
            land_manager (LandManager): An instance of the
                LandManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        # Add a land
        land1 = await LandFactory.create_async(session=session)
        land2 = await land_manager.get_by_id(land_id=land1.land_id)
        assert land_manager.is_equal(land1, land2) is True
        land1_dict = land_manager.to_dict(land1)
        land3 = land_manager.from_dict(land1_dict)
        assert land_manager.is_equal(land1, land3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_land(
        self,
        land_manager: LandManager
    ):
        """
        Test case to check if a land with a
        non-existent ID exists in the database.
        Args:
            land_manager (LandManager): The
                instance of the LandManager class.
        Returns:
            bool: True if the land exists, False otherwise.
        """
        non_existent_id = 999
        assert await land_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.
        Args:
            land_manager (LandManager): The instance
                of the LandManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not raised by the exists method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await land_manager.exists(invalid_id)  # type: ignore  # noqa: E501
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
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when a land with
        a specific pac_id exists.
        Steps:
        1. Create a land using the LandFactory.
        2. Fetch the land using the
            `get_by_pac_id` method of the land_manager.
        3. Assert that the fetched lands list contains
            only one land.
        4. Assert that the fetched land is an instance
            of the Land class.
        5. Assert that the code of the fetched land
            matches the code of the created land.
        6. Fetch the corresponding pac object
            using the pac_id of the created land.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            land matches the code of the fetched pac.
        """
        # Add a land with a specific pac_id
        land1 = await LandFactory.create_async(session=session)
        # Fetch the land using the manager function
        fetched_lands = await land_manager.get_by_pac_id(land1.pac_id)
        assert len(fetched_lands) == 1
        assert isinstance(fetched_lands[0], Land)
        assert fetched_lands[0].code == land1.code
        stmt = select(models.Pac).where(
            models.Pac._pac_id == land1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert isinstance(pac, models.Pac)
        assert fetched_lands[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        land_manager: LandManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.
        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_lands = await land_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_lands) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        land_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.
        Args:
            land_manager (LandManager): An
                instance of the LandManager class.
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
            await land_manager.get_by_pac_id(invalid_id)  # type: ignore
        await session.rollback()
# endset
