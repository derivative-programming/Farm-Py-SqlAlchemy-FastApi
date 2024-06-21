# models/managers/tests/flavor_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `FlavorManager` class.
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
from managers.flavor import FlavorManager
from models import Flavor
from models.factory import FlavorFactory
from models.serialization_schema.flavor import FlavorSchema
class TestFlavorManager:
    """
    This class contains unit tests for the
    `FlavorManager` class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def flavor_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `FlavorManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return FlavorManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case for the `build` method of
        `FlavorManager`.
        """
        # Define mock data for our flavor
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        flavor = await flavor_manager.build(
            **mock_data)
        # Assert that the returned object is an instance of Flavor
        assert isinstance(
            flavor, Flavor)
        # Assert that the attributes of the
        # flavor match our mock data
        assert flavor.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `FlavorManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await flavor_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_flavor_to_database(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `FlavorManager` that checks if a
        flavor is correctly added to the database.
        """
        test_flavor = await FlavorFactory.build_async(
            session)
        assert test_flavor.flavor_id == 0
        # Add the flavor using the
        # manager's add method
        added_flavor = await flavor_manager.add(
            flavor=test_flavor)
        assert isinstance(added_flavor, Flavor)
        assert str(added_flavor.insert_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert str(added_flavor.last_update_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert added_flavor.flavor_id > 0
        # Fetch the flavor from
        # the database directly
        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == added_flavor.flavor_id  # type: ignore
            )
        )
        fetched_flavor = result.scalars().first()
        # Assert that the fetched flavor
        # is not None and matches the
        # added flavor
        assert fetched_flavor is not None
        assert isinstance(fetched_flavor, Flavor)
        assert fetched_flavor.flavor_id == added_flavor.flavor_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_flavor_object(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `FlavorManager` that checks if the
        correct flavor object is returned.
        """
        # Create a test flavor
        # using the FlavorFactory
        # without persisting it to the database
        test_flavor = await FlavorFactory.build_async(
            session)
        assert test_flavor.flavor_id == 0
        test_flavor.code = uuid.uuid4()
        # Add the flavor using
        # the manager's add method
        added_flavor = await flavor_manager.add(
            flavor=test_flavor)
        assert isinstance(added_flavor, Flavor)
        assert str(added_flavor.insert_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert str(added_flavor.last_update_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert added_flavor.flavor_id > 0
        # Assert that the returned
        # flavor matches the
        # test flavor
        assert added_flavor.flavor_id == \
            test_flavor.flavor_id
        assert added_flavor.code == \
            test_flavor.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `FlavorManager`.
        """
        test_flavor = await FlavorFactory.create_async(
            session)
        flavor = await flavor_manager.get_by_id(
            test_flavor.flavor_id)
        assert isinstance(
            flavor, Flavor)
        assert test_flavor.flavor_id == \
            flavor.flavor_id
        assert test_flavor.code == \
            flavor.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case for the `get_by_id` method of
        `FlavorManager` when the
        flavor is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_flavor = await flavor_manager.get_by_id(
            non_existent_id)
        assert retrieved_flavor is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `FlavorManager` that checks if
        a flavor is
        returned by its code.
        """
        test_flavor = await FlavorFactory.create_async(
            session)
        flavor = await flavor_manager.get_by_code(
            test_flavor.code)
        assert isinstance(
            flavor, Flavor)
        assert test_flavor.flavor_id == \
            flavor.flavor_id
        assert test_flavor.code == \
            flavor.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case for the `get_by_code` method of
        `FlavorManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Flavor in the database
        random_code = uuid.uuid4()
        flavor = await flavor_manager.get_by_code(
            random_code)
        assert flavor is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `FlavorManager`
        that checks if a flavor
        is correctly updated.
        """
        test_flavor = await FlavorFactory.create_async(
            session)
        test_flavor.code = uuid.uuid4()
        updated_flavor = await flavor_manager.update(
            flavor=test_flavor)
        assert isinstance(updated_flavor, Flavor)
        assert str(updated_flavor.last_update_user_id) == str(
            flavor_manager._session_context.customer_code)
        assert updated_flavor.flavor_id == \
            test_flavor.flavor_id
        assert updated_flavor.code == \
            test_flavor.code
        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == test_flavor.flavor_id)  # type: ignore
        )
        fetched_flavor = result.scalars().first()
        assert updated_flavor.flavor_id == \
            fetched_flavor.flavor_id
        assert updated_flavor.code == \
            fetched_flavor.code
        assert test_flavor.flavor_id == \
            fetched_flavor.flavor_id
        assert test_flavor.code == \
            fetched_flavor.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `FlavorManager`
        that checks if a flavor is
        correctly updated using a dictionary.
        """
        test_flavor = await FlavorFactory.create_async(
            session)
        new_code = uuid.uuid4()
        updated_flavor = await flavor_manager.update(
            flavor=test_flavor,
            code=new_code
        )
        assert isinstance(updated_flavor, Flavor)
        assert str(updated_flavor.last_update_user_id) == str(
            flavor_manager._session_context.customer_code
        )
        assert updated_flavor.flavor_id == \
            test_flavor.flavor_id
        assert updated_flavor.code == new_code
        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == test_flavor.flavor_id)  # type: ignore
        )
        fetched_flavor = result.scalars().first()
        assert updated_flavor.flavor_id == \
            fetched_flavor.flavor_id
        assert updated_flavor.code == \
            fetched_flavor.code
        assert test_flavor.flavor_id == \
            fetched_flavor.flavor_id
        assert new_code == \
            fetched_flavor.code
    @pytest.mark.asyncio
    async def test_update_invalid_flavor(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case for the `update` method of `FlavorManager`
        with an invalid flavor.
        """
        # None flavor
        flavor = None
        new_code = uuid.uuid4()
        updated_flavor = await (
            flavor_manager.update(
                flavor, code=new_code))  # type: ignore
        # Assertions
        assert updated_flavor is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `FlavorManager`
        with a nonexistent attribute.
        """
        test_flavor = await FlavorFactory.create_async(
            session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await flavor_manager.update(
                flavor=test_flavor,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `FlavorManager`.
        """
        flavor_data = await FlavorFactory.create_async(
            session)
        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == flavor_data.flavor_id)  # type: ignore
        )
        fetched_flavor = result.scalars().first()
        assert isinstance(fetched_flavor, Flavor)
        assert fetched_flavor.flavor_id == \
            flavor_data.flavor_id
        await flavor_manager.delete(
            flavor_id=flavor_data.flavor_id)
        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == flavor_data.flavor_id)  # type: ignore
        )
        fetched_flavor = result.scalars().first()
        assert fetched_flavor is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent flavor.
        This test case ensures that when the delete method
        is called with the ID of a nonexistent flavor,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.
        :param flavor_manager: The instance of the FlavorManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await flavor_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a flavor
        with an invalid type.
        This test case ensures that when the `delete` method
        of the `flavor_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.
        Args:
            flavor_manager (FlavorManager): An
                instance of the
                `FlavorManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            Exception: If the `delete` method does not raise an exception.
        """
        with pytest.raises(Exception):
            await flavor_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `FlavorManager` class.
        This test verifies that the `get_list`
        method returns the correct list of flavors.
        Steps:
        1. Call the `get_list` method of the
            `flavor_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 flavor objects using the
            `FlavorFactory.create_async` method.
        4. Assert that the `flavors_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `flavor_manager` instance again.
        6. Assert that the returned list contains 5 flavors.
        7. Assert that all elements in the returned list are
            instances of the `Flavor` class.
        """
        flavors = await flavor_manager.get_list()
        assert len(flavors) == 0
        flavors_data = (
            [await FlavorFactory.create_async(session) for _ in range(5)])
        assert isinstance(flavors_data, List)
        flavors = await flavor_manager.get_list()
        assert len(flavors) == 5
        assert all(isinstance(
            flavor, Flavor) for flavor in flavors)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the FlavorManager class.
        Args:
            flavor_manager (FlavorManager): An
                instance of the
                FlavorManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        Raises:
            AssertionError: If the json_data is None.
        """
        flavor = await FlavorFactory.build_async(
            session)
        json_data = flavor_manager.to_json(
            flavor)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the FlavorManager class.
        Args:
            flavor_manager (FlavorManager): An
                instance of the
                FlavorManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        flavor = await FlavorFactory.build_async(
            session)
        dict_data = flavor_manager.to_dict(
            flavor)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `FlavorManager` class.
        This method tests the functionality of the
        `from_json` method of the `FlavorManager` class.
        It creates a flavor using
        the `FlavorFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        flavor is an instance of the
        `Flavor` class and has
        the same code as the original flavor.
        Args:
            flavor_manager (FlavorManager): An
            instance of the
                `FlavorManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        flavor = await FlavorFactory.create_async(
            session)
        json_data = flavor_manager.to_json(
            flavor)
        deserialized_flavor = flavor_manager.from_json(json_data)
        assert isinstance(deserialized_flavor, Flavor)
        assert deserialized_flavor.code == \
            flavor.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `FlavorManager` class.
        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        flavor object.
        Args:
            flavor_manager (FlavorManager): An instance
                of the `FlavorManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        flavor = await FlavorFactory.create_async(
            session)
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        assert isinstance(flavor_data, dict)
        deserialized_flavor = flavor_manager.from_dict(
            flavor_data)
        assert isinstance(deserialized_flavor, Flavor)
        assert deserialized_flavor.code == \
            flavor.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `FlavorManager` class.
        This test case verifies that the `add_bulk`
        method correctly adds multiple flavors to the database.
        Steps:
        1. Generate a list of flavor data using the
            `FlavorFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `flavor_manager` instance,
            passing in the
            generated flavor data.
        3. Verify that the number of flavors
            returned is
            equal to the number of flavors added.
        4. For each updated flavor, fetch the corresponding
            flavor from the database.
        5. Verify that the fetched flavor
            is an instance of the
            `Flavor` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            flavor match the
            customer code of the session context.
        7. Verify that the flavor_id of the fetched
            flavor matches the
            flavor_id of the updated
            flavor.
        """
        flavors_data = [
            await FlavorFactory.build_async(session) for _ in range(5)]
        flavors = await flavor_manager.add_bulk(
            flavors_data)
        assert len(flavors) == 5
        for updated_flavor in flavors:
            result = await session.execute(
                select(Flavor).filter(
                    Flavor._flavor_id == updated_flavor.flavor_id  # type: ignore
                )
            )
            fetched_flavor = result.scalars().first()
            assert isinstance(fetched_flavor, Flavor)
            assert str(fetched_flavor.insert_user_id) == (
                str(flavor_manager._session_context.customer_code))
            assert str(fetched_flavor.last_update_user_id) == (
                str(flavor_manager._session_context.customer_code))
            assert fetched_flavor.flavor_id == \
                updated_flavor.flavor_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of flavors.
        This test case verifies the functionality of the
        `update_bulk` method in the `FlavorManager` class.
        It creates two flavor instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.
        Steps:
        1. Create two flavor instances using the
            `FlavorFactory.create_async` method.
        2. Generate new codes for the flavors.
        3. Update the flavors' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.
        Args:
            flavor_manager (FlavorManager): An instance of the
                `FlavorManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        # Mocking flavor instances
        flavor1 = await FlavorFactory.create_async(
            session=session)
        flavor2 = await FlavorFactory.create_async(
            session=session)
        logging.info(flavor1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update flavors
        updates = [
            {
                "flavor_id": flavor1.flavor_id,
                "code": code_updated1
            },
            {
                "flavor_id": flavor2.flavor_id,
                "code": code_updated2
            }
        ]
        updated_flavors = await flavor_manager.update_bulk(
            updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_flavors) == 2
        logging.info(updated_flavors[0].__dict__)
        logging.info(updated_flavors[1].__dict__)
        logging.info('getall')
        flavors = await flavor_manager.get_list()
        logging.info(flavors[0].__dict__)
        logging.info(flavors[1].__dict__)
        assert updated_flavors[0].code == code_updated1
        assert updated_flavors[1].code == code_updated2
        assert str(updated_flavors[0].last_update_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert str(updated_flavors[1].last_update_user_id) == (
            str(flavor_manager._session_context.customer_code))
        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == 1)  # type: ignore
        )
        fetched_flavor = result.scalars().first()
        assert isinstance(fetched_flavor, Flavor)
        assert fetched_flavor.code == code_updated1
        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == 2)  # type: ignore
        )
        fetched_flavor = result.scalars().first()
        assert isinstance(fetched_flavor, Flavor)
        assert fetched_flavor.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_flavor_id(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the flavor_id is missing.
        This test case ensures that when the flavor_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.
        Steps:
        1. Prepare the updates list with a missing flavor_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.
        """
        # No flavors to update since flavor_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await flavor_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_flavor_not_found(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a flavor is not found.
        This test case performs the following steps:
        1. Defines a list of flavor updates,
            where each update
            contains a flavor_id and a code.
        2. Calls the update_bulk method of the
            flavor_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the flavor was not found.
        4. Rolls back the session to undo any changes made during the test.
        Note: This test assumes that the update_bulk method
        throws an exception when a
        flavor is not found.
        """
        # Update flavors
        updates = [{"flavor_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await flavor_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        flavor_manager: FlavorManager,
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
        :param flavor_manager: An instance of the FlavorManager class.
        :param session: An instance of the AsyncSession class.
        """
        updates = [{"flavor_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await flavor_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        FlavorManager class.
        This test verifies that the delete_bulk method
        successfully deletes multiple flavors
        from the database.
        Steps:
        1. Create two flavor objects
            using the FlavorFactory.
        2. Delete the flavors using the
            delete_bulk method
            of the flavor_manager.
        3. Verify that the delete operation was successful by
            checking if the flavors no longer exist in the database.
        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The flavors should no longer exist in the database.
        """
        flavor1 = await FlavorFactory.create_async(
            session=session)
        flavor2 = await FlavorFactory.create_async(
            session=session)
        # Delete flavors
        flavor_ids = [flavor1.flavor_id, flavor2.flavor_id]
        result = await flavor_manager.delete_bulk(
            flavor_ids)
        assert result is True
        for flavor_id in flavor_ids:
            execute_result = await session.execute(
                select(Flavor).filter(
                    Flavor._flavor_id == flavor_id)  # type: ignore
            )
            fetched_flavor = execute_result.scalars().first()
            assert fetched_flavor is None
    @pytest.mark.asyncio
    async def test_delete_bulk_flavors_not_found(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        flavors when some flavors are not found.
        Steps:
        1. Create a flavor using the
            FlavorFactory.
        2. Assert that the created flavor
            is an instance of the
            Flavor class.
        3. Define a list of flavor IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk flavors.
        5. Rollback the session to undo any changes made during the test.
        This test case ensures that the delete_bulk method of the
        FlavorManager raises an exception
        when some flavors with the specified IDs are
        not found in the database.
        """
        flavor1 = await FlavorFactory.create_async(
            session=session)
        assert isinstance(flavor1, Flavor)
        # Delete flavors
        flavor_ids = [1, 2]
        with pytest.raises(Exception):
            await flavor_manager.delete_bulk(
                flavor_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case to verify the behavior of deleting
        flavors with an empty list.
        Args:
            flavor_manager (FlavorManager): The
                instance of the
                FlavorManager class.
        Returns:
            None
        Raises:
            AssertionError: If the result is not True.
        """
        # Delete flavors with an empty list
        flavor_ids = []
        result = await flavor_manager.delete_bulk(
            flavor_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid flavor IDs are provided.
        Args:
            flavor_manager (FlavorManager): The
                instance of the
                FlavorManager class.
            session (AsyncSession): The async session object.
        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.
        Returns:
            None
        """
        flavor_ids = ["1", 2]
        with pytest.raises(Exception):
            await flavor_manager.delete_bulk(
                flavor_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the FlavorManager class.
        This test case creates 5 flavor
        objects using the
        FlavorFactory and checks if the count method
        returns the correct count of
        flavors.
        Steps:
        1. Create 5 flavor objects using
            the FlavorFactory.
        2. Call the count method of the flavor_manager.
        3. Assert that the count is equal to 5.
        """
        flavors_data = (
            [await FlavorFactory.create_async(session) for _ in range(5)])
        assert isinstance(flavors_data, List)
        count = await flavor_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test the count method when the database is empty.
        This test case checks if the count method of the
        FlavorManager class returns 0 when the database is empty.
        Args:
            flavor_manager (FlavorManager): An
                instance of the
                FlavorManager class.
        Returns:
            None
        """
        count = await flavor_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case for the 'get_sorted_list' method with basic sorting.
        This test case verifies that the 'get_sorted_list'
        method returns a list of flavors
        sorted by the '_flavor_id' attribute in ascending order.
        Steps:
        1. Add flavors to the database.
        2. Call the 'get_sorted_list' method with the
            sort_by parameter set to '_flavor_id'.
        3. Verify that the returned list of flavors is
            sorted by the '_flavor_id' attribute.
        """
        # Add flavors
        flavors_data = (
            [await FlavorFactory.create_async(session) for _ in range(5)])
        assert isinstance(flavors_data, List)
        sorted_flavors = await flavor_manager.get_sorted_list(
            sort_by="_flavor_id")
        assert [flavor.flavor_id for flavor in sorted_flavors] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        'get_sorted_list' method
        when sorting the list of flavors in descending order.
        Steps:
        1. Create a list of flavors using the FlavorFactory.
        2. Assert that the flavors_data is of type List.
        3. Call the 'get_sorted_list' method with
            sort_by="flavor_id" and order="desc".
        4. Assert that the flavor_ids of the
            sorted_flavors are in descending order.
        """
        # Add flavors
        flavors_data = (
            [await FlavorFactory.create_async(session) for _ in range(5)])
        assert isinstance(flavors_data, List)
        sorted_flavors = await flavor_manager.get_sorted_list(
            sort_by="flavor_id", order="desc")
        assert [flavor.flavor_id for flavor in sorted_flavors] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to check if an AttributeError is raised when
        sorting the list by an invalid attribute.
        Args:
            flavor_manager (FlavorManager): The
                instance of the
                FlavorManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            AttributeError: If an invalid attribute is used for sorting.
        Returns:
            None
        """
        with pytest.raises(AttributeError):
            await flavor_manager.get_sorted_list(
                sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case to verify the behavior of
        `get_sorted_list` method when the database is empty.
        This test ensures that when the database is empty, the
        `get_sorted_list` method returns an empty list.
        Args:
            flavor_manager (FlavorManager): An
                instance of the
                FlavorManager class.
        Returns:
            None
        """
        sorted_flavors = await flavor_manager.get_sorted_list(
            sort_by="flavor_id")
        assert len(sorted_flavors) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a flavor instance.
        This test performs the following steps:
        1. Creates a flavor instance using
            the FlavorFactory.
        2. Retrieves the flavor from th
            database to ensure
            it was added correctly.
        3. Updates the flavor's code and verifies the update.
        4. Refreshes the original flavor instance
            and checks if
            it reflects the updated code.
        Args:
            flavor_manager (FlavorManager): The
                manager responsible
                for flavor operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a flavor
        flavor1 = await FlavorFactory.create_async(
            session=session)
        # Retrieve the flavor from the database
        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == flavor1.flavor_id)  # type: ignore
        )  # type: ignore
        flavor2 = result.scalars().first()
        # Verify that the retrieved flavor
        # matches the added flavor
        assert flavor1.code == \
            flavor2.code
        # Update the flavor's code
        updated_code1 = uuid.uuid4()
        flavor1.code = updated_code1
        updated_flavor1 = await flavor_manager.update(
            flavor1)
        # Verify that the updated flavor
        # is of type Flavor
        # and has the updated code
        assert isinstance(updated_flavor1, Flavor)
        assert updated_flavor1.code == updated_code1
        # Refresh the original flavor instance
        refreshed_flavor2 = await flavor_manager.refresh(
            flavor2)
        # Verify that the refreshed flavor
        # reflects the updated code
        assert refreshed_flavor2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent flavor.
        Args:
            flavor_manager (FlavorManager): The
                instance of the
                FlavorManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If the flavor
            refresh operation raises an exception.
        Returns:
            None
        """
        flavor = Flavor(
            flavor_id=999)
        with pytest.raises(Exception):
            await flavor_manager.refresh(
                flavor)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to check if a flavor
        exists using the manager function.
        Args:
            flavor_manager (FlavorManager): The
                flavor manager instance.
            session (AsyncSession): The async session object.
        Returns:
            None
        """
        # Add a flavor
        flavor1 = await FlavorFactory.create_async(
            session=session)
        # Check if the flavor exists
        # using the manager function
        assert await flavor_manager.exists(
            flavor1.flavor_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        FlavorManager class correctly compares two flavors.
        Args:
            flavor_manager (FlavorManager): An
                instance of the
                FlavorManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        # Add a flavor
        flavor1 = await FlavorFactory.create_async(
            session=session)
        flavor2 = await flavor_manager.get_by_id(
            flavor_id=flavor1.flavor_id)
        assert flavor_manager.is_equal(
            flavor1, flavor2) is True
        flavor1_dict = flavor_manager.to_dict(
            flavor1)
        flavor3 = flavor_manager.from_dict(
            flavor1_dict)
        assert flavor_manager.is_equal(
            flavor1, flavor3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_flavor(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case to check if a flavor with a
        non-existent ID exists in the database.
        Args:
            flavor_manager (FlavorManager): The
                instance of the FlavorManager class.
        Returns:
            bool: True if the flavor exists,
                False otherwise.
        """
        non_existent_id = 999
        assert await flavor_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.
        Args:
            flavor_manager (FlavorManager): The instance
                of the FlavorManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not raised by the exists method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await flavor_manager.exists(invalid_id)  # type: ignore  # noqa: E501
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
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a flavor with
        a specific pac_id exists.
        Steps:
        1. Create a flavor using the
            FlavorFactory.
        2. Fetch the flavor using the
            `get_by_pac_id` method of the flavor_manager.
        3. Assert that the fetched flavors list contains
            only one flavor.
        4. Assert that the fetched flavor
            is an instance
            of the Flavor class.
        5. Assert that the code of the fetched flavor
            matches the code of the created flavor.
        6. Fetch the corresponding pac object
            using the pac_id of the created flavor.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            flavor matches the
            code of the fetched pac.
        """
        # Add a flavor with a specific
        # pac_id
        flavor1 = await FlavorFactory.create_async(
            session=session)
        # Fetch the flavor using
        # the manager function
        fetched_flavors = await flavor_manager.get_by_pac_id(
            flavor1.pac_id)
        assert len(fetched_flavors) == 1
        assert isinstance(fetched_flavors[0], Flavor)
        assert fetched_flavors[0].code == \
            flavor1.code
        stmt = select(models.Pac).where(
            models.Pac._pac_id == flavor1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert isinstance(pac, models.Pac)
        assert fetched_flavors[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        flavor_manager: FlavorManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.
        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_flavors = await flavor_manager.get_by_pac_id(
            non_existent_id)
        assert len(fetched_flavors) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.
        Args:
            flavor_manager (FlavorManager): An
                instance of the FlavorManager class.
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
            await flavor_manager.get_by_pac_id(
                invalid_id)  # type: ignore
        await session.rollback()
# endset
