# models/managers/tests/org_api_key_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `OrgApiKeyManager` class.
"""

from typing import List
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
        org_api_key = await org_api_key_manager.build(
            **mock_data)

        # Assert that the returned object is an instance of OrgApiKey
        assert isinstance(
            org_api_key, OrgApiKey)

        # Assert that the attributes of the
        # org_api_key match our mock data
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
        test_org_api_key = await OrgApiKeyFactory.build_async(
            session)

        assert test_org_api_key.org_api_key_id == 0

        # Add the org_api_key using the
        # manager's add method
        added_org_api_key = await org_api_key_manager.add(
            org_api_key=test_org_api_key)

        assert isinstance(added_org_api_key, OrgApiKey)

        assert str(added_org_api_key.insert_user_id) == (
            str(org_api_key_manager._session_context.customer_code))
        assert str(added_org_api_key.last_update_user_id) == (
            str(org_api_key_manager._session_context.customer_code))

        assert added_org_api_key.org_api_key_id > 0

        # Fetch the org_api_key from
        # the database directly
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == added_org_api_key.org_api_key_id  # type: ignore
            )
        )
        fetched_org_api_key = result.scalars().first()

        # Assert that the fetched org_api_key
        # is not None and matches the
        # added org_api_key
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
        # Create a test org_api_key
        # using the OrgApiKeyFactory
        # without persisting it to the database
        test_org_api_key = await OrgApiKeyFactory.build_async(
            session)

        assert test_org_api_key.org_api_key_id == 0

        test_org_api_key.code = uuid.uuid4()

        # Add the org_api_key using
        # the manager's add method
        added_org_api_key = await org_api_key_manager.add(
            org_api_key=test_org_api_key)

        assert isinstance(added_org_api_key, OrgApiKey)

        assert str(added_org_api_key.insert_user_id) == (
            str(org_api_key_manager._session_context.customer_code))
        assert str(added_org_api_key.last_update_user_id) == (
            str(org_api_key_manager._session_context.customer_code))

        assert added_org_api_key.org_api_key_id > 0

        # Assert that the returned
        # org_api_key matches the
        # test org_api_key
        assert added_org_api_key.org_api_key_id == \
            test_org_api_key.org_api_key_id
        assert added_org_api_key.code == \
            test_org_api_key.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrgApiKeyManager`
        that checks if a org_api_key
        is correctly updated.
        """
        test_org_api_key = await OrgApiKeyFactory.create_async(
            session)

        test_org_api_key.code = uuid.uuid4()

        updated_org_api_key = await org_api_key_manager.update(
            org_api_key=test_org_api_key)

        assert isinstance(updated_org_api_key, OrgApiKey)

        assert str(updated_org_api_key.last_update_user_id) == str(
            org_api_key_manager._session_context.customer_code)

        assert updated_org_api_key.org_api_key_id == \
            test_org_api_key.org_api_key_id
        assert updated_org_api_key.code == \
            test_org_api_key.code

        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == test_org_api_key.org_api_key_id)  # type: ignore
        )

        fetched_org_api_key = result.scalars().first()

        assert updated_org_api_key.org_api_key_id == \
            fetched_org_api_key.org_api_key_id
        assert updated_org_api_key.code == \
            fetched_org_api_key.code

        assert test_org_api_key.org_api_key_id == \
            fetched_org_api_key.org_api_key_id
        assert test_org_api_key.code == \
            fetched_org_api_key.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrgApiKeyManager`
        that checks if a org_api_key is
        correctly updated using a dictionary.
        """
        test_org_api_key = await OrgApiKeyFactory.create_async(
            session)

        new_code = uuid.uuid4()

        updated_org_api_key = await org_api_key_manager.update(
            org_api_key=test_org_api_key,
            code=new_code
        )

        assert isinstance(updated_org_api_key, OrgApiKey)

        assert str(updated_org_api_key.last_update_user_id) == str(
            org_api_key_manager._session_context.customer_code
        )

        assert updated_org_api_key.org_api_key_id == \
            test_org_api_key.org_api_key_id
        assert updated_org_api_key.code == new_code

        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == test_org_api_key.org_api_key_id)  # type: ignore
        )

        fetched_org_api_key = result.scalars().first()

        assert updated_org_api_key.org_api_key_id == \
            fetched_org_api_key.org_api_key_id
        assert updated_org_api_key.code == \
            fetched_org_api_key.code

        assert test_org_api_key.org_api_key_id == \
            fetched_org_api_key.org_api_key_id
        assert new_code == \
            fetched_org_api_key.code

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
            org_api_key_manager.update(
                org_api_key, code=new_code))  # type: ignore

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
        test_org_api_key = await OrgApiKeyFactory.create_async(
            session)

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
        org_api_key_data = await OrgApiKeyFactory.create_async(
            session)

        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == org_api_key_data.org_api_key_id)  # type: ignore
        )
        fetched_org_api_key = result.scalars().first()

        assert isinstance(fetched_org_api_key, OrgApiKey)

        assert fetched_org_api_key.org_api_key_id == \
            org_api_key_data.org_api_key_id

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
        Test case to verify the behavior of deleting a nonexistent org_api_key.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent org_api_key,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param org_api_key_manager: The instance of the OrgApiKeyManager class.
        :param session: The instance of the AsyncSession class.
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
        Test case to verify the behavior of deleting a org_api_key
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `org_api_key_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            org_api_key_manager (OrgApiKeyManager): An
                instance of the
                `OrgApiKeyManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

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
        Test case for the `get_list` method of the
        `OrgApiKeyManager` class.

        This test verifies that the `get_list`
        method returns the correct list of org_api_keys.

        Steps:
        1. Call the `get_list` method of the
            `org_api_key_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 org_api_key objects using the
            `OrgApiKeyFactory.create_async` method.
        4. Assert that the `org_api_keys_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `org_api_key_manager` instance again.
        6. Assert that the returned list contains 5 org_api_keys.
        7. Assert that all elements in the returned list are
            instances of the `OrgApiKey` class.
        """

        org_api_keys = await org_api_key_manager.get_list()

        assert len(org_api_keys) == 0

        org_api_keys_data = (
            [await OrgApiKeyFactory.create_async(session) for _ in range(5)])

        assert isinstance(org_api_keys_data, List)

        org_api_keys = await org_api_key_manager.get_list()

        assert len(org_api_keys) == 5
        assert all(isinstance(
            org_api_key, OrgApiKey) for org_api_key in org_api_keys)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the OrgApiKeyManager class.

        Args:
            org_api_key_manager (OrgApiKeyManager): An
                instance of the
                OrgApiKeyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        org_api_key = await OrgApiKeyFactory.build_async(
            session)

        json_data = org_api_key_manager.to_json(
            org_api_key)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the OrgApiKeyManager class.

        Args:
            org_api_key_manager (OrgApiKeyManager): An
                instance of the
                OrgApiKeyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        org_api_key = await OrgApiKeyFactory.build_async(
            session)

        dict_data = org_api_key_manager.to_dict(
            org_api_key)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `OrgApiKeyManager` class.

        This method tests the functionality of the
        `from_json` method of the `OrgApiKeyManager` class.
        It creates a org_api_key using
        the `OrgApiKeyFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        org_api_key is an instance of the
        `OrgApiKey` class and has
        the same code as the original org_api_key.

        Args:
            org_api_key_manager (OrgApiKeyManager): An
            instance of the
                `OrgApiKeyManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        org_api_key = await OrgApiKeyFactory.create_async(
            session)

        json_data = org_api_key_manager.to_json(
            org_api_key)

        deserialized_org_api_key = org_api_key_manager.from_json(json_data)

        assert isinstance(deserialized_org_api_key, OrgApiKey)
        assert deserialized_org_api_key.code == \
            org_api_key.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `OrgApiKeyManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        org_api_key object.

        Args:
            org_api_key_manager (OrgApiKeyManager): An instance
                of the `OrgApiKeyManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        org_api_key = await OrgApiKeyFactory.create_async(
            session)

        schema = OrgApiKeySchema()

        org_api_key_data = schema.dump(org_api_key)

        assert isinstance(org_api_key_data, dict)

        deserialized_org_api_key = org_api_key_manager.from_dict(
            org_api_key_data)

        assert isinstance(deserialized_org_api_key, OrgApiKey)

        assert deserialized_org_api_key.code == \
            org_api_key.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the OrgApiKeyManager class.

        This test case creates 5 org_api_key
        objects using the
        OrgApiKeyFactory and checks if the count method
        returns the correct count of
        org_api_keys.

        Steps:
        1. Create 5 org_api_key objects using
            the OrgApiKeyFactory.
        2. Call the count method of the org_api_key_manager.
        3. Assert that the count is equal to 5.

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
        Test the count method when the database is empty.

        This test case checks if the count method of the
        OrgApiKeyManager class returns 0 when the database is empty.

        Args:
            org_api_key_manager (OrgApiKeyManager): An
                instance of the
                OrgApiKeyManager class.

        Returns:
            None
        """

        count = await org_api_key_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a org_api_key instance.

        This test performs the following steps:
        1. Creates a org_api_key instance using
            the OrgApiKeyFactory.
        2. Retrieves the org_api_key from th
            database to ensure
            it was added correctly.
        3. Updates the org_api_key's code and verifies the update.
        4. Refreshes the original org_api_key instance
            and checks if
            it reflects the updated code.

        Args:
            org_api_key_manager (OrgApiKeyManager): The
                manager responsible
                for org_api_key operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(
            session=session)

        # Retrieve the org_api_key from the database
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == org_api_key1.org_api_key_id)  # type: ignore
        )  # type: ignore
        org_api_key2 = result.scalars().first()

        # Verify that the retrieved org_api_key
        # matches the added org_api_key
        assert org_api_key1.code == \
            org_api_key2.code

        # Update the org_api_key's code
        updated_code1 = uuid.uuid4()
        org_api_key1.code = updated_code1
        updated_org_api_key1 = await org_api_key_manager.update(
            org_api_key1)

        # Verify that the updated org_api_key
        # is of type OrgApiKey
        # and has the updated code
        assert isinstance(updated_org_api_key1, OrgApiKey)

        assert updated_org_api_key1.code == updated_code1

        # Refresh the original org_api_key instance
        refreshed_org_api_key2 = await org_api_key_manager.refresh(
            org_api_key2)

        # Verify that the refreshed org_api_key
        # reflects the updated code
        assert refreshed_org_api_key2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent org_api_key.

        Args:
            org_api_key_manager (OrgApiKeyManager): The
                instance of the
                OrgApiKeyManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the org_api_key
            refresh operation raises an exception.

        Returns:
            None
        """
        org_api_key = OrgApiKey(
            org_api_key_id=999)

        with pytest.raises(Exception):
            await org_api_key_manager.refresh(
                org_api_key)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to check if a org_api_key
        exists using the manager function.

        Args:
            org_api_key_manager (OrgApiKeyManager): The
                org_api_key manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(
            session=session)

        # Check if the org_api_key exists
        # using the manager function
        assert await org_api_key_manager.exists(
            org_api_key1.org_api_key_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        OrgApiKeyManager class correctly compares two org_api_keys.

        Args:
            org_api_key_manager (OrgApiKeyManager): An
                instance of the
                OrgApiKeyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a org_api_key
        org_api_key1 = await OrgApiKeyFactory.create_async(
            session=session)

        org_api_key2 = await org_api_key_manager.get_by_id(
            org_api_key_id=org_api_key1.org_api_key_id)

        assert org_api_key_manager.is_equal(
            org_api_key1, org_api_key2) is True

        org_api_key1_dict = org_api_key_manager.to_dict(
            org_api_key1)

        org_api_key3 = org_api_key_manager.from_dict(
            org_api_key1_dict)

        assert org_api_key_manager.is_equal(
            org_api_key1, org_api_key3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_org_api_key(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
        Test case to check if a org_api_key with a
        non-existent ID exists in the database.

        Args:
            org_api_key_manager (OrgApiKeyManager): The
                instance of the OrgApiKeyManager class.

        Returns:
            bool: True if the org_api_key exists,
                False otherwise.
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
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            org_api_key_manager (OrgApiKeyManager): The instance
                of the OrgApiKeyManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await org_api_key_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()

