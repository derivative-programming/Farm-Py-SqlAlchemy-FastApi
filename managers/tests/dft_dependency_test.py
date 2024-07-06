# managers/tests/dft_dependency_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DFTDependencyManager` class.
"""

import uuid  # noqa: F401
from typing import List

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.dft_dependency import DFTDependencyManager
from models import DFTDependency
from models.factory import DFTDependencyFactory
from models.serialization_schema.dft_dependency import DFTDependencySchema


class TestDFTDependencyManager:
    """
    This class contains unit tests for the
    `DFTDependencyManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DFTDependencyManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DFTDependencyManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test case for the `build` method of
        `DFTDependencyManager`.
        """
        # Define mock data for our dft_dependency
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        dft_dependency = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of DFTDependency
        assert isinstance(
            dft_dependency,
            DFTDependency)

        # Assert that the attributes of the
        # dft_dependency match our mock data
        assert dft_dependency.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `DFTDependencyManager` with missing data.
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
    async def test_add_correctly_adds_dft_dependency_to_database(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DFTDependencyManager` that checks if a
        dft_dependency is correctly added to the database.
        """
        new_obj = await \
            DFTDependencyFactory.build_async(
                session)

        assert new_obj.dft_dependency_id == 0

        # Add the dft_dependency using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                dft_dependency=new_obj)

        assert isinstance(added_obj,
                          DFTDependency)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.dft_dependency_id > 0

        # Fetch the dft_dependency from
        # the database directly
        result = await session.execute(
            select(DFTDependency).filter(
                DFTDependency._dft_dependency_id == (
                    added_obj.dft_dependency_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched dft_dependency
        # is not None and matches the
        # added dft_dependency
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          DFTDependency)
        assert fetched_obj.dft_dependency_id == \
            added_obj.dft_dependency_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_dft_dependency_object(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DFTDependencyManager` that checks if the
        correct dft_dependency object is returned.
        """
        # Create a test dft_dependency
        # using the DFTDependencyFactory
        # without persisting it to the database
        new_obj = await \
            DFTDependencyFactory.build_async(
                session)

        assert new_obj.dft_dependency_id == 0

        new_obj.code = uuid.uuid4()

        # Add the dft_dependency using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                dft_dependency=new_obj)

        assert isinstance(added_obj,
                          DFTDependency)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.dft_dependency_id > 0

        # Assert that the returned
        # dft_dependency matches the
        # test dft_dependency
        assert added_obj.dft_dependency_id == \
            new_obj.dft_dependency_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DFTDependencyManager`
        that checks if a dft_dependency
        is correctly updated.
        """
        new_obj = await \
            DFTDependencyFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                dft_dependency=new_obj)

        assert isinstance(updated_obj,
                          DFTDependency)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.dft_dependency_id == \
            new_obj.dft_dependency_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(DFTDependency).filter(
                DFTDependency._dft_dependency_id == (
                    new_obj.dft_dependency_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.dft_dependency_id == \
            fetched_obj.dft_dependency_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.dft_dependency_id == \
            fetched_obj.dft_dependency_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DFTDependencyManager`
        that checks if a dft_dependency is
        correctly updated using a dictionary.
        """
        new_obj = await \
            DFTDependencyFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                dft_dependency=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          DFTDependency)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.dft_dependency_id == \
            new_obj.dft_dependency_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(DFTDependency).filter(
                DFTDependency._dft_dependency_id == (
                    new_obj.dft_dependency_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.dft_dependency_id == \
            fetched_obj.dft_dependency_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.dft_dependency_id == \
            fetched_obj.dft_dependency_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_dft_dependency(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test case for the `update` method of
        `DFTDependencyManager`
        with an invalid dft_dependency.
        """

        # None dft_dependency
        dft_dependency = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                dft_dependency, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `DFTDependencyManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            DFTDependencyFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                dft_dependency=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `DFTDependencyManager`.
        """
        new_obj = await DFTDependencyFactory.create_async(
            session)

        result = await session.execute(
            select(DFTDependency).filter(
                DFTDependency._dft_dependency_id == (
                    new_obj.dft_dependency_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DFTDependency)

        assert fetched_obj.dft_dependency_id == \
            new_obj.dft_dependency_id

        await obj_manager.delete(
            dft_dependency_id=new_obj.dft_dependency_id)

        result = await session.execute(
            select(DFTDependency).filter(
                DFTDependency._dft_dependency_id == (
                    new_obj.dft_dependency_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        dft_dependency.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        dft_dependency,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            DFTDependencyManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a dft_dependency
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (DFTDependencyManager): An
                instance of the
                `DFTDependencyManager` class.
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
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `DFTDependencyManager` class.

        This test verifies that the `get_list`
        method returns the correct list of dft_dependencys.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 dft_dependency objects using the
            `DFTDependencyFactory.create_async` method.
        4. Assert that the
            `dft_dependencys_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 dft_dependencys.
        7. Assert that all elements in the returned list are
            instances of the
            `DFTDependency` class.
        """

        dft_dependencys = await obj_manager.get_list()

        assert len(dft_dependencys) == 0

        dft_dependencys_data = (
            [await DFTDependencyFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(dft_dependencys_data, List)

        dft_dependencys = await obj_manager.get_list()

        assert len(dft_dependencys) == 5
        assert all(isinstance(
            dft_dependency,
            DFTDependency
        ) for dft_dependency in dft_dependencys)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the DFTDependencyManager class.

        Args:
            obj_manager
            (DFTDependencyManager): An
                instance of the
                DFTDependencyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        dft_dependency = await \
            DFTDependencyFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            dft_dependency)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the DFTDependencyManager class.

        Args:
            obj_manager
            (DFTDependencyManager): An
                instance of the
                DFTDependencyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        dft_dependency = await \
            DFTDependencyFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                dft_dependency)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `DFTDependencyManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `DFTDependencyManager` class.
        It creates a dft_dependency using
        the `DFTDependencyFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        dft_dependency is an instance of the
        `DFTDependency` class and has
        the same code as the original dft_dependency.

        Args:
            obj_manager
            (DFTDependencyManager): An
                instance of the
                `DFTDependencyManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            dft_dependency)

        deserialized_dft_dependency = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_dft_dependency,
                          DFTDependency)
        assert deserialized_dft_dependency.code == \
            dft_dependency.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `DFTDependencyManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        dft_dependency object.

        Args:
            obj_manager
            (DFTDependencyManager): An instance
                of the `DFTDependencyManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        dft_dependency = await \
            DFTDependencyFactory.create_async(
                session)

        schema = DFTDependencySchema()

        new_obj = schema.dump(dft_dependency)

        assert isinstance(new_obj, dict)

        deserialized_dft_dependency = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_dft_dependency,
                          DFTDependency)

        assert deserialized_dft_dependency.code == \
            dft_dependency.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the DFTDependencyManager class.

        This test case creates 5 dft_dependency
        objects using the
        DFTDependencyFactory and checks if the count method
        returns the correct count of
        dft_dependencys.

        Steps:
        1. Create 5 dft_dependency objects using
            the DFTDependencyFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        dft_dependencys_data = (
            [await DFTDependencyFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(dft_dependencys_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        DFTDependencyManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (DFTDependencyManager): An
                instance of the
                DFTDependencyManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a dft_dependency instance.

        This test performs the following steps:
        1. Creates a dft_dependency instance using
            the DFTDependencyFactory.
        2. Retrieves the dft_dependency from th
            database to ensure
            it was added correctly.
        3. Updates the dft_dependency's code and verifies the update.
        4. Refreshes the original dft_dependency instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (DFTDependencyManager): The
                manager responsible
                for dft_dependency operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a dft_dependency
        obj_1 = await DFTDependencyFactory.create_async(
            session=session)

        # Retrieve the dft_dependency from the database
        result = await session.execute(
            select(DFTDependency).filter(
                DFTDependency._dft_dependency_id == (
                    obj_1.dft_dependency_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved dft_dependency
        # matches the added dft_dependency
        assert obj_1.code == \
            obj_2.code

        # Update the dft_dependency's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated dft_dependency
        # is of type DFTDependency
        # and has the updated code
        assert isinstance(updated_obj_1,
                          DFTDependency)

        assert updated_obj_1.code == updated_code1

        # Refresh the original dft_dependency instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed dft_dependency
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_dft_dependency(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent dft_dependency.

        Args:
            obj_manager
            (DFTDependencyManager): The
                instance of the
                DFTDependencyManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the dft_dependency
            refresh operation raises an exception.

        Returns:
            None
        """
        dft_dependency = DFTDependency(
            dft_dependency_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                dft_dependency)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_dft_dependency(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to check if a dft_dependency
        exists using the manager function.

        Args:
            obj_manager
            (DFTDependencyManager): The
                dft_dependency manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a dft_dependency
        obj_1 = await DFTDependencyFactory.create_async(
            session=session)

        # Check if the dft_dependency exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.dft_dependency_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_dft_dependency(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        DFTDependencyManager
        class correctly compares two
        dft_dependencys.

        Args:
            obj_manager
            (DFTDependencyManager): An
                instance of the
                DFTDependencyManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a dft_dependency
        obj_1 = await \
            DFTDependencyFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                dft_dependency_id=obj_1.dft_dependency_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        dft_dependency3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, dft_dependency3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_dft_dependency(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test case to check if a dft_dependency with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (DFTDependencyManager): The
                instance of the DFTDependencyManager class.

        Returns:
            bool: True if the dft_dependency exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (DFTDependencyManager): The instance
                of the DFTDependencyManager class.
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
