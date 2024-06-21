# models/managers/tests/plant_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `PlantManager` class.
"""

from typing import List
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.plant import PlantManager
from models import Plant
from models.factory import PlantFactory
from models.serialization_schema.plant import PlantSchema


class TestPlantManager:
    """
    This class contains unit tests for the
    `PlantManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def plant_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `PlantManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return PlantManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        plant_manager: PlantManager
    ):
        """
        Test case for the `build` method of
        `PlantManager`.
        """
        # Define mock data for our plant
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        plant = await plant_manager.build(
            **mock_data)

        # Assert that the returned object is an instance of Plant
        assert isinstance(
            plant, Plant)

        # Assert that the attributes of the
        # plant match our mock data
        assert plant.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `PlantManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }

        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await plant_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_plant_to_database(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `PlantManager` that checks if a
        plant is correctly added to the database.
        """
        test_plant = await PlantFactory.build_async(
            session)

        assert test_plant.plant_id == 0

        # Add the plant using the
        # manager's add method
        added_plant = await plant_manager.add(
            plant=test_plant)

        assert isinstance(added_plant, Plant)

        assert str(added_plant.insert_user_id) == (
            str(plant_manager._session_context.customer_code))
        assert str(added_plant.last_update_user_id) == (
            str(plant_manager._session_context.customer_code))

        assert added_plant.plant_id > 0

        # Fetch the plant from
        # the database directly
        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == added_plant.plant_id  # type: ignore
            )
        )
        fetched_plant = result.scalars().first()

        # Assert that the fetched plant
        # is not None and matches the
        # added plant
        assert fetched_plant is not None
        assert isinstance(fetched_plant, Plant)
        assert fetched_plant.plant_id == added_plant.plant_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_plant_object(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `PlantManager` that checks if the
        correct plant object is returned.
        """
        # Create a test plant
        # using the PlantFactory
        # without persisting it to the database
        test_plant = await PlantFactory.build_async(
            session)

        assert test_plant.plant_id == 0

        test_plant.code = uuid.uuid4()

        # Add the plant using
        # the manager's add method
        added_plant = await plant_manager.add(
            plant=test_plant)

        assert isinstance(added_plant, Plant)

        assert str(added_plant.insert_user_id) == (
            str(plant_manager._session_context.customer_code))
        assert str(added_plant.last_update_user_id) == (
            str(plant_manager._session_context.customer_code))

        assert added_plant.plant_id > 0

        # Assert that the returned
        # plant matches the
        # test plant
        assert added_plant.plant_id == \
            test_plant.plant_id
        assert added_plant.code == \
            test_plant.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `PlantManager`
        that checks if a plant
        is correctly updated.
        """
        test_plant = await PlantFactory.create_async(
            session)

        test_plant.code = uuid.uuid4()

        updated_plant = await plant_manager.update(
            plant=test_plant)

        assert isinstance(updated_plant, Plant)

        assert str(updated_plant.last_update_user_id) == str(
            plant_manager._session_context.customer_code)

        assert updated_plant.plant_id == \
            test_plant.plant_id
        assert updated_plant.code == \
            test_plant.code

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == test_plant.plant_id)  # type: ignore
        )

        fetched_plant = result.scalars().first()

        assert updated_plant.plant_id == \
            fetched_plant.plant_id
        assert updated_plant.code == \
            fetched_plant.code

        assert test_plant.plant_id == \
            fetched_plant.plant_id
        assert test_plant.code == \
            fetched_plant.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `PlantManager`
        that checks if a plant is
        correctly updated using a dictionary.
        """
        test_plant = await PlantFactory.create_async(
            session)

        new_code = uuid.uuid4()

        updated_plant = await plant_manager.update(
            plant=test_plant,
            code=new_code
        )

        assert isinstance(updated_plant, Plant)

        assert str(updated_plant.last_update_user_id) == str(
            plant_manager._session_context.customer_code
        )

        assert updated_plant.plant_id == \
            test_plant.plant_id
        assert updated_plant.code == new_code

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == test_plant.plant_id)  # type: ignore
        )

        fetched_plant = result.scalars().first()

        assert updated_plant.plant_id == \
            fetched_plant.plant_id
        assert updated_plant.code == \
            fetched_plant.code

        assert test_plant.plant_id == \
            fetched_plant.plant_id
        assert new_code == \
            fetched_plant.code

    @pytest.mark.asyncio
    async def test_update_invalid_plant(
        self,
        plant_manager: PlantManager
    ):
        """
        Test case for the `update` method of `PlantManager`
        with an invalid plant.
        """

        # None plant
        plant = None

        new_code = uuid.uuid4()

        updated_plant = await (
            plant_manager.update(
                plant, code=new_code))  # type: ignore

        # Assertions
        assert updated_plant is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `PlantManager`
        with a nonexistent attribute.
        """
        test_plant = await PlantFactory.create_async(
            session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await plant_manager.update(
                plant=test_plant,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `PlantManager`.
        """
        plant_data = await PlantFactory.create_async(
            session)

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == plant_data.plant_id)  # type: ignore
        )
        fetched_plant = result.scalars().first()

        assert isinstance(fetched_plant, Plant)

        assert fetched_plant.plant_id == \
            plant_data.plant_id

        await plant_manager.delete(
            plant_id=plant_data.plant_id)

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == plant_data.plant_id)  # type: ignore
        )
        fetched_plant = result.scalars().first()

        assert fetched_plant is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent plant.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent plant,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param plant_manager: The instance of the PlantManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await plant_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a plant
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `plant_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            plant_manager (PlantManager): An
                instance of the
                `PlantManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await plant_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `PlantManager` class.

        This test verifies that the `get_list`
        method returns the correct list of plants.

        Steps:
        1. Call the `get_list` method of the
            `plant_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 plant objects using the
            `PlantFactory.create_async` method.
        4. Assert that the `plants_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `plant_manager` instance again.
        6. Assert that the returned list contains 5 plants.
        7. Assert that all elements in the returned list are
            instances of the `Plant` class.
        """

        plants = await plant_manager.get_list()

        assert len(plants) == 0

        plants_data = (
            [await PlantFactory.create_async(session) for _ in range(5)])

        assert isinstance(plants_data, List)

        plants = await plant_manager.get_list()

        assert len(plants) == 5
        assert all(isinstance(
            plant, Plant) for plant in plants)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the PlantManager class.

        Args:
            plant_manager (PlantManager): An
                instance of the
                PlantManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        plant = await PlantFactory.build_async(
            session)

        json_data = plant_manager.to_json(
            plant)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the PlantManager class.

        Args:
            plant_manager (PlantManager): An
                instance of the
                PlantManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        plant = await PlantFactory.build_async(
            session)

        dict_data = plant_manager.to_dict(
            plant)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `PlantManager` class.

        This method tests the functionality of the
        `from_json` method of the `PlantManager` class.
        It creates a plant using
        the `PlantFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        plant is an instance of the
        `Plant` class and has
        the same code as the original plant.

        Args:
            plant_manager (PlantManager): An
            instance of the
                `PlantManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        plant = await PlantFactory.create_async(
            session)

        json_data = plant_manager.to_json(
            plant)

        deserialized_plant = plant_manager.from_json(json_data)

        assert isinstance(deserialized_plant, Plant)
        assert deserialized_plant.code == \
            plant.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `PlantManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        plant object.

        Args:
            plant_manager (PlantManager): An instance
                of the `PlantManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        plant = await PlantFactory.create_async(
            session)

        schema = PlantSchema()

        plant_data = schema.dump(plant)

        assert isinstance(plant_data, dict)

        deserialized_plant = plant_manager.from_dict(
            plant_data)

        assert isinstance(deserialized_plant, Plant)

        assert deserialized_plant.code == \
            plant.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the PlantManager class.

        This test case creates 5 plant
        objects using the
        PlantFactory and checks if the count method
        returns the correct count of
        plants.

        Steps:
        1. Create 5 plant objects using
            the PlantFactory.
        2. Call the count method of the plant_manager.
        3. Assert that the count is equal to 5.

        """
        plants_data = (
            [await PlantFactory.create_async(session) for _ in range(5)])

        assert isinstance(plants_data, List)

        count = await plant_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        plant_manager: PlantManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        PlantManager class returns 0 when the database is empty.

        Args:
            plant_manager (PlantManager): An
                instance of the
                PlantManager class.

        Returns:
            None
        """

        count = await plant_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a plant instance.

        This test performs the following steps:
        1. Creates a plant instance using
            the PlantFactory.
        2. Retrieves the plant from th
            database to ensure
            it was added correctly.
        3. Updates the plant's code and verifies the update.
        4. Refreshes the original plant instance
            and checks if
            it reflects the updated code.

        Args:
            plant_manager (PlantManager): The
                manager responsible
                for plant operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a plant
        plant1 = await PlantFactory.create_async(
            session=session)

        # Retrieve the plant from the database
        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == plant1.plant_id)  # type: ignore
        )  # type: ignore
        plant2 = result.scalars().first()

        # Verify that the retrieved plant
        # matches the added plant
        assert plant1.code == \
            plant2.code

        # Update the plant's code
        updated_code1 = uuid.uuid4()
        plant1.code = updated_code1
        updated_plant1 = await plant_manager.update(
            plant1)

        # Verify that the updated plant
        # is of type Plant
        # and has the updated code
        assert isinstance(updated_plant1, Plant)

        assert updated_plant1.code == updated_code1

        # Refresh the original plant instance
        refreshed_plant2 = await plant_manager.refresh(
            plant2)

        # Verify that the refreshed plant
        # reflects the updated code
        assert refreshed_plant2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_plant(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent plant.

        Args:
            plant_manager (PlantManager): The
                instance of the
                PlantManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the plant
            refresh operation raises an exception.

        Returns:
            None
        """
        plant = Plant(
            plant_id=999)

        with pytest.raises(Exception):
            await plant_manager.refresh(
                plant)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_plant(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to check if a plant
        exists using the manager function.

        Args:
            plant_manager (PlantManager): The
                plant manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a plant
        plant1 = await PlantFactory.create_async(
            session=session)

        # Check if the plant exists
        # using the manager function
        assert await plant_manager.exists(
            plant1.plant_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_plant(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        PlantManager class correctly compares two plants.

        Args:
            plant_manager (PlantManager): An
                instance of the
                PlantManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a plant
        plant1 = await PlantFactory.create_async(
            session=session)

        plant2 = await plant_manager.get_by_id(
            plant_id=plant1.plant_id)

        assert plant_manager.is_equal(
            plant1, plant2) is True

        plant1_dict = plant_manager.to_dict(
            plant1)

        plant3 = plant_manager.from_dict(
            plant1_dict)

        assert plant_manager.is_equal(
            plant1, plant3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_plant(
        self,
        plant_manager: PlantManager
    ):
        """
        Test case to check if a plant with a
        non-existent ID exists in the database.

        Args:
            plant_manager (PlantManager): The
                instance of the PlantManager class.

        Returns:
            bool: True if the plant exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await plant_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            plant_manager (PlantManager): The instance
                of the PlantManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await plant_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
# endset
