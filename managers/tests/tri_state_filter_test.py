import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from models import TriStateFilter
import models
from models.factory import TriStateFilterFactory
from managers.tri_state_filter import TriStateFilterManager
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.future import select
import logging
# DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestTriStateFilterManager:
    @pytest_asyncio.fixture(scope="function")
    async def tri_state_filter_manager(self, session:AsyncSession):
        return TriStateFilterManager(session)
    @pytest.mark.asyncio
    async def test_build(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Define some mock data for our tri_state_filter
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        tri_state_filter = await tri_state_filter_manager.build(**mock_data)
        # Assert that the returned object is an instance of TriStateFilter
        assert isinstance(tri_state_filter, TriStateFilter)
        # Assert that the attributes of the tri_state_filter match our mock data
        assert tri_state_filter.code == mock_data["code"]
        # Optionally, if the build method has some default values or computations:
        # assert tri_state_filter.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await tri_state_filter_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_tri_state_filter_to_database(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        test_tri_state_filter = await TriStateFilterFactory.build_async(session)
        assert test_tri_state_filter.tri_state_filter_id is None
        # Add the tri_state_filter using the manager's add method
        added_tri_state_filter = await tri_state_filter_manager.add(tri_state_filter=test_tri_state_filter)
        assert isinstance(added_tri_state_filter, TriStateFilter)
        assert added_tri_state_filter.tri_state_filter_id > 0
        # Fetch the tri_state_filter from the database directly
        result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == added_tri_state_filter.tri_state_filter_id))
        fetched_tri_state_filter = result.scalars().first()
        # Assert that the fetched tri_state_filter is not None and matches the added tri_state_filter
        assert fetched_tri_state_filter is not None
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.tri_state_filter_id == added_tri_state_filter.tri_state_filter_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_tri_state_filter_object(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Create a test tri_state_filter using the TriStateFilterFactory without persisting it to the database
        test_tri_state_filter = await TriStateFilterFactory.build_async(session)
        assert test_tri_state_filter.tri_state_filter_id is None
        test_tri_state_filter.code = generate_uuid()
        # Add the tri_state_filter using the manager's add method
        added_tri_state_filter = await tri_state_filter_manager.add(tri_state_filter=test_tri_state_filter)
        assert isinstance(added_tri_state_filter, TriStateFilter)
        assert added_tri_state_filter.tri_state_filter_id > 0
        # Assert that the returned tri_state_filter matches the test tri_state_filter
        assert added_tri_state_filter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id
        assert added_tri_state_filter.code == test_tri_state_filter.code
    @pytest.mark.asyncio
    async def test_get_by_id(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        tri_state_filter = await tri_state_filter_manager.get_by_id(test_tri_state_filter.tri_state_filter_id)
        assert isinstance(tri_state_filter, TriStateFilter)
        assert test_tri_state_filter.tri_state_filter_id == tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == tri_state_filter.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, tri_state_filter_manager:TriStateFilterManager, session: AsyncSession):
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_tri_state_filter = await tri_state_filter_manager.get_by_id(non_existent_id)
        assert retrieved_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        tri_state_filter = await tri_state_filter_manager.get_by_code(test_tri_state_filter.code)
        assert isinstance(tri_state_filter, TriStateFilter)
        assert test_tri_state_filter.tri_state_filter_id == tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == tri_state_filter.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Generate a random UUID that doesn't correspond to any TriStateFilter in the database
        random_code = generate_uuid()
        tri_state_filter = await tri_state_filter_manager.get_by_code(random_code)
        assert tri_state_filter is None
    @pytest.mark.asyncio
    async def test_update(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        test_tri_state_filter.code = generate_uuid()
        updated_tri_state_filter = await tri_state_filter_manager.update(tri_state_filter=test_tri_state_filter)
        assert isinstance(updated_tri_state_filter, TriStateFilter)
        assert updated_tri_state_filter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == test_tri_state_filter.code
        result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id))
        fetched_tri_state_filter = result.scalars().first()
        assert updated_tri_state_filter.tri_state_filter_id == fetched_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == fetched_tri_state_filter.code
        assert test_tri_state_filter.tri_state_filter_id == fetched_tri_state_filter.tri_state_filter_id
        assert test_tri_state_filter.code == fetched_tri_state_filter.code
    @pytest.mark.asyncio
    async def test_update_via_dict(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        test_tri_state_filter = await TriStateFilterFactory.create_async(session)
        new_code = generate_uuid()
        updated_tri_state_filter = await tri_state_filter_manager.update(tri_state_filter=test_tri_state_filter,code=new_code)
        assert isinstance(updated_tri_state_filter, TriStateFilter)
        assert updated_tri_state_filter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == new_code
        result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == test_tri_state_filter.tri_state_filter_id))
        fetched_tri_state_filter = result.scalars().first()
        assert updated_tri_state_filter.tri_state_filter_id == fetched_tri_state_filter.tri_state_filter_id
        assert updated_tri_state_filter.code == fetched_tri_state_filter.code
        assert test_tri_state_filter.tri_state_filter_id == fetched_tri_state_filter.tri_state_filter_id
        assert new_code == fetched_tri_state_filter.code
    @pytest.mark.asyncio
    async def test_update_invalid_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager):
        # None tri_state_filter
        tri_state_filter = None
        new_code = generate_uuid()
        updated_tri_state_filter = await tri_state_filter_manager.update(tri_state_filter, code=new_code)
        # Assertions
        assert updated_tri_state_filter is None
    #todo fix test
    # @pytest.mark.asyncio
    # async def test_update_with_nonexistent_attribute(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
    #     test_tri_state_filter = await TriStateFilterFactory.create_async(session)
    #     new_code = generate_uuid()
    #     # This should raise an AttributeError since 'color' is not an attribute of TriStateFilter
    #     with pytest.raises(Exception):
    #         updated_tri_state_filter = await tri_state_filter_manager.update(tri_state_filter=test_tri_state_filter,xxx=new_code)
    #     await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter_data = await TriStateFilterFactory.create_async(session)
        result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == tri_state_filter_data.tri_state_filter_id))
        fetched_tri_state_filter = result.scalars().first()
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.tri_state_filter_id == tri_state_filter_data.tri_state_filter_id
        deleted_tri_state_filter = await tri_state_filter_manager.delete(tri_state_filter_id=tri_state_filter_data.tri_state_filter_id)
        result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == tri_state_filter_data.tri_state_filter_id))
        fetched_tri_state_filter = result.scalars().first()
        assert fetched_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        with pytest.raises(Exception):
            await tri_state_filter_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        with pytest.raises(Exception):
            await tri_state_filter_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filters = await tri_state_filter_manager.get_list()
        assert len(tri_state_filters) == 0
        tri_state_filters_data = [await TriStateFilterFactory.create_async(session) for _ in range(5)]
        tri_state_filters = await tri_state_filter_manager.get_list()
        assert len(tri_state_filters) == 5
        assert all(isinstance(tri_state_filter, TriStateFilter) for tri_state_filter in tri_state_filters)
    @pytest.mark.asyncio
    async def test_to_json(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter = await TriStateFilterFactory.build_async(session)
        json_data = tri_state_filter_manager.to_json(tri_state_filter)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter = await TriStateFilterFactory.build_async(session)
        dict_data = tri_state_filter_manager.to_dict(tri_state_filter)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter = await TriStateFilterFactory.create_async(session)
        json_data = tri_state_filter_manager.to_json(tri_state_filter)
        deserialized_tri_state_filter = tri_state_filter_manager.from_json(json_data)
        assert isinstance(deserialized_tri_state_filter, TriStateFilter)
        assert deserialized_tri_state_filter.code == tri_state_filter.code
    @pytest.mark.asyncio
    async def test_from_dict(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter = await TriStateFilterFactory.create_async(session)
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)
        deserialized_tri_state_filter = tri_state_filter_manager.from_dict(tri_state_filter_data)
        assert isinstance(deserialized_tri_state_filter, TriStateFilter)
        assert deserialized_tri_state_filter.code == tri_state_filter.code
    @pytest.mark.asyncio
    async def test_add_bulk(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filters_data = [await TriStateFilterFactory.build_async(session) for _ in range(5)]
        tri_state_filters = await tri_state_filter_manager.add_bulk(tri_state_filters_data)
        assert len(tri_state_filters) == 5
        for updated_tri_state_filter in tri_state_filters:
            result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == updated_tri_state_filter.tri_state_filter_id))
            fetched_tri_state_filter = result.scalars().first()
            assert isinstance(fetched_tri_state_filter, TriStateFilter)
            assert fetched_tri_state_filter.tri_state_filter_id == updated_tri_state_filter.tri_state_filter_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Mocking tri_state_filter instances
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter2 = await TriStateFilterFactory.create_async(session=session)
        logging.info(tri_state_filter1.__dict__)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update tri_state_filters
        updates = [{"tri_state_filter_id": 1, "code": code_updated1}, {"tri_state_filter_id": 2, "code": code_updated2}]
        updated_tri_state_filters = await tri_state_filter_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_tri_state_filters) == 2
        logging.info(updated_tri_state_filters[0].__dict__)
        logging.info(updated_tri_state_filters[1].__dict__)
        logging.info('getall')
        tri_state_filters = await tri_state_filter_manager.get_list()
        logging.info(tri_state_filters[0].__dict__)
        logging.info(tri_state_filters[1].__dict__)
        assert updated_tri_state_filters[0].code == code_updated1
        assert updated_tri_state_filters[1].code == code_updated2
        result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == 1))
        fetched_tri_state_filter = result.scalars().first()
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.code == code_updated1
        result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == 2))
        fetched_tri_state_filter = result.scalars().first()
        assert isinstance(fetched_tri_state_filter, TriStateFilter)
        assert fetched_tri_state_filter.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_tri_state_filter_id(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # No tri_state_filters to update since tri_state_filter_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_tri_state_filters = await tri_state_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_tri_state_filter_not_found(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Update tri_state_filters
        updates = [{"tri_state_filter_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_tri_state_filters = await tri_state_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        updates = [{"tri_state_filter_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_tri_state_filters = await tri_state_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter2 = await TriStateFilterFactory.create_async(session=session)
        # Delete tri_state_filters
        tri_state_filter_ids = [1, 2]
        result = await tri_state_filter_manager.delete_bulk(tri_state_filter_ids)
        assert result is True
        for tri_state_filter_id in tri_state_filter_ids:
            execute_result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == tri_state_filter_id))
            fetched_tri_state_filter = execute_result.scalars().first()
            assert fetched_tri_state_filter is None
    @pytest.mark.asyncio
    async def test_delete_bulk_some_tri_state_filters_not_found(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        # Delete tri_state_filters
        tri_state_filter_ids = [1, 2]
        with pytest.raises(Exception):
           result = await tri_state_filter_manager.delete_bulk(tri_state_filter_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Delete tri_state_filters with an empty list
        tri_state_filter_ids = []
        result = await tri_state_filter_manager.delete_bulk(tri_state_filter_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter_ids = ["1", 2]
        with pytest.raises(Exception):
           result = await tri_state_filter_manager.delete_bulk(tri_state_filter_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filters_data = [await TriStateFilterFactory.create_async(session) for _ in range(5)]
        count = await tri_state_filter_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        count = await tri_state_filter_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Add tri_state_filters
        tri_state_filters_data = [await TriStateFilterFactory.create_async(session) for _ in range(5)]
        sorted_tri_state_filters = await tri_state_filter_manager.get_sorted_list(sort_by="tri_state_filter_id")
        assert [tri_state_filter.tri_state_filter_id for tri_state_filter in sorted_tri_state_filters] == [(i + 1) for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Add tri_state_filters
        tri_state_filters_data = [await TriStateFilterFactory.create_async(session) for _ in range(5)]
        sorted_tri_state_filters = await tri_state_filter_manager.get_sorted_list(sort_by="tri_state_filter_id", order="desc")
        assert [tri_state_filter.tri_state_filter_id for tri_state_filter in sorted_tri_state_filters] == [(i + 1) for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        with pytest.raises(AttributeError):
            await tri_state_filter_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        sorted_tri_state_filters = await tri_state_filter_manager.get_sorted_list(sort_by="tri_state_filter_id")
        assert len(sorted_tri_state_filters) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Add a tri_state_filter
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        result = await session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == tri_state_filter1.tri_state_filter_id))
        tri_state_filter2 = result.scalars().first()
        assert tri_state_filter1.code == tri_state_filter2.code
        updated_code1 = generate_uuid()
        tri_state_filter1.code = updated_code1
        updated_tri_state_filter1 = await tri_state_filter_manager.update(tri_state_filter1)
        assert updated_tri_state_filter1.code == updated_code1
        refreshed_tri_state_filter2 = await tri_state_filter_manager.refresh(tri_state_filter2)
        assert refreshed_tri_state_filter2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        tri_state_filter = TriStateFilter(tri_state_filter_id=999)
        with pytest.raises(Exception):
            await tri_state_filter_manager.refresh(tri_state_filter)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Add a tri_state_filter
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        # Check if the tri_state_filter exists using the manager function
        assert await tri_state_filter_manager.exists(tri_state_filter1.tri_state_filter_id) == True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Add a tri_state_filter
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        tri_state_filter2 = await tri_state_filter_manager.get_by_id(tri_state_filter_id=tri_state_filter1.tri_state_filter_id)
        assert tri_state_filter_manager.is_equal(tri_state_filter1,tri_state_filter2) == True
        tri_state_filter1_dict = tri_state_filter_manager.to_dict(tri_state_filter1)
        tri_state_filter3 = tri_state_filter_manager.from_dict(tri_state_filter1_dict)
        assert tri_state_filter_manager.is_equal(tri_state_filter1,tri_state_filter3) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tri_state_filter(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        non_existent_id = 999
        assert await tri_state_filter_manager.exists(non_existent_id) == False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await tri_state_filter_manager.exists(invalid_id)
        await session.rollback()
#endet
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        # Add a tri_state_filter with a specific pac_id
        tri_state_filter1 = await TriStateFilterFactory.create_async(session=session)
        # Fetch the tri_state_filter using the manager function
        fetched_tri_state_filters = await tri_state_filter_manager.get_by_pac_id(tri_state_filter1.pac_id)
        assert len(fetched_tri_state_filters) == 1
        assert isinstance(fetched_tri_state_filters[0],TriStateFilter)
        assert fetched_tri_state_filters[0].code == tri_state_filter1.code
        stmt = select(models.Pac).where(models.Pac.pac_id==tri_state_filter1.pac_id)
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert fetched_tri_state_filters[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        non_existent_id = 999
        fetched_tri_state_filters = await tri_state_filter_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_tri_state_filters) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(self, tri_state_filter_manager:TriStateFilterManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await tri_state_filter_manager.get_by_pac_id(invalid_id)
        await session.rollback()
    #stateIntValue,
#endet
