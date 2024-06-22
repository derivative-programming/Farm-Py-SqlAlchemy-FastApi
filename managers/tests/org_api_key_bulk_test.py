# models/managers/tests/org_api_key_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `OrgApiKeyManager` class.
"""

import logging
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.org_api_key import OrgApiKeyManager
from models import OrgApiKey
from models.factory import OrgApiKeyFactory

class TestOrgApiKeyBulkManager:
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
    async def test_add_bulk(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `OrgApiKeyManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        org_api_keys to the database.

        Steps:
        1. Generate a list of org_api_key data using the
            `OrgApiKeyFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `org_api_key_manager` instance,
            passing in the
            generated org_api_key data.
        3. Verify that the number of org_api_keys
            returned is
            equal to the number of org_api_keys added.
        4. For each updated org_api_key, fetch the corresponding
            org_api_key from the database.
        5. Verify that the fetched org_api_key
            is an instance of the
            `OrgApiKey` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            org_api_key match the
            customer code of the session context.
        7. Verify that the org_api_key_id of the fetched
            org_api_key matches the
            org_api_key_id of the updated
            org_api_key.

        """
        org_api_keys_data = [
            await OrgApiKeyFactory.build_async(session) for _ in range(5)]

        org_api_keys = await org_api_key_manager.add_bulk(
            org_api_keys_data)

        assert len(org_api_keys) == 5

        for updated_org_api_key in org_api_keys:
            result = await session.execute(
                select(OrgApiKey).filter(
                    OrgApiKey._org_api_key_id == updated_org_api_key.org_api_key_id  # type: ignore
                )
            )
            fetched_org_api_key = result.scalars().first()

            assert isinstance(
                fetched_org_api_key, OrgApiKey)

            assert str(fetched_org_api_key.insert_user_id) == (
                str(org_api_key_manager._session_context.customer_code))
            assert str(fetched_org_api_key.last_update_user_id) == (
                str(org_api_key_manager._session_context.customer_code))

            assert fetched_org_api_key.org_api_key_id == \
                updated_org_api_key.org_api_key_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of org_api_keys.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `OrgApiKeyManager` class.
        It creates two org_api_key instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two org_api_key instances using the
            `OrgApiKeyFactory.create_async` method.
        2. Generate new codes for the org_api_keys.
        3. Update the org_api_keys' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            org_api_key_manager (OrgApiKeyManager):
                An instance of the
                `OrgApiKeyManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking org_api_key instances
        org_api_key1 = await OrgApiKeyFactory. \
            create_async(
                session=session)
        org_api_key2 = await OrgApiKeyFactory. \
            create_async(
                session=session)
        logging.info(org_api_key1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update org_api_keys
        updates = [
            {
                "org_api_key_id":
                    org_api_key1.org_api_key_id,
                "code": code_updated1
            },
            {
                "org_api_key_id":
                    org_api_key2.org_api_key_id,
                "code": code_updated2
            }
        ]
        updated_org_api_keys = await org_api_key_manager.update_bulk(
            updates)

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
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == 1)  # type: ignore
        )
        fetched_org_api_key = result.scalars().first()

        assert isinstance(fetched_org_api_key, OrgApiKey)

        assert fetched_org_api_key.code == code_updated1

        result = await session.execute(
            select(OrgApiKey).filter(
                OrgApiKey._org_api_key_id == 2)  # type: ignore
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
        Test case to verify the behavior of the `update_bulk`
        method when the org_api_key_id is missing.

        This test case ensures that when the org_api_key_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing org_api_key_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

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
        Test case to verify the behavior of the update_bulk
        method when a org_api_key is not found.

        This test case performs the following steps:
        1. Defines a list of org_api_key updates,
            where each update
            contains a org_api_key_id and a code.
        2. Calls the update_bulk method of the
            org_api_key_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the org_api_key was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        org_api_key is not found.

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
        Test case to verify the behavior of the
        update_bulk method when invalid data types are provided.

        This test case verifies that when the update_bulk method
        is called with a list of updates containing invalid data types,
        an exception is raised. The test case also ensures
        that the session is rolled back after the test
        to maintain data integrity.

        :param org_api_key_manager: An instance of the OrgApiKeyManager class.
        :param session: An instance of the AsyncSession class.
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
        Test case for the delete_bulk method of the
        OrgApiKeyManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple org_api_keys
        from the database.

        Steps:
        1. Create two org_api_key objects
            using the OrgApiKeyFactory.
        2. Delete the org_api_keys using the
            delete_bulk method
            of the org_api_key_manager.
        3. Verify that the delete operation was successful by
            checking if the org_api_keys no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The org_api_keys should no longer exist in the database.

        """

        org_api_key1 = await OrgApiKeyFactory.create_async(
            session=session)

        org_api_key2 = await OrgApiKeyFactory.create_async(
            session=session)

        # Delete org_api_keys
        org_api_key_ids = [org_api_key1.org_api_key_id, org_api_key2.org_api_key_id]
        result = await org_api_key_manager.delete_bulk(
            org_api_key_ids)

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
        Test case to verify the behavior of deleting bulk
        org_api_keys when some org_api_keys are not found.

        Steps:
        1. Create a org_api_key using the
            OrgApiKeyFactory.
        2. Assert that the created org_api_key
            is an instance of the
            OrgApiKey class.
        3. Define a list of org_api_key IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk org_api_keys.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        OrgApiKeyManager raises an exception
        when some org_api_keys with the specified IDs are
        not found in the database.
        """
        org_api_key1 = await OrgApiKeyFactory.create_async(
            session=session)

        assert isinstance(org_api_key1, OrgApiKey)

        # Delete org_api_keys
        org_api_key_ids = [1, 2]

        with pytest.raises(Exception):
            await org_api_key_manager.delete_bulk(
                org_api_key_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        org_api_key_manager: OrgApiKeyManager
    ):
        """
        Test case to verify the behavior of deleting
        org_api_keys with an empty list.

        Args:
            org_api_key_manager (OrgApiKeyManager): The
                instance of the
                OrgApiKeyManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete org_api_keys with an empty list
        org_api_key_ids = []
        result = await org_api_key_manager.delete_bulk(
            org_api_key_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        org_api_key_manager: OrgApiKeyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid org_api_key IDs are provided.

        Args:
            org_api_key_manager (OrgApiKeyManager): The
                instance of the
                OrgApiKeyManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        org_api_key_ids = ["1", 2]

        with pytest.raises(Exception):
            await org_api_key_manager.delete_bulk(
                org_api_key_ids)

        await session.rollback()
