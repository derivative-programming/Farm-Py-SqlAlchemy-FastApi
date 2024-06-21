# models/managers/tests/tac_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `TacManager` class.
"""
# TODO file too big. split into separate test files
import logging
from typing import List
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from helpers.session_context import SessionContext
from managers.tac import TacManager
from models import Tac
from models.factory import TacFactory
from models.serialization_schema.tac import TacSchema
class TestTacManager:
    """
    This class contains unit tests for the
    `TacManager` class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def tac_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `TacManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return TacManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        tac_manager: TacManager
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
        tac = await tac_manager.build(
            **mock_data)
        # Assert that the returned object is an instance of Tac
        assert isinstance(
            tac, Tac)
        # Assert that the attributes of the
        # tac match our mock data
        assert tac.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        tac_manager: TacManager,
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
            await tac_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_tac_to_database(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `TacManager` that checks if a
        tac is correctly added to the database.
        """
        test_tac = await TacFactory.build_async(
            session)
        assert test_tac.tac_id == 0
        # Add the tac using the
        # manager's add method
        added_tac = await tac_manager.add(
            tac=test_tac)
        assert isinstance(added_tac, Tac)
        assert str(added_tac.insert_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert str(added_tac.last_update_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert added_tac.tac_id > 0
        # Fetch the tac from
        # the database directly
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == added_tac.tac_id  # type: ignore
            )
        )
        fetched_tac = result.scalars().first()
        # Assert that the fetched tac
        # is not None and matches the
        # added tac
        assert fetched_tac is not None
        assert isinstance(fetched_tac, Tac)
        assert fetched_tac.tac_id == added_tac.tac_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_tac_object(
        self,
        tac_manager: TacManager,
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
        test_tac = await TacFactory.build_async(
            session)
        assert test_tac.tac_id == 0
        test_tac.code = uuid.uuid4()
        # Add the tac using
        # the manager's add method
        added_tac = await tac_manager.add(
            tac=test_tac)
        assert isinstance(added_tac, Tac)
        assert str(added_tac.insert_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert str(added_tac.last_update_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert added_tac.tac_id > 0
        # Assert that the returned
        # tac matches the
        # test tac
        assert added_tac.tac_id == \
            test_tac.tac_id
        assert added_tac.code == \
            test_tac.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `TacManager`.
        """
        test_tac = await TacFactory.create_async(
            session)
        tac = await tac_manager.get_by_id(
            test_tac.tac_id)
        assert isinstance(
            tac, Tac)
        assert test_tac.tac_id == \
            tac.tac_id
        assert test_tac.code == \
            tac.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        tac_manager: TacManager
    ):
        """
        Test case for the `get_by_id` method of
        `TacManager` when the
        tac is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_tac = await tac_manager.get_by_id(
            non_existent_id)
        assert retrieved_tac is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `TacManager` that checks if
        a tac is
        returned by its code.
        """
        test_tac = await TacFactory.create_async(
            session)
        tac = await tac_manager.get_by_code(
            test_tac.code)
        assert isinstance(
            tac, Tac)
        assert test_tac.tac_id == \
            tac.tac_id
        assert test_tac.code == \
            tac.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        tac_manager: TacManager
    ):
        """
        Test case for the `get_by_code` method of
        `TacManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any Tac in the database
        random_code = uuid.uuid4()
        tac = await tac_manager.get_by_code(
            random_code)
        assert tac is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `TacManager`
        that checks if a tac
        is correctly updated.
        """
        test_tac = await TacFactory.create_async(
            session)
        test_tac.code = uuid.uuid4()
        updated_tac = await tac_manager.update(
            tac=test_tac)
        assert isinstance(updated_tac, Tac)
        assert str(updated_tac.last_update_user_id) == str(
            tac_manager._session_context.customer_code)
        assert updated_tac.tac_id == \
            test_tac.tac_id
        assert updated_tac.code == \
            test_tac.code
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == test_tac.tac_id)  # type: ignore
        )
        fetched_tac = result.scalars().first()
        assert updated_tac.tac_id == \
            fetched_tac.tac_id
        assert updated_tac.code == \
            fetched_tac.code
        assert test_tac.tac_id == \
            fetched_tac.tac_id
        assert test_tac.code == \
            fetched_tac.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `TacManager`
        that checks if a tac is
        correctly updated using a dictionary.
        """
        test_tac = await TacFactory.create_async(
            session)
        new_code = uuid.uuid4()
        updated_tac = await tac_manager.update(
            tac=test_tac,
            code=new_code
        )
        assert isinstance(updated_tac, Tac)
        assert str(updated_tac.last_update_user_id) == str(
            tac_manager._session_context.customer_code
        )
        assert updated_tac.tac_id == \
            test_tac.tac_id
        assert updated_tac.code == new_code
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == test_tac.tac_id)  # type: ignore
        )
        fetched_tac = result.scalars().first()
        assert updated_tac.tac_id == \
            fetched_tac.tac_id
        assert updated_tac.code == \
            fetched_tac.code
        assert test_tac.tac_id == \
            fetched_tac.tac_id
        assert new_code == \
            fetched_tac.code
    @pytest.mark.asyncio
    async def test_update_invalid_tac(
        self,
        tac_manager: TacManager
    ):
        """
        Test case for the `update` method of `TacManager`
        with an invalid tac.
        """
        # None tac
        tac = None
        new_code = uuid.uuid4()
        updated_tac = await (
            tac_manager.update(
                tac, code=new_code))  # type: ignore
        # Assertions
        assert updated_tac is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `TacManager`
        with a nonexistent attribute.
        """
        test_tac = await TacFactory.create_async(
            session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await tac_manager.update(
                tac=test_tac,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `TacManager`.
        """
        tac_data = await TacFactory.create_async(
            session)
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == tac_data.tac_id)  # type: ignore
        )
        fetched_tac = result.scalars().first()
        assert isinstance(fetched_tac, Tac)
        assert fetched_tac.tac_id == \
            tac_data.tac_id
        await tac_manager.delete(
            tac_id=tac_data.tac_id)
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == tac_data.tac_id)  # type: ignore
        )
        fetched_tac = result.scalars().first()
        assert fetched_tac is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent tac.
        This test case ensures that when the delete method
        is called with the ID of a nonexistent tac,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.
        :param tac_manager: The instance of the TacManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await tac_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a tac
        with an invalid type.
        This test case ensures that when the `delete` method
        of the `tac_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.
        Args:
            tac_manager (TacManager): An
                instance of the
                `TacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            Exception: If the `delete` method does not raise an exception.
        """
        with pytest.raises(Exception):
            await tac_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `TacManager` class.
        This test verifies that the `get_list`
        method returns the correct list of tacs.
        Steps:
        1. Call the `get_list` method of the
            `tac_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 tac objects using the
            `TacFactory.create_async` method.
        4. Assert that the `tacs_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `tac_manager` instance again.
        6. Assert that the returned list contains 5 tacs.
        7. Assert that all elements in the returned list are
            instances of the `Tac` class.
        """
        tacs = await tac_manager.get_list()
        assert len(tacs) == 0
        tacs_data = (
            [await TacFactory.create_async(session) for _ in range(5)])
        assert isinstance(tacs_data, List)
        tacs = await tac_manager.get_list()
        assert len(tacs) == 5
        assert all(isinstance(
            tac, Tac) for tac in tacs)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the TacManager class.
        Args:
            tac_manager (TacManager): An
                instance of the
                TacManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        Raises:
            AssertionError: If the json_data is None.
        """
        tac = await TacFactory.build_async(
            session)
        json_data = tac_manager.to_json(
            tac)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the TacManager class.
        Args:
            tac_manager (TacManager): An
                instance of the
                TacManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        tac = await TacFactory.build_async(
            session)
        dict_data = tac_manager.to_dict(
            tac)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `TacManager` class.
        This method tests the functionality of the
        `from_json` method of the `TacManager` class.
        It creates a tac using
        the `TacFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        tac is an instance of the
        `Tac` class and has
        the same code as the original tac.
        Args:
            tac_manager (TacManager): An
            instance of the
                `TacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        tac = await TacFactory.create_async(
            session)
        json_data = tac_manager.to_json(
            tac)
        deserialized_tac = tac_manager.from_json(json_data)
        assert isinstance(deserialized_tac, Tac)
        assert deserialized_tac.code == \
            tac.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        tac_manager: TacManager,
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
            tac_manager (TacManager): An instance
                of the `TacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        Raises:
            AssertionError: If any of the assertions fail.
        """
        tac = await TacFactory.create_async(
            session)
        schema = TacSchema()
        tac_data = schema.dump(tac)
        assert isinstance(tac_data, dict)
        deserialized_tac = tac_manager.from_dict(
            tac_data)
        assert isinstance(deserialized_tac, Tac)
        assert deserialized_tac.code == \
            tac.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the `add_bulk` method of the
        `TacManager` class.
        This test case verifies that the `add_bulk`
        method correctly adds multiple tacs to the database.
        Steps:
        1. Generate a list of tac data using the
            `TacFactory.build_async` method.
        2. Call the `add_bulk` method of the
            `tac_manager` instance,
            passing in the
            generated tac data.
        3. Verify that the number of tacs
            returned is
            equal to the number of tacs added.
        4. For each updated tac, fetch the corresponding
            tac from the database.
        5. Verify that the fetched tac
            is an instance of the
            `Tac` class.
        6. Verify that the insert_user_id and
            last_update_user_id of the fetched
            tac match the
            customer code of the session context.
        7. Verify that the tac_id of the fetched
            tac matches the
            tac_id of the updated
            tac.
        """
        tacs_data = [
            await TacFactory.build_async(session) for _ in range(5)]
        tacs = await tac_manager.add_bulk(
            tacs_data)
        assert len(tacs) == 5
        for updated_tac in tacs:
            result = await session.execute(
                select(Tac).filter(
                    Tac._tac_id == updated_tac.tac_id  # type: ignore
                )
            )
            fetched_tac = result.scalars().first()
            assert isinstance(fetched_tac, Tac)
            assert str(fetched_tac.insert_user_id) == (
                str(tac_manager._session_context.customer_code))
            assert str(fetched_tac.last_update_user_id) == (
                str(tac_manager._session_context.customer_code))
            assert fetched_tac.tac_id == \
                updated_tac.tac_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for bulk update of tacs.
        This test case verifies the functionality of the
        `update_bulk` method in the `TacManager` class.
        It creates two tac instances,
        updates their codes
        using the `update_bulk` method, and then verifies
        that the updates were successful by checking the
        updated codes in the database.
        Steps:
        1. Create two tac instances using the
            `TacFactory.create_async` method.
        2. Generate new codes for the tacs.
        3. Update the tacs' codes using the `update_bulk` method.
        4. Verify that the update was successful by checking
            the updated codes in the database.
        Args:
            tac_manager (TacManager): An instance of the
                `TacManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.
        Returns:
            None
        """
        # Mocking tac instances
        tac1 = await TacFactory.create_async(
            session=session)
        tac2 = await TacFactory.create_async(
            session=session)
        logging.info(tac1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update tacs
        updates = [
            {
                "tac_id": tac1.tac_id,
                "code": code_updated1
            },
            {
                "tac_id": tac2.tac_id,
                "code": code_updated2
            }
        ]
        updated_tacs = await tac_manager.update_bulk(
            updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_tacs) == 2
        logging.info(updated_tacs[0].__dict__)
        logging.info(updated_tacs[1].__dict__)
        logging.info('getall')
        tacs = await tac_manager.get_list()
        logging.info(tacs[0].__dict__)
        logging.info(tacs[1].__dict__)
        assert updated_tacs[0].code == code_updated1
        assert updated_tacs[1].code == code_updated2
        assert str(updated_tacs[0].last_update_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert str(updated_tacs[1].last_update_user_id) == (
            str(tac_manager._session_context.customer_code))
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == 1)  # type: ignore
        )
        fetched_tac = result.scalars().first()
        assert isinstance(fetched_tac, Tac)
        assert fetched_tac.code == code_updated1
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == 2)  # type: ignore
        )
        fetched_tac = result.scalars().first()
        assert isinstance(fetched_tac, Tac)
        assert fetched_tac.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_tac_id(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the `update_bulk`
        method when the tac_id is missing.
        This test case ensures that when the tac_id is
        missing in the updates list,
        an exception is raised and the session is rolled back.
        Steps:
        1. Prepare the updates list with a missing tac_id.
        2. Call the `update_bulk` method with the updates list.
        3. Assert that an exception is raised.
        4. Rollback the session to undo any changes made during the test.
        """
        # No tacs to update since tac_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await tac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_tac_not_found(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the update_bulk
        method when a tac is not found.
        This test case performs the following steps:
        1. Defines a list of tac updates,
            where each update
            contains a tac_id and a code.
        2. Calls the update_bulk method of the
            tac_manager with the list of updates.
        3. Expects an exception to be raised, indicating that
            the tac was not found.
        4. Rolls back the session to undo any changes made during the test.
        Note: This test assumes that the update_bulk method
        throws an exception when a
        tac is not found.
        """
        # Update tacs
        updates = [{"tac_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await tac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        tac_manager: TacManager,
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
        :param tac_manager: An instance of the TacManager class.
        :param session: An instance of the AsyncSession class.
        """
        updates = [{"tac_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await tac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the delete_bulk method of the
        TacManager class.
        This test verifies that the delete_bulk method
        successfully deletes multiple tacs
        from the database.
        Steps:
        1. Create two tac objects
            using the TacFactory.
        2. Delete the tacs using the
            delete_bulk method
            of the tac_manager.
        3. Verify that the delete operation was successful by
            checking if the tacs no longer exist in the database.
        Expected Result:
        - The delete_bulk method should return True, indicating
            that the delete operation was successful.
        - The tacs should no longer exist in the database.
        """
        tac1 = await TacFactory.create_async(
            session=session)
        tac2 = await TacFactory.create_async(
            session=session)
        # Delete tacs
        tac_ids = [tac1.tac_id, tac2.tac_id]
        result = await tac_manager.delete_bulk(
            tac_ids)
        assert result is True
        for tac_id in tac_ids:
            execute_result = await session.execute(
                select(Tac).filter(
                    Tac._tac_id == tac_id)  # type: ignore
            )
            fetched_tac = execute_result.scalars().first()
            assert fetched_tac is None
    @pytest.mark.asyncio
    async def test_delete_bulk_tacs_not_found(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting bulk
        tacs when some tacs are not found.
        Steps:
        1. Create a tac using the
            TacFactory.
        2. Assert that the created tac
            is an instance of the
            Tac class.
        3. Define a list of tac IDs to delete.
        4. Use pytest.raises to assert that an exception is
            raised when deleting the bulk tacs.
        5. Rollback the session to undo any changes made during the test.
        This test case ensures that the delete_bulk method of the
        TacManager raises an exception
        when some tacs with the specified IDs are
        not found in the database.
        """
        tac1 = await TacFactory.create_async(
            session=session)
        assert isinstance(tac1, Tac)
        # Delete tacs
        tac_ids = [1, 2]
        with pytest.raises(Exception):
            await tac_manager.delete_bulk(
                tac_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        tac_manager: TacManager
    ):
        """
        Test case to verify the behavior of deleting
        tacs with an empty list.
        Args:
            tac_manager (TacManager): The
                instance of the
                TacManager class.
        Returns:
            None
        Raises:
            AssertionError: If the result is not True.
        """
        # Delete tacs with an empty list
        tac_ids = []
        result = await tac_manager.delete_bulk(
            tac_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the delete_bulk
        method when invalid tac IDs are provided.
        Args:
            tac_manager (TacManager): The
                instance of the
                TacManager class.
            session (AsyncSession): The async session object.
        Raises:
            Exception: If an exception is raised during the
                execution of the delete_bulk method.
        Returns:
            None
        """
        tac_ids = ["1", 2]
        with pytest.raises(Exception):
            await tac_manager.delete_bulk(
                tac_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        tac_manager: TacManager,
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
        2. Call the count method of the tac_manager.
        3. Assert that the count is equal to 5.
        """
        tacs_data = (
            [await TacFactory.create_async(session) for _ in range(5)])
        assert isinstance(tacs_data, List)
        count = await tac_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        tac_manager: TacManager
    ):
        """
        Test the count method when the database is empty.
        This test case checks if the count method of the
        TacManager class returns 0 when the database is empty.
        Args:
            tac_manager (TacManager): An
                instance of the
                TacManager class.
        Returns:
            None
        """
        count = await tac_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case for the 'get_sorted_list' method with basic sorting.
        This test case verifies that the 'get_sorted_list'
        method returns a list of tacs
        sorted by the '_tac_id' attribute in ascending order.
        Steps:
        1. Add tacs to the database.
        2. Call the 'get_sorted_list' method with the
            sort_by parameter set to '_tac_id'.
        3. Verify that the returned list of tacs is
            sorted by the '_tac_id' attribute.
        """
        # Add tacs
        tacs_data = (
            [await TacFactory.create_async(session) for _ in range(5)])
        assert isinstance(tacs_data, List)
        sorted_tacs = await tac_manager.get_sorted_list(
            sort_by="_tac_id")
        assert [tac.tac_id for tac in sorted_tacs] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        'get_sorted_list' method
        when sorting the list of tacs in descending order.
        Steps:
        1. Create a list of tacs using the TacFactory.
        2. Assert that the tacs_data is of type List.
        3. Call the 'get_sorted_list' method with
            sort_by="tac_id" and order="desc".
        4. Assert that the tac_ids of the
            sorted_tacs are in descending order.
        """
        # Add tacs
        tacs_data = (
            [await TacFactory.create_async(session) for _ in range(5)])
        assert isinstance(tacs_data, List)
        sorted_tacs = await tac_manager.get_sorted_list(
            sort_by="tac_id", order="desc")
        assert [tac.tac_id for tac in sorted_tacs] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to check if an AttributeError is raised when
        sorting the list by an invalid attribute.
        Args:
            tac_manager (TacManager): The
                instance of the
                TacManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            AttributeError: If an invalid attribute is used for sorting.
        Returns:
            None
        """
        with pytest.raises(AttributeError):
            await tac_manager.get_sorted_list(
                sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        tac_manager: TacManager
    ):
        """
        Test case to verify the behavior of
        `get_sorted_list` method when the database is empty.
        This test ensures that when the database is empty, the
        `get_sorted_list` method returns an empty list.
        Args:
            tac_manager (TacManager): An
                instance of the
                TacManager class.
        Returns:
            None
        """
        sorted_tacs = await tac_manager.get_sorted_list(
            sort_by="tac_id")
        assert len(sorted_tacs) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        tac_manager: TacManager,
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
            tac_manager (TacManager): The
                manager responsible
                for tac operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a tac
        tac1 = await TacFactory.create_async(
            session=session)
        # Retrieve the tac from the database
        result = await session.execute(
            select(Tac).filter(
                Tac._tac_id == tac1.tac_id)  # type: ignore
        )  # type: ignore
        tac2 = result.scalars().first()
        # Verify that the retrieved tac
        # matches the added tac
        assert tac1.code == \
            tac2.code
        # Update the tac's code
        updated_code1 = uuid.uuid4()
        tac1.code = updated_code1
        updated_tac1 = await tac_manager.update(
            tac1)
        # Verify that the updated tac
        # is of type Tac
        # and has the updated code
        assert isinstance(updated_tac1, Tac)
        assert updated_tac1.code == updated_code1
        # Refresh the original tac instance
        refreshed_tac2 = await tac_manager.refresh(
            tac2)
        # Verify that the refreshed tac
        # reflects the updated code
        assert refreshed_tac2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent tac.
        Args:
            tac_manager (TacManager): The
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
            await tac_manager.refresh(
                tac)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to check if a tac
        exists using the manager function.
        Args:
            tac_manager (TacManager): The
                tac manager instance.
            session (AsyncSession): The async session object.
        Returns:
            None
        """
        # Add a tac
        tac1 = await TacFactory.create_async(
            session=session)
        # Check if the tac exists
        # using the manager function
        assert await tac_manager.exists(
            tac1.tac_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        TacManager class correctly compares two tacs.
        Args:
            tac_manager (TacManager): An
                instance of the
                TacManager class.
            session (AsyncSession): An instance of the AsyncSession class.
        Returns:
            None
        """
        # Add a tac
        tac1 = await TacFactory.create_async(
            session=session)
        tac2 = await tac_manager.get_by_id(
            tac_id=tac1.tac_id)
        assert tac_manager.is_equal(
            tac1, tac2) is True
        tac1_dict = tac_manager.to_dict(
            tac1)
        tac3 = tac_manager.from_dict(
            tac1_dict)
        assert tac_manager.is_equal(
            tac1, tac3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tac(
        self,
        tac_manager: TacManager
    ):
        """
        Test case to check if a tac with a
        non-existent ID exists in the database.
        Args:
            tac_manager (TacManager): The
                instance of the TacManager class.
        Returns:
            bool: True if the tac exists,
                False otherwise.
        """
        non_existent_id = 999
        assert await tac_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.
        Args:
            tac_manager (TacManager): The instance
                of the TacManager class.
            session (AsyncSession): The instance of the AsyncSession class.
        Raises:
            Exception: If an exception is not raised by the exists method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await tac_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when
        a tac with
        a specific pac_id exists.
        Steps:
        1. Create a tac using the
            TacFactory.
        2. Fetch the tac using the
            `get_by_pac_id` method of the tac_manager.
        3. Assert that the fetched tacs list contains
            only one tac.
        4. Assert that the fetched tac
            is an instance
            of the Tac class.
        5. Assert that the code of the fetched tac
            matches the code of the created tac.
        6. Fetch the corresponding pac object
            using the pac_id of the created tac.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            tac matches the
            code of the fetched pac.
        """
        # Add a tac with a specific
        # pac_id
        tac1 = await TacFactory.create_async(
            session=session)
        # Fetch the tac using
        # the manager function
        fetched_tacs = await tac_manager.get_by_pac_id(
            tac1.pac_id)
        assert len(fetched_tacs) == 1
        assert isinstance(fetched_tacs[0], Tac)
        assert fetched_tacs[0].code == \
            tac1.code
        stmt = select(models.Pac).where(
            models.Pac._pac_id == tac1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert isinstance(pac, models.Pac)
        assert fetched_tacs[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        tac_manager: TacManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.
        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_tacs = await tac_manager.get_by_pac_id(
            non_existent_id)
        assert len(fetched_tacs) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.
        Args:
            tac_manager (TacManager): An
                instance of the TacManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.
        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_pac_id` method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await tac_manager.get_by_pac_id(
                invalid_id)  # type: ignore
        await session.rollback()
# endset
