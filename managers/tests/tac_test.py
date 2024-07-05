# managers/tests/tac_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `TacManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.tac import (
    TacManager)
from models import Tac
from models.factory import (
    TacFactory)
from models.serialization_schema.tac import (
    TacSchema)


class TestTacManager:
    """
    This class contains unit tests for the
    `TacManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `TacManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return TacManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: TacManager
    ):
        """
        Test case for the `build` method of
        `TacManager`.
        """
        # Define mock data for our tac
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        tac = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of Tac
        assert isinstance(
            tac,
            Tac)

        # Assert that the attributes of the
        # tac match our mock data
        assert tac.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `TacManager` with missing data.
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
    async def test_add_correctly_adds_tac_to_database(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `TacManager` that checks if a
        tac is correctly added to the database.
        """
        new_obj = await \
            TacFactory.build_async(
                session)

        assert new_obj.tac_id == 0

        # Add the tac using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                tac=new_obj)

        assert isinstance(added_obj,
                          Tac)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.tac_id > 0

        # Fetch the tac from
        # the database directly
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == (
                    added_obj.tac_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched tac
        # is not None and matches the
        # added tac
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          Tac)
        assert fetched_obj.tac_id == \
            added_obj.tac_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_tac_object(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `TacManager` that checks if the
        correct tac object is returned.
        """
        # Create a test tac
        # using the TacFactory
        # without persisting it to the database
        new_obj = await \
            TacFactory.build_async(
                session)

        assert new_obj.tac_id == 0

        new_obj.code = uuid.uuid4()

        # Add the tac using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                tac=new_obj)

        assert isinstance(added_obj,
                          Tac)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.tac_id > 0

        # Assert that the returned
        # tac matches the
        # test tac
        assert added_obj.tac_id == \
            new_obj.tac_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `TacManager`
        that checks if a tac
        is correctly updated.
        """
        new_obj = await \
            TacFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                tac=new_obj)

        assert isinstance(updated_obj,
                          Tac)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.tac_id == \
            new_obj.tac_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == (
                    new_obj.tac_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.tac_id == \
            fetched_obj.tac_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.tac_id == \
            fetched_obj.tac_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `TacManager`
        that checks if a tac is
        correctly updated using a dictionary.
        """
        new_obj = await \
            TacFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                tac=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          Tac)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.tac_id == \
            new_obj.tac_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == (
                    new_obj.tac_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.tac_id == \
            fetched_obj.tac_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.tac_id == \
            fetched_obj.tac_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_tac(
        self,
        obj_manager: TacManager
    ):
        """
        Test case for the `update` method of
        `TacManager`
        with an invalid tac.
        """

        # None tac
        tac = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                tac, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `TacManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            TacFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                tac=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `TacManager`.
        """
        new_obj = await TacFactory.create_async(
            session)

        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == (
                    new_obj.tac_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          Tac)

        assert fetched_obj.tac_id == \
            new_obj.tac_id

        await obj_manager.delete(
            tac_id=new_obj.tac_id)

        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == (
                    new_obj.tac_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        tac.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        tac,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            TacManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a tac
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (TacManager): An
                instance of the
                `TacManager` class.
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
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `TacManager` class.

        This test verifies that the `get_list`
        method returns the correct list of tacs.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 tac objects using the
            `TacFactory.create_async` method.
        4. Assert that the
            `tacs_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 tacs.
        7. Assert that all elements in the returned list are
            instances of the
            `Tac` class.
        """

        tacs = await obj_manager.get_list()

        assert len(tacs) == 0

        tacs_data = (
            [await TacFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(tacs_data, List)

        tacs = await obj_manager.get_list()

        assert len(tacs) == 5
        assert all(isinstance(
            tac,
            Tac
        ) for tac in tacs)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the TacManager class.

        Args:
            obj_manager
            (TacManager): An
                instance of the
                TacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        tac = await \
            TacFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            tac)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the TacManager class.

        Args:
            obj_manager
            (TacManager): An
                instance of the
                TacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        tac = await \
            TacFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                tac)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `TacManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `TacManager` class.
        It creates a tac using
        the `TacFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        tac is an instance of the
        `Tac` class and has
        the same code as the original tac.

        Args:
            obj_manager
            (TacManager): An
                instance of the
                `TacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        tac = await \
            TacFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            tac)

        deserialized_tac = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_tac,
                          Tac)
        assert deserialized_tac.code == \
            tac.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `TacManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        tac object.

        Args:
            obj_manager
            (TacManager): An instance
                of the `TacManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        tac = await \
            TacFactory.create_async(
                session)

        schema = TacSchema()

        new_obj = schema.dump(tac)

        assert isinstance(new_obj, dict)

        deserialized_tac = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_tac,
                          Tac)

        assert deserialized_tac.code == \
            tac.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the TacManager class.

        This test case creates 5 tac
        objects using the
        TacFactory and checks if the count method
        returns the correct count of
        tacs.

        Steps:
        1. Create 5 tac objects using
            the TacFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        tacs_data = (
            [await TacFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(tacs_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: TacManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        TacManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (TacManager): An
                instance of the
                TacManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a tac instance.

        This test performs the following steps:
        1. Creates a tac instance using
            the TacFactory.
        2. Retrieves the tac from th
            database to ensure
            it was added correctly.
        3. Updates the tac's code and verifies the update.
        4. Refreshes the original tac instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (TacManager): The
                manager responsible
                for tac operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a tac
        obj_1 = await TacFactory.create_async(
            session=session)

        # Retrieve the tac from the database
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == (
                    obj_1.tac_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved tac
        # matches the added tac
        assert obj_1.code == \
            obj_2.code

        # Update the tac's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated tac
        # is of type Tac
        # and has the updated code
        assert isinstance(updated_obj_1,
                          Tac)

        assert updated_obj_1.code == updated_code1

        # Refresh the original tac instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed tac
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tac(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent tac.

        Args:
            obj_manager
            (TacManager): The
                instance of the
                TacManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the tac
            refresh operation raises an exception.

        Returns:
            None
        """
        tac = Tac(
            tac_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                tac)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_tac(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to check if a tac
        exists using the manager function.

        Args:
            obj_manager
            (TacManager): The
                tac manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a tac
        obj_1 = await TacFactory.create_async(
            session=session)

        # Check if the tac exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.tac_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_tac(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        TacManager
        class correctly compares two
        tacs.

        Args:
            obj_manager
            (TacManager): An
                instance of the
                TacManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a tac
        obj_1 = await \
            TacFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                tac_id=obj_1.tac_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        tac3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, tac3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tac(
        self,
        obj_manager: TacManager
    ):
        """
        Test case to check if a tac with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (TacManager): The
                instance of the TacManager class.

        Returns:
            bool: True if the tac exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (TacManager): The instance
                of the TacManager class.
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
