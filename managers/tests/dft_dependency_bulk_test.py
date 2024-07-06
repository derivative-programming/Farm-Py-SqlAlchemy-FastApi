# models/managers/tests/dft_dependency_test.py  # pylint: disable=duplicate-code
# pylint: disable=protected-access, too-many-public-methods
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `DFTDependencyManager` class.
"""

import logging
import uuid  # noqa: F401

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import pytest
from helpers.session_context import SessionContext
from managers.dft_dependency import DFTDependencyManager
from models import DFTDependency
from models.factory import DFTDependencyFactory


class TestDFTDependencyBulkManager:
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
    async def test_add_bulk(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `DFTDependencyManager` class.

        This test case verifies that the `add_bulk`
        method correctly adds multiple
        dft_dependencys to the database.

        Steps:
        1. Generate a list of dft_dependency data using the
            `DFTDependencyFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `obj_manager` instance,
            passing in the
            generated dft_dependency data.
        3. Verify that the number of dft_dependencys
            returned is
            equal to the number of dft_dependencys added.
        4. For each updated dft_dependency, fetch the corresponding
            dft_dependency from the database.
        5. Verify that the fetched dft_dependency
            is an instance of the
            `DFTDependency` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            dft_dependency match the
            customer code of the session context.
        7. Verify that the dft_dependency_id of the fetched
            dft_dependency matches the
            dft_dependency_id of the updated
            dft_dependency.

        """
        dft_dependencys_data = [
            await DFTDependencyFactory.build_async(session)
            for _ in range(5)]

        dft_dependencys = await obj_manager.add_bulk(
            dft_dependencys_data)

        assert len(dft_dependencys) == 5

        for updated_obj in dft_dependencys:
            result = await session.execute(
                select(DFTDependency).filter(
                    DFTDependency._dft_dependency_id == (
                        updated_obj.dft_dependency_id)  # type: ignore
                )
            )
            fetched_obj = result.scalars().first()

            assert isinstance(
                fetched_obj,
                DFTDependency)

            assert str(fetched_obj.insert_user_id) == (
                str(obj_manager._session_context.customer_code))
            assert str(fetched_obj.last_update_user_id) == (
                str(obj_manager._session_context.customer_code))

            assert fetched_obj.dft_dependency_id == \
                updated_obj.dft_dependency_id

    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of dft_dependencys.

        This test case verifies the functionality of the
        `update_bulk` method in the
        `DFTDependencyManager` class.
        It creates two dft_dependency instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.

        Steps:
        1. Create two dft_dependency instances using the
            `DFTDependencyFactory.create_async` method.
        2. Generate new codes for the dft_dependencys.
        3. Update the dft_dependencys' codes
            using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.

        Args:
            obj_manager (DFTDependencyManager):
                An instance of the
                `DFTDependencyManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        # Mocking dft_dependency instances
        obj_1 = await DFTDependencyFactory. \
            create_async(
                session=session)
        obj_2 = await DFTDependencyFactory. \
            create_async(
                session=session)
        logging.info(obj_1.__dict__)

        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)

        # Update dft_dependencys
        updates = [
            {
                "dft_dependency_id":
                    obj_1.dft_dependency_id,
                "code": code_updated1
            },
            {
                "dft_dependency_id":
                    obj_2.dft_dependency_id,
                "code": code_updated2
            }
        ]
        updated_dft_dependencys = await obj_manager.update_bulk(
            updates)

        logging.info('bulk update results')
        # Assertions
        assert len(updated_dft_dependencys) == 2
        logging.info(updated_dft_dependencys[0]
                     .__dict__)
        logging.info(updated_dft_dependencys[1]
                     .__dict__)

        logging.info('getall')
        dft_dependencys = await obj_manager.get_list()
        logging.info(dft_dependencys[0]
                     .__dict__)
        logging.info(dft_dependencys[1]
                     .__dict__)

        assert updated_dft_dependencys[0].code == \
            code_updated1
        assert updated_dft_dependencys[1].code == \
            code_updated2

        assert str(updated_dft_dependencys[0]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        assert str(updated_dft_dependencys[1]
                   .last_update_user_id) == (
            str(obj_manager
                ._session_context.customer_code))

        result = await session.execute(
            select(DFTDependency).filter(
                DFTDependency._dft_dependency_id == 1)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DFTDependency)

        assert fetched_obj.code == code_updated1

        result = await session.execute(
            select(DFTDependency).filter(
                DFTDependency._dft_dependency_id == 2)  # type: ignore
        )
        fetched_obj = result.scalars().first()

        assert isinstance(fetched_obj,
                          DFTDependency)

        assert fetched_obj.code == code_updated2

    @pytest.mark.asyncio
    async def test_update_bulk_missing_dft_dependency_id(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the dft_dependency_id is missing.

        This test case ensures that when the dft_dependency_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.

        Steps:
        1. Prepare the updates list with a missing dft_dependency_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.

        """
        # No dft_dependencys to update since
        # dft_dependency_id is missing
        updates = [{"name": "Red Rose"}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_dft_dependency_not_found(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a dft_dependency is not found.

        This test case performs the following steps:
        1. Defines a list of dft_dependency updates,
            where each update
            contains a dft_dependency_id and a code.
        2. Calls the update_bulk method of the
            obj_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the dft_dependency was not found.
        4. Rolls back the session to undo any changes made during the test.

        Note: This test assumes that the update_bulk method
        throws an exception when a
        dft_dependency is not found.

        """

        # Update dft_dependencys
        updates = [{"dft_dependency_id": 1, "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        obj_manager: DFTDependencyManager,
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
            DFTDependencyManager class.
        :param session: An instance of the AsyncSession class.
        """

        updates = [{"dft_dependency_id": "2", "code": uuid.uuid4()}]

        with pytest.raises(Exception):
            await obj_manager.update_bulk(updates)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        DFTDependencyManager class.

        This test verifies that the delete_bulk method
        successfully deletes multiple dft_dependencys
        from the database.

        Steps:
        1. Create two dft_dependency objects
            using the DFTDependencyFactory.
        2. Delete the dft_dependencys using the
            delete_bulk method
            of the obj_manager.
        3. Verify that the delete operation was successful by
            checking if the dft_dependencys
            no longer exist in the database.

        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The dft_dependencys should
            no longer exist in the database.

        """

        obj_1 = await DFTDependencyFactory.create_async(
            session=session)

        obj_2 = await DFTDependencyFactory.create_async(
            session=session)

        # Delete dft_dependencys
        dft_dependency_ids = [
            obj_1.dft_dependency_id,
            obj_2.dft_dependency_id
        ]
        result = await obj_manager.delete_bulk(
            dft_dependency_ids)

        assert result is True

        for dft_dependency_id in dft_dependency_ids:
            execute_result = await session.execute(
                select(DFTDependency).filter(
                    DFTDependency._dft_dependency_id == (
                        dft_dependency_id))  # type: ignore
            )
            fetched_obj = execute_result.scalars().first()

            assert fetched_obj is None

    @pytest.mark.asyncio
    async def test_delete_bulk_dft_dependencys_not_found(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        dft_dependencys when some
        dft_dependencys are not found.

        Steps:
        1. Create a dft_dependency using the
            DFTDependencyFactory.
        2. Assert that the created dft_dependency
            is an instance of the
            DFTDependency class.
        3. Define a list of dft_dependency IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk dft_dependencys.
        5. Rollback the session to undo any changes made during the test.

        This test case ensures that the delete_bulk method of the
        DFTDependencyManager raises an exception
        when some dft_dependencys with the specified IDs are
        not found in the database.
        """
        obj_1 = await DFTDependencyFactory.create_async(
            session=session)

        assert isinstance(obj_1,
                          DFTDependency)

        # Delete dft_dependencys
        dft_dependency_ids = [1, 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                dft_dependency_ids)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        obj_manager: DFTDependencyManager
    ):
        """
        Test case to verify the behavior of deleting
        dft_dependencys with an empty list.

        Args:
            obj_manager (DFTDependencyManager): The
                instance of the
                DFTDependencyManager class.

        Returns:
            None

        Raises:
            AssertionError: If the result is not True.
        """

        # Delete dft_dependencys with an empty list
        dft_dependency_ids = []
        result = await obj_manager.delete_bulk(
            dft_dependency_ids)

        # Assertions
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        obj_manager: DFTDependencyManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid dft_dependency IDs are provided.

        Args:
            obj_manager (DFTDependencyManager): The
                instance of the
                DFTDependencyManager class.
            session (AsyncSession): The async session object.

        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.

        Returns:
            None
        """

        dft_dependency_ids = ["1", 2]

        with pytest.raises(Exception):
            await obj_manager.delete_bulk(
                dft_dependency_ids)

        await session.rollback()
