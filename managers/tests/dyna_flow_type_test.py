# managers/tests/dyna_flow_type_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowTypeManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.dyna_flow_type import (
    DynaFlowTypeManager)
from models import DynaFlowType
from models.factory import (
    DynaFlowTypeFactory)
from models.serialization_schema.dyna_flow_type import (
    DynaFlowTypeSchema)


class TestDynaFlowTypeManager:
    """
    This class contains unit tests for the
    `DynaFlowTypeManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DynaFlowTypeManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return DynaFlowTypeManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DynaFlowTypeManager
    ):
        """
        Test case for the `build` method of
        `DynaFlowTypeManager`.
        """
        # Define mock data for our dyna_flow_type
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        dyna_flow_type = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of DynaFlowType
        assert isinstance(
            dyna_flow_type,
            DynaFlowType)

        # Assert that the attributes of the
        # dyna_flow_type match our mock data
        assert dyna_flow_type.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `DynaFlowTypeManager` with missing data.
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
    async def test_add_correctly_adds_dyna_flow_type_to_database(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DynaFlowTypeManager` that checks if a
        dyna_flow_type is correctly added to the database.
        """
        new_obj = await \
            DynaFlowTypeFactory.build_async(
                session)

        assert new_obj.dyna_flow_type_id == 0

        # Add the dyna_flow_type using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                dyna_flow_type=new_obj)

        assert isinstance(added_obj,
                          DynaFlowType)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.dyna_flow_type_id > 0

        # Fetch the dyna_flow_type from
        # the database directly
        result = await session.execute(
            select(DynaFlowType).filter(
                DynaFlowType._dyna_flow_type_id == (
                    added_obj.dyna_flow_type_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched dyna_flow_type
        # is not None and matches the
        # added dyna_flow_type
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          DynaFlowType)
        assert fetched_obj.dyna_flow_type_id == \
            added_obj.dyna_flow_type_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_dyna_flow_type_object(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DynaFlowTypeManager` that checks if the
        correct dyna_flow_type object is returned.
        """
        # Create a test dyna_flow_type
        # using the DynaFlowTypeFactory
        # without persisting it to the database
        new_obj = await \
            DynaFlowTypeFactory.build_async(
                session)

        assert new_obj.dyna_flow_type_id == 0

        new_obj.code = uuid.uuid4()

        # Add the dyna_flow_type using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                dyna_flow_type=new_obj)

        assert isinstance(added_obj,
                          DynaFlowType)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.dyna_flow_type_id > 0

        # Assert that the returned
        # dyna_flow_type matches the
        # test dyna_flow_type
        assert added_obj.dyna_flow_type_id == \
            new_obj.dyna_flow_type_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DynaFlowTypeManager`
        that checks if a dyna_flow_type
        is correctly updated.
        """
        new_obj = await \
            DynaFlowTypeFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                dyna_flow_type=new_obj)

        assert isinstance(updated_obj,
                          DynaFlowType)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.dyna_flow_type_id == \
            new_obj.dyna_flow_type_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(DynaFlowType).filter(
                DynaFlowType._dyna_flow_type_id == (
                    new_obj.dyna_flow_type_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.dyna_flow_type_id == \
            fetched_obj.dyna_flow_type_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.dyna_flow_type_id == \
            fetched_obj.dyna_flow_type_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DynaFlowTypeManager`
        that checks if a dyna_flow_type is
        correctly updated using a dictionary.
        """
        new_obj = await \
            DynaFlowTypeFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                dyna_flow_type=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          DynaFlowType)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.dyna_flow_type_id == \
            new_obj.dyna_flow_type_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(DynaFlowType).filter(
                DynaFlowType._dyna_flow_type_id == (
                    new_obj.dyna_flow_type_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.dyna_flow_type_id == \
            fetched_obj.dyna_flow_type_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.dyna_flow_type_id == \
            fetched_obj.dyna_flow_type_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_dyna_flow_type(
        self,
        obj_manager: DynaFlowTypeManager
    ):
        """
        Test case for the `update` method of
        `DynaFlowTypeManager`
        with an invalid dyna_flow_type.
        """

        # None dyna_flow_type
        dyna_flow_type = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                dyna_flow_type, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `DynaFlowTypeManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            DynaFlowTypeFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                dyna_flow_type=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `DynaFlowTypeManager`.
        """
        new_obj = await DynaFlowTypeFactory.create_async(
            session)

        result = await session.execute(
            select(DynaFlowType).filter(
                DynaFlowType._dyna_flow_type_id == (
                    new_obj.dyna_flow_type_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlowType)

        assert fetched_obj.dyna_flow_type_id == \
            new_obj.dyna_flow_type_id

        await obj_manager.delete(
            dyna_flow_type_id=new_obj.dyna_flow_type_id)

        result = await session.execute(
            select(DynaFlowType).filter(
                DynaFlowType._dyna_flow_type_id == (
                    new_obj.dyna_flow_type_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        dyna_flow_type.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        dyna_flow_type,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            DynaFlowTypeManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a dyna_flow_type
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (DynaFlowTypeManager): An
                instance of the
                `DynaFlowTypeManager` class.
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
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `DynaFlowTypeManager` class.

        This test verifies that the `get_list`
        method returns the correct list of dyna_flow_types.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 dyna_flow_type objects using the
            `DynaFlowTypeFactory.create_async` method.
        4. Assert that the
            `dyna_flow_types_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 dyna_flow_types.
        7. Assert that all elements in the returned list are
            instances of the
            `DynaFlowType` class.
        """

        dyna_flow_types = await obj_manager.get_list()

        assert len(dyna_flow_types) == 0

        dyna_flow_types_data = (
            [await DynaFlowTypeFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(dyna_flow_types_data, List)

        dyna_flow_types = await obj_manager.get_list()

        assert len(dyna_flow_types) == 5
        assert all(isinstance(
            dyna_flow_type,
            DynaFlowType
        ) for dyna_flow_type in dyna_flow_types)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the DynaFlowTypeManager class.

        Args:
            obj_manager
            (DynaFlowTypeManager): An
                instance of the
                DynaFlowTypeManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        dyna_flow_type = await \
            DynaFlowTypeFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            dyna_flow_type)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the DynaFlowTypeManager class.

        Args:
            obj_manager
            (DynaFlowTypeManager): An
                instance of the
                DynaFlowTypeManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        dyna_flow_type = await \
            DynaFlowTypeFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                dyna_flow_type)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `DynaFlowTypeManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `DynaFlowTypeManager` class.
        It creates a dyna_flow_type using
        the `DynaFlowTypeFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        dyna_flow_type is an instance of the
        `DynaFlowType` class and has
        the same code as the original dyna_flow_type.

        Args:
            obj_manager
            (DynaFlowTypeManager): An
                instance of the
                `DynaFlowTypeManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        dyna_flow_type = await \
            DynaFlowTypeFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            dyna_flow_type)

        deserialized_dyna_flow_type = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_dyna_flow_type,
                          DynaFlowType)
        assert deserialized_dyna_flow_type.code == \
            dyna_flow_type.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `DynaFlowTypeManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        dyna_flow_type object.

        Args:
            obj_manager
            (DynaFlowTypeManager): An instance
                of the `DynaFlowTypeManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        dyna_flow_type = await \
            DynaFlowTypeFactory.create_async(
                session)

        schema = DynaFlowTypeSchema()

        new_obj = schema.dump(dyna_flow_type)

        assert isinstance(new_obj, dict)

        deserialized_dyna_flow_type = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_dyna_flow_type,
                          DynaFlowType)

        assert deserialized_dyna_flow_type.code == \
            dyna_flow_type.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the DynaFlowTypeManager class.

        This test case creates 5 dyna_flow_type
        objects using the
        DynaFlowTypeFactory and checks if the count method
        returns the correct count of
        dyna_flow_types.

        Steps:
        1. Create 5 dyna_flow_type objects using
            the DynaFlowTypeFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        dyna_flow_types_data = (
            [await DynaFlowTypeFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(dyna_flow_types_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: DynaFlowTypeManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        DynaFlowTypeManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (DynaFlowTypeManager): An
                instance of the
                DynaFlowTypeManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a dyna_flow_type instance.

        This test performs the following steps:
        1. Creates a dyna_flow_type instance using
            the DynaFlowTypeFactory.
        2. Retrieves the dyna_flow_type from th
            database to ensure
            it was added correctly.
        3. Updates the dyna_flow_type's code and verifies the update.
        4. Refreshes the original dyna_flow_type instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (DynaFlowTypeManager): The
                manager responsible
                for dyna_flow_type operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a dyna_flow_type
        obj_1 = await DynaFlowTypeFactory.create_async(
            session=session)

        # Retrieve the dyna_flow_type from the database
        result = await session.execute(
            select(DynaFlowType).filter(
                DynaFlowType._dyna_flow_type_id == (
                    obj_1.dyna_flow_type_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved dyna_flow_type
        # matches the added dyna_flow_type
        assert obj_1.code == \
            obj_2.code

        # Update the dyna_flow_type's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated dyna_flow_type
        # is of type DynaFlowType
        # and has the updated code
        assert isinstance(updated_obj_1,
                          DynaFlowType)

        assert updated_obj_1.code == updated_code1

        # Refresh the original dyna_flow_type instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed dyna_flow_type
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_dyna_flow_type(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent dyna_flow_type.

        Args:
            obj_manager
            (DynaFlowTypeManager): The
                instance of the
                DynaFlowTypeManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the dyna_flow_type
            refresh operation raises an exception.

        Returns:
            None
        """
        dyna_flow_type = DynaFlowType(
            dyna_flow_type_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                dyna_flow_type)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_dyna_flow_type(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case to check if a dyna_flow_type
        exists using the manager function.

        Args:
            obj_manager
            (DynaFlowTypeManager): The
                dyna_flow_type manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a dyna_flow_type
        obj_1 = await DynaFlowTypeFactory.create_async(
            session=session)

        # Check if the dyna_flow_type exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.dyna_flow_type_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_dyna_flow_type(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        DynaFlowTypeManager
        class correctly compares two
        dyna_flow_types.

        Args:
            obj_manager
            (DynaFlowTypeManager): An
                instance of the
                DynaFlowTypeManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a dyna_flow_type
        obj_1 = await \
            DynaFlowTypeFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                dyna_flow_type_id=obj_1.dyna_flow_type_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        dyna_flow_type3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, dyna_flow_type3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_dyna_flow_type(
        self,
        obj_manager: DynaFlowTypeManager
    ):
        """
        Test case to check if a dyna_flow_type with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (DynaFlowTypeManager): The
                instance of the DynaFlowTypeManager class.

        Returns:
            bool: True if the dyna_flow_type exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: DynaFlowTypeManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (DynaFlowTypeManager): The instance
                of the DynaFlowTypeManager class.
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
