# managers/tests/plant_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `PlantManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.plant import (
    PlantManager)
from models import Plant
from models.factory import (
    PlantFactory)
from models.serialization_schema.plant import (
    PlantSchema)


class TestPlantManager:
    """
    This class contains unit tests for the
    `PlantManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `PlantManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return PlantManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: PlantManager
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
        plant = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of Plant
        assert isinstance(
            plant,
            Plant)

        # Assert that the attributes of the
        # plant match our mock data
        assert plant.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: PlantManager,
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
            await obj_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_plant_to_database(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `PlantManager` that checks if a
        plant is correctly added to the database.
        """
        new_obj = await \
            PlantFactory.build_async(
                session)

        assert new_obj.plant_id == 0

        # Add the plant using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                plant=new_obj)

        assert isinstance(added_obj,
                          Plant)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.plant_id > 0

        # Fetch the plant from
        # the database directly
        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == (
                    added_obj.plant_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched plant
        # is not None and matches the
        # added plant
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          Plant)
        assert fetched_obj.plant_id == \
            added_obj.plant_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_plant_object(
        self,
        obj_manager: PlantManager,
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
        new_obj = await \
            PlantFactory.build_async(
                session)

        assert new_obj.plant_id == 0

        new_obj.code = uuid.uuid4()

        # Add the plant using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                plant=new_obj)

        assert isinstance(added_obj,
                          Plant)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.plant_id > 0

        # Assert that the returned
        # plant matches the
        # test plant
        assert added_obj.plant_id == \
            new_obj.plant_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `PlantManager`
        that checks if a plant
        is correctly updated.
        """
        new_obj = await \
            PlantFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                plant=new_obj)

        assert isinstance(updated_obj,
                          Plant)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.plant_id == \
            new_obj.plant_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == (
                    new_obj.plant_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.plant_id == \
            fetched_obj.plant_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.plant_id == \
            fetched_obj.plant_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `PlantManager`
        that checks if a plant is
        correctly updated using a dictionary.
        """
        new_obj = await \
            PlantFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                plant=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          Plant)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.plant_id == \
            new_obj.plant_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == (
                    new_obj.plant_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.plant_id == \
            fetched_obj.plant_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.plant_id == \
            fetched_obj.plant_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_plant(
        self,
        obj_manager: PlantManager
    ):
        """
        Test case for the `update` method of
        `PlantManager`
        with an invalid plant.
        """

        # None plant
        plant = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                plant, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `PlantManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            PlantFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                plant=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `PlantManager`.
        """
        new_obj = await PlantFactory.create_async(
            session)

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == (
                    new_obj.plant_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Plant)

        assert fetched_obj.plant_id == \
            new_obj.plant_id

        await obj_manager.delete(
            plant_id=new_obj.plant_id)

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == (
                    new_obj.plant_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        plant.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        plant,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            PlantManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a plant
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (PlantManager): An
                instance of the
                `PlantManager` class.
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
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `PlantManager` class.

        This test verifies that the `get_list`
        method returns the correct list of plants.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 plant objects using the
            `PlantFactory.create_async` method.
        4. Assert that the
            `plants_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 plants.
        7. Assert that all elements in the returned list are
            instances of the
            `Plant` class.
        """

        plants = await obj_manager.get_list()

        assert len(plants) == 0

        plants_data = (
            [await PlantFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(plants_data, List)

        plants = await obj_manager.get_list()

        assert len(plants) == 5
        assert all(isinstance(
            plant,
            Plant
        ) for plant in plants)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the PlantManager class.

        Args:
            obj_manager
            (PlantManager): An
                instance of the
                PlantManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        plant = await \
            PlantFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            plant)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the PlantManager class.

        Args:
            obj_manager
            (PlantManager): An
                instance of the
                PlantManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        plant = await \
            PlantFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                plant)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `PlantManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `PlantManager` class.
        It creates a plant using
        the `PlantFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        plant is an instance of the
        `Plant` class and has
        the same code as the original plant.

        Args:
            obj_manager
            (PlantManager): An
                instance of the
                `PlantManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        plant = await \
            PlantFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            plant)

        deserialized_plant = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_plant,
                          Plant)
        assert deserialized_plant.code == \
            plant.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: PlantManager,
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
            obj_manager
            (PlantManager): An instance
                of the `PlantManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        plant = await \
            PlantFactory.create_async(
                session)

        schema = PlantSchema()

        new_obj = schema.dump(plant)

        assert isinstance(new_obj, dict)

        deserialized_plant = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_plant,
                          Plant)

        assert deserialized_plant.code == \
            plant.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: PlantManager,
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
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        plants_data = (
            [await PlantFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(plants_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: PlantManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        PlantManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (PlantManager): An
                instance of the
                PlantManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: PlantManager,
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
            obj_manager
            (PlantManager): The
                manager responsible
                for plant operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a plant
        obj_1 = await PlantFactory.create_async(
            session=session)

        # Retrieve the plant from the database
        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == (
                    obj_1.plant_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved plant
        # matches the added plant
        assert obj_1.code == \
            obj_2.code

        # Update the plant's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated plant
        # is of type Plant
        # and has the updated code
        assert isinstance(updated_obj_1,
                          Plant)

        assert updated_obj_1.code == updated_code1

        # Refresh the original plant instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed plant
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_plant(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent plant.

        Args:
            obj_manager
            (PlantManager): The
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
            await obj_manager.refresh(
                plant)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_plant(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to check if a plant
        exists using the manager function.

        Args:
            obj_manager
            (PlantManager): The
                plant manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a plant
        obj_1 = await PlantFactory.create_async(
            session=session)

        # Check if the plant exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.plant_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_plant(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        PlantManager
        class correctly compares two
        plants.

        Args:
            obj_manager
            (PlantManager): An
                instance of the
                PlantManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a plant
        obj_1 = await \
            PlantFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                plant_id=obj_1.plant_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        plant3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, plant3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_plant(
        self,
        obj_manager: PlantManager
    ):
        """
        Test case to check if a plant with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (PlantManager): The
                instance of the PlantManager class.

        Returns:
            bool: True if the plant exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (PlantManager): The instance
                of the PlantManager class.
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
# endset
