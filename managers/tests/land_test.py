import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, Land
from models.factory import LandFactory
from managers.land import LandManager
from models.serialization_schema.land import LandSchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
# DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestLandManager:
    @pytest_asyncio.fixture(scope="function")
    async def land_manager(self, session:AsyncSession):
        return LandManager(session)
    @pytest.mark.asyncio
    async def test_build(self, land_manager:LandManager, session:AsyncSession):
        # Define some mock data for our land
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        land = await land_manager.build(**mock_data)
        # Assert that the returned object is an instance of Land
        assert isinstance(land, Land)
        # Assert that the attributes of the land match our mock data
        assert land.code == mock_data["code"]
        # Optionally, if the build method has some default values or computations:
        # assert land.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, land_manager:LandManager, session:AsyncSession):
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await land_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_land_to_database(self, land_manager:LandManager, session:AsyncSession):
        test_land = await LandFactory.build_async(session)
        assert test_land.land_id is None
        # Add the land using the manager's add method
        added_land = await land_manager.add(land=test_land)
        assert isinstance(added_land, Land)
        assert added_land.land_id > 0
        # Fetch the land from the database directly
        result = await session.execute(select(Land).filter(Land.land_id == added_land.land_id))
        fetched_land = result.scalars().first()
        # Assert that the fetched land is not None and matches the added land
        assert fetched_land is not None
        assert isinstance(fetched_land, Land)
        assert fetched_land.land_id == added_land.land_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_land_object(self, land_manager:LandManager, session:AsyncSession):
        # Create a test land using the LandFactory without persisting it to the database
        test_land = await LandFactory.build_async(session)
        assert test_land.land_id is None
        test_land.code = generate_uuid()
        # Add the land using the manager's add method
        added_land = await land_manager.add(land=test_land)
        assert isinstance(added_land, Land)
        assert added_land.land_id > 0
        # Assert that the returned land matches the test land
        assert added_land.land_id == test_land.land_id
        assert added_land.code == test_land.code
    @pytest.mark.asyncio
    async def test_get_by_id(self, land_manager:LandManager, session:AsyncSession):
        test_land = await LandFactory.create_async(session)
        land = await land_manager.get_by_id(test_land.land_id)
        assert isinstance(land, Land)
        assert test_land.land_id == land.land_id
        assert test_land.code == land.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, land_manager:LandManager, session: AsyncSession):
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_land = await land_manager.get_by_id(non_existent_id)
        assert retrieved_land is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_land(self, land_manager:LandManager, session:AsyncSession):
        test_land = await LandFactory.create_async(session)
        land = await land_manager.get_by_code(test_land.code)
        assert isinstance(land, Land)
        assert test_land.land_id == land.land_id
        assert test_land.code == land.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, land_manager:LandManager, session:AsyncSession):
        # Generate a random UUID that doesn't correspond to any Land in the database
        random_code = generate_uuid()
        land = await land_manager.get_by_code(random_code)
        assert land is None
    @pytest.mark.asyncio
    async def test_update(self, land_manager:LandManager, session:AsyncSession):
        test_land = await LandFactory.create_async(session)
        test_land.code = generate_uuid()
        updated_land = await land_manager.update(land=test_land)
        assert isinstance(updated_land, Land)
        assert updated_land.land_id == test_land.land_id
        assert updated_land.code == test_land.code
        result = await session.execute(select(Land).filter(Land.land_id == test_land.land_id))
        fetched_land = result.scalars().first()
        assert updated_land.land_id == fetched_land.land_id
        assert updated_land.code == fetched_land.code
        assert test_land.land_id == fetched_land.land_id
        assert test_land.code == fetched_land.code
    @pytest.mark.asyncio
    async def test_update_via_dict(self, land_manager:LandManager, session:AsyncSession):
        test_land = await LandFactory.create_async(session)
        new_code = generate_uuid()
        updated_land = await land_manager.update(land=test_land,code=new_code)
        assert isinstance(updated_land, Land)
        assert updated_land.land_id == test_land.land_id
        assert updated_land.code == new_code
        result = await session.execute(select(Land).filter(Land.land_id == test_land.land_id))
        fetched_land = result.scalars().first()
        assert updated_land.land_id == fetched_land.land_id
        assert updated_land.code == fetched_land.code
        assert test_land.land_id == fetched_land.land_id
        assert new_code == fetched_land.code
    @pytest.mark.asyncio
    async def test_update_invalid_land(self, land_manager:LandManager):
        # None land
        land = None
        new_code = generate_uuid()
        updated_land = await land_manager.update(land, code=new_code)
        # Assertions
        assert updated_land is None
    #todo fix test
    # @pytest.mark.asyncio
    # async def test_update_with_nonexistent_attribute(self, land_manager:LandManager, session:AsyncSession):
    #     test_land = await LandFactory.create_async(session)
    #     new_code = generate_uuid()
    #     # This should raise an AttributeError since 'color' is not an attribute of Land
    #     with pytest.raises(Exception):
    #         updated_land = await land_manager.update(land=test_land,xxx=new_code)
    #     await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(self, land_manager:LandManager, session:AsyncSession):
        land_data = await LandFactory.create_async(session)
        result = await session.execute(select(Land).filter(Land.land_id == land_data.land_id))
        fetched_land = result.scalars().first()
        assert isinstance(fetched_land, Land)
        assert fetched_land.land_id == land_data.land_id
        deleted_land = await land_manager.delete(land_id=land_data.land_id)
        result = await session.execute(select(Land).filter(Land.land_id == land_data.land_id))
        fetched_land = result.scalars().first()
        assert fetched_land is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, land_manager:LandManager, session:AsyncSession):
        with pytest.raises(Exception):
            await land_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(self, land_manager:LandManager, session:AsyncSession):
        with pytest.raises(Exception):
            await land_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(self, land_manager:LandManager, session:AsyncSession):
        lands = await land_manager.get_list()
        assert len(lands) == 0
        lands_data = [await LandFactory.create_async(session) for _ in range(5)]
        lands = await land_manager.get_list()
        assert len(lands) == 5
        assert all(isinstance(land, Land) for land in lands)
    @pytest.mark.asyncio
    async def test_to_json(self, land_manager:LandManager, session:AsyncSession):
        land = await LandFactory.build_async(session)
        json_data = land_manager.to_json(land)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(self, land_manager:LandManager, session:AsyncSession):
        land = await LandFactory.build_async(session)
        dict_data = land_manager.to_dict(land)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(self, land_manager:LandManager, session:AsyncSession):
        land = await LandFactory.create_async(session)
        json_data = land_manager.to_json(land)
        deserialized_land = land_manager.from_json(json_data)
        assert isinstance(deserialized_land, Land)
        assert deserialized_land.code == land.code
    @pytest.mark.asyncio
    async def test_from_dict(self, land_manager:LandManager, session:AsyncSession):
        land = await LandFactory.create_async(session)
        schema = LandSchema()
        land_data = schema.dump(land)
        deserialized_land = land_manager.from_dict(land_data)
        assert isinstance(deserialized_land, Land)
        assert deserialized_land.code == land.code
    @pytest.mark.asyncio
    async def test_add_bulk(self, land_manager:LandManager, session:AsyncSession):
        lands_data = [await LandFactory.build_async(session) for _ in range(5)]
        lands = await land_manager.add_bulk(lands_data)
        assert len(lands) == 5
        for updated_land in lands:
            result = await session.execute(select(Land).filter(Land.land_id == updated_land.land_id))
            fetched_land = result.scalars().first()
            assert isinstance(fetched_land, Land)
            assert fetched_land.land_id == updated_land.land_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(self, land_manager:LandManager, session:AsyncSession):
        # Mocking land instances
        land1 = await LandFactory.create_async(session=session)
        land2 = await LandFactory.create_async(session=session)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        # Update lands
        updates = [{"land_id": 1, "code": code_updated1}, {"land_id": 2, "code": code_updated2}]
        updated_lands = await land_manager.update_bulk(updates)
        # Assertions
        assert len(updated_lands) == 2
        assert updated_lands[0].code == code_updated1
        assert updated_lands[1].code == code_updated2
        result = await session.execute(select(Land).filter(Land.land_id == 1))
        fetched_land = result.scalars().first()
        assert isinstance(fetched_land, Land)
        assert fetched_land.code == code_updated1
        result = await session.execute(select(Land).filter(Land.land_id == 2))
        fetched_land = result.scalars().first()
        assert isinstance(fetched_land, Land)
        assert fetched_land.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_land_id(self, land_manager:LandManager, session:AsyncSession):
        # No lands to update since land_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_lands = await land_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_land_not_found(self, land_manager:LandManager, session:AsyncSession):
        # Update lands
        updates = [{"land_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_lands = await land_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(self, land_manager:LandManager, session:AsyncSession):
        updates = [{"land_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_lands = await land_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(self, land_manager:LandManager, session:AsyncSession):
        land1 = await LandFactory.create_async(session=session)
        land2 = await LandFactory.create_async(session=session)
        # Delete lands
        land_ids = [1, 2]
        result = await land_manager.delete_bulk(land_ids)
        assert result is True
        for land_id in land_ids:
            execute_result = await session.execute(select(Land).filter(Land.land_id == land_id))
            fetched_land = execute_result.scalars().first()
            assert fetched_land is None
    @pytest.mark.asyncio
    async def test_delete_bulk_some_lands_not_found(self, land_manager:LandManager, session:AsyncSession):
        land1 = await LandFactory.create_async(session=session)
        # Delete lands
        land_ids = [1, 2]
        with pytest.raises(Exception):
           result = await land_manager.delete_bulk(land_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(self, land_manager:LandManager, session:AsyncSession):
        # Delete lands with an empty list
        land_ids = []
        result = await land_manager.delete_bulk(land_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(self, land_manager:LandManager, session:AsyncSession):
        land_ids = ["1", 2]
        with pytest.raises(Exception):
           result = await land_manager.delete_bulk(land_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(self, land_manager:LandManager, session:AsyncSession):
        lands_data = [await LandFactory.create_async(session) for _ in range(5)]
        count = await land_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(self, land_manager:LandManager, session:AsyncSession):
        count = await land_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(self, land_manager:LandManager, session:AsyncSession):
        # Add lands
        lands_data = [await LandFactory.create_async(session) for _ in range(5)]
        sorted_lands = await land_manager.get_sorted_list(sort_by="land_id")
        assert [land.land_id for land in sorted_lands] == [(i + 1) for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(self, land_manager:LandManager, session:AsyncSession):
        # Add lands
        lands_data = [await LandFactory.create_async(session) for _ in range(5)]
        sorted_lands = await land_manager.get_sorted_list(sort_by="land_id", order="desc")
        assert [land.land_id for land in sorted_lands] == [(i + 1) for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(self, land_manager:LandManager, session:AsyncSession):
        with pytest.raises(AttributeError):
            await land_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(self, land_manager:LandManager, session:AsyncSession):
        sorted_lands = await land_manager.get_sorted_list(sort_by="land_id")
        assert len(sorted_lands) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(self, land_manager:LandManager, session:AsyncSession):
        # Add a land
        land1 = await LandFactory.create_async(session=session)
        result = await session.execute(select(Land).filter(Land.land_id == land1.land_id))
        land2 = result.scalars().first()
        assert land1.code == land2.code
        updated_code1 = generate_uuid()
        land1.code = updated_code1
        updated_land1 = await land_manager.update(land1)
        assert updated_land1.code == updated_code1
        refreshed_land2 = await land_manager.refresh(land2)
        assert refreshed_land2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_land(self, land_manager:LandManager, session:AsyncSession):
        land = Land(land_id=999)
        with pytest.raises(Exception):
            await land_manager.refresh(land)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_land(self, land_manager:LandManager, session:AsyncSession):
        # Add a land
        land1 = await LandFactory.create_async(session=session)
        # Check if the land exists using the manager function
        assert await land_manager.exists(land1.land_id) == True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_land(self, land_manager:LandManager, session:AsyncSession):
        # Add a land
        land1 = await LandFactory.create_async(session=session)
        land2 = await land_manager.get_by_id(land_id=land1.land_id)
        assert land_manager.is_equal(land1,land2) == True
        land1_dict = land_manager.to_dict(land1)
        land3 = land_manager.from_dict(land1_dict)
        assert land_manager.is_equal(land1,land3) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_land(self, land_manager:LandManager, session:AsyncSession):
        non_existent_id = 999
        assert await land_manager.exists(non_existent_id) == False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(self, land_manager:LandManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await land_manager.exists(invalid_id)
        await session.rollback()
#endet
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(self, land_manager:LandManager, session:AsyncSession):
        # Add a land with a specific pac_id
        land1 = await LandFactory.create_async(session=session)
        # Fetch the land using the manager function
        fetched_lands = await land_manager.get_by_pac_id(land1.pac_id)
        assert len(fetched_lands) == 1
        assert fetched_lands[0].code == land1.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(self, land_manager:LandManager, session:AsyncSession):
        non_existent_id = 999
        fetched_lands = await land_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_lands) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(self, land_manager:LandManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await land_manager.get_by_pac_id(invalid_id)
        await session.rollback()
#endet
