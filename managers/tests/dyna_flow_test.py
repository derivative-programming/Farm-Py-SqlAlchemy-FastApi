# managers/tests/dyna_flow_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.dyna_flow import (
    DynaFlowManager)
from models import DynaFlow
from models.factory import (
    DynaFlowFactory)
from models.serialization_schema.dyna_flow import (
    DynaFlowSchema)


class TestDynaFlowManager:
    """
    This class contains unit tests for the
    `DynaFlowManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DynaFlowManager` for testing.
        """
        session_context = SessionContext({}, session)
        session_context.customer_code = uuid.uuid4()
        return DynaFlowManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        obj_manager: DynaFlowManager
    ):
        """
        Test case for the `build` method of
        `DynaFlowManager`.
        """
        # Define mock data for our dyna_flow
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        dyna_flow = await \
            obj_manager.build(
                **mock_data)

        # Assert that the returned object is an
        # instance of DynaFlow
        assert isinstance(
            dyna_flow,
            DynaFlow)

        # Assert that the attributes of the
        # dyna_flow match our mock data
        assert dyna_flow.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `DynaFlowManager` with missing data.
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
    async def test_add_correctly_adds_dyna_flow_to_database(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DynaFlowManager` that checks if a
        dyna_flow is correctly added to the database.
        """
        new_obj = await \
            DynaFlowFactory.build_async(
                session)

        assert new_obj.dyna_flow_id == 0

        # Add the dyna_flow using the
        # manager's add method
        added_obj = await \
            obj_manager.add(
                dyna_flow=new_obj)

        assert isinstance(added_obj,
                          DynaFlow)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.dyna_flow_id > 0

        # Fetch the dyna_flow from
        # the database directly
        result = await session.execute(
            select(DynaFlow).filter(
                DynaFlow._dyna_flow_id == (
                    added_obj.dyna_flow_id)  # type: ignore
            )
        )
        fetched_obj = result.scalars().first()

        # Assert that the fetched dyna_flow
        # is not None and matches the
        # added dyna_flow
        assert fetched_obj is not None
        assert isinstance(fetched_obj,
                          DynaFlow)
        assert fetched_obj.dyna_flow_id == \
            added_obj.dyna_flow_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_dyna_flow_object(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DynaFlowManager` that checks if the
        correct dyna_flow object is returned.
        """
        # Create a test dyna_flow
        # using the DynaFlowFactory
        # without persisting it to the database
        new_obj = await \
            DynaFlowFactory.build_async(
                session)

        assert new_obj.dyna_flow_id == 0

        new_obj.code = uuid.uuid4()

        # Add the dyna_flow using
        # the manager's add method
        added_obj = await \
            obj_manager.add(
                dyna_flow=new_obj)

        assert isinstance(added_obj,
                          DynaFlow)

        assert str(added_obj.insert_user_id) == (
            str(obj_manager._session_context.customer_code))
        assert str(added_obj.last_update_user_id) == (
            str(obj_manager._session_context.customer_code))

        assert added_obj.dyna_flow_id > 0

        # Assert that the returned
        # dyna_flow matches the
        # test dyna_flow
        assert added_obj.dyna_flow_id == \
            new_obj.dyna_flow_id
        assert added_obj.code == \
            new_obj.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DynaFlowManager`
        that checks if a dyna_flow
        is correctly updated.
        """
        new_obj = await \
            DynaFlowFactory.create_async(
                session)

        new_obj.code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                dyna_flow=new_obj)

        assert isinstance(updated_obj,
                          DynaFlow)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code)

        assert updated_obj.dyna_flow_id == \
            new_obj.dyna_flow_id
        assert updated_obj.code == \
            new_obj.code

        result = await session.execute(
            select(DynaFlow).filter(
                DynaFlow._dyna_flow_id == (
                    new_obj.dyna_flow_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.dyna_flow_id == \
            fetched_obj.dyna_flow_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.dyna_flow_id == \
            fetched_obj.dyna_flow_id
        assert new_obj.code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `DynaFlowManager`
        that checks if a dyna_flow is
        correctly updated using a dictionary.
        """
        new_obj = await \
            DynaFlowFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_obj = await \
            obj_manager.update(
                dyna_flow=new_obj,
                code=new_code
            )

        assert isinstance(updated_obj,
                          DynaFlow)

        assert str(updated_obj.last_update_user_id) == str(
            obj_manager._session_context.customer_code
        )

        assert updated_obj.dyna_flow_id == \
            new_obj.dyna_flow_id
        assert updated_obj.code == new_code

        result = await session.execute(
            select(DynaFlow).filter(
                DynaFlow._dyna_flow_id == (
                    new_obj.dyna_flow_id))  # type: ignore
        )

        fetched_obj = result.scalars().first()

        assert updated_obj.dyna_flow_id == \
            fetched_obj.dyna_flow_id
        assert updated_obj.code == \
            fetched_obj.code

        assert new_obj.dyna_flow_id == \
            fetched_obj.dyna_flow_id
        assert new_code == \
            fetched_obj.code

    @pytest.mark.asyncio
    async def test_update_invalid_dyna_flow(
        self,
        obj_manager: DynaFlowManager
    ):
        """
        Test case for the `update` method of
        `DynaFlowManager`
        with an invalid dyna_flow.
        """

        # None dyna_flow
        dyna_flow = None

        new_code = uuid.uuid4()

        updated_obj = await (
            obj_manager.update(
                dyna_flow, code=new_code))  # type: ignore

        # Assertions
        assert updated_obj is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `DynaFlowManager`
        with a nonexistent attribute.
        """
        new_obj = await \
            DynaFlowFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await obj_manager.update(
                dyna_flow=new_obj,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `DynaFlowManager`.
        """
        new_obj = await DynaFlowFactory.create_async(
            session)

        result = await session.execute(
            select(DynaFlow).filter(
                DynaFlow._dyna_flow_id == (
                    new_obj.dyna_flow_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlow)

        assert fetched_obj.dyna_flow_id == \
            new_obj.dyna_flow_id

        await obj_manager.delete(
            dyna_flow_id=new_obj.dyna_flow_id)

        result = await session.execute(
            select(DynaFlow).filter(
                DynaFlow._dyna_flow_id == (
                    new_obj.dyna_flow_id))  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent
        dyna_flow.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent
        dyna_flow,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param obj_manager: The instance of the
            DynaFlowManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await obj_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a dyna_flow
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `obj_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            obj_manager
            (DynaFlowManager): An
                instance of the
                `DynaFlowManager` class.
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
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `DynaFlowManager` class.

        This test verifies that the `get_list`
        method returns the correct list of dyna_flows.

        Steps:
        1. Call the `get_list` method of the
            `obj_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 dyna_flow objects using the
            `DynaFlowFactory.create_async` method.
        4. Assert that the
            `dyna_flows_data` variable
            is of type `List`.
        5. Call the `get_list` method of the
            `obj_manager` instance again.
        6. Assert that the returned list contains 5 dyna_flows.
        7. Assert that all elements in the returned list are
            instances of the
            `DynaFlow` class.
        """

        dyna_flows = await obj_manager.get_list()

        assert len(dyna_flows) == 0

        dyna_flows_data = (
            [await DynaFlowFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(dyna_flows_data, List)

        dyna_flows = await obj_manager.get_list()

        assert len(dyna_flows) == 5
        assert all(isinstance(
            dyna_flow,
            DynaFlow
        ) for dyna_flow in dyna_flows)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the DynaFlowManager class.

        Args:
            obj_manager
            (DynaFlowManager): An
                instance of the
                DynaFlowManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        dyna_flow = await \
            DynaFlowFactory.build_async(
                session)

        json_data = obj_manager.to_json(
            dyna_flow)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the DynaFlowManager class.

        Args:
            obj_manager
            (DynaFlowManager): An
                instance of the
                DynaFlowManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        dyna_flow = await \
            DynaFlowFactory.build_async(
                session)

        dict_data = \
            obj_manager.to_dict(
                dyna_flow)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the
        `DynaFlowManager` class.

        This method tests the functionality of the
        `from_json` method of the
        `DynaFlowManager` class.
        It creates a dyna_flow using
        the `DynaFlowFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        dyna_flow is an instance of the
        `DynaFlow` class and has
        the same code as the original dyna_flow.

        Args:
            obj_manager
            (DynaFlowManager): An
                instance of the
                `DynaFlowManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session)

        json_data = obj_manager.to_json(
            dyna_flow)

        deserialized_dyna_flow = await \
            obj_manager.from_json(json_data)

        assert isinstance(deserialized_dyna_flow,
                          DynaFlow)
        assert deserialized_dyna_flow.code == \
            dyna_flow.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `DynaFlowManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        dyna_flow object.

        Args:
            obj_manager
            (DynaFlowManager): An instance
                of the `DynaFlowManager` class.
            session (AsyncSession): An instance of the
            `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        dyna_flow = await \
            DynaFlowFactory.create_async(
                session)

        schema = DynaFlowSchema()

        new_obj = schema.dump(dyna_flow)

        assert isinstance(new_obj, dict)

        deserialized_dyna_flow = await \
            obj_manager.from_dict(
                new_obj)

        assert isinstance(deserialized_dyna_flow,
                          DynaFlow)

        assert deserialized_dyna_flow.code == \
            dyna_flow.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the DynaFlowManager class.

        This test case creates 5 dyna_flow
        objects using the
        DynaFlowFactory and checks if the count method
        returns the correct count of
        dyna_flows.

        Steps:
        1. Create 5 dyna_flow objects using
            the DynaFlowFactory.
        2. Call the count method of the obj_manager.
        3. Assert that the count is equal to 5.

        """
        dyna_flows_data = (
            [await DynaFlowFactory.create_async(session)
             for _ in range(5)])

        assert isinstance(dyna_flows_data, List)

        count = await obj_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        obj_manager: DynaFlowManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        DynaFlowManager class
        returns 0 when the database is empty.

        Args:
            obj_manager
            (DynaFlowManager): An
                instance of the
                DynaFlowManager class.

        Returns:
            None
        """

        count = await obj_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a dyna_flow instance.

        This test performs the following steps:
        1. Creates a dyna_flow instance using
            the DynaFlowFactory.
        2. Retrieves the dyna_flow from th
            database to ensure
            it was added correctly.
        3. Updates the dyna_flow's code and verifies the update.
        4. Refreshes the original dyna_flow instance
            and checks if
            it reflects the updated code.

        Args:
            obj_manager
            (DynaFlowManager): The
                manager responsible
                for dyna_flow operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a dyna_flow
        obj_1 = await DynaFlowFactory.create_async(
            session=session)

        # Retrieve the dyna_flow from the database
        result = await session.execute(
            select(DynaFlow).filter(
                DynaFlow._dyna_flow_id == (
                    obj_1.dyna_flow_id))  # type: ignore
        )  # type: ignore
        obj_2 = result.scalars().first()

        # Verify that the retrieved dyna_flow
        # matches the added dyna_flow
        assert obj_1.code == \
            obj_2.code

        # Update the dyna_flow's code
        updated_code1 = uuid.uuid4()
        obj_1.code = updated_code1
        updated_obj_1 = await obj_manager.update(
            obj_1)

        # Verify that the updated dyna_flow
        # is of type DynaFlow
        # and has the updated code
        assert isinstance(updated_obj_1,
                          DynaFlow)

        assert updated_obj_1.code == updated_code1

        # Refresh the original dyna_flow instance
        refreshed_obj_2 = await obj_manager.refresh(
            obj_2)

        # Verify that the refreshed dyna_flow
        # reflects the updated code
        assert refreshed_obj_2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_dyna_flow(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a
        nonexistent dyna_flow.

        Args:
            obj_manager
            (DynaFlowManager): The
                instance of the
                DynaFlowManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the dyna_flow
            refresh operation raises an exception.

        Returns:
            None
        """
        dyna_flow = DynaFlow(
            dyna_flow_id=999)

        with pytest.raises(Exception):
            await obj_manager.refresh(
                dyna_flow)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_dyna_flow(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to check if a dyna_flow
        exists using the manager function.

        Args:
            obj_manager
            (DynaFlowManager): The
                dyna_flow manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a dyna_flow
        obj_1 = await DynaFlowFactory.create_async(
            session=session)

        # Check if the dyna_flow exists
        # using the manager function
        assert await obj_manager.exists(
            obj_1.dyna_flow_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_dyna_flow(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        DynaFlowManager
        class correctly compares two
        dyna_flows.

        Args:
            obj_manager
            (DynaFlowManager): An
                instance of the
                DynaFlowManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a dyna_flow
        obj_1 = await \
            DynaFlowFactory.create_async(
                session=session)

        obj_2 = await \
            obj_manager.get_by_id(
                dyna_flow_id=obj_1.dyna_flow_id)

        assert obj_manager.is_equal(
            obj_1, obj_2) is True

        obj_1_dict = \
            obj_manager.to_dict(
                obj_1)

        dyna_flow3 = await \
            obj_manager.from_dict(
                obj_1_dict)

        assert obj_manager.is_equal(
            obj_1, dyna_flow3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_dyna_flow(
        self,
        obj_manager: DynaFlowManager
    ):
        """
        Test case to check if a dyna_flow with a
        non-existent ID exists in the database.

        Args:
            obj_manager
            (DynaFlowManager): The
                instance of the DynaFlowManager class.

        Returns:
            bool: True if the dyna_flow exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await obj_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            obj_manager
            (DynaFlowManager): The instance
                of the DynaFlowManager class.
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
