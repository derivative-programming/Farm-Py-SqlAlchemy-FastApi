# models/managers/tests/flavor_test.py
"""
    #TODO add comment
"""
import logging
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
    #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def flavor_manager(self, session: AsyncSession):
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return FlavorManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        flavor_manager: FlavorManager
    ):
        """
            #TODO add comment
        """
        # Define mock data for our flavor
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        flavor = await flavor_manager.build(**mock_data)
        # Assert that the returned object is an instance of Flavor
        assert isinstance(flavor, Flavor)
        # Assert that the attributes of the flavor match our mock data
        assert flavor.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        flavor_manager: FlavorManager,
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
            await flavor_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_flavor_to_database(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_flavor = await FlavorFactory.build_async(session)
        assert test_flavor.flavor_id is None
        # Add the flavor using the manager's add method
        added_flavor = await flavor_manager.add(flavor=test_flavor)
        assert isinstance(added_flavor, Flavor)
        assert str(added_flavor.insert_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert str(added_flavor.last_update_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert added_flavor.flavor_id > 0
        # Fetch the flavor from the database directly
        result = await session.execute(
            select(Flavor).filter(Flavor.flavor_id == added_flavor.flavor_id))
        fetched_flavor = result.scalars().first()
        # Assert that the fetched flavor is not None and matches the added flavor
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
            #TODO add comment
        """
        # Create a test flavor using the FlavorFactory without persisting it to the database
        test_flavor = await FlavorFactory.build_async(session)
        assert test_flavor.flavor_id is None
        test_flavor.code = uuid.uuid4()
        # Add the flavor using the manager's add method
        added_flavor = await flavor_manager.add(flavor=test_flavor)
        assert isinstance(added_flavor, Flavor)
        assert str(added_flavor.insert_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert str(added_flavor.last_update_user_id) == (
            str(flavor_manager._session_context.customer_code))
        assert added_flavor.flavor_id > 0
        # Assert that the returned flavor matches the test flavor
        assert added_flavor.flavor_id == test_flavor.flavor_id
        assert added_flavor.code == test_flavor.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_flavor = await FlavorFactory.create_async(session)
        flavor = await flavor_manager.get_by_id(test_flavor.flavor_id)
        assert isinstance(flavor, Flavor)
        assert test_flavor.flavor_id == flavor.flavor_id
        assert test_flavor.code == flavor.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        flavor_manager: FlavorManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_flavor = await flavor_manager.get_by_id(non_existent_id)
        assert retrieved_flavor is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_flavor = await FlavorFactory.create_async(session)
        flavor = await flavor_manager.get_by_code(test_flavor.code)
        assert isinstance(flavor, Flavor)
        assert test_flavor.flavor_id == flavor.flavor_id
        assert test_flavor.code == flavor.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        flavor_manager: FlavorManager
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any Flavor in the database
        random_code = uuid.uuid4()
        flavor = await flavor_manager.get_by_code(random_code)
        assert flavor is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_flavor = await FlavorFactory.create_async(session)
        test_flavor.code = uuid.uuid4()
        updated_flavor = await flavor_manager.update(flavor=test_flavor)
        assert isinstance(updated_flavor, Flavor)
        assert str(updated_flavor.last_update_user_id) == str(
            flavor_manager._session_context.customer_code)
        assert updated_flavor.flavor_id == test_flavor.flavor_id
        assert updated_flavor.code == test_flavor.code
        result = await session.execute(
            select(Flavor).filter(
                Flavor.flavor_id == test_flavor.flavor_id)
        )
        fetched_flavor = result.scalars().first()
        assert updated_flavor.flavor_id == fetched_flavor.flavor_id
        assert updated_flavor.code == fetched_flavor.code
        assert test_flavor.flavor_id == fetched_flavor.flavor_id
        assert test_flavor.code == fetched_flavor.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_flavor = await FlavorFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_flavor = await flavor_manager.update(
            flavor=test_flavor,
            code=new_code
        )
        assert isinstance(updated_flavor, Flavor)
        assert str(updated_flavor.last_update_user_id) == str(
            flavor_manager._session_context.customer_code
        )
        assert updated_flavor.flavor_id == test_flavor.flavor_id
        assert updated_flavor.code == new_code
        result = await session.execute(
            select(Flavor).filter(
                Flavor.flavor_id == test_flavor.flavor_id)
        )
        fetched_flavor = result.scalars().first()
        assert updated_flavor.flavor_id == fetched_flavor.flavor_id
        assert updated_flavor.code == fetched_flavor.code
        assert test_flavor.flavor_id == fetched_flavor.flavor_id
        assert new_code == fetched_flavor.code
    @pytest.mark.asyncio
    async def test_update_invalid_flavor(self, flavor_manager: FlavorManager):
        # None flavor
        flavor = None
        new_code = uuid.uuid4()
        updated_flavor = await flavor_manager.update(flavor, code=new_code)
        # Assertions
        assert updated_flavor is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_flavor = await FlavorFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            updated_flavor = await flavor_manager.update(
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
            #TODO add comment
        """
        flavor_data = await FlavorFactory.create_async(session)
        result = await session.execute(
            select(Flavor).filter(Flavor.flavor_id == flavor_data.flavor_id))
        fetched_flavor = result.scalars().first()
        assert isinstance(fetched_flavor, Flavor)
        assert fetched_flavor.flavor_id == flavor_data.flavor_id
        deleted_flavor = await flavor_manager.delete(
            flavor_id=flavor_data.flavor_id)
        result = await session.execute(
            select(Flavor).filter(Flavor.flavor_id == flavor_data.flavor_id))
        fetched_flavor = result.scalars().first()
        assert fetched_flavor is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        with pytest.raises(Exception):
            await flavor_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavors = await flavor_manager.get_list()
        assert len(flavors) == 0
        flavors_data = (
            [await FlavorFactory.create_async(session) for _ in range(5)])
        flavors = await flavor_manager.get_list()
        assert len(flavors) == 5
        assert all(isinstance(flavor, Flavor) for flavor in flavors)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavor = await FlavorFactory.build_async(session)
        json_data = flavor_manager.to_json(flavor)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavor = await FlavorFactory.build_async(session)
        dict_data = flavor_manager.to_dict(flavor)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session)
        json_data = flavor_manager.to_json(flavor)
        deserialized_flavor = flavor_manager.from_json(json_data)
        assert isinstance(deserialized_flavor, Flavor)
        assert deserialized_flavor.code == flavor.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavor = await FlavorFactory.create_async(session)
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        deserialized_flavor = flavor_manager.from_dict(flavor_data)
        assert isinstance(deserialized_flavor, Flavor)
        assert deserialized_flavor.code == flavor.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavors_data = [await FlavorFactory.build_async(session) for _ in range(5)]
        flavors = await flavor_manager.add_bulk(flavors_data)
        assert len(flavors) == 5
        for updated_flavor in flavors:
            result = await session.execute(select(Flavor).filter(Flavor.flavor_id == updated_flavor.flavor_id))
            fetched_flavor = result.scalars().first()
            assert isinstance(fetched_flavor, Flavor)
            assert str(fetched_flavor.insert_user_id) == (
                str(flavor_manager._session_context.customer_code))
            assert str(fetched_flavor.last_update_user_id) == (
                str(flavor_manager._session_context.customer_code))
            assert fetched_flavor.flavor_id == updated_flavor.flavor_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking flavor instances
        flavor1 = await FlavorFactory.create_async(session=session)
        flavor2 = await FlavorFactory.create_async(session=session)
        logging.info(flavor1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update flavors
        updates = [
            {
                "flavor_id": 1,
                "code": code_updated1
            },
            {
                "flavor_id": 2,
                "code": code_updated2
            }
        ]
        updated_flavors = await flavor_manager.update_bulk(updates)
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
        result = await session.execute(select(Flavor).filter(Flavor.flavor_id == 1))
        fetched_flavor = result.scalars().first()
        assert isinstance(fetched_flavor, Flavor)
        assert fetched_flavor.code == code_updated1
        result = await session.execute(select(Flavor).filter(Flavor.flavor_id == 2))
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
            #TODO add comment
        """
        # No flavors to update since flavor_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_flavors = await flavor_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_flavor_not_found(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update flavors
        updates = [{"flavor_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            updated_flavors = await flavor_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"flavor_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            updated_flavors = await flavor_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavor1 = await FlavorFactory.create_async(session=session)
        flavor2 = await FlavorFactory.create_async(session=session)
        # Delete flavors
        flavor_ids = [1, 2]
        result = await flavor_manager.delete_bulk(flavor_ids)
        assert result is True
        for flavor_id in flavor_ids:
            execute_result = await session.execute(
                select(Flavor).filter(Flavor.flavor_id == flavor_id))
            fetched_flavor = execute_result.scalars().first()
            assert fetched_flavor is None
    @pytest.mark.asyncio
    async def test_delete_bulk_flavors_not_found(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavor1 = await FlavorFactory.create_async(session=session)
        # Delete flavors
        flavor_ids = [1, 2]
        with pytest.raises(Exception):
            result = await flavor_manager.delete_bulk(flavor_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        flavor_manager: FlavorManager
    ):
        """
            #TODO add comment
        """
        # Delete flavors with an empty list
        flavor_ids = []
        result = await flavor_manager.delete_bulk(flavor_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavor_ids = ["1", 2]
        with pytest.raises(Exception):
            result = await flavor_manager.delete_bulk(flavor_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavors_data = (
            [await FlavorFactory.create_async(session) for _ in range(5)])
        count = await flavor_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        flavor_manager: FlavorManager
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        # Add flavors
        flavors_data = (
            [await FlavorFactory.create_async(session) for _ in range(5)])
        sorted_flavors = await flavor_manager.get_sorted_list(sort_by="flavor_id")
        assert [flavor.flavor_id for flavor in sorted_flavors] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add flavors
        flavors_data = (
            [await FlavorFactory.create_async(session) for _ in range(5)])
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
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await flavor_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        flavor_manager: FlavorManager
    ):
        """
            #TODO add comment
        """
        sorted_flavors = await flavor_manager.get_sorted_list(sort_by="flavor_id")
        assert len(sorted_flavors) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a flavor
        flavor1 = await FlavorFactory.create_async(session=session)
        result = await session.execute(select(Flavor).filter(Flavor.flavor_id == flavor1.flavor_id))
        flavor2 = result.scalars().first()
        assert flavor1.code == flavor2.code
        updated_code1 = uuid.uuid4()
        flavor1.code = updated_code1
        updated_flavor1 = await flavor_manager.update(flavor1)
        assert updated_flavor1.code == updated_code1
        refreshed_flavor2 = await flavor_manager.refresh(flavor2)
        assert refreshed_flavor2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        flavor = Flavor(flavor_id=999)
        with pytest.raises(Exception):
            await flavor_manager.refresh(flavor)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a flavor
        flavor1 = await FlavorFactory.create_async(session=session)
        # Check if the flavor exists using the manager function
        assert await flavor_manager.exists(flavor1.flavor_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_flavor(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a flavor
        flavor1 = await FlavorFactory.create_async(session=session)
        flavor2 = await flavor_manager.get_by_id(flavor_id=flavor1.flavor_id)
        assert flavor_manager.is_equal(flavor1, flavor2) is True
        flavor1_dict = flavor_manager.to_dict(flavor1)
        flavor3 = flavor_manager.from_dict(flavor1_dict)
        assert flavor_manager.is_equal(flavor1, flavor3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_flavor(
        self,
        flavor_manager: FlavorManager
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await flavor_manager.exists(invalid_id)
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
        # Add a flavor with a specific pac_id
        flavor1 = await FlavorFactory.create_async(session=session)
        # Fetch the flavor using the manager function
        fetched_flavors = await flavor_manager.get_by_pac_id(flavor1.pac_id)
        assert len(fetched_flavors) == 1
        assert isinstance(fetched_flavors[0], Flavor)
        assert fetched_flavors[0].code == flavor1.code
        stmt = select(models.Pac).where(
            models.Pac.pac_id == flavor1.pac_id)
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert fetched_flavors[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        flavor_manager: FlavorManager
    ):
        non_existent_id = 999
        fetched_flavors = await flavor_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_flavors) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        flavor_manager: FlavorManager,
        session: AsyncSession
    ):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await flavor_manager.get_by_pac_id(invalid_id)
        await session.rollback()
# endset
