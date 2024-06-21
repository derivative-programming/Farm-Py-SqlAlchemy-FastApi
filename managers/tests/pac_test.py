# models/managers/tests/pac_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `PacManager` class.
"""

from typing import List
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.pac import PacManager
from models import Pac
from models.factory import PacFactory
from models.serialization_schema.pac import PacSchema

class TestPacManager:
    """
    This class contains unit tests for the
    `PacManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def pac_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `PacManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return PacManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        pac_manager: PacManager
    ):
        """
        Test case for the `build` method of
        `PacManager`.
        """
        # Define mock data for our pac
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        pac = await pac_manager.build(
            **mock_data)

        # Assert that the returned object is an instance of Pac
        assert isinstance(
            pac, Pac)

        # Assert that the attributes of the
        # pac match our mock data
        assert pac.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `PacManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }

        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await pac_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_pac_to_database(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `PacManager` that checks if a
        pac is correctly added to the database.
        """
        test_pac = await PacFactory.build_async(
            session)

        assert test_pac.pac_id == 0

        # Add the pac using the
        # manager's add method
        added_pac = await pac_manager.add(
            pac=test_pac)

        assert isinstance(added_pac, Pac)

        assert str(added_pac.insert_user_id) == (
            str(pac_manager._session_context.customer_code))
        assert str(added_pac.last_update_user_id) == (
            str(pac_manager._session_context.customer_code))

        assert added_pac.pac_id > 0

        # Fetch the pac from
        # the database directly
        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == added_pac.pac_id  # type: ignore
            )
        )
        fetched_pac = result.scalars().first()

        # Assert that the fetched pac
        # is not None and matches the
        # added pac
        assert fetched_pac is not None
        assert isinstance(fetched_pac, Pac)
        assert fetched_pac.pac_id == added_pac.pac_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_pac_object(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `PacManager` that checks if the
        correct pac object is returned.
        """
        # Create a test pac
        # using the PacFactory
        # without persisting it to the database
        test_pac = await PacFactory.build_async(
            session)

        assert test_pac.pac_id == 0

        test_pac.code = uuid.uuid4()

        # Add the pac using
        # the manager's add method
        added_pac = await pac_manager.add(
            pac=test_pac)

        assert isinstance(added_pac, Pac)

        assert str(added_pac.insert_user_id) == (
            str(pac_manager._session_context.customer_code))
        assert str(added_pac.last_update_user_id) == (
            str(pac_manager._session_context.customer_code))

        assert added_pac.pac_id > 0

        # Assert that the returned
        # pac matches the
        # test pac
        assert added_pac.pac_id == \
            test_pac.pac_id
        assert added_pac.code == \
            test_pac.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `PacManager`
        that checks if a pac
        is correctly updated.
        """
        test_pac = await PacFactory.create_async(
            session)

        test_pac.code = uuid.uuid4()

        updated_pac = await pac_manager.update(
            pac=test_pac)

        assert isinstance(updated_pac, Pac)

        assert str(updated_pac.last_update_user_id) == str(
            pac_manager._session_context.customer_code)

        assert updated_pac.pac_id == \
            test_pac.pac_id
        assert updated_pac.code == \
            test_pac.code

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == test_pac.pac_id)  # type: ignore
        )

        fetched_pac = result.scalars().first()

        assert updated_pac.pac_id == \
            fetched_pac.pac_id
        assert updated_pac.code == \
            fetched_pac.code

        assert test_pac.pac_id == \
            fetched_pac.pac_id
        assert test_pac.code == \
            fetched_pac.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `PacManager`
        that checks if a pac is
        correctly updated using a dictionary.
        """
        test_pac = await PacFactory.create_async(
            session)

        new_code = uuid.uuid4()

        updated_pac = await pac_manager.update(
            pac=test_pac,
            code=new_code
        )

        assert isinstance(updated_pac, Pac)

        assert str(updated_pac.last_update_user_id) == str(
            pac_manager._session_context.customer_code
        )

        assert updated_pac.pac_id == \
            test_pac.pac_id
        assert updated_pac.code == new_code

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == test_pac.pac_id)  # type: ignore
        )

        fetched_pac = result.scalars().first()

        assert updated_pac.pac_id == \
            fetched_pac.pac_id
        assert updated_pac.code == \
            fetched_pac.code

        assert test_pac.pac_id == \
            fetched_pac.pac_id
        assert new_code == \
            fetched_pac.code

    @pytest.mark.asyncio
    async def test_update_invalid_pac(
        self,
        pac_manager: PacManager
    ):
        """
        Test case for the `update` method of `PacManager`
        with an invalid pac.
        """

        # None pac
        pac = None

        new_code = uuid.uuid4()

        updated_pac = await (
            pac_manager.update(
                pac, code=new_code))  # type: ignore

        # Assertions
        assert updated_pac is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `PacManager`
        with a nonexistent attribute.
        """
        test_pac = await PacFactory.create_async(
            session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await pac_manager.update(
                pac=test_pac,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `PacManager`.
        """
        pac_data = await PacFactory.create_async(
            session)

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == pac_data.pac_id)  # type: ignore
        )
        fetched_pac = result.scalars().first()

        assert isinstance(fetched_pac, Pac)

        assert fetched_pac.pac_id == \
            pac_data.pac_id

        await pac_manager.delete(
            pac_id=pac_data.pac_id)

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == pac_data.pac_id)  # type: ignore
        )
        fetched_pac = result.scalars().first()

        assert fetched_pac is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent pac.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent pac,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param pac_manager: The instance of the PacManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await pac_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a pac
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `pac_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            pac_manager (PacManager): An
                instance of the
                `PacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await pac_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `PacManager` class.

        This test verifies that the `get_list`
        method returns the correct list of pacs.

        Steps:
        1. Call the `get_list` method of the
            `pac_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 pac objects using the
            `PacFactory.create_async` method.
        4. Assert that the `pacs_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `pac_manager` instance again.
        6. Assert that the returned list contains 5 pacs.
        7. Assert that all elements in the returned list are
            instances of the `Pac` class.
        """

        pacs = await pac_manager.get_list()

        assert len(pacs) == 0

        pacs_data = (
            [await PacFactory.create_async(session) for _ in range(5)])

        assert isinstance(pacs_data, List)

        pacs = await pac_manager.get_list()

        assert len(pacs) == 5
        assert all(isinstance(
            pac, Pac) for pac in pacs)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the PacManager class.

        Args:
            pac_manager (PacManager): An
                instance of the
                PacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        pac = await PacFactory.build_async(
            session)

        json_data = pac_manager.to_json(
            pac)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the PacManager class.

        Args:
            pac_manager (PacManager): An
                instance of the
                PacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        pac = await PacFactory.build_async(
            session)

        dict_data = pac_manager.to_dict(
            pac)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `PacManager` class.

        This method tests the functionality of the
        `from_json` method of the `PacManager` class.
        It creates a pac using
        the `PacFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        pac is an instance of the
        `Pac` class and has
        the same code as the original pac.

        Args:
            pac_manager (PacManager): An
            instance of the
                `PacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        pac = await PacFactory.create_async(
            session)

        json_data = pac_manager.to_json(
            pac)

        deserialized_pac = pac_manager.from_json(json_data)

        assert isinstance(deserialized_pac, Pac)
        assert deserialized_pac.code == \
            pac.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `PacManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        pac object.

        Args:
            pac_manager (PacManager): An instance
                of the `PacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        pac = await PacFactory.create_async(
            session)

        schema = PacSchema()

        pac_data = schema.dump(pac)

        assert isinstance(pac_data, dict)

        deserialized_pac = pac_manager.from_dict(
            pac_data)

        assert isinstance(deserialized_pac, Pac)

        assert deserialized_pac.code == \
            pac.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the PacManager class.

        This test case creates 5 pac
        objects using the
        PacFactory and checks if the count method
        returns the correct count of
        pacs.

        Steps:
        1. Create 5 pac objects using
            the PacFactory.
        2. Call the count method of the pac_manager.
        3. Assert that the count is equal to 5.

        """
        pacs_data = (
            [await PacFactory.create_async(session) for _ in range(5)])

        assert isinstance(pacs_data, List)

        count = await pac_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        pac_manager: PacManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        PacManager class returns 0 when the database is empty.

        Args:
            pac_manager (PacManager): An
                instance of the
                PacManager class.

        Returns:
            None
        """

        count = await pac_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a pac instance.

        This test performs the following steps:
        1. Creates a pac instance using
            the PacFactory.
        2. Retrieves the pac from th
            database to ensure
            it was added correctly.
        3. Updates the pac's code and verifies the update.
        4. Refreshes the original pac instance
            and checks if
            it reflects the updated code.

        Args:
            pac_manager (PacManager): The
                manager responsible
                for pac operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a pac
        pac1 = await PacFactory.create_async(
            session=session)

        # Retrieve the pac from the database
        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == pac1.pac_id)  # type: ignore
        )  # type: ignore
        pac2 = result.scalars().first()

        # Verify that the retrieved pac
        # matches the added pac
        assert pac1.code == \
            pac2.code

        # Update the pac's code
        updated_code1 = uuid.uuid4()
        pac1.code = updated_code1
        updated_pac1 = await pac_manager.update(
            pac1)

        # Verify that the updated pac
        # is of type Pac
        # and has the updated code
        assert isinstance(updated_pac1, Pac)

        assert updated_pac1.code == updated_code1

        # Refresh the original pac instance
        refreshed_pac2 = await pac_manager.refresh(
            pac2)

        # Verify that the refreshed pac
        # reflects the updated code
        assert refreshed_pac2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_pac(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent pac.

        Args:
            pac_manager (PacManager): The
                instance of the
                PacManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the pac
            refresh operation raises an exception.

        Returns:
            None
        """
        pac = Pac(
            pac_id=999)

        with pytest.raises(Exception):
            await pac_manager.refresh(
                pac)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_pac(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to check if a pac
        exists using the manager function.

        Args:
            pac_manager (PacManager): The
                pac manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a pac
        pac1 = await PacFactory.create_async(
            session=session)

        # Check if the pac exists
        # using the manager function
        assert await pac_manager.exists(
            pac1.pac_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_pac(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        PacManager class correctly compares two pacs.

        Args:
            pac_manager (PacManager): An
                instance of the
                PacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a pac
        pac1 = await PacFactory.create_async(
            session=session)

        pac2 = await pac_manager.get_by_id(
            pac_id=pac1.pac_id)

        assert pac_manager.is_equal(
            pac1, pac2) is True

        pac1_dict = pac_manager.to_dict(
            pac1)

        pac3 = pac_manager.from_dict(
            pac1_dict)

        assert pac_manager.is_equal(
            pac1, pac3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_pac(
        self,
        pac_manager: PacManager
    ):
        """
        Test case to check if a pac with a
        non-existent ID exists in the database.

        Args:
            pac_manager (PacManager): The
                instance of the PacManager class.

        Returns:
            bool: True if the pac exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await pac_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        pac_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            pac_manager (PacManager): The instance
                of the PacManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await pac_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()
# endset
