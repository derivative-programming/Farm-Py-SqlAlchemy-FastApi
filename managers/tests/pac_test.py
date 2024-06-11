import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.session_context import SessionContext
from models import Pac
import models
from models.factory import PacFactory
from managers.pac import PacManager
from models.serialization_schema.pac import PacSchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.future import select
import logging
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestPacManager:
    @pytest_asyncio.fixture(scope="function")
    async def pac_manager(self, session: AsyncSession):
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return PacManager(session_context)
    @pytest.mark.asyncio
    async def test_build(self, pac_manager: PacManager, session: AsyncSession):
        # Define some mock data for our pac
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        pac = await pac_manager.build(**mock_data)
        # Assert that the returned object is an instance of Pac
        assert isinstance(pac, Pac)
        # Assert that the attributes of the pac match our mock data
        assert pac.code == mock_data["code"]
        # Optionally, if the build method has some default values or computations:
        # assert pac.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, pac_manager: PacManager, session: AsyncSession):
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await pac_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_pac_to_database(self, pac_manager: PacManager, session: AsyncSession):
        test_pac = await PacFactory.build_async(session)
        assert test_pac.pac_id is None
        # Add the pac using the manager's add method
        added_pac = await pac_manager.add(pac=test_pac)
        assert isinstance(added_pac, Pac)
        assert str(added_pac.insert_user_id) == str(pac_manager._session_context.customer_code)
        assert str(added_pac.last_update_user_id) == str(pac_manager._session_context.customer_code)
        assert added_pac.pac_id > 0
        # Fetch the pac from the database directly
        result = await session.execute(select(Pac).filter(Pac.pac_id == added_pac.pac_id))
        fetched_pac = result.scalars().first()
        # Assert that the fetched pac is not None and matches the added pac
        assert fetched_pac is not None
        assert isinstance(fetched_pac, Pac)
        assert fetched_pac.pac_id == added_pac.pac_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_pac_object(self, pac_manager: PacManager, session: AsyncSession):
        # Create a test pac using the PacFactory without persisting it to the database
        test_pac = await PacFactory.build_async(session)
        assert test_pac.pac_id is None
        test_pac.code = generate_uuid()
        # Add the pac using the manager's add method
        added_pac = await pac_manager.add(pac=test_pac)
        assert isinstance(added_pac, Pac)
        assert str(added_pac.insert_user_id) == str(pac_manager._session_context.customer_code)
        assert str(added_pac.last_update_user_id) == str(pac_manager._session_context.customer_code)
        assert added_pac.pac_id > 0
        # Assert that the returned pac matches the test pac
        assert added_pac.pac_id == test_pac.pac_id
        assert added_pac.code == test_pac.code
    @pytest.mark.asyncio
    async def test_get_by_id(self, pac_manager: PacManager, session: AsyncSession):
        test_pac = await PacFactory.create_async(session)
        pac = await pac_manager.get_by_id(test_pac.pac_id)
        assert isinstance(pac, Pac)
        assert test_pac.pac_id == pac.pac_id
        assert test_pac.code == pac.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, pac_manager: PacManager, session: AsyncSession):
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_pac = await pac_manager.get_by_id(non_existent_id)
        assert retrieved_pac is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_pac(self, pac_manager: PacManager, session: AsyncSession):
        test_pac = await PacFactory.create_async(session)
        pac = await pac_manager.get_by_code(test_pac.code)
        assert isinstance(pac, Pac)
        assert test_pac.pac_id == pac.pac_id
        assert test_pac.code == pac.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, pac_manager: PacManager, session: AsyncSession):
        # Generate a random UUID that doesn't correspond to any Pac in the database
        random_code = generate_uuid()
        pac = await pac_manager.get_by_code(random_code)
        assert pac is None
    @pytest.mark.asyncio
    async def test_update(self, pac_manager: PacManager, session: AsyncSession):
        test_pac = await PacFactory.create_async(session)
        test_pac.code = generate_uuid()
        updated_pac = await pac_manager.update(pac=test_pac)
        assert isinstance(updated_pac, Pac)
        assert str(updated_pac.last_update_user_id) == str(pac_manager._session_context.customer_code)
        assert updated_pac.pac_id == test_pac.pac_id
        assert updated_pac.code == test_pac.code
        result = await session.execute(select(Pac).filter(Pac.pac_id == test_pac.pac_id))
        fetched_pac = result.scalars().first()
        assert updated_pac.pac_id == fetched_pac.pac_id
        assert updated_pac.code == fetched_pac.code
        assert test_pac.pac_id == fetched_pac.pac_id
        assert test_pac.code == fetched_pac.code
    @pytest.mark.asyncio
    async def test_update_via_dict(self, pac_manager: PacManager, session: AsyncSession):
        test_pac = await PacFactory.create_async(session)
        new_code = generate_uuid()
        updated_pac = await pac_manager.update(pac=test_pac,code=new_code)
        assert isinstance(updated_pac, Pac)
        assert str(updated_pac.last_update_user_id) == str(pac_manager._session_context.customer_code)
        assert updated_pac.pac_id == test_pac.pac_id
        assert updated_pac.code == new_code
        result = await session.execute(select(Pac).filter(Pac.pac_id == test_pac.pac_id))
        fetched_pac = result.scalars().first()
        assert updated_pac.pac_id == fetched_pac.pac_id
        assert updated_pac.code == fetched_pac.code
        assert test_pac.pac_id == fetched_pac.pac_id
        assert new_code == fetched_pac.code
    @pytest.mark.asyncio
    async def test_update_invalid_pac(self, pac_manager: PacManager):
        # None pac
        pac = None
        new_code = generate_uuid()
        updated_pac = await pac_manager.update(pac, code=new_code)
        # Assertions
        assert updated_pac is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(self, pac_manager: PacManager, session: AsyncSession):
        test_pac = await PacFactory.create_async(session)
        new_code = generate_uuid()
        # This should raise an AttributeError since 'color' is not an attribute of Pac
        with pytest.raises(ValueError):
            updated_pac = await pac_manager.update(pac=test_pac,xxx=new_code)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(self, pac_manager: PacManager, session: AsyncSession):
        pac_data = await PacFactory.create_async(session)
        result = await session.execute(select(Pac).filter(Pac.pac_id == pac_data.pac_id))
        fetched_pac = result.scalars().first()
        assert isinstance(fetched_pac, Pac)
        assert fetched_pac.pac_id == pac_data.pac_id
        deleted_pac = await pac_manager.delete(pac_id=pac_data.pac_id)
        result = await session.execute(select(Pac).filter(Pac.pac_id == pac_data.pac_id))
        fetched_pac = result.scalars().first()
        assert fetched_pac is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, pac_manager: PacManager, session: AsyncSession):
        with pytest.raises(Exception):
            await pac_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(self, pac_manager: PacManager, session: AsyncSession):
        with pytest.raises(Exception):
            await pac_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(self, pac_manager: PacManager, session: AsyncSession):
        pacs = await pac_manager.get_list()
        assert len(pacs) == 0
        pacs_data = [await PacFactory.create_async(session) for _ in range(5)]
        pacs = await pac_manager.get_list()
        assert len(pacs) == 5
        assert all(isinstance(pac, Pac) for pac in pacs)
    @pytest.mark.asyncio
    async def test_to_json(self, pac_manager: PacManager, session: AsyncSession):
        pac = await PacFactory.build_async(session)
        json_data = pac_manager.to_json(pac)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(self, pac_manager: PacManager, session: AsyncSession):
        pac = await PacFactory.build_async(session)
        dict_data = pac_manager.to_dict(pac)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(self, pac_manager: PacManager, session: AsyncSession):
        pac = await PacFactory.create_async(session)
        json_data = pac_manager.to_json(pac)
        deserialized_pac = pac_manager.from_json(json_data)
        assert isinstance(deserialized_pac, Pac)
        assert deserialized_pac.code == pac.code
    @pytest.mark.asyncio
    async def test_from_dict(self, pac_manager: PacManager, session: AsyncSession):
        pac = await PacFactory.create_async(session)
        schema = PacSchema()
        pac_data = schema.dump(pac)
        deserialized_pac = pac_manager.from_dict(pac_data)
        assert isinstance(deserialized_pac, Pac)
        assert deserialized_pac.code == pac.code
    @pytest.mark.asyncio
    async def test_add_bulk(self, pac_manager: PacManager, session: AsyncSession):
        pacs_data = [await PacFactory.build_async(session) for _ in range(5)]
        pacs = await pac_manager.add_bulk(pacs_data)
        assert len(pacs) == 5
        for updated_pac in pacs:
            result = await session.execute(select(Pac).filter(Pac.pac_id == updated_pac.pac_id))
            fetched_pac = result.scalars().first()
            assert isinstance(fetched_pac, Pac)
            assert str(fetched_pac.insert_user_id) == str(pac_manager._session_context.customer_code)
            assert str(fetched_pac.last_update_user_id) == str(pac_manager._session_context.customer_code)
            assert fetched_pac.pac_id == updated_pac.pac_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(self, pac_manager: PacManager, session: AsyncSession):
        # Mocking pac instances
        pac1 = await PacFactory.create_async(session=session)
        pac2 = await PacFactory.create_async(session=session)
        logging.info(pac1.__dict__)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update pacs
        updates = [{"pac_id": 1, "code": code_updated1}, {"pac_id": 2, "code": code_updated2}]
        updated_pacs = await pac_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_pacs) == 2
        logging.info(updated_pacs[0].__dict__)
        logging.info(updated_pacs[1].__dict__)
        logging.info('getall')
        pacs = await pac_manager.get_list()
        logging.info(pacs[0].__dict__)
        logging.info(pacs[1].__dict__)
        assert updated_pacs[0].code == code_updated1
        assert updated_pacs[1].code == code_updated2
        assert str(updated_pacs[0].last_update_user_id) == str(pac_manager._session_context.customer_code)
        assert str(updated_pacs[1].last_update_user_id) == str(pac_manager._session_context.customer_code)
        result = await session.execute(select(Pac).filter(Pac.pac_id == 1))
        fetched_pac = result.scalars().first()
        assert isinstance(fetched_pac, Pac)
        assert fetched_pac.code == code_updated1
        result = await session.execute(select(Pac).filter(Pac.pac_id == 2))
        fetched_pac = result.scalars().first()
        assert isinstance(fetched_pac, Pac)
        assert fetched_pac.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_pac_id(self, pac_manager: PacManager, session: AsyncSession):
        # No pacs to update since pac_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_pacs = await pac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_pac_not_found(self, pac_manager: PacManager, session: AsyncSession):
        # Update pacs
        updates = [{"pac_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_pacs = await pac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(self, pac_manager: PacManager, session: AsyncSession):
        updates = [{"pac_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_pacs = await pac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(self, pac_manager: PacManager, session: AsyncSession):
        pac1 = await PacFactory.create_async(session=session)
        pac2 = await PacFactory.create_async(session=session)
        # Delete pacs
        pac_ids = [1, 2]
        result = await pac_manager.delete_bulk(pac_ids)
        assert result is True
        for pac_id in pac_ids:
            execute_result = await session.execute(select(Pac).filter(Pac.pac_id == pac_id))
            fetched_pac = execute_result.scalars().first()
            assert fetched_pac is None
    @pytest.mark.asyncio
    async def test_delete_bulk_some_pacs_not_found(self, pac_manager: PacManager, session: AsyncSession):
        pac1 = await PacFactory.create_async(session=session)
        # Delete pacs
        pac_ids = [1, 2]
        with pytest.raises(Exception):
           result = await pac_manager.delete_bulk(pac_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(self, pac_manager: PacManager, session: AsyncSession):
        # Delete pacs with an empty list
        pac_ids = []
        result = await pac_manager.delete_bulk(pac_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(self, pac_manager: PacManager, session: AsyncSession):
        pac_ids = ["1", 2]
        with pytest.raises(Exception):
           result = await pac_manager.delete_bulk(pac_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(self, pac_manager: PacManager, session: AsyncSession):
        pacs_data = [await PacFactory.create_async(session) for _ in range(5)]
        count = await pac_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(self, pac_manager: PacManager, session: AsyncSession):
        count = await pac_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(self, pac_manager: PacManager, session: AsyncSession):
        # Add pacs
        pacs_data = [await PacFactory.create_async(session) for _ in range(5)]
        sorted_pacs = await pac_manager.get_sorted_list(sort_by="pac_id")
        assert [pac.pac_id for pac in sorted_pacs] == [(i + 1) for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(self, pac_manager: PacManager, session: AsyncSession):
        # Add pacs
        pacs_data = [await PacFactory.create_async(session) for _ in range(5)]
        sorted_pacs = await pac_manager.get_sorted_list(sort_by="pac_id", order="desc")
        assert [pac.pac_id for pac in sorted_pacs] == [(i + 1) for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(self, pac_manager: PacManager, session: AsyncSession):
        with pytest.raises(AttributeError):
            await pac_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(self, pac_manager: PacManager, session: AsyncSession):
        sorted_pacs = await pac_manager.get_sorted_list(sort_by="pac_id")
        assert len(sorted_pacs) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(self, pac_manager: PacManager, session: AsyncSession):
        # Add a pac
        pac1 = await PacFactory.create_async(session=session)
        result = await session.execute(select(Pac).filter(Pac.pac_id == pac1.pac_id))
        pac2 = result.scalars().first()
        assert pac1.code == pac2.code
        updated_code1 = generate_uuid()
        pac1.code = updated_code1
        updated_pac1 = await pac_manager.update(pac1)
        assert updated_pac1.code == updated_code1
        refreshed_pac2 = await pac_manager.refresh(pac2)
        assert refreshed_pac2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_pac(self, pac_manager: PacManager, session: AsyncSession):
        pac = Pac(pac_id=999)
        with pytest.raises(Exception):
            await pac_manager.refresh(pac)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_pac(self, pac_manager: PacManager, session: AsyncSession):
        # Add a pac
        pac1 = await PacFactory.create_async(session=session)
        # Check if the pac exists using the manager function
        assert await pac_manager.exists(pac1.pac_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_pac(self, pac_manager: PacManager, session: AsyncSession):
        # Add a pac
        pac1 = await PacFactory.create_async(session=session)
        pac2 = await pac_manager.get_by_id(pac_id=pac1.pac_id)
        assert pac_manager.is_equal(pac1, pac2) is True
        pac1_dict = pac_manager.to_dict(pac1)
        pac3 = pac_manager.from_dict(pac1_dict)
        assert pac_manager.is_equal(pac1, pac3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_pac(self, pac_manager: PacManager, session: AsyncSession):
        non_existent_id = 999
        assert await pac_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(self, pac_manager: PacManager, session: AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await pac_manager.exists(invalid_id)
        await session.rollback()
#endet
    #description,
    #displayOrder,
    # isActive,
    #lookupEnumName,
    #name,
#endet
