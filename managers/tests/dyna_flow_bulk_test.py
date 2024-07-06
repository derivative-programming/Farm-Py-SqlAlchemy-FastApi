# models/managers/tests/dyna_flow_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DynaFlowManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.dyna_flow import DynaFlowManager
from models import DynaFlow
from models.factory import DynaFlowFactory


class TestDynaFlowBulkManager:
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
    async def test_add_bulk(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `DynaFlowManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        dyna_flows to the database.

        Steps:
        1. Generate a list of dyna_flow data using the
            `DynaFlowFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated dyna_flow data.
        3. Verify that the number of dyna_flows
            returned is
            equal to the number of dyna_flows added.
        4. For each updated dyna_flow, fetch the corresponding
            dyna_flow from the database.
        5. Verify that the fetched dyna_flow
            is an instance of the
            `DynaFlow` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            dyna_flow match the
            customer code of the session context.
        7. Verify that the dyna_flow_id of the fetched
            dyna_flow matches the
            dyna_flow_id of the updated
            dyna_flow.

        """
        dyna_flows_data = [
            await DynaFlowFactory.build_async(session)
            for _ in range(5)]

        dyna_flows = await obj_manager.add_bulk(
            dyna_flows_data)

        assert len(dyna_flows) == 5

        for updated_obj in dyna_flows:
            result = await session.execute(
                select(DynaFlow).filter(
                    DynaFlow._dyna_flow_id == (
                        updated_obj.dyna_flow_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                DynaFlow)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.dyna_flow_id == \
                updated_obj.dyna_flow_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of dyna_flows.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `DynaFlowManager` class.
        It creates two dyna_flow instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two dyna_flow instances using the
            `DynaFlowFactory.create_async` method.
        2. Generate new codes for the dyna_flows.
        3. Update the dyna_flows' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (DynaFlowManager):
                An instance of the
                `DynaFlowManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking dyna_flow instances
        obj_1 = await DynaFlowFactory. \
            create_async(
                session=session)
        obj_2 = await DynaFlowFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update dyna_flows
        updates = [
            {
                "dyna_flow_id":
                    obj_1.dyna_flow_id,
                "code": code_updated1
            },
            {
                "dyna_flow_id":
                    obj_2.dyna_flow_id,
                "code": code_updated2
            }
        ]
        updated_dyna_flows = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_dyna_flows) == 2
        logging.info(updated_dyna_flows[0]
                     .__dict__)
        logging.info(updated_dyna_flows[1]
                     .__dict__)

        logging.info('getall')
        dyna_flows = await obj_manager.get_list()
        logging.info(dyna_flows[0]
                     .__dict__)
        logging.info(dyna_flows[1]
                     .__dict__)

        assert updated_dyna_flows[0].code == \
            code_updated1
        assert updated_dyna_flows[1].code == \
            code_updated2

        assert str(updated_dyna_flows[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_dyna_flows[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(DynaFlow).filter(
                DynaFlow._dyna_flow_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlow)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(DynaFlow).filter(
                DynaFlow._dyna_flow_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DynaFlow)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_dyna_flow_id(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the dyna_flow_id is missing.

        This test case ensures that when the dyna_flow_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing dyna_flow_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No dyna_flows to update since
        # dyna_flow_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_dyna_flow_not_found(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a dyna_flow is not found.

        This test case performs the following steps:
        1. Defines a list of dyna_flow updates,
            where each update
            contains a dyna_flow_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the dyna_flow was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        dyna_flow is not found.

        """

        # Update dyna_flows
        updates = [{"dyna_flow_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: DynaFlowManager,
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

        :param obj_manager: An instance of the
            DynaFlowManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"dyna_flow_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        DynaFlowManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple dyna_flows
        from the database.

        Steps:
        1. Create two dyna_flow objects
            using the DynaFlowFactory.
        2. Delete the dyna_flows using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the dyna_flows
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The dyna_flows should
            no longer exist in the database.

        """

        obj_1 = await DynaFlowFactory.create_async(
            session=session)

        obj_2 = await DynaFlowFactory.create_async(
            session=session)

        # Delete dyna_flows
        dyna_flow_ids = [
            obj_1.dyna_flow_id,
            obj_2.dyna_flow_id
        ]
        result = await obj_manager.delete_bulk(
            dyna_flow_ids)

        assert result is True

        for dyna_flow_id in dyna_flow_ids:
            execute_result = await session.execute(
                select(DynaFlow).filter(
                    DynaFlow._dyna_flow_id == (
                        dyna_flow_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_dyna_flows_not_found(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        dyna_flows when some
        dyna_flows are not found.

        Steps:
        1. Create a dyna_flow using the
            DynaFlowFactory.
        2. Assert that the created dyna_flow
            is an instance of the
            DynaFlow class.
        3. Define a list of dyna_flow IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk dyna_flows.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        DynaFlowManager raises an exception
        when some dyna_flows with the specified IDs are
        not found in the database.
        """
        obj_1 = await DynaFlowFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          DynaFlow)

        # Delete dyna_flows
        dyna_flow_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                dyna_flow_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: DynaFlowManager
    ):
        """
        Test case to verify the behavior of deleting
        dyna_flows with an empty list.

        Args:
            obj_manager (DynaFlowManager): The
                instance of the
                DynaFlowManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete dyna_flows with an empty list
        dyna_flow_ids = []
        result = await obj_manager.delete_bulk(
            dyna_flow_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: DynaFlowManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid dyna_flow IDs are provided.

        Args:
            obj_manager (DynaFlowManager): The
                instance of the
                DynaFlowManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        dyna_flow_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                dyna_flow_ids)

        await session.rollback()
