# models/managers/tests/plant_test.py

"""
    #TODO add comment
"""

import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.session_context import SessionContext
from models import Plant
import models
from models.factory import PlantFactory
from managers.plant import PlantManager
from models.serialization_schema.plant import PlantSchema
from services.db_config import DB_DIALECT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT, generate_uuid
from sqlalchemy import String
from sqlalchemy.future import select
import logging

DB_DIALECT = "sqlite"

# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)


class TestPlantManager:
    """
    #TODO add comment
    """

    @pytest_asyncio.fixture(scope="function")
    async def plant_manager(self, session: AsyncSession):
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return PlantManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Define mock data for our plant
        mock_data = {
            "code": generate_uuid()
        }

        # Call the build function of the manager
        plant = await plant_manager.build(**mock_data)

        # Assert that the returned object is an instance of Plant
        assert isinstance(plant, Plant)

        # Assert that the attributes of the plant match our mock data
        assert plant.code == mock_data["code"] 

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }

        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await plant_manager.build_async(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_plant_to_database(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_plant = await PlantFactory.build_async(session)

        assert test_plant.plant_id is None

        # Add the plant using the manager's add method
        added_plant = await plant_manager.add(plant=test_plant)

        assert isinstance(added_plant, Plant)

        assert str(added_plant.insert_user_id) == (
            str(plant_manager._session_context.customer_code))
        assert str(added_plant.last_update_user_id) == (
            str(plant_manager._session_context.customer_code))

        assert added_plant.plant_id > 0

        # Fetch the plant from the database directly
        result = await session.execute(
            select(Plant).filter(Plant.plant_id == added_plant.plant_id))
        fetched_plant = result.scalars().first()

        # Assert that the fetched plant is not None and matches the added plant
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
            #TODO add comment
        """
        # Create a test plant using the PlantFactory without persisting it to the database
        test_plant = await PlantFactory.build_async(session)

        assert test_plant.plant_id is None

        test_plant.code = generate_uuid()

        # Add the plant using the manager's add method
        added_plant = await plant_manager.add(plant=test_plant)

        assert isinstance(added_plant, Plant)

        assert str(added_plant.insert_user_id) == (
            str(plant_manager._session_context.customer_code))
        assert str(added_plant.last_update_user_id) == (
            str(plant_manager._session_context.customer_code))

        assert added_plant.plant_id > 0

        # Assert that the returned plant matches the test plant
        assert added_plant.plant_id == test_plant.plant_id
        assert added_plant.code == test_plant.code

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_plant = await PlantFactory.create_async(session)

        plant = await plant_manager.get_by_id(test_plant.plant_id)

        assert isinstance(plant, Plant)

        assert test_plant.plant_id == plant.plant_id
        assert test_plant.code == plant.code

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        non_existent_id = 9999  # An ID that's not in the database

        retrieved_plant = await plant_manager.get_by_id(non_existent_id)

        assert retrieved_plant is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_plant(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        test_plant = await PlantFactory.create_async(session)

        plant = await plant_manager.get_by_code(test_plant.code)

        assert isinstance(plant, Plant)

        assert test_plant.plant_id == plant.plant_id
        assert test_plant.code == plant.code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any Plant in the database
        random_code = generate_uuid()

        plant = await plant_manager.get_by_code(random_code)

        assert plant is None

    @pytest.mark.asyncio
    async def test_update(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_plant = await PlantFactory.create_async(session)

        test_plant.code = generate_uuid()

        updated_plant = await plant_manager.update(plant=test_plant)

        assert isinstance(updated_plant, Plant)

        assert str(updated_plant.last_update_user_id) == str(
            plant_manager._session_context.customer_code)

        assert updated_plant.plant_id == test_plant.plant_id
        assert updated_plant.code == test_plant.code

        result = await session.execute(
            select(Plant).filter(
                Plant.plant_id == test_plant.plant_id)
        )

        fetched_plant = result.scalars().first()

        assert updated_plant.plant_id == fetched_plant.plant_id
        assert updated_plant.code == fetched_plant.code

        assert test_plant.plant_id == fetched_plant.plant_id
        assert test_plant.code == fetched_plant.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_plant = await PlantFactory.create_async(session)

        new_code = generate_uuid()

        updated_plant = await plant_manager.update(
            plant=test_plant,
            code=new_code
        )

        assert isinstance(updated_plant, Plant)

        assert str(updated_plant.last_update_user_id) == str(
            plant_manager._session_context.customer_code
        )

        assert updated_plant.plant_id == test_plant.plant_id
        assert updated_plant.code == new_code

        result = await session.execute(
            select(Plant).filter(
                Plant.plant_id == test_plant.plant_id)
        )

        fetched_plant = result.scalars().first()

        assert updated_plant.plant_id == fetched_plant.plant_id
        assert updated_plant.code == fetched_plant.code

        assert test_plant.plant_id == fetched_plant.plant_id
        assert new_code == fetched_plant.code

    @pytest.mark.asyncio
    async def test_update_invalid_plant(self, plant_manager: PlantManager):
        # None plant
        plant = None

        new_code = generate_uuid()

        updated_plant = await plant_manager.update(plant, code=new_code)

        # Assertions
        assert updated_plant is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_plant = await PlantFactory.create_async(session)

        new_code = generate_uuid()

        with pytest.raises(ValueError):
            updated_plant = await plant_manager.update(
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
            #TODO add comment
        """
        plant_data = await PlantFactory.create_async(session)

        result = await session.execute(
            select(Plant).filter(Plant.plant_id == plant_data.plant_id))
        fetched_plant = result.scalars().first()

        assert isinstance(fetched_plant, Plant)

        assert fetched_plant.plant_id == plant_data.plant_id

        deleted_plant = await plant_manager.delete(
            plant_id=plant_data.plant_id)

        result = await session.execute(
            select(Plant).filter(Plant.plant_id == plant_data.plant_id))
        fetched_plant = result.scalars().first()

        assert fetched_plant is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """

        with pytest.raises(Exception):
            await plant_manager.delete("999")

        await session.rollback()


    @pytest.mark.asyncio
    async def test_get_list(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        plants = await plant_manager.get_list()

        assert len(plants) == 0

        plants_data = (
            [await PlantFactory.create_async(session) for _ in range(5)])

        plants = await plant_manager.get_list()

        assert len(plants) == 5
        assert all(isinstance(plant, Plant) for plant in plants)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        plant = await PlantFactory.build_async(session)

        json_data = plant_manager.to_json(plant)

        assert json_data is not None


    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        plant = await PlantFactory.build_async(session)

        dict_data = plant_manager.to_dict(plant)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        plant = await PlantFactory.create_async(session)

        json_data = plant_manager.to_json(plant)

        deserialized_plant = plant_manager.from_json(json_data)

        assert isinstance(deserialized_plant, Plant)
        assert deserialized_plant.code == plant.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        plant = await PlantFactory.create_async(session)

        schema = PlantSchema()

        plant_data = schema.dump(plant)

        deserialized_plant = plant_manager.from_dict(plant_data)

        assert isinstance(deserialized_plant, Plant)

        assert deserialized_plant.code == plant.code

    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        plants_data = [await PlantFactory.build_async(session) for _ in range(5)]

        plants = await plant_manager.add_bulk(plants_data)

        assert len(plants) == 5

        for updated_plant in plants:
            result = await session.execute(select(Plant).filter(Plant.plant_id == updated_plant.plant_id))
            fetched_plant = result.scalars().first()

            assert isinstance(fetched_plant, Plant)

            assert str(fetched_plant.insert_user_id) == (
                str(plant_manager._session_context.customer_code))
            assert str(fetched_plant.last_update_user_id) == (
                str(plant_manager._session_context.customer_code))

            assert fetched_plant.plant_id == updated_plant.plant_id


    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking plant instances
        plant1 = await PlantFactory.create_async(session=session)
        plant2 = await PlantFactory.create_async(session=session)
        logging.info(plant1.__dict__)

        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update plants
        updates = [
            {
                "plant_id": 1,
                "code": code_updated1
            },
            {
                "plant_id": 2,
                "code": code_updated2
            }
        ]
        updated_plants = await plant_manager.update_bulk(updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_plants) == 2
        logging.info(updated_plants[0].__dict__)
        logging.info(updated_plants[1].__dict__)

        logging.info('getall')
        plants = await plant_manager.get_list()
        logging.info(plants[0].__dict__)
        logging.info(plants[1].__dict__)

        assert updated_plants[0].code == code_updated1
        assert updated_plants[1].code == code_updated2

        assert str(updated_plants[0].last_update_user_id) == (
            str(plant_manager._session_context.customer_code))

        assert str(updated_plants[1].last_update_user_id) == (
            str(plant_manager._session_context.customer_code))

        result = await session.execute(select(Plant).filter(Plant.plant_id == 1))
        fetched_plant = result.scalars().first()

        assert isinstance(fetched_plant, Plant)

        assert fetched_plant.code == code_updated1

        result = await session.execute(select(Plant).filter(Plant.plant_id == 2))
        fetched_plant = result.scalars().first()

        assert isinstance(fetched_plant, Plant)

        assert fetched_plant.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_plant_id(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No plants to update since plant_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            updated_plants = await plant_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_plant_not_found(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        # Update plants
        updates = [{"plant_id": 1, "code": generate_uuid()}]

        with pytest.raises(Exception):
            updated_plants = await plant_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        updates = [{"plant_id": "2", "code": generate_uuid()}]

        with pytest.raises(Exception):
            updated_plants = await plant_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        plant1 = await PlantFactory.create_async(session=session)

        plant2 = await PlantFactory.create_async(session=session)

        # Delete plants
        plant_ids = [1, 2]
        result = await plant_manager.delete_bulk(plant_ids)

        assert result is True

        for plant_id in plant_ids:
            execute_result = await session.execute(
                select(Plant).filter(Plant.plant_id == plant_id))
            fetched_plant = execute_result.scalars().first()

            assert fetched_plant is None

    @pytest.mark.asyncio
    async def test_delete_bulk_plants_not_found(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        plant1 = await PlantFactory.create_async(session=session)

        # Delete plants
        plant_ids = [1, 2]

        with pytest.raises(Exception):
           result = await plant_manager.delete_bulk(plant_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        # Delete plants with an empty list
        plant_ids = []
        result = await plant_manager.delete_bulk(plant_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        plant_ids = ["1", 2]

        with pytest.raises(Exception):
           result = await plant_manager.delete_bulk(plant_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        plants_data = (
            [await PlantFactory.create_async(session) for _ in range(5)])

        count = await plant_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        count = await plant_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add plants
        plants_data = (
            [await PlantFactory.create_async(session) for _ in range(5)])

        sorted_plants = await plant_manager.get_sorted_list(sort_by="plant_id")

        assert [plant.plant_id for plant in sorted_plants] == (
            [(i + 1) for i in range(5)])

    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add plants
        plants_data = (
            [await PlantFactory.create_async(session) for _ in range(5)])

        sorted_plants = await plant_manager.get_sorted_list(
            sort_by="plant_id", order="desc")

        assert [plant.plant_id for plant in sorted_plants] == (
            [(i + 1) for i in reversed(range(5))])

    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        with pytest.raises(AttributeError):
            await plant_manager.get_sorted_list(sort_by="invalid_attribute")

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        sorted_plants = await plant_manager.get_sorted_list(sort_by="plant_id")

        assert len(sorted_plants) == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a plant
        plant1 = await PlantFactory.create_async(session=session)

        result = await session.execute(select(Plant).filter(Plant.plant_id == plant1.plant_id))
        plant2 = result.scalars().first()

        assert plant1.code == plant2.code

        updated_code1 = generate_uuid()
        plant1.code = updated_code1
        updated_plant1 = await plant_manager.update(plant1)

        assert updated_plant1.code == updated_code1

        refreshed_plant2 = await plant_manager.refresh(plant2)
        assert refreshed_plant2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_plant(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        plant = Plant(plant_id=999)

        with pytest.raises(Exception):
            await plant_manager.refresh(plant)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_plant(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a plant
        plant1 = await PlantFactory.create_async(session=session)

        # Check if the plant exists using the manager function

        assert await plant_manager.exists(plant1.plant_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_plant(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a plant
        plant1 = await PlantFactory.create_async(session=session)

        plant2 = await plant_manager.get_by_id(plant_id=plant1.plant_id)

        assert plant_manager.is_equal(plant1, plant2) is True

        plant1_dict = plant_manager.to_dict(plant1)

        plant3 = plant_manager.from_dict(plant1_dict)

        assert plant_manager.is_equal(plant1, plant3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_plant(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await plant_manager.exists(invalid_id)

        await session.rollback()
#endet

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
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a plant with a specific flvr_foreign_key_id
        plant1 = await PlantFactory.create_async(session=session)

        # Fetch the plant using the manager function

        fetched_plants = await plant_manager.get_by_flvr_foreign_key_id(
            plant1.flvr_foreign_key_id)
        assert len(fetched_plants) == 1
        assert isinstance(fetched_plants[0], Plant)
        assert fetched_plants[0].code == plant1.code

        stmt = select(models.Flavor).where(
            models.Flavor.flavor_id == plant1.flvr_foreign_key_id)
        result = await session.execute(stmt)
        flavor = result.scalars().first()

        assert fetched_plants[0].flvr_foreign_key_code_peek == flavor.code

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_nonexistent(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999

        fetched_plants = (
            await plant_manager.get_by_flvr_foreign_key_id(non_existent_id))
        assert len(fetched_plants) == 0

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_invalid_type(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await plant_manager.get_by_flvr_foreign_key_id(invalid_id)

        await session.rollback()

    # LandID
    @pytest.mark.asyncio
    async def test_get_by_land_id_existing(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        # Add a plant with a specific land_id
        plant1 = await PlantFactory.create_async(session=session)

        # Fetch the plant using the manager function

        fetched_plants = await plant_manager.get_by_land_id(plant1.land_id)
        assert len(fetched_plants) == 1
        assert isinstance(fetched_plants[0], Plant)
        assert fetched_plants[0].code == plant1.code

        stmt = select(models.Land).where(
            models.Land.land_id == plant1.land_id)
        result = await session.execute(stmt)
        land = result.scalars().first()

        assert fetched_plants[0].land_code_peek == land.code

    @pytest.mark.asyncio
    async def test_get_by_land_id_nonexistent(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        non_existent_id = 999

        fetched_plants = await plant_manager.get_by_land_id(non_existent_id)
        assert len(fetched_plants) == 0

    @pytest.mark.asyncio
    async def test_get_by_land_id_invalid_type(
        self,
        plant_manager: PlantManager,
        session: AsyncSession
    ):
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await plant_manager.get_by_land_id(invalid_id)

        await session.rollback()
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,
#endet
