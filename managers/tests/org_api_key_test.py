import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from models import OrgApiKey
from models.factory import OrgApiKeyFactory
from managers.org_api_key import OrgApiKeyManager
from models.serialization_schema.org_api_key import OrgApiKeySchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
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
class TestOrgApiKeyManager:
    @pytest_asyncio.fixture(scope="function")
    async def org_api_key_manager(self, session:AsyncSession):
        return OrgApiKeyManager(session)
    @pytest.mark.asyncio
    async def test_build(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Define some mock data for our org_api_key
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        org_api_key = await org_api_key_manager.build(**mock_data)
        # Assert that the returned object is an instance of OrgApiKey
        assert isinstance(org_api_key, OrgApiKey)
        # Assert that the attributes of the org_api_key match our mock data
        assert org_api_key.code == mock_data["code"]
        # Optionally, if the build method has some default values or computations:
        # assert org_api_key.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await org_api_key_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_org_api_key_to_database(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        test_org_api_key = await OrgApiKeyFactory.build_async(session)
        assert test_org_api_key.org_api_key_id is None
        # Add the org_api_key using the manager's add method
        added_org_api_key = await org_api_key_manager.add(org_api_key=test_org_api_key)
        assert isinstance(added_org_api_key, OrgApiKey)
        assert added_org_api_key.org_api_key_id > 0
        # Fetch the org_api_key from the database directly
        result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == added_org_api_key.org_api_key_id))
        fetched_org_api_key = result.scalars().first()
        # Assert that the fetched org_api_key is not None and matches the added org_api_key
        assert fetched_org_api_key is not None
        assert isinstance(fetched_org_api_key, OrgApiKey)
        assert fetched_org_api_key.org_api_key_id == added_org_api_key.org_api_key_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_org_api_key_object(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Create a test org_api_key using the OrgApiKeyFactory without persisting it to the database
        test_org_api_key = await OrgApiKeyFactory.build_async(session)
        assert test_org_api_key.org_api_key_id is None
        test_org_api_key.code = generate_uuid()
        # Add the org_api_key using the manager's add method
        added_org_api_key = await org_api_key_manager.add(org_api_key=test_org_api_key)
        assert isinstance(added_org_api_key, OrgApiKey)
        assert added_org_api_key.org_api_key_id > 0
        # Assert that the returned org_api_key matches the test org_api_key
        assert added_org_api_key.org_api_key_id == test_org_api_key.org_api_key_id
        assert added_org_api_key.code == test_org_api_key.code
    @pytest.mark.asyncio
    async def test_get_by_id(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        org_api_key = await org_api_key_manager.get_by_id(test_org_api_key.org_api_key_id)
        assert isinstance(org_api_key, OrgApiKey)
        assert test_org_api_key.org_api_key_id == org_api_key.org_api_key_id
        assert test_org_api_key.code == org_api_key.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, org_api_key_manager:OrgApiKeyManager, session: AsyncSession):
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_org_api_key = await org_api_key_manager.get_by_id(non_existent_id)
        assert retrieved_org_api_key is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_org_api_key(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        org_api_key = await org_api_key_manager.get_by_code(test_org_api_key.code)
        assert isinstance(org_api_key, OrgApiKey)
        assert test_org_api_key.org_api_key_id == org_api_key.org_api_key_id
        assert test_org_api_key.code == org_api_key.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Generate a random UUID that doesn't correspond to any OrgApiKey in the database
        random_code = generate_uuid()
        org_api_key = await org_api_key_manager.get_by_code(random_code)
        assert org_api_key is None
    @pytest.mark.asyncio
    async def test_update(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        test_org_api_key.code = generate_uuid()
        updated_org_api_key = await org_api_key_manager.update(org_api_key=test_org_api_key)
        assert isinstance(updated_org_api_key, OrgApiKey)
        assert updated_org_api_key.org_api_key_id == test_org_api_key.org_api_key_id
        assert updated_org_api_key.code == test_org_api_key.code
        result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == test_org_api_key.org_api_key_id))
        fetched_org_api_key = result.scalars().first()
        assert updated_org_api_key.org_api_key_id == fetched_org_api_key.org_api_key_id
        assert updated_org_api_key.code == fetched_org_api_key.code
        assert test_org_api_key.org_api_key_id == fetched_org_api_key.org_api_key_id
        assert test_org_api_key.code == fetched_org_api_key.code
    @pytest.mark.asyncio
    async def test_update_via_dict(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        new_code = generate_uuid()
        updated_org_api_key = await org_api_key_manager.update(org_api_key=test_org_api_key,code=new_code)
        assert isinstance(updated_org_api_key, OrgApiKey)
        assert updated_org_api_key.org_api_key_id == test_org_api_key.org_api_key_id
        assert updated_org_api_key.code == new_code
        result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == test_org_api_key.org_api_key_id))
        fetched_org_api_key = result.scalars().first()
        assert updated_org_api_key.org_api_key_id == fetched_org_api_key.org_api_key_id
        assert updated_org_api_key.code == fetched_org_api_key.code
        assert test_org_api_key.org_api_key_id == fetched_org_api_key.org_api_key_id
        assert new_code == fetched_org_api_key.code
    @pytest.mark.asyncio
    async def test_update_invalid_org_api_key(self, org_api_key_manager:OrgApiKeyManager):
        # None org_api_key
        org_api_key = None
        new_code = generate_uuid()
        updated_org_api_key = await org_api_key_manager.update(org_api_key, code=new_code)
        # Assertions
        assert updated_org_api_key is None
    #todo fix test
    # @pytest.mark.asyncio
    # async def test_update_with_nonexistent_attribute(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
    #     test_org_api_key = await OrgApiKeyFactory.create_async(session)
    #     new_code = generate_uuid()
    #     # This should raise an AttributeError since 'color' is not an attribute of OrgApiKey
    #     with pytest.raises(Exception):
    #         updated_org_api_key = await org_api_key_manager.update(org_api_key=test_org_api_key,xxx=new_code)
    #     await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key_data = await OrgApiKeyFactory.create_async(session)
        result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == org_api_key_data.org_api_key_id))
        fetched_org_api_key = result.scalars().first()
        assert isinstance(fetched_org_api_key, OrgApiKey)
        assert fetched_org_api_key.org_api_key_id == org_api_key_data.org_api_key_id
        deleted_org_api_key = await org_api_key_manager.delete(org_api_key_id=org_api_key_data.org_api_key_id)
        result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == org_api_key_data.org_api_key_id))
        fetched_org_api_key = result.scalars().first()
        assert fetched_org_api_key is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        with pytest.raises(Exception):
            await org_api_key_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        with pytest.raises(Exception):
            await org_api_key_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_keys = await org_api_key_manager.get_list()
        assert len(org_api_keys) == 0
        org_api_keys_data = [await OrgApiKeyFactory.create_async(session) for _ in range(5)]
        org_api_keys = await org_api_key_manager.get_list()
        assert len(org_api_keys) == 5
        assert all(isinstance(org_api_key, OrgApiKey) for org_api_key in org_api_keys)
    @pytest.mark.asyncio
    async def test_to_json(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key = await OrgApiKeyFactory.build_async(session)
        json_data = org_api_key_manager.to_json(org_api_key)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key = await OrgApiKeyFactory.build_async(session)
        dict_data = org_api_key_manager.to_dict(org_api_key)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key = await OrgApiKeyFactory.create_async(session)
        json_data = org_api_key_manager.to_json(org_api_key)
        deserialized_org_api_key = org_api_key_manager.from_json(json_data)
        assert isinstance(deserialized_org_api_key, OrgApiKey)
        assert deserialized_org_api_key.code == org_api_key.code
    @pytest.mark.asyncio
    async def test_from_dict(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key = await OrgApiKeyFactory.create_async(session)
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        deserialized_org_api_key = org_api_key_manager.from_dict(org_api_key_data)
        assert isinstance(deserialized_org_api_key, OrgApiKey)
        assert deserialized_org_api_key.code == org_api_key.code
    @pytest.mark.asyncio
    async def test_add_bulk(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_keys_data = [await OrgApiKeyFactory.build_async(session) for _ in range(5)]
        org_api_keys = await org_api_key_manager.add_bulk(org_api_keys_data)
        assert len(org_api_keys) == 5
        for updated_org_api_key in org_api_keys:
            result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == updated_org_api_key.org_api_key_id))
            fetched_org_api_key = result.scalars().first()
            assert isinstance(fetched_org_api_key, OrgApiKey)
            assert fetched_org_api_key.org_api_key_id == updated_org_api_key.org_api_key_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Mocking org_api_key instances
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key2 = await OrgApiKeyFactory.create_async(session=session)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        # Update org_api_keys
        updates = [{"org_api_key_id": 1, "code": code_updated1}, {"org_api_key_id": 2, "code": code_updated2}]
        updated_org_api_keys = await org_api_key_manager.update_bulk(updates)
        # Assertions
        assert len(updated_org_api_keys) == 2
        assert updated_org_api_keys[0].code == code_updated1
        assert updated_org_api_keys[1].code == code_updated2
        result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == 1))
        fetched_org_api_key = result.scalars().first()
        assert isinstance(fetched_org_api_key, OrgApiKey)
        assert fetched_org_api_key.code == code_updated1
        result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == 2))
        fetched_org_api_key = result.scalars().first()
        assert isinstance(fetched_org_api_key, OrgApiKey)
        assert fetched_org_api_key.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_org_api_key_id(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # No org_api_keys to update since org_api_key_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_org_api_keys = await org_api_key_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_org_api_key_not_found(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Update org_api_keys
        updates = [{"org_api_key_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_org_api_keys = await org_api_key_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        updates = [{"org_api_key_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_org_api_keys = await org_api_key_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key2 = await OrgApiKeyFactory.create_async(session=session)
        # Delete org_api_keys
        org_api_key_ids = [1, 2]
        result = await org_api_key_manager.delete_bulk(org_api_key_ids)
        assert result is True
        for org_api_key_id in org_api_key_ids:
            execute_result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == org_api_key_id))
            fetched_org_api_key = execute_result.scalars().first()
            assert fetched_org_api_key is None
    @pytest.mark.asyncio
    async def test_delete_bulk_some_org_api_keys_not_found(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        # Delete org_api_keys
        org_api_key_ids = [1, 2]
        with pytest.raises(Exception):
           result = await org_api_key_manager.delete_bulk(org_api_key_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Delete org_api_keys with an empty list
        org_api_key_ids = []
        result = await org_api_key_manager.delete_bulk(org_api_key_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key_ids = ["1", 2]
        with pytest.raises(Exception):
           result = await org_api_key_manager.delete_bulk(org_api_key_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_keys_data = [await OrgApiKeyFactory.create_async(session) for _ in range(5)]
        count = await org_api_key_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        count = await org_api_key_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Add org_api_keys
        org_api_keys_data = [await OrgApiKeyFactory.create_async(session) for _ in range(5)]
        sorted_org_api_keys = await org_api_key_manager.get_sorted_list(sort_by="org_api_key_id")
        assert [org_api_key.org_api_key_id for org_api_key in sorted_org_api_keys] == [(i + 1) for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Add org_api_keys
        org_api_keys_data = [await OrgApiKeyFactory.create_async(session) for _ in range(5)]
        sorted_org_api_keys = await org_api_key_manager.get_sorted_list(sort_by="org_api_key_id", order="desc")
        assert [org_api_key.org_api_key_id for org_api_key in sorted_org_api_keys] == [(i + 1) for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        with pytest.raises(AttributeError):
            await org_api_key_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        sorted_org_api_keys = await org_api_key_manager.get_sorted_list(sort_by="org_api_key_id")
        assert len(sorted_org_api_keys) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        result = await session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == org_api_key1.org_api_key_id))
        org_api_key2 = result.scalars().first()
        assert org_api_key1.code == org_api_key2.code
        updated_code1 = generate_uuid()
        org_api_key1.code = updated_code1
        updated_org_api_key1 = await org_api_key_manager.update(org_api_key1)
        assert updated_org_api_key1.code == updated_code1
        refreshed_org_api_key2 = await org_api_key_manager.refresh(org_api_key2)
        assert refreshed_org_api_key2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_org_api_key(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        org_api_key = OrgApiKey(org_api_key_id=999)
        with pytest.raises(Exception):
            await org_api_key_manager.refresh(org_api_key)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_org_api_key(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        # Check if the org_api_key exists using the manager function
        assert await org_api_key_manager.exists(org_api_key1.org_api_key_id) == True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_org_api_key(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key2 = await org_api_key_manager.get_by_id(org_api_key_id=org_api_key1.org_api_key_id)
        assert org_api_key_manager.is_equal(org_api_key1,org_api_key2) == True
        org_api_key1_dict = org_api_key_manager.to_dict(org_api_key1)
        org_api_key3 = org_api_key_manager.from_dict(org_api_key1_dict)
        assert org_api_key_manager.is_equal(org_api_key1,org_api_key3) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_org_api_key(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        non_existent_id = 999
        assert await org_api_key_manager.exists(non_existent_id) == False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_api_key_manager.exists(invalid_id)
        await session.rollback()
#endet
    #apiKeyValue,
    #createdBy,
    #createdUTCDateTime
    #expirationUTCDateTime
    #isActive,
    #isTempUserKey,
    #name,
    #OrganizationID
    @pytest.mark.asyncio
    async def test_get_by_organization_id_existing(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Add a org_api_key with a specific organization_id
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        # Fetch the org_api_key using the manager function
        fetched_org_api_keys = await org_api_key_manager.get_by_organization_id(org_api_key1.organization_id)
        assert len(fetched_org_api_keys) == 1
        assert fetched_org_api_keys[0].code == org_api_key1.code
    @pytest.mark.asyncio
    async def test_get_by_organization_id_nonexistent(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        non_existent_id = 999
        fetched_org_api_keys = await org_api_key_manager.get_by_organization_id(non_existent_id)
        assert len(fetched_org_api_keys) == 0
    @pytest.mark.asyncio
    async def test_get_by_organization_id_invalid_type(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_api_key_manager.get_by_organization_id(invalid_id)
        await session.rollback()
    #OrgCustomerID
    @pytest.mark.asyncio
    async def test_get_by_org_customer_id_existing(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        # Add a org_api_key with a specific org_customer_id
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        # Fetch the org_api_key using the manager function
        fetched_org_api_keys = await org_api_key_manager.get_by_org_customer_id(org_api_key1.org_customer_id)
        assert len(fetched_org_api_keys) == 1
        assert fetched_org_api_keys[0].code == org_api_key1.code
    @pytest.mark.asyncio
    async def test_get_by_org_customer_id_nonexistent(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        non_existent_id = 999
        fetched_org_api_keys = await org_api_key_manager.get_by_org_customer_id(non_existent_id)
        assert len(fetched_org_api_keys) == 0
    @pytest.mark.asyncio
    async def test_get_by_org_customer_id_invalid_type(self, org_api_key_manager:OrgApiKeyManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_api_key_manager.get_by_org_customer_id(invalid_id)
        await session.rollback()
#endet
