# managers/tests/org_api_key_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `OrgApiKeyManager` class.
"""

import uuid  # noqa: F401
from typing import List

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
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
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `OrgApiKeyManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return OrgApiKeyManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: OrgApiKeyManager
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
        org_api_key = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of OrgApiKey
        assert isinstance(
            org_api_key,
            OrgApiKey)

        # Assert that the attributes of the
        # org_api_key match our mock data
        assert org_api_key.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: OrgApiKeyManager,
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
            await obj_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_org_api_key_to_database(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `OrgApiKeyManager` that checks if a
        org_api_key is correctly added to the database.
        """
        new_obj = await \
            OrgApiKeyFactory.build_async(
                session)

        assert new_obj.org_api_key_id == 0

        # Add the org_api_key using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                org_api_key=new_obj)

        assert isinstance(added_obj,
                          OrgApiKey)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.org_api_key_id > 0

        # Fetch the org_api_key from
        # the database directly
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == (
                    added_obj.org_api_key_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched org_api_key
        # is not None and matches the
        # added org_api_key
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          OrgApiKey)
        assert fetched_obj.org_api_key_id == \
            added_obj.org_api_key_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_org_api_key_object(
        self,
        obj_manager: OrgApiKeyManager,
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
        new_obj = await \
            OrgApiKeyFactory.build_async(
                session)

        assert new_obj.org_api_key_id == 0

        new_obj.code = uuid.uuid4()

        # Add the org_api_key using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                org_api_key=new_obj)

        assert isinstance(added_obj,
                          OrgApiKey)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.org_api_key_id > 0

        # Assert that the returned
        # org_api_key matches the
        # test org_api_key
        assert added_obj.org_api_key_id == \
            new_obj.org_api_key_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrgApiKeyManager`
        that checks if a org_api_key
        is correctly updated.
        """
        new_obj = await \
            OrgApiKeyFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                org_api_key=new_obj)

        assert isinstance(updated_obj,
                          OrgApiKey)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.org_api_key_id == \
            new_obj.org_api_key_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == (
                    new_obj.org_api_key_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.org_api_key_id == \
            fetched_obj.org_api_key_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.org_api_key_id == \
            fetched_obj.org_api_key_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `OrgApiKeyManager`
        that checks if a org_api_key is
        correctly updated using a dictionary.
        """
        new_obj = await \
            OrgApiKeyFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                org_api_key=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          OrgApiKey)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.org_api_key_id == \
            new_obj.org_api_key_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == (
                    new_obj.org_api_key_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.org_api_key_id == \
            fetched_obj.org_api_key_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.org_api_key_id == \
            fetched_obj.org_api_key_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_org_api_key(
        self,
        obj_manager: OrgApiKeyManager
    ):
        """
        Test case for the `update` method of
        `OrgApiKeyManager`
        with an invalid org_api_key.
        """

        # None org_api_key
        org_api_key = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                org_api_key, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `OrgApiKeyManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            OrgApiKeyFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                org_api_key=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `OrgApiKeyManager`.
        """
        new_obj = await OrgApiKeyFactory.create_async(
            session)

        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == (
                    new_obj.org_api_key_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          OrgApiKey)

        assert fetched_obj.org_api_key_id == \
            new_obj.org_api_key_id

        await obj_manager.delete(
            org_api_key_id=new_obj.org_api_key_id)

        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == (
                    new_obj.org_api_key_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        org_api_key.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        org_api_key,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            OrgApiKeyManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a org_api_key
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (OrgApiKeyManager): An
                instance of the
                `OrgApiKeyManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await obj_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `OrgApiKeyManager` class.

        This test verifies that the `get_list`
        method returns the correct list of org_api_keys.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 org_api_key objects using the
            `OrgApiKeyFactory.create_async` method.
        4. Assert that the
            `org_api_keys_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 org_api_keys.
        7. Assert that all elements in the returned list are
            instances of the
            `OrgApiKey` class.
        """

        org_api_keys = await obj_manager.get_list()

        assert len(org_api_keys) == 0

        org_api_keys_data = (
            [await OrgApiKeyFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(org_api_keys_data, List)

        org_api_keys = await obj_manager.get_list()

        assert len(org_api_keys) == 5
        assert all(isinstance(
            org_api_key,
            OrgApiKey
        ) for org_api_key in org_api_keys)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the OrgApiKeyManager class.

        Args:
            obj_manager
            (OrgApiKeyManager): An
                instance of the
                OrgApiKeyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        org_api_key = await \
            OrgApiKeyFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            org_api_key)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the OrgApiKeyManager class.

        Args:
            obj_manager
            (OrgApiKeyManager): An
                instance of the
                OrgApiKeyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        org_api_key = await \
            OrgApiKeyFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                org_api_key)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `OrgApiKeyManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `OrgApiKeyManager` class.
        It creates a org_api_key using
        the `OrgApiKeyFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        org_api_key is an instance of the
        `OrgApiKey` class and has
        the same code as the original org_api_key.

        Args:
            obj_manager
            (OrgApiKeyManager): An
                instance of the
                `OrgApiKeyManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        org_api_key = await \
            OrgApiKeyFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            org_api_key)

        deserialized_org_api_key = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_org_api_key,
                          OrgApiKey)
        assert deserialized_org_api_key.code == \
            org_api_key.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: OrgApiKeyManager,
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
            obj_manager
            (OrgApiKeyManager): An instance
                of the `OrgApiKeyManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        org_api_key = await \
            OrgApiKeyFactory.create_async(
                session)

        schema = OrgApiKeySchema()

        new_obj = schema.dump(org_api_key)

        assert isinstance(new_obj, dict)

        deserialized_org_api_key = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_org_api_key,
                          OrgApiKey)

        assert deserialized_org_api_key.code == \
            org_api_key.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: OrgApiKeyManager,
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
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        org_api_keys_data = (
            [await OrgApiKeyFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(org_api_keys_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: OrgApiKeyManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        OrgApiKeyManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (OrgApiKeyManager): An
                instance of the
                OrgApiKeyManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: OrgApiKeyManager,
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
            obj_manager
            (OrgApiKeyManager): The
                manager responsible
                for org_api_key operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a org_api_key
        obj_1 = await OrgApiKeyFactory.create_async(
            session=session)

        # Retrieve the org_api_key from the database
        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == (
                    obj_1.org_api_key_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved org_api_key
        # matches the added org_api_key
        assert obj_1.code == \
            obj_2.code

        # Update the org_api_key's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated org_api_key
        # is of type OrgApiKey
        # and has the updated code
        assert isinstance(updated_obj_1,
                          OrgApiKey)

        assert updated_obj_1.code == updated_code1

        # Refresh the original org_api_key instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed org_api_key
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_org_api_key(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent org_api_key.

        Args:
            obj_manager
            (OrgApiKeyManager): The
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
            await obj_manager.refresh(
                org_api_key)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_org_api_key(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to check if a org_api_key
        exists using the manager function.

        Args:
            obj_manager
            (OrgApiKeyManager): The
                org_api_key manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a org_api_key
        obj_1 = await OrgApiKeyFactory.create_async(
            session=session)

        # Check if the org_api_key exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.org_api_key_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_org_api_key(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        OrgApiKeyManager
        class correctly compares two
        org_api_keys.

        Args:
            obj_manager
            (OrgApiKeyManager): An
                instance of the
                OrgApiKeyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a org_api_key
        obj_1 = await \
            OrgApiKeyFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                org_api_key_id=obj_1.org_api_key_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        org_api_key3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, org_api_key3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_org_api_key(
        self,
        obj_manager: OrgApiKeyManager
    ):
        """
        Test case to check if a org_api_key with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (OrgApiKeyManager): The
                instance of the OrgApiKeyManager class.

        Returns:
            bool: True if the org_api_key exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (OrgApiKeyManager): The instance
                of the OrgApiKeyManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await obj_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
