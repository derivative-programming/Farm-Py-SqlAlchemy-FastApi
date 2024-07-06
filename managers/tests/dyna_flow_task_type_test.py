# managers/tests/dyna_flow_task_type_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowTaskTypeManager` class.
"""

import uuid  # noqa: F401
from typing import List

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.dyna_flow_task_type import DynaFlowTaskTypeManager
from models import DynaFlowTaskType
from models.factory import DynaFlowTaskTypeFactory
from models.serialization_schema.dyna_flow_task_type import DynaFlowTaskTypeSchema


class TestDynaFlowTaskTypeManager:
    """
    This class contains unit tests for the
    `DynaFlowTaskTypeManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DynaFlowTaskTypeManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DynaFlowTaskTypeManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DynaFlowTaskTypeManager
    ):
        """
        Test case for the `build` method of
        `DynaFlowTaskTypeManager`.
        """
        # Define mock data for our dyna_flow_task_type
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        dyna_flow_task_type = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of DynaFlowTaskType
        assert isinstance(
            dyna_flow_task_type,
            DynaFlowTaskType)

        # Assert that the attributes of the
        # dyna_flow_task_type match our mock data
        assert dyna_flow_task_type.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `DynaFlowTaskTypeManager` with missing data.
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
    async def test_add_correctly_adds_dyna_flow_task_type_to_database(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DynaFlowTaskTypeManager` that checks if a
        dyna_flow_task_type is correctly added to the database.
        """
        new_obj = await \
            DynaFlowTaskTypeFactory.build_async(
                session)

        assert new_obj.dyna_flow_task_type_id == 0

        # Add the dyna_flow_task_type using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                dyna_flow_task_type=new_obj)

        assert isinstance(added_obj,
                          DynaFlowTaskType)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.dyna_flow_task_type_id > 0

        # Fetch the dyna_flow_task_type from
        # the database directly
        result = await session.execute(
            select(DynaFlowTaskType).filter(
                DynaFlowTaskType._dyna_flow_task_type_id == (
                    added_obj.dyna_flow_task_type_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched dyna_flow_task_type
        # is not None and matches the
        # added dyna_flow_task_type
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          DynaFlowTaskType)
        assert fetched_obj.dyna_flow_task_type_id == \
            added_obj.dyna_flow_task_type_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_dyna_flow_task_type_object(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DynaFlowTaskTypeManager` that checks if the
        correct dyna_flow_task_type object is returned.
        """
        # Create a test dyna_flow_task_type
        # using the DynaFlowTaskTypeFactory
        # without persisting it to the database
        new_obj = await \
            DynaFlowTaskTypeFactory.build_async(
                session)

        assert new_obj.dyna_flow_task_type_id == 0

        new_obj.code = uuid.uuid4()

        # Add the dyna_flow_task_type using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                dyna_flow_task_type=new_obj)

        assert isinstance(added_obj,
                          DynaFlowTaskType)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.dyna_flow_task_type_id > 0

        # Assert that the returned
        # dyna_flow_task_type matches the
        # test dyna_flow_task_type
        assert added_obj.dyna_flow_task_type_id == \
            new_obj.dyna_flow_task_type_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DynaFlowTaskTypeManager`
        that checks if a dyna_flow_task_type
        is correctly updated.
        """
        new_obj = await \
            DynaFlowTaskTypeFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                dyna_flow_task_type=new_obj)

        assert isinstance(updated_obj,
                          DynaFlowTaskType)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.dyna_flow_task_type_id == \
            new_obj.dyna_flow_task_type_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(DynaFlowTaskType).filter(
                DynaFlowTaskType._dyna_flow_task_type_id == (
                    new_obj.dyna_flow_task_type_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.dyna_flow_task_type_id == \
            fetched_obj.dyna_flow_task_type_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.dyna_flow_task_type_id == \
            fetched_obj.dyna_flow_task_type_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DynaFlowTaskTypeManager`
        that checks if a dyna_flow_task_type is
        correctly updated using a dictionary.
        """
        new_obj = await \
            DynaFlowTaskTypeFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                dyna_flow_task_type=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          DynaFlowTaskType)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.dyna_flow_task_type_id == \
            new_obj.dyna_flow_task_type_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(DynaFlowTaskType).filter(
                DynaFlowTaskType._dyna_flow_task_type_id == (
                    new_obj.dyna_flow_task_type_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.dyna_flow_task_type_id == \
            fetched_obj.dyna_flow_task_type_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.dyna_flow_task_type_id == \
            fetched_obj.dyna_flow_task_type_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_dyna_flow_task_type(
        self,
        obj_manager: DynaFlowTaskTypeManager
    ):
        """
        Test case for the `update` method of
        `DynaFlowTaskTypeManager`
        with an invalid dyna_flow_task_type.
        """

        # None dyna_flow_task_type
        dyna_flow_task_type = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                dyna_flow_task_type, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `DynaFlowTaskTypeManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            DynaFlowTaskTypeFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                dyna_flow_task_type=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `DynaFlowTaskTypeManager`.
        """
        new_obj = await DynaFlowTaskTypeFactory.create_async(
            session)

        result = await session.execute(
            select(DynaFlowTaskType).filter(
                DynaFlowTaskType._dyna_flow_task_type_id == (
                    new_obj.dyna_flow_task_type_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlowTaskType)

        assert fetched_obj.dyna_flow_task_type_id == \
            new_obj.dyna_flow_task_type_id

        await obj_manager.delete(
            dyna_flow_task_type_id=new_obj.dyna_flow_task_type_id)

        result = await session.execute(
            select(DynaFlowTaskType).filter(
                DynaFlowTaskType._dyna_flow_task_type_id == (
                    new_obj.dyna_flow_task_type_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        dyna_flow_task_type.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        dyna_flow_task_type,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            DynaFlowTaskTypeManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a dyna_flow_task_type
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): An
                instance of the
                `DynaFlowTaskTypeManager` class.
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
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `DynaFlowTaskTypeManager` class.

        This test verifies that the `get_list`
        method returns the correct list of dyna_flow_task_types.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 dyna_flow_task_type objects using the
            `DynaFlowTaskTypeFactory.create_async` method.
        4. Assert that the
            `dyna_flow_task_types_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 dyna_flow_task_types.
        7. Assert that all elements in the returned list are
            instances of the
            `DynaFlowTaskType` class.
        """

        dyna_flow_task_types = await obj_manager.get_list()

        assert len(dyna_flow_task_types) == 0

        dyna_flow_task_types_data = (
            [await DynaFlowTaskTypeFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(dyna_flow_task_types_data, List)

        dyna_flow_task_types = await obj_manager.get_list()

        assert len(dyna_flow_task_types) == 5
        assert all(isinstance(
            dyna_flow_task_type,
            DynaFlowTaskType
        ) for dyna_flow_task_type in dyna_flow_task_types)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the DynaFlowTaskTypeManager class.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): An
                instance of the
                DynaFlowTaskTypeManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        dyna_flow_task_type = await \
            DynaFlowTaskTypeFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            dyna_flow_task_type)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the DynaFlowTaskTypeManager class.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): An
                instance of the
                DynaFlowTaskTypeManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        dyna_flow_task_type = await \
            DynaFlowTaskTypeFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                dyna_flow_task_type)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `DynaFlowTaskTypeManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `DynaFlowTaskTypeManager` class.
        It creates a dyna_flow_task_type using
        the `DynaFlowTaskTypeFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        dyna_flow_task_type is an instance of the
        `DynaFlowTaskType` class and has
        the same code as the original dyna_flow_task_type.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): An
                instance of the
                `DynaFlowTaskTypeManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        dyna_flow_task_type = await \
            DynaFlowTaskTypeFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            dyna_flow_task_type)

        deserialized_dyna_flow_task_type = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_dyna_flow_task_type,
                          DynaFlowTaskType)
        assert deserialized_dyna_flow_task_type.code == \
            dyna_flow_task_type.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `DynaFlowTaskTypeManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        dyna_flow_task_type object.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): An instance
                of the `DynaFlowTaskTypeManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        dyna_flow_task_type = await \
            DynaFlowTaskTypeFactory.create_async(
                session)

        schema = DynaFlowTaskTypeSchema()

        new_obj = schema.dump(dyna_flow_task_type)

        assert isinstance(new_obj, dict)

        deserialized_dyna_flow_task_type = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_dyna_flow_task_type,
                          DynaFlowTaskType)

        assert deserialized_dyna_flow_task_type.code == \
            dyna_flow_task_type.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the DynaFlowTaskTypeManager class.

        This test case creates 5 dyna_flow_task_type
        objects using the
        DynaFlowTaskTypeFactory and checks if the count method
        returns the correct count of
        dyna_flow_task_types.

        Steps:
        1. Create 5 dyna_flow_task_type objects using
            the DynaFlowTaskTypeFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        dyna_flow_task_types_data = (
            [await DynaFlowTaskTypeFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(dyna_flow_task_types_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: DynaFlowTaskTypeManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        DynaFlowTaskTypeManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): An
                instance of the
                DynaFlowTaskTypeManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a dyna_flow_task_type instance.

        This test performs the following steps:
        1. Creates a dyna_flow_task_type instance using
            the DynaFlowTaskTypeFactory.
        2. Retrieves the dyna_flow_task_type from th
            database to ensure
            it was added correctly.
        3. Updates the dyna_flow_task_type's code and verifies the update.
        4. Refreshes the original dyna_flow_task_type instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): The
                manager responsible
                for dyna_flow_task_type operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a dyna_flow_task_type
        obj_1 = await DynaFlowTaskTypeFactory.create_async(
            session=session)

        # Retrieve the dyna_flow_task_type from the database
        result = await session.execute(
            select(DynaFlowTaskType).filter(
                DynaFlowTaskType._dyna_flow_task_type_id == (
                    obj_1.dyna_flow_task_type_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved dyna_flow_task_type
        # matches the added dyna_flow_task_type
        assert obj_1.code == \
            obj_2.code

        # Update the dyna_flow_task_type's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated dyna_flow_task_type
        # is of type DynaFlowTaskType
        # and has the updated code
        assert isinstance(updated_obj_1,
                          DynaFlowTaskType)

        assert updated_obj_1.code == updated_code1

        # Refresh the original dyna_flow_task_type instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed dyna_flow_task_type
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_dyna_flow_task_type(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent dyna_flow_task_type.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): The
                instance of the
                DynaFlowTaskTypeManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the dyna_flow_task_type
            refresh operation raises an exception.

        Returns:
            None
        """
        dyna_flow_task_type = DynaFlowTaskType(
            dyna_flow_task_type_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                dyna_flow_task_type)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_dyna_flow_task_type(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case to check if a dyna_flow_task_type
        exists using the manager function.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): The
                dyna_flow_task_type manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a dyna_flow_task_type
        obj_1 = await DynaFlowTaskTypeFactory.create_async(
            session=session)

        # Check if the dyna_flow_task_type exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.dyna_flow_task_type_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_dyna_flow_task_type(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        DynaFlowTaskTypeManager
        class correctly compares two
        dyna_flow_task_types.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): An
                instance of the
                DynaFlowTaskTypeManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a dyna_flow_task_type
        obj_1 = await \
            DynaFlowTaskTypeFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                dyna_flow_task_type_id=obj_1.dyna_flow_task_type_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        dyna_flow_task_type3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, dyna_flow_task_type3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_dyna_flow_task_type(
        self,
        obj_manager: DynaFlowTaskTypeManager
    ):
        """
        Test case to check if a dyna_flow_task_type with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): The
                instance of the DynaFlowTaskTypeManager class.

        Returns:
            bool: True if the dyna_flow_task_type exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: DynaFlowTaskTypeManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (DynaFlowTaskTypeManager): The instance
                of the DynaFlowTaskTypeManager class.
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
