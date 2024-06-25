# models/managers/tests/flavor_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `FlavorManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
        flavor = await \
            flavor_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of Flavor
        assert isinstance(
            flavor,
            Flavor)

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
        test_flavor = await \
            FlavorFactory.build_async(
                session)

        assert test_flavor.flavor_id == 0

        # Add the flavor using the
        # manager's add method
        added_flavor = await \
            flavor_manager.add(
                flavor=test_flavor)

        assert isinstance(added_flavor,
                          Flavor)

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
        assert isinstance(fetched_flavor,
                          Flavor)
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
        test_flavor = await \
            FlavorFactory.build_async(
                session)

        assert test_flavor.flavor_id == 0

        test_flavor.code = uuid.uuid4()

        # Add the flavor using
        # the manager's add method
        added_flavor = await \
            flavor_manager.add(
                flavor=test_flavor)

        assert isinstance(added_flavor,
                          Flavor)

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
        test_flavor = await \
            FlavorFactory.create_async(
                session)

        test_flavor.code = uuid.uuid4()

        updated_flavor = await \
            flavor_manager.update(
                flavor=test_flavor)

        assert isinstance(updated_flavor,
                          Flavor)

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
        test_flavor = await \
            FlavorFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_flavor = await \
            flavor_manager.update(
                flavor=test_flavor,
                code=new_code
            )

        assert isinstance(updated_flavor,
                          Flavor)

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
        Test case for the `update` method of
        `FlavorManager`
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
        Test case for the `update` method of
        `FlavorManager`
        with a nonexistent attribute.
        """
        test_flavor = await \
            FlavorFactory.create_async(
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
        Test case for the `delete` method of
        `FlavorManager`.
        """
        flavor_data = await FlavorFactory.create_async(
            session)

        result = await session.execute(
            select(Flavor).filter(
                Flavor._flavor_id == flavor_data.flavor_id)  # type: ignore
        )
        fetched_flavor = result.scalars().first()

        assert isinstance(fetched_flavor,
                          Flavor)

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

        :param flavor_manager: The instance of the
            FlavorManager class.
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
            flavor_manager
            (FlavorManager): An
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
            flavor_manager
            (FlavorManager): An
                instance of the
                FlavorManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        flavor = await \
            FlavorFactory.build_async(
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
            flavor_manager
            (FlavorManager): An
                instance of the
                FlavorManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        flavor = await \
            FlavorFactory.build_async(
                session)

        dict_data = \
            flavor_manager.to_dict(
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
            flavor_manager
            (FlavorManager): An
                instance of the
                `FlavorManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        flavor = await \
            FlavorFactory.create_async(
                session)

        json_data = flavor_manager.to_json(
            flavor)

        deserialized_flavor = await \
                flavor_manager.from_json(json_data)

        assert isinstance(deserialized_flavor,
                          Flavor)
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
            flavor_manager
            (FlavorManager): An instance
                of the `FlavorManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        flavor = await \
            FlavorFactory.create_async(
                session)

        schema = FlavorSchema()

        flavor_data = schema.dump(flavor)

        assert isinstance(flavor_data, dict)

        deserialized_flavor = await \
            flavor_manager.from_dict(
                flavor_data)

        assert isinstance(deserialized_flavor,
                          Flavor)

        assert deserialized_flavor.code == \
            flavor.code

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
            flavor_manager
            (FlavorManager): An
                instance of the
                FlavorManager class.

        Returns:
            None
        """

        count = await flavor_manager.count()

        assert count == 0

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
            flavor_manager
            (FlavorManager): The
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
        assert isinstance(updated_flavor1,
                          Flavor)

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
            flavor_manager
            (FlavorManager): The
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
            flavor_manager
            (FlavorManager): The
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
            flavor_manager
            (FlavorManager): An
                instance of the
                FlavorManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a flavor
        flavor1 = await \
            FlavorFactory.create_async(
                session=session)

        flavor2 = await \
            flavor_manager.get_by_id(
                flavor_id=flavor1.flavor_id)

        assert flavor_manager.is_equal(
            flavor1, flavor2) is True

        flavor1_dict = \
            flavor_manager.to_dict(
                flavor1)

        flavor3 = await \
            flavor_manager.from_dict(
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
            flavor_manager
            (FlavorManager): The
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
            flavor_manager
            (FlavorManager): The instance
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

