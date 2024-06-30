# managers/tests/df_maintenance_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DFMaintenanceManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.df_maintenance import (
    DFMaintenanceManager)
from models import DFMaintenance
from models.factory import (
    DFMaintenanceFactory)
from models.serialization_schema.df_maintenance import (
    DFMaintenanceSchema)


class TestDFMaintenanceManager:
    """
    This class contains unit tests for the
    `DFMaintenanceManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DFMaintenanceManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return DFMaintenanceManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DFMaintenanceManager
    ):
        """
        Test case for the `build` method of
        `DFMaintenanceManager`.
        """
        # Define mock data for our df_maintenance
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        df_maintenance = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of DFMaintenance
        assert isinstance(
            df_maintenance,
            DFMaintenance)

        # Assert that the attributes of the
        # df_maintenance match our mock data
        assert df_maintenance.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `DFMaintenanceManager` with missing data.
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
    async def test_add_correctly_adds_df_maintenance_to_database(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DFMaintenanceManager` that checks if a
        df_maintenance is correctly added to the database.
        """
        new_obj = await \
            DFMaintenanceFactory.build_async(
                session)

        assert new_obj.df_maintenance_id == 0

        # Add the df_maintenance using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                df_maintenance=new_obj)

        assert isinstance(added_obj,
                          DFMaintenance)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.df_maintenance_id > 0

        # Fetch the df_maintenance from
        # the database directly
        result = await session.execute(
            select(DFMaintenance).filter(
                DFMaintenance._df_maintenance_id == (
                    added_obj.df_maintenance_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched df_maintenance
        # is not None and matches the
        # added df_maintenance
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          DFMaintenance)
        assert fetched_obj.df_maintenance_id == \
            added_obj.df_maintenance_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_df_maintenance_object(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DFMaintenanceManager` that checks if the
        correct df_maintenance object is returned.
        """
        # Create a test df_maintenance
        # using the DFMaintenanceFactory
        # without persisting it to the database
        new_obj = await \
            DFMaintenanceFactory.build_async(
                session)

        assert new_obj.df_maintenance_id == 0

        new_obj.code = uuid.uuid4()

        # Add the df_maintenance using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                df_maintenance=new_obj)

        assert isinstance(added_obj,
                          DFMaintenance)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.df_maintenance_id > 0

        # Assert that the returned
        # df_maintenance matches the
        # test df_maintenance
        assert added_obj.df_maintenance_id == \
            new_obj.df_maintenance_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DFMaintenanceManager`
        that checks if a df_maintenance
        is correctly updated.
        """
        new_obj = await \
            DFMaintenanceFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                df_maintenance=new_obj)

        assert isinstance(updated_obj,
                          DFMaintenance)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.df_maintenance_id == \
            new_obj.df_maintenance_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(DFMaintenance).filter(
                DFMaintenance._df_maintenance_id == (
                    new_obj.df_maintenance_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.df_maintenance_id == \
            fetched_obj.df_maintenance_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.df_maintenance_id == \
            fetched_obj.df_maintenance_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DFMaintenanceManager`
        that checks if a df_maintenance is
        correctly updated using a dictionary.
        """
        new_obj = await \
            DFMaintenanceFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                df_maintenance=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          DFMaintenance)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.df_maintenance_id == \
            new_obj.df_maintenance_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(DFMaintenance).filter(
                DFMaintenance._df_maintenance_id == (
                    new_obj.df_maintenance_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.df_maintenance_id == \
            fetched_obj.df_maintenance_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.df_maintenance_id == \
            fetched_obj.df_maintenance_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_df_maintenance(
        self,
        obj_manager: DFMaintenanceManager
    ):
        """
        Test case for the `update` method of
        `DFMaintenanceManager`
        with an invalid df_maintenance.
        """

        # None df_maintenance
        df_maintenance = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                df_maintenance, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `DFMaintenanceManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            DFMaintenanceFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                df_maintenance=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `DFMaintenanceManager`.
        """
        new_obj = await DFMaintenanceFactory.create_async(
            session)

        result = await session.execute(
            select(DFMaintenance).filter(
                DFMaintenance._df_maintenance_id == (
                    new_obj.df_maintenance_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DFMaintenance)

        assert fetched_obj.df_maintenance_id == \
            new_obj.df_maintenance_id

        await obj_manager.delete(
            df_maintenance_id=new_obj.df_maintenance_id)

        result = await session.execute(
            select(DFMaintenance).filter(
                DFMaintenance._df_maintenance_id == (
                    new_obj.df_maintenance_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        df_maintenance.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        df_maintenance,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            DFMaintenanceManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a df_maintenance
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (DFMaintenanceManager): An
                instance of the
                `DFMaintenanceManager` class.
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
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `DFMaintenanceManager` class.

        This test verifies that the `get_list`
        method returns the correct list of df_maintenances.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 df_maintenance objects using the
            `DFMaintenanceFactory.create_async` method.
        4. Assert that the
            `df_maintenances_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 df_maintenances.
        7. Assert that all elements in the returned list are
            instances of the
            `DFMaintenance` class.
        """

        df_maintenances = await obj_manager.get_list()

        assert len(df_maintenances) == 0

        df_maintenances_data = (
            [await DFMaintenanceFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(df_maintenances_data, List)

        df_maintenances = await obj_manager.get_list()

        assert len(df_maintenances) == 5
        assert all(isinstance(
            df_maintenance,
            DFMaintenance
        ) for df_maintenance in df_maintenances)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the DFMaintenanceManager class.

        Args:
            obj_manager
            (DFMaintenanceManager): An
                instance of the
                DFMaintenanceManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        df_maintenance = await \
            DFMaintenanceFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            df_maintenance)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the DFMaintenanceManager class.

        Args:
            obj_manager
            (DFMaintenanceManager): An
                instance of the
                DFMaintenanceManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        df_maintenance = await \
            DFMaintenanceFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                df_maintenance)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `DFMaintenanceManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `DFMaintenanceManager` class.
        It creates a df_maintenance using
        the `DFMaintenanceFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        df_maintenance is an instance of the
        `DFMaintenance` class and has
        the same code as the original df_maintenance.

        Args:
            obj_manager
            (DFMaintenanceManager): An
                instance of the
                `DFMaintenanceManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            df_maintenance)

        deserialized_df_maintenance = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_df_maintenance,
                          DFMaintenance)
        assert deserialized_df_maintenance.code == \
            df_maintenance.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `DFMaintenanceManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        df_maintenance object.

        Args:
            obj_manager
            (DFMaintenanceManager): An instance
                of the `DFMaintenanceManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        df_maintenance = await \
            DFMaintenanceFactory.create_async(
                session)

        schema = DFMaintenanceSchema()

        new_obj = schema.dump(df_maintenance)

        assert isinstance(new_obj, dict)

        deserialized_df_maintenance = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_df_maintenance,
                          DFMaintenance)

        assert deserialized_df_maintenance.code == \
            df_maintenance.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the DFMaintenanceManager class.

        This test case creates 5 df_maintenance
        objects using the
        DFMaintenanceFactory and checks if the count method
        returns the correct count of
        df_maintenances.

        Steps:
        1. Create 5 df_maintenance objects using
            the DFMaintenanceFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        df_maintenances_data = (
            [await DFMaintenanceFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(df_maintenances_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: DFMaintenanceManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        DFMaintenanceManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (DFMaintenanceManager): An
                instance of the
                DFMaintenanceManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a df_maintenance instance.

        This test performs the following steps:
        1. Creates a df_maintenance instance using
            the DFMaintenanceFactory.
        2. Retrieves the df_maintenance from th
            database to ensure
            it was added correctly.
        3. Updates the df_maintenance's code and verifies the update.
        4. Refreshes the original df_maintenance instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (DFMaintenanceManager): The
                manager responsible
                for df_maintenance operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a df_maintenance
        obj_1 = await DFMaintenanceFactory.create_async(
            session=session)

        # Retrieve the df_maintenance from the database
        result = await session.execute(
            select(DFMaintenance).filter(
                DFMaintenance._df_maintenance_id == (
                    obj_1.df_maintenance_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved df_maintenance
        # matches the added df_maintenance
        assert obj_1.code == \
            obj_2.code

        # Update the df_maintenance's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated df_maintenance
        # is of type DFMaintenance
        # and has the updated code
        assert isinstance(updated_obj_1,
                          DFMaintenance)

        assert updated_obj_1.code == updated_code1

        # Refresh the original df_maintenance instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed df_maintenance
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_df_maintenance(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent df_maintenance.

        Args:
            obj_manager
            (DFMaintenanceManager): The
                instance of the
                DFMaintenanceManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the df_maintenance
            refresh operation raises an exception.

        Returns:
            None
        """
        df_maintenance = DFMaintenance(
            df_maintenance_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                df_maintenance)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_df_maintenance(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to check if a df_maintenance
        exists using the manager function.

        Args:
            obj_manager
            (DFMaintenanceManager): The
                df_maintenance manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a df_maintenance
        obj_1 = await DFMaintenanceFactory.create_async(
            session=session)

        # Check if the df_maintenance exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.df_maintenance_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_df_maintenance(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        DFMaintenanceManager
        class correctly compares two
        df_maintenances.

        Args:
            obj_manager
            (DFMaintenanceManager): An
                instance of the
                DFMaintenanceManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a df_maintenance
        obj_1 = await \
            DFMaintenanceFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                df_maintenance_id=obj_1.df_maintenance_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        df_maintenance3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, df_maintenance3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_df_maintenance(
        self,
        obj_manager: DFMaintenanceManager
    ):
        """
        Test case to check if a df_maintenance with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (DFMaintenanceManager): The
                instance of the DFMaintenanceManager class.

        Returns:
            bool: True if the df_maintenance exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: DFMaintenanceManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (DFMaintenanceManager): The instance
                of the DFMaintenanceManager class.
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
