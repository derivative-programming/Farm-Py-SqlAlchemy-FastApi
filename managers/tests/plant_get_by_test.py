# models/managers/tests/plant_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `PlantManager` class.
"""

import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from helpers.session_context import SessionContext
from managers.plant import (
    PlantManager)
from models import Plant
from models.factory import (
    PlantFactory)


class TestPlantGetByManager:
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
        session_context = SessionContext(dict(), session)
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

        # Assert that the returned object is an instance of
        # Plant
        assert isinstance(
            plant,
            Plant)

        # Assert that the attributes of the
        # plant match our mock data
        assert plant.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `PlantManager`.
        """
        new_obj = await \
            PlantFactory.create_async(
                session)

        plant = await \
            obj_manager.get_by_id(
                new_obj.plant_id)

        assert isinstance(
            plant,
            Plant)

        assert new_obj.plant_id == \
            plant.plant_id
        assert new_obj.code == \
            plant.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        obj_manager: PlantManager
    ):
        """
        Test case for the `get_by_id` method of
        `PlantManager` when the
        plant is not found.
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_plant = await \
            obj_manager.get_by_id(
                non_existent_id)

        assert retrieved_plant is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_plant(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `PlantManager` that checks if
        a plant is
        returned by its code.
        """

        new_obj = await \
            PlantFactory.create_async(
                session)

        plant = await \
            obj_manager.get_by_code(
                new_obj.code)

        assert isinstance(
            plant,
            Plant)

        assert new_obj.plant_id == \
            plant.plant_id
        assert new_obj.code == \
            plant.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        obj_manager: PlantManager
    ):
        """
        Test case for the `get_by_code` method of
        `PlantManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Plant in the database
        random_code = uuid.uuid4()

        plant = await \
            obj_manager.get_by_code(
                random_code)

        assert plant is None

# endset

    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # FlvrForeignKeyID

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_existing(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_flvr_foreign_key_id` method
        when a plant with a
        specific flvr_foreign_key_id exists.

        Steps:
        1. Create a plant using the
            PlantFactory.
        2. Fetch the plant using the
            `get_by_flvr_foreign_key_id`
            method of the obj_manager.
        3. Assert that the fetched plants list has a length of 1.
        4. Assert that the first element in the fetched
            plants list is an instance of the
            Plant class.
        5. Assert that the code of the fetched
            plant
            matches the code of the created plant.
        6. Execute a select statement to fetch the
            Flavor object associated with the
            flvr_foreign_key_id.
        7. Assert that the fetched flavor is an
            instance of the Flavor class.
        8. Assert that the flvr_foreign_key_code_peek
            of the fetched plant matches
            the code of the fetched flavor.
        """
        # Add a plant with a specific
        # flvr_foreign_key_id
        obj_1 = await PlantFactory.create_async(
            session=session)

        # Fetch the plant using the
        # manager function

        fetched_objs = await \
            obj_manager.get_by_flvr_foreign_key_id(
                obj_1.flvr_foreign_key_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          Plant)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Flavor).where(
            models.Flavor._flavor_id == obj_1.flvr_foreign_key_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        flavor = result.scalars().first()

        assert isinstance(flavor, models.Flavor)

        assert fetched_objs[0].flvr_foreign_key_code_peek == flavor.code

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_nonexistent(
        self,
        obj_manager: PlantManager
    ):
        """
        Test case to verify the behavior of the
        'get_by_flvr_foreign_key_id' method
        when the provided foreign key ID does
        not exist in the database.

        This test ensures that when a non-existent
        foreign key ID is passed to the
        'get_by_flvr_foreign_key_id' method, it
        returns an empty list.

        Steps:
        1. Set a non-existent foreign key ID.
        2. Call the 'get_by_flvr_foreign_key_id'
            method with the non-existent ID.
        3. Assert that the returned list of fetched plants is empty.

        """
        non_existent_id = 999

        fetched_objs = (
            await obj_manager.get_by_flvr_foreign_key_id(
                non_existent_id))
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_invalid_type(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_flvr_foreign_key_id` method
        when an invalid foreign key ID type is provided.

        It ensures that an exception is raised
        when an invalid ID is passed to the method.

        Args:
            obj_manager (PlantManager): The
                instance of the PlantManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not
                raised when an invalid ID is passed.

        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_flvr_foreign_key_id(
                invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
    # LandID

    @pytest.mark.asyncio
    async def test_get_by_land_id_existing(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_land_id` method when
        a plant with
        a specific land_id exists.

        Steps:
        1. Create a plant using the
            PlantFactory.
        2. Fetch the plant using the
            `get_by_land_id` method of the obj_manager.
        3. Assert that the fetched plants list contains
            only one plant.
        4. Assert that the fetched plant
            is an instance
            of the Plant class.
        5. Assert that the code of the fetched plant
            matches the code of the created plant.
        6. Fetch the corresponding land object
            using the land_id of the created plant.
        7. Assert that the fetched land object is
            an instance of the Land class.
        8. Assert that the land_code_peek of the fetched
            plant matches the
            code of the fetched land.

        """
        # Add a plant with a specific
        # land_id
        obj_1 = await PlantFactory.create_async(
            session=session)

        # Fetch the plant using
        # the manager function

        fetched_objs = await \
            obj_manager.get_by_land_id(
                obj_1.land_id)
        assert len(fetched_objs) == 1
        assert isinstance(fetched_objs[0],
                          Plant)
        assert fetched_objs[0].code == \
            obj_1.code

        stmt = select(models.Land).where(
            models.Land._land_id == obj_1.land_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        land = result.scalars().first()

        assert isinstance(land, models.Land)

        assert fetched_objs[0].land_code_peek == land.code

    @pytest.mark.asyncio
    async def test_get_by_land_id_nonexistent(
        self,
        obj_manager: PlantManager
    ):
        """
        Test case to verify the behavior of the
        get_by_land_id method when the land ID does not exist.

        This test case ensures that when a non-existent
        land ID is provided to the get_by_land_id method,
        an empty list is returned.
        """

        non_existent_id = 999

        fetched_objs = await \
            obj_manager.get_by_land_id(
                non_existent_id)
        assert len(fetched_objs) == 0

    @pytest.mark.asyncio
    async def test_get_by_land_id_invalid_type(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_land_id` method when an invalid land ID is provided.

        Args:
            obj_manager (PlantManager): An
                instance of the PlantManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.

        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_land_id` method.

        Returns:
            None
        """

        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.get_by_land_id(
                invalid_id)  # type: ignore

        await session.rollback()
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,
# endset
