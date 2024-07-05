# managers/tests/land_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `LandManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.land import (
    LandManager)
from models import Land
from models.factory import (
    LandFactory)
from models.serialization_schema.land import (
    LandSchema)


class TestLandManager:
    """
    This class contains unit tests for the
    `LandManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `LandManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return LandManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: LandManager
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
        land = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of Land
        assert isinstance(
            land,
            Land)

        # Assert that the attributes of the
        # land match our mock data
        assert land.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: LandManager,
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
            await obj_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_land_to_database(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `LandManager` that checks if a
        land is correctly added to the database.
        """
        new_obj = await \
            LandFactory.build_async(
                session)

        assert new_obj.land_id == 0

        # Add the land using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                land=new_obj)

        assert isinstance(added_obj,
                          Land)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.land_id > 0

        # Fetch the land from
        # the database directly
        result = await session.execute(
            select(Land).filter(
                Land._land_id == (
                    added_obj.land_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched land
        # is not None and matches the
        # added land
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          Land)
        assert fetched_obj.land_id == \
            added_obj.land_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_land_object(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `LandManager` that checks if the
        correct land object is returned.
        """
        # Create a test land
        # using the LandFactory
        # without persisting it to the database
        new_obj = await \
            LandFactory.build_async(
                session)

        assert new_obj.land_id == 0

        new_obj.code = uuid.uuid4()

        # Add the land using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                land=new_obj)

        assert isinstance(added_obj,
                          Land)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.land_id > 0

        # Assert that the returned
        # land matches the
        # test land
        assert added_obj.land_id == \
            new_obj.land_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `LandManager`
        that checks if a land
        is correctly updated.
        """
        new_obj = await \
            LandFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                land=new_obj)

        assert isinstance(updated_obj,
                          Land)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.land_id == \
            new_obj.land_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(Land).filter(
                Land._land_id == (
                    new_obj.land_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.land_id == \
            fetched_obj.land_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.land_id == \
            fetched_obj.land_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `LandManager`
        that checks if a land is
        correctly updated using a dictionary.
        """
        new_obj = await \
            LandFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                land=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          Land)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.land_id == \
            new_obj.land_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(Land).filter(
                Land._land_id == (
                    new_obj.land_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.land_id == \
            fetched_obj.land_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.land_id == \
            fetched_obj.land_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_land(
        self,
        obj_manager: LandManager
    ):
        """
        Test case for the `update` method of
        `LandManager`
        with an invalid land.
        """

        # None land
        land = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                land, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `LandManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            LandFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                land=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `LandManager`.
        """
        new_obj = await LandFactory.create_async(
            session)

        result = await session.execute(
            select(Land).filter(
                Land._land_id == (
                    new_obj.land_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Land)

        assert fetched_obj.land_id == \
            new_obj.land_id

        await obj_manager.delete(
            land_id=new_obj.land_id)

        result = await session.execute(
            select(Land).filter(
                Land._land_id == (
                    new_obj.land_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        land.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        land,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            LandManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a land
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (LandManager): An
                instance of the
                `LandManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await obj_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `LandManager` class.

        This test verifies that the `get_list`
        method returns the correct list of lands.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 land objects using the
            `LandFactory.create_async` method.
        4. Assert that the
            `lands_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 lands.
        7. Assert that all elements in the returned list are
            instances of the
            `Land` class.
        """

        lands = await obj_manager.get_list()

        assert len(lands) == 0

        lands_data = (
            [await LandFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(lands_data, List)

        lands = await obj_manager.get_list()

        assert len(lands) == 5
        assert all(isinstance(
            land,
            Land
        ) for land in lands)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the LandManager class.

        Args:
            obj_manager
            (LandManager): An
                instance of the
                LandManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        land = await \
            LandFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            land)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the LandManager class.

        Args:
            obj_manager
            (LandManager): An
                instance of the
                LandManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        land = await \
            LandFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                land)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `LandManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `LandManager` class.
        It creates a land using
        the `LandFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        land is an instance of the
        `Land` class and has
        the same code as the original land.

        Args:
            obj_manager
            (LandManager): An
                instance of the
                `LandManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        land = await \
            LandFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            land)

        deserialized_land = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_land,
                          Land)
        assert deserialized_land.code == \
            land.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `LandManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        land object.

        Args:
            obj_manager
            (LandManager): An instance
                of the `LandManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        land = await \
            LandFactory.create_async(
                session)

        schema = LandSchema()

        new_obj = schema.dump(land)

        assert isinstance(new_obj, dict)

        deserialized_land = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_land,
                          Land)

        assert deserialized_land.code == \
            land.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the LandManager class.

        This test case creates 5 land
        objects using the
        LandFactory and checks if the count method
        returns the correct count of
        lands.

        Steps:
        1. Create 5 land objects using
            the LandFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        lands_data = (
            [await LandFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(lands_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: LandManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        LandManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (LandManager): An
                instance of the
                LandManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a land instance.

        This test performs the following steps:
        1. Creates a land instance using
            the LandFactory.
        2. Retrieves the land from th
            database to ensure
            it was added correctly.
        3. Updates the land's code and verifies the update.
        4. Refreshes the original land instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (LandManager): The
                manager responsible
                for land operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a land
        obj_1 = await LandFactory.create_async(
            session=session)

        # Retrieve the land from the database
        result = await session.execute(
            select(Land).filter(
                Land._land_id == (
                    obj_1.land_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved land
        # matches the added land
        assert obj_1.code == \
            obj_2.code

        # Update the land's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated land
        # is of type Land
        # and has the updated code
        assert isinstance(updated_obj_1,
                          Land)

        assert updated_obj_1.code == updated_code1

        # Refresh the original land instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed land
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_land(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent land.

        Args:
            obj_manager
            (LandManager): The
                instance of the
                LandManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the land
            refresh operation raises an exception.

        Returns:
            None
        """
        land = Land(
            land_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                land)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_land(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to check if a land
        exists using the manager function.

        Args:
            obj_manager
            (LandManager): The
                land manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a land
        obj_1 = await LandFactory.create_async(
            session=session)

        # Check if the land exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.land_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_land(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        LandManager
        class correctly compares two
        lands.

        Args:
            obj_manager
            (LandManager): An
                instance of the
                LandManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a land
        obj_1 = await \
            LandFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                land_id=obj_1.land_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        land3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, land3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_land(
        self,
        obj_manager: LandManager
    ):
        """
        Test case to check if a land with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (LandManager): The
                instance of the LandManager class.

        Returns:
            bool: True if the land exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: LandManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (LandManager): The instance
                of the LandManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
