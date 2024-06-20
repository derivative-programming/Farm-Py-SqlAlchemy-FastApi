# models/managers/tests/org_api_key_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `OrgApiKeyManager` class.
"""
# TODO file too big. split into separate test files
import logging
from typing import List
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from helpers.session_context import SessionContext
from managers.org_api_key import OrgApiKeyManager
from models import OrgApiKey
from models.factory import OrgApiKeyFactory
from models.serialization_schema.org_api_key import OrgApiKeySchema
class TestOrgApiKeyManager:
    """
    This class contains unit tests for the
    `OrgApiKeyManager` class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def org_api_key_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `OrgApiKeyManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return OrgApiKeyManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
        Test case for the `build` method of
        `OrgApiKeyManager`.
        """
        # Define mock data for our org_api_key
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        org_api_key = await org_api_key_manager.build(**mock_data)
        # Assert that the returned object is an instance of OrgApiKey
        assert isinstance(org_api_key, OrgApiKey)
        # Assert that the attributes of the org_api_key match our mock data
        assert org_api_key.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `OrgApiKeyManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await org_api_key_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_org_api_key_to_database(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `OrgApiKeyManager` that checks if a
        org_api_key is correctly added to the database.
        """
        test_org_api_key = await OrgApiKeyFactory.build_async(session)
        assert test_org_api_key.org_api_key_id == 0
        # Add the org_api_key using the manager's add method
        added_org_api_key = await org_api_key_manager.add(org_api_key=test_org_api_key)
        assert isinstance(added_org_api_key, OrgApiKey)
        assert str(added_org_api_key.insert_user_id) == (
            str(org_api_key_manager._session_context.customer_code))
        assert str(added_org_api_key.last_update_user_id) == (
            str(org_api_key_manager._session_context.customer_code))
        assert added_org_api_key.org_api_key_id > 0
        # Fetch the org_api_key from the database directly
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == added_org_api_key.org_api_key_id  # type: ignore
            )
        )
        fetched_org_api_key = result.scalars().first()
        # Assert that the fetched org_api_key is not None and matches the added org_api_key
        assert fetched_org_api_key is not None
        assert isinstance(fetched_org_api_key, OrgApiKey)
        assert fetched_org_api_key.org_api_key_id == added_org_api_key.org_api_key_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_org_api_key_object(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `OrgApiKeyManager` that checks if the
        correct org_api_key object is returned.
        """
        # Create a test org_api_key using the OrgApiKeyFactory
        # without persisting it to the database
        test_org_api_key = await OrgApiKeyFactory.build_async(session)
        assert test_org_api_key.org_api_key_id == 0
        test_org_api_key.code = uuid.uuid4()
        # Add the org_api_key using the manager's add method
        added_org_api_key = await org_api_key_manager.add(org_api_key=test_org_api_key)
        assert isinstance(added_org_api_key, OrgApiKey)
        assert str(added_org_api_key.insert_user_id) == (
            str(org_api_key_manager._session_context.customer_code))
        assert str(added_org_api_key.last_update_user_id) == (
            str(org_api_key_manager._session_context.customer_code))
        assert added_org_api_key.org_api_key_id > 0
        # Assert that the returned org_api_key matches the test org_api_key
        assert added_org_api_key.org_api_key_id == test_org_api_key.org_api_key_id
        assert added_org_api_key.code == test_org_api_key.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `OrgApiKeyManager`.
        """
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        org_api_key = await org_api_key_manager.get_by_id(test_org_api_key.org_api_key_id)
        assert isinstance(org_api_key, OrgApiKey)
        assert test_org_api_key.org_api_key_id == org_api_key.org_api_key_id
        assert test_org_api_key.code == org_api_key.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
        Test case for the `get_by_id` method of
        `OrgApiKeyManager` when the org_api_key is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_org_api_key = await org_api_key_manager.get_by_id(non_existent_id)
        assert retrieved_org_api_key is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `OrgApiKeyManager` that checks if a org_api_key is
        returned by its code.
        """
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        org_api_key = await org_api_key_manager.get_by_code(test_org_api_key.code)
        assert isinstance(org_api_key, OrgApiKey)
        assert test_org_api_key.org_api_key_id == org_api_key.org_api_key_id
        assert test_org_api_key.code == org_api_key.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
        Test case for the `get_by_code` method of
        `OrgApiKeyManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any OrgApiKey in the database
        random_code = uuid.uuid4()
        org_api_key = await org_api_key_manager.get_by_code(random_code)
        assert org_api_key is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `OrgApiKeyManager`
        that checks if a org_api_key is correctly updated.
        """
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        test_org_api_key.code = uuid.uuid4()
        updated_org_api_key = await org_api_key_manager.update(org_api_key=test_org_api_key)
        assert isinstance(updated_org_api_key, OrgApiKey)
        assert str(updated_org_api_key.last_update_user_id) == str(
            org_api_key_manager._session_context.customer_code)
        assert updated_org_api_key.org_api_key_id == test_org_api_key.org_api_key_id
        assert updated_org_api_key.code == test_org_api_key.code
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == test_org_api_key.org_api_key_id)  # type: ignore
        )
        fetched_org_api_key = result.scalars().first()
        assert updated_org_api_key.org_api_key_id == fetched_org_api_key.org_api_key_id
        assert updated_org_api_key.code == fetched_org_api_key.code
        assert test_org_api_key.org_api_key_id == fetched_org_api_key.org_api_key_id
        assert test_org_api_key.code == fetched_org_api_key.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `OrgApiKeyManager`
        that checks if a org_api_key is correctly updated using a dictionary.
        """
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_org_api_key = await org_api_key_manager.update(
            org_api_key=test_org_api_key,
            code=new_code
        )
        assert isinstance(updated_org_api_key, OrgApiKey)
        assert str(updated_org_api_key.last_update_user_id) == str(
            org_api_key_manager._session_context.customer_code
        )
        assert updated_org_api_key.org_api_key_id == test_org_api_key.org_api_key_id
        assert updated_org_api_key.code == new_code
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == test_org_api_key.org_api_key_id)  # type: ignore
        )
        fetched_org_api_key = result.scalars().first()
        assert updated_org_api_key.org_api_key_id == fetched_org_api_key.org_api_key_id
        assert updated_org_api_key.code == fetched_org_api_key.code
        assert test_org_api_key.org_api_key_id == fetched_org_api_key.org_api_key_id
        assert new_code == fetched_org_api_key.code
    @pytest.mark.asyncio
    async def test_update_invalid_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
        Test case for the `update` method of `OrgApiKeyManager`
        with an invalid org_api_key.
        """
        # None org_api_key
        org_api_key = None
        new_code = uuid.uuid4()
        updated_org_api_key = await (
            org_api_key_manager.update(org_api_key, code=new_code))  # type: ignore
        # Assertions
        assert updated_org_api_key is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `OrgApiKeyManager`
        with a nonexistent attribute.
        """
        test_org_api_key = await OrgApiKeyFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await org_api_key_manager.update(
                org_api_key=test_org_api_key,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `OrgApiKeyManager`.
        """
        org_api_key_data = await OrgApiKeyFactory.create_async(session)
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == org_api_key_data.org_api_key_id)  # type: ignore
        )
        fetched_org_api_key = result.scalars().first()
        assert isinstance(fetched_org_api_key, OrgApiKey)
        assert fetched_org_api_key.org_api_key_id == org_api_key_data.org_api_key_id
        await org_api_key_manager.delete(
            org_api_key_id=org_api_key_data.org_api_key_id)
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == org_api_key_data.org_api_key_id)  # type: ignore
        )
        fetched_org_api_key = result.scalars().first()
        assert fetched_org_api_key is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await org_api_key_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await org_api_key_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_keys = await org_api_key_manager.get_list()
        assert len(org_api_keys) == 0
        org_api_keys_data = (
            [await OrgApiKeyFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_api_keys_data, List)
        org_api_keys = await org_api_key_manager.get_list()
        assert len(org_api_keys) == 5
        assert all(isinstance(org_api_key, OrgApiKey) for org_api_key in org_api_keys)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.build_async(session)
        json_data = org_api_key_manager.to_json(org_api_key)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.build_async(session)
        dict_data = org_api_key_manager.to_dict(org_api_key)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session)
        json_data = org_api_key_manager.to_json(org_api_key)
        deserialized_org_api_key = org_api_key_manager.from_json(json_data)
        assert isinstance(deserialized_org_api_key, OrgApiKey)
        assert deserialized_org_api_key.code == org_api_key.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_key = await OrgApiKeyFactory.create_async(session)
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        assert isinstance(org_api_key_data, dict)
        deserialized_org_api_key = org_api_key_manager.from_dict(org_api_key_data)
        assert isinstance(deserialized_org_api_key, OrgApiKey)
        assert deserialized_org_api_key.code == org_api_key.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_keys_data = [
            await OrgApiKeyFactory.build_async(session) for _ in range(5)]
        org_api_keys = await org_api_key_manager.add_bulk(org_api_keys_data)
        assert len(org_api_keys) == 5
        for updated_org_api_key in org_api_keys:
            result = await session.execute(
                select(OrgApiKey).filter(
                    OrgApiKey._org_api_key_id == updated_org_api_key.org_api_key_id  # type: ignore
                )
            )
            fetched_org_api_key = result.scalars().first()
            assert isinstance(fetched_org_api_key, OrgApiKey)
            assert str(fetched_org_api_key.insert_user_id) == (
                str(org_api_key_manager._session_context.customer_code))
            assert str(fetched_org_api_key.last_update_user_id) == (
                str(org_api_key_manager._session_context.customer_code))
            assert fetched_org_api_key.org_api_key_id == updated_org_api_key.org_api_key_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking org_api_key instances
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key2 = await OrgApiKeyFactory.create_async(session=session)
        logging.info(org_api_key1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update org_api_keys
        updates = [
            {
                "org_api_key_id": org_api_key1.org_api_key_id,
                "code": code_updated1
            },
            {
                "org_api_key_id": org_api_key2.org_api_key_id,
                "code": code_updated2
            }
        ]
        updated_org_api_keys = await org_api_key_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_org_api_keys) == 2
        logging.info(updated_org_api_keys[0].__dict__)
        logging.info(updated_org_api_keys[1].__dict__)
        logging.info('getall')
        org_api_keys = await org_api_key_manager.get_list()
        logging.info(org_api_keys[0].__dict__)
        logging.info(org_api_keys[1].__dict__)
        assert updated_org_api_keys[0].code == code_updated1
        assert updated_org_api_keys[1].code == code_updated2
        assert str(updated_org_api_keys[0].last_update_user_id) == (
            str(org_api_key_manager._session_context.customer_code))
        assert str(updated_org_api_keys[1].last_update_user_id) == (
            str(org_api_key_manager._session_context.customer_code))
        result = await session.execute(
            select(OrgApiKey).filter(OrgApiKey._org_api_key_id == 1)  # type: ignore
        )
        fetched_org_api_key = result.scalars().first()
        assert isinstance(fetched_org_api_key, OrgApiKey)
        assert fetched_org_api_key.code == code_updated1
        result = await session.execute(
            select(OrgApiKey).filter(OrgApiKey._org_api_key_id == 2)  # type: ignore
        )
        fetched_org_api_key = result.scalars().first()
        assert isinstance(fetched_org_api_key, OrgApiKey)
        assert fetched_org_api_key.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_org_api_key_id(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No org_api_keys to update since org_api_key_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await org_api_key_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_org_api_key_not_found(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update org_api_keys
        updates = [{"org_api_key_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await org_api_key_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"org_api_key_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await org_api_key_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key2 = await OrgApiKeyFactory.create_async(session=session)
        # Delete org_api_keys
        org_api_key_ids = [org_api_key1.org_api_key_id, org_api_key2.org_api_key_id]
        result = await org_api_key_manager.delete_bulk(org_api_key_ids)
        assert result is True
        for org_api_key_id in org_api_key_ids:
            execute_result = await session.execute(
                select(OrgApiKey).filter(
                    OrgApiKey._org_api_key_id == org_api_key_id)  # type: ignore
            )
            fetched_org_api_key = execute_result.scalars().first()
            assert fetched_org_api_key is None
    @pytest.mark.asyncio
    async def test_delete_bulk_org_api_keys_not_found(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        assert isinstance(org_api_key1, OrgApiKey)
        # Delete org_api_keys
        org_api_key_ids = [1, 2]
        with pytest.raises(Exception):
            await org_api_key_manager.delete_bulk(org_api_key_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
            #TODO add comment
        """
        # Delete org_api_keys with an empty list
        org_api_key_ids = []
        result = await org_api_key_manager.delete_bulk(org_api_key_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_key_ids = ["1", 2]
        with pytest.raises(Exception):
            await org_api_key_manager.delete_bulk(org_api_key_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_keys_data = (
            [await OrgApiKeyFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_api_keys_data, List)
        count = await org_api_key_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
            #TODO add comment
        """
        count = await org_api_key_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add org_api_keys
        org_api_keys_data = (
            [await OrgApiKeyFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_api_keys_data, List)
        sorted_org_api_keys = await org_api_key_manager.get_sorted_list(
            sort_by="_org_api_key_id")
        assert [org_api_key.org_api_key_id for org_api_key in sorted_org_api_keys] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add org_api_keys
        org_api_keys_data = (
            [await OrgApiKeyFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_api_keys_data, List)
        sorted_org_api_keys = await org_api_key_manager.get_sorted_list(
            sort_by="org_api_key_id", order="desc")
        assert [org_api_key.org_api_key_id for org_api_key in sorted_org_api_keys] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await org_api_key_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
            #TODO add comment
        """
        sorted_org_api_keys = await org_api_key_manager.get_sorted_list(sort_by="org_api_key_id")
        assert len(sorted_org_api_keys) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a org_api_key instance.
        This test performs the following steps:
        1. Creates a org_api_key instance using the OrgApiKeyFactory.
        2. Retrieves the org_api_key from the database to ensure
            it was added correctly.
        3. Updates the org_api_key's code and verifies the update.
        4. Refreshes the original org_api_key instance and checks if
            it reflects the updated code.
        Args:
            org_api_key_manager (OrgApiKeyManager): The manager responsible
                for org_api_key operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        # Retrieve the org_api_key from the database
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == org_api_key1.org_api_key_id)  # type: ignore
        )  # type: ignore
        org_api_key2 = result.scalars().first()
        # Verify that the retrieved org_api_key matches the added org_api_key
        assert org_api_key1.code == org_api_key2.code
        # Update the org_api_key's code
        updated_code1 = uuid.uuid4()
        org_api_key1.code = updated_code1
        updated_org_api_key1 = await org_api_key_manager.update(org_api_key1)
        # Verify that the updated org_api_key is of type OrgApiKey
        # and has the updated code
        assert isinstance(updated_org_api_key1, OrgApiKey)
        assert updated_org_api_key1.code == updated_code1
        # Refresh the original org_api_key instance
        refreshed_org_api_key2 = await org_api_key_manager.refresh(org_api_key2)
        # Verify that the refreshed org_api_key reflects the updated code
        assert refreshed_org_api_key2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_api_key = OrgApiKey(org_api_key_id=999)
        with pytest.raises(Exception):
            await org_api_key_manager.refresh(org_api_key)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        # Check if the org_api_key exists using the manager function
        assert await org_api_key_manager.exists(org_api_key1.org_api_key_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        org_api_key2 = await org_api_key_manager.get_by_id(org_api_key_id=org_api_key1.org_api_key_id)
        assert org_api_key_manager.is_equal(org_api_key1, org_api_key2) is True
        org_api_key1_dict = org_api_key_manager.to_dict(org_api_key1)
        org_api_key3 = org_api_key_manager.from_dict(org_api_key1_dict)
        assert org_api_key_manager.is_equal(org_api_key1, org_api_key3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        assert await org_api_key_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_api_key_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID
    @pytest.mark.asyncio
    async def test_get_by_organization_id_existing(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_organization_id` method when a org_api_key with
        a specific organization_id exists.
        Steps:
        1. Create a org_api_key using the OrgApiKeyFactory.
        2. Fetch the org_api_key using the
            `get_by_organization_id` method of the org_api_key_manager.
        3. Assert that the fetched org_api_keys list contains
            only one org_api_key.
        4. Assert that the fetched org_api_key is an instance
            of the OrgApiKey class.
        5. Assert that the code of the fetched org_api_key
            matches the code of the created org_api_key.
        6. Fetch the corresponding organization object
            using the organization_id of the created org_api_key.
        7. Assert that the fetched organization object is
            an instance of the Organization class.
        8. Assert that the organization_code_peek of the fetched
            org_api_key matches the code of the fetched organization.
        """
        # Add a org_api_key with a specific organization_id
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        # Fetch the org_api_key using the manager function
        fetched_org_api_keys = await org_api_key_manager.get_by_organization_id(org_api_key1.organization_id)
        assert len(fetched_org_api_keys) == 1
        assert isinstance(fetched_org_api_keys[0], OrgApiKey)
        assert fetched_org_api_keys[0].code == org_api_key1.code
        stmt = select(models.Organization).where(
            models.Organization._organization_id == org_api_key1.organization_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        organization = result.scalars().first()
        assert isinstance(organization, models.Organization)
        assert fetched_org_api_keys[0].organization_code_peek == organization.code
    @pytest.mark.asyncio
    async def test_get_by_organization_id_nonexistent(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
        Test case to verify the behavior of the
        get_by_organization_id method when the organization ID does not exist.
        This test case ensures that when a non-existent
        organization ID is provided to the get_by_organization_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_org_api_keys = await org_api_key_manager.get_by_organization_id(non_existent_id)
        assert len(fetched_org_api_keys) == 0
    @pytest.mark.asyncio
    async def test_get_by_organization_id_invalid_type(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_organization_id` method when an invalid organization ID is provided.
        Args:
            org_api_key_manager (OrgApiKeyManager): An
                instance of the OrgApiKeyManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.
        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_organization_id` method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_api_key_manager.get_by_organization_id(invalid_id)  # type: ignore
        await session.rollback()
    # OrgCustomerID
    @pytest.mark.asyncio
    async def test_get_by_org_customer_id_existing(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a org_api_key with a specific org_customer_id
        org_api_key1 = await OrgApiKeyFactory.create_async(session=session)
        # Fetch the org_api_key using the manager function
        fetched_org_api_keys = await org_api_key_manager.get_by_org_customer_id(
            org_api_key1.org_customer_id)
        assert len(fetched_org_api_keys) == 1
        assert isinstance(fetched_org_api_keys[0], OrgApiKey)
        assert fetched_org_api_keys[0].code == org_api_key1.code
        stmt = select(models.OrgCustomer).where(
            models.OrgCustomer._org_customer_id == org_api_key1.org_customer_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        org_customer = result.scalars().first()
        assert isinstance(org_customer, models.OrgCustomer)
        assert fetched_org_api_keys[0].org_customer_code_peek == org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_org_customer_id_nonexistent(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
        Test case to verify the behavior of the
        'get_by_org_customer_id' method
        when the provided foreign key ID does
        not exist in the database.
        This test ensures that when a non-existent
        foreign key ID is passed to the
        'get_by_org_customer_id' method, it
        returns an empty list.
        Steps:
        1. Set a non-existent foreign key ID.
        2. Call the 'get_by_org_customer_id'
            method with the non-existent ID.
        3. Assert that the returned list of fetched org_api_keys is empty.
        """
        non_existent_id = 999
        fetched_org_api_keys = (
            await org_api_key_manager.get_by_org_customer_id(non_existent_id))
        assert len(fetched_org_api_keys) == 0
    @pytest.mark.asyncio
    async def test_get_by_org_customer_id_invalid_type(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_org_customer_id` method
        when an invalid foreign key ID type is provided.
        It ensures that an exception is raised
        when an invalid ID is passed to the method.
        Args:
            org_api_key_manager (OrgApiKeyManager): The
                instance of the OrgApiKeyManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not
                raised when an invalid ID is passed.
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_api_key_manager.get_by_org_customer_id(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
