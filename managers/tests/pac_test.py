# managers/tests/pac_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `PacManager` class.
"""

import uuid  # noqa: F401
from typing import List

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
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
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `PacManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return PacManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: PacManager
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
        pac = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of Pac
        assert isinstance(
            pac,
            Pac)

        # Assert that the attributes of the
        # pac match our mock data
        assert pac.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: PacManager,
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
            await obj_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_pac_to_database(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `PacManager` that checks if a
        pac is correctly added to the database.
        """
        new_obj = await \
            PacFactory.build_async(
                session)

        assert new_obj.pac_id == 0

        # Add the pac using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                pac=new_obj)

        assert isinstance(added_obj,
                          Pac)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.pac_id > 0

        # Fetch the pac from
        # the database directly
        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == (
                    added_obj.pac_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched pac
        # is not None and matches the
        # added pac
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          Pac)
        assert fetched_obj.pac_id == \
            added_obj.pac_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_pac_object(
        self,
        obj_manager: PacManager,
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
        new_obj = await \
            PacFactory.build_async(
                session)

        assert new_obj.pac_id == 0

        new_obj.code = uuid.uuid4()

        # Add the pac using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                pac=new_obj)

        assert isinstance(added_obj,
                          Pac)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.pac_id > 0

        # Assert that the returned
        # pac matches the
        # test pac
        assert added_obj.pac_id == \
            new_obj.pac_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `PacManager`
        that checks if a pac
        is correctly updated.
        """
        new_obj = await \
            PacFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                pac=new_obj)

        assert isinstance(updated_obj,
                          Pac)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.pac_id == \
            new_obj.pac_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == (
                    new_obj.pac_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.pac_id == \
            fetched_obj.pac_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.pac_id == \
            fetched_obj.pac_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `PacManager`
        that checks if a pac is
        correctly updated using a dictionary.
        """
        new_obj = await \
            PacFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                pac=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          Pac)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.pac_id == \
            new_obj.pac_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == (
                    new_obj.pac_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.pac_id == \
            fetched_obj.pac_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.pac_id == \
            fetched_obj.pac_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_pac(
        self,
        obj_manager: PacManager
    ):
        """
        Test case for the `update` method of
        `PacManager`
        with an invalid pac.
        """

        # None pac
        pac = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                pac, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `PacManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            PacFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                pac=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `PacManager`.
        """
        new_obj = await PacFactory.create_async(
            session)

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == (
                    new_obj.pac_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Pac)

        assert fetched_obj.pac_id == \
            new_obj.pac_id

        await obj_manager.delete(
            pac_id=new_obj.pac_id)

        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == (
                    new_obj.pac_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        pac.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        pac,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            PacManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a pac
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (PacManager): An
                instance of the
                `PacManager` class.
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
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `PacManager` class.

        This test verifies that the `get_list`
        method returns the correct list of pacs.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 pac objects using the
            `PacFactory.create_async` method.
        4. Assert that the
            `pacs_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 pacs.
        7. Assert that all elements in the returned list are
            instances of the
            `Pac` class.
        """

        pacs = await obj_manager.get_list()

        assert len(pacs) == 0

        pacs_data = (
            [await PacFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(pacs_data, List)

        pacs = await obj_manager.get_list()

        assert len(pacs) == 5
        assert all(isinstance(
            pac,
            Pac
        ) for pac in pacs)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the PacManager class.

        Args:
            obj_manager
            (PacManager): An
                instance of the
                PacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        pac = await \
            PacFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            pac)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the PacManager class.

        Args:
            obj_manager
            (PacManager): An
                instance of the
                PacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        pac = await \
            PacFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                pac)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `PacManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `PacManager` class.
        It creates a pac using
        the `PacFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        pac is an instance of the
        `Pac` class and has
        the same code as the original pac.

        Args:
            obj_manager
            (PacManager): An
                instance of the
                `PacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        pac = await \
            PacFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            pac)

        deserialized_pac = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_pac,
                          Pac)
        assert deserialized_pac.code == \
            pac.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: PacManager,
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
            obj_manager
            (PacManager): An instance
                of the `PacManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        pac = await \
            PacFactory.create_async(
                session)

        schema = PacSchema()

        new_obj = schema.dump(pac)

        assert isinstance(new_obj, dict)

        deserialized_pac = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_pac,
                          Pac)

        assert deserialized_pac.code == \
            pac.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: PacManager,
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
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        pacs_data = (
            [await PacFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(pacs_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: PacManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        PacManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (PacManager): An
                instance of the
                PacManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: PacManager,
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
            obj_manager
            (PacManager): The
                manager responsible
                for pac operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a pac
        obj_1 = await PacFactory.create_async(
            session=session)

        # Retrieve the pac from the database
        result = await session.execute(
            select(Pac).filter(
                Pac._pac_id == (
                    obj_1.pac_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved pac
        # matches the added pac
        assert obj_1.code == \
            obj_2.code

        # Update the pac's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated pac
        # is of type Pac
        # and has the updated code
        assert isinstance(updated_obj_1,
                          Pac)

        assert updated_obj_1.code == updated_code1

        # Refresh the original pac instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed pac
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_pac(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent pac.

        Args:
            obj_manager
            (PacManager): The
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
            await obj_manager.refresh(
                pac)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_pac(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to check if a pac
        exists using the manager function.

        Args:
            obj_manager
            (PacManager): The
                pac manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a pac
        obj_1 = await PacFactory.create_async(
            session=session)

        # Check if the pac exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.pac_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_pac(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        PacManager
        class correctly compares two
        pacs.

        Args:
            obj_manager
            (PacManager): An
                instance of the
                PacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a pac
        obj_1 = await \
            PacFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                pac_id=obj_1.pac_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        pac3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, pac3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_pac(
        self,
        obj_manager: PacManager
    ):
        """
        Test case to check if a pac with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (PacManager): The
                instance of the PacManager class.

        Returns:
            bool: True if the pac exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: PacManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (PacManager): The instance
                of the PacManager class.
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
