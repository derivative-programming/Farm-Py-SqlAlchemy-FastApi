# models/managers/tests/plant_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `PlantManager` class.
"""

import logging
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


class TestPlantBulkManager:
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
    async def test_add_bulk(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `PlantManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        plants to the database.

        Steps:
        1. Generate a list of plant data using the
            `PlantFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated plant data.
        3. Verify that the number of plants
            returned is
            equal to the number of plants added.
        4. For each updated plant, fetch the corresponding
            plant from the database.
        5. Verify that the fetched plant
            is an instance of the
            `Plant` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            plant match the
            customer code of the session context.
        7. Verify that the plant_id of the fetched
            plant matches the
            plant_id of the updated
            plant.

        """
        plants_data = [
            await PlantFactory.build_async(session) for _ in range(5)]

        plants = await obj_manager.add_bulk(
            plants_data)

        assert len(plants) == 5

        for updated_obj in plants:
            result = await session.execute(
                select(Plant).filter(
                    Plant._plant_id == (
                        updated_obj.plant_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                Plant)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.plant_id == \
                updated_obj.plant_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of plants.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `PlantManager` class.
        It creates two plant instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two plant instances using the
            `PlantFactory.create_async` method.
        2. Generate new codes for the plants.
        3. Update the plants' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (PlantManager):
                An instance of the
                `PlantManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking plant instances
        obj_1 = await PlantFactory. \
            create_async(
                session=session)
        obj_2 = await PlantFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update plants
        updates = [
            {
                "plant_id":
                    obj_1.plant_id,
                "code": code_updated1
            },
            {
                "plant_id":
                    obj_2.plant_id,
                "code": code_updated2
            }
        ]
        updated_plants = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_plants) == 2
        logging.info(updated_plants[0]
                     .__dict__)
        logging.info(updated_plants[1]
                     .__dict__)

        logging.info('getall')
        plants = await obj_manager.get_list()
        logging.info(plants[0]
                     .__dict__)
        logging.info(plants[1]
                     .__dict__)

        assert updated_plants[0].code == \
            code_updated1
        assert updated_plants[1].code == \
            code_updated2

        assert str(updated_plants[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_plants[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Plant)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(Plant).filter(
                Plant._plant_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Plant)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_plant_id(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the plant_id is missing.

        This test case ensures that when the plant_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing plant_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No plants to update since
        # plant_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_plant_not_found(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a plant is not found.

        This test case performs the following steps:
        1. Defines a list of plant updates,
            where each update
            contains a plant_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the plant was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        plant is not found.

        """

        # Update plants
        updates = [{"plant_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: PlantManager,
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

        :param obj_manager: An instance of the
            PlantManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"plant_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        PlantManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple plants
        from the database.

        Steps:
        1. Create two plant objects
            using the PlantFactory.
        2. Delete the plants using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the plants
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The plants should
            no longer exist in the database.

        """

        obj_1 = await PlantFactory.create_async(
            session=session)

        obj_2 = await PlantFactory.create_async(
            session=session)

        # Delete plants
        plant_ids = [
            obj_1.plant_id,
            obj_2.plant_id
        ]
        result = await obj_manager.delete_bulk(
            plant_ids)

        assert result is True

        for plant_id in plant_ids:
            execute_result = await session.execute(
                select(Plant).filter(
                    Plant._plant_id == (
                        plant_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_plants_not_found(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        plants when some
        plants are not found.

        Steps:
        1. Create a plant using the
            PlantFactory.
        2. Assert that the created plant
            is an instance of the
            Plant class.
        3. Define a list of plant IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk plants.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        PlantManager raises an exception
        when some plants with the specified IDs are
        not found in the database.
        """
        obj_1 = await PlantFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          Plant)

        # Delete plants
        plant_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                plant_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: PlantManager
    ):
        """
        Test case to verify the behavior of deleting
        plants with an empty list.

        Args:
            obj_manager (PlantManager): The
                instance of the
                PlantManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete plants with an empty list
        plant_ids = []
        result = await obj_manager.delete_bulk(
            plant_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: PlantManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid plant IDs are provided.

        Args:
            obj_manager (PlantManager): The
                instance of the
                PlantManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        plant_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                plant_ids)

        await session.rollback()
