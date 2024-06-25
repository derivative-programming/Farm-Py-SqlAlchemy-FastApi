# models/managers/tests/role_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
    This class contains unit tests for the
    `RoleManager` class.
"""

from typing import List
import uuid  # noqa: F401

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from helpers.session_context import SessionContext
from managers.role import RoleManager
from models import Role
from models.factory import RoleFactory
from models.serialization_schema.role import RoleSchema


class TestRoleManager:
    """
    This class contains unit tests for the
    `RoleManager` class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def role_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `RoleManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return RoleManager(session_context)

    @pytest.mark.asyncio
    async def test_build(
        self,
        role_manager: RoleManager
    ):
        """
        Test case for the `build` method of
        `RoleManager`.
        """
        # Define mock data for our role
        mock_data = {
            "code": uuid.uuid4()
        }

        # Call the build function of the manager
        role = await \
            role_manager.build(
                **mock_data)

        # Assert that the returned object is an instance of Role
        assert isinstance(
            role,
            Role)

        # Assert that the attributes of the
        # role match our mock data
        assert role.code == mock_data["code"]

    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `RoleManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }

        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await role_manager.build(**mock_data)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_add_correctly_adds_role_to_database(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `RoleManager` that checks if a
        role is correctly added to the database.
        """
        test_role = await \
            RoleFactory.build_async(
                session)

        assert test_role.role_id == 0

        # Add the role using the
        # manager's add method
        added_role = await \
            role_manager.add(
                role=test_role)

        assert isinstance(added_role,
                          Role)

        assert str(added_role.insert_user_id) == (
            str(role_manager._session_context.customer_code))
        assert str(added_role.last_update_user_id) == (
            str(role_manager._session_context.customer_code))

        assert added_role.role_id > 0

        # Fetch the role from
        # the database directly
        result = await session.execute(
            select(Role).filter(
                Role._role_id == added_role.role_id  # type: ignore
            )
        )
        fetched_role = result.scalars().first()

        # Assert that the fetched role
        # is not None and matches the
        # added role
        assert fetched_role is not None
        assert isinstance(fetched_role,
                          Role)
        assert fetched_role.role_id == added_role.role_id

    @pytest.mark.asyncio
    async def test_add_returns_correct_role_object(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `RoleManager` that checks if the
        correct role object is returned.
        """
        # Create a test role
        # using the RoleFactory
        # without persisting it to the database
        test_role = await \
            RoleFactory.build_async(
                session)

        assert test_role.role_id == 0

        test_role.code = uuid.uuid4()

        # Add the role using
        # the manager's add method
        added_role = await \
            role_manager.add(
                role=test_role)

        assert isinstance(added_role,
                          Role)

        assert str(added_role.insert_user_id) == (
            str(role_manager._session_context.customer_code))
        assert str(added_role.last_update_user_id) == (
            str(role_manager._session_context.customer_code))

        assert added_role.role_id > 0

        # Assert that the returned
        # role matches the
        # test role
        assert added_role.role_id == \
            test_role.role_id
        assert added_role.code == \
            test_role.code

    @pytest.mark.asyncio
    async def test_update(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `RoleManager`
        that checks if a role
        is correctly updated.
        """
        test_role = await \
            RoleFactory.create_async(
                session)

        test_role.code = uuid.uuid4()

        updated_role = await \
            role_manager.update(
                role=test_role)

        assert isinstance(updated_role,
                          Role)

        assert str(updated_role.last_update_user_id) == str(
            role_manager._session_context.customer_code)

        assert updated_role.role_id == \
            test_role.role_id
        assert updated_role.code == \
            test_role.code

        result = await session.execute(
            select(Role).filter(
                Role._role_id == test_role.role_id)  # type: ignore
        )

        fetched_role = result.scalars().first()

        assert updated_role.role_id == \
            fetched_role.role_id
        assert updated_role.code == \
            fetched_role.code

        assert test_role.role_id == \
            fetched_role.role_id
        assert test_role.code == \
            fetched_role.code

    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method
        of `RoleManager`
        that checks if a role is
        correctly updated using a dictionary.
        """
        test_role = await \
            RoleFactory.create_async(
                session)

        new_code = uuid.uuid4()

        updated_role = await \
            role_manager.update(
                role=test_role,
                code=new_code
            )

        assert isinstance(updated_role,
                          Role)

        assert str(updated_role.last_update_user_id) == str(
            role_manager._session_context.customer_code
        )

        assert updated_role.role_id == \
            test_role.role_id
        assert updated_role.code == new_code

        result = await session.execute(
            select(Role).filter(
                Role._role_id == test_role.role_id)  # type: ignore
        )

        fetched_role = result.scalars().first()

        assert updated_role.role_id == \
            fetched_role.role_id
        assert updated_role.code == \
            fetched_role.code

        assert test_role.role_id == \
            fetched_role.role_id
        assert new_code == \
            fetched_role.code

    @pytest.mark.asyncio
    async def test_update_invalid_role(
        self,
        role_manager: RoleManager
    ):
        """
        Test case for the `update` method of
        `RoleManager`
        with an invalid role.
        """

        # None role
        role = None

        new_code = uuid.uuid4()

        updated_role = await (
            role_manager.update(
                role, code=new_code))  # type: ignore

        # Assertions
        assert updated_role is None

    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of
        `RoleManager`
        with a nonexistent attribute.
        """
        test_role = await \
            RoleFactory.create_async(
                session)

        new_code = uuid.uuid4()

        with pytest.raises(ValueError):
            await role_manager.update(
                role=test_role,
                xxx=new_code
            )

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of
        `RoleManager`.
        """
        role_data = await RoleFactory.create_async(
            session)

        result = await session.execute(
            select(Role).filter(
                Role._role_id == role_data.role_id)  # type: ignore
        )
        fetched_role = result.scalars().first()

        assert isinstance(fetched_role,
                          Role)

        assert fetched_role.role_id == \
            role_data.role_id

        await role_manager.delete(
            role_id=role_data.role_id)

        result = await session.execute(
            select(Role).filter(
                Role._role_id == role_data.role_id)  # type: ignore
        )
        fetched_role = result.scalars().first()

        assert fetched_role is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a nonexistent role.

        This test case ensures that when the delete method
        is called with the ID of a nonexistent role,
        an exception is raised. The test also verifies that
        the session is rolled back after the delete operation.

        :param role_manager: The instance of the
            RoleManager class.
        :param session: The instance of the AsyncSession class.
        """
        with pytest.raises(Exception):
            await role_manager.delete(999)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of deleting a role
        with an invalid type.

        This test case ensures that when the `delete` method
        of the `role_manager` is called with an invalid type,
        an exception is raised. The test case expects the
        `delete` method to raise an exception, and if it doesn't,
        the test case will fail.

        Args:
            role_manager
            (RoleManager): An
                instance of the
                `RoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            Exception: If the `delete` method does not raise an exception.

        """
        with pytest.raises(Exception):
            await role_manager.delete("999")  # type: ignore

        await session.rollback()

    @pytest.mark.asyncio
    async def test_get_list(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_list` method of the
        `RoleManager` class.

        This test verifies that the `get_list`
        method returns the correct list of roles.

        Steps:
        1. Call the `get_list` method of the
            `role_manager` instance.
        2. Assert that the returned list is empty.
        3. Create 5 role objects using the
            `RoleFactory.create_async` method.
        4. Assert that the `roles_data` variable is of type `List`.
        5. Call the `get_list` method of the
            `role_manager` instance again.
        6. Assert that the returned list contains 5 roles.
        7. Assert that all elements in the returned list are
            instances of the `Role` class.
        """

        roles = await role_manager.get_list()

        assert len(roles) == 0

        roles_data = (
            [await RoleFactory.create_async(session) for _ in range(5)])

        assert isinstance(roles_data, List)

        roles = await role_manager.get_list()

        assert len(roles) == 5
        assert all(isinstance(
            role, Role) for role in roles)

    @pytest.mark.asyncio
    async def test_to_json(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test the 'to_json' method of the RoleManager class.

        Args:
            role_manager
            (RoleManager): An
                instance of the
                RoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None

        Raises:
            AssertionError: If the json_data is None.
        """
        role = await \
            RoleFactory.build_async(
                session)

        json_data = role_manager.to_json(
            role)

        assert json_data is not None

    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test the to_dict method of the RoleManager class.

        Args:
            role_manager
            (RoleManager): An
                instance of the
                RoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        role = await \
            RoleFactory.build_async(
                session)

        dict_data = \
            role_manager.to_dict(
                role)

        assert dict_data is not None

    @pytest.mark.asyncio
    async def test_from_json(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test the `from_json` method of the `RoleManager` class.

        This method tests the functionality of the
        `from_json` method of the `RoleManager` class.
        It creates a role using
        the `RoleFactory`
        and converts it to JSON using the `to_json` method.
        Then, it deserializes the JSON data using the
        `from_json` method and asserts that the deserialized
        role is an instance of the
        `Role` class and has
        the same code as the original role.

        Args:
            role_manager
            (RoleManager): An
                instance of the
                `RoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None
        """
        role = await \
            RoleFactory.create_async(
                session)

        json_data = role_manager.to_json(
            role)

        deserialized_role = await \
                role_manager.from_json(json_data)

        assert isinstance(deserialized_role,
                          Role)
        assert deserialized_role.code == \
            role.code

    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test the `from_dict` method of the
        `RoleManager` class.

        This method tests the functionality of the
        `from_dict` method, which is used to deserialize
        a dictionary representation of a
        role object.

        Args:
            role_manager
            (RoleManager): An instance
                of the `RoleManager` class.
            session (AsyncSession): An instance of the `AsyncSession` class.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        role = await \
            RoleFactory.create_async(
                session)

        schema = RoleSchema()

        role_data = schema.dump(role)

        assert isinstance(role_data, dict)

        deserialized_role = await \
            role_manager.from_dict(
                role_data)

        assert isinstance(deserialized_role,
                          Role)

        assert deserialized_role.code == \
            role.code

    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of the count method
        in the RoleManager class.

        This test case creates 5 role
        objects using the
        RoleFactory and checks if the count method
        returns the correct count of
        roles.

        Steps:
        1. Create 5 role objects using
            the RoleFactory.
        2. Call the count method of the role_manager.
        3. Assert that the count is equal to 5.

        """
        roles_data = (
            [await RoleFactory.create_async(session) for _ in range(5)])

        assert isinstance(roles_data, List)

        count = await role_manager.count()

        assert count == 5

    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        role_manager: RoleManager
    ):
        """
        Test the count method when the database is empty.

        This test case checks if the count method of the
        RoleManager class returns 0 when the database is empty.

        Args:
            role_manager
            (RoleManager): An
                instance of the
                RoleManager class.

        Returns:
            None
        """

        count = await role_manager.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing
        a role instance.

        This test performs the following steps:
        1. Creates a role instance using
            the RoleFactory.
        2. Retrieves the role from th
            database to ensure
            it was added correctly.
        3. Updates the role's code and verifies the update.
        4. Refreshes the original role instance
            and checks if
            it reflects the updated code.

        Args:
            role_manager
            (RoleManager): The
                manager responsible
                for role operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a role
        role1 = await RoleFactory.create_async(
            session=session)

        # Retrieve the role from the database
        result = await session.execute(
            select(Role).filter(
                Role._role_id == role1.role_id)  # type: ignore
        )  # type: ignore
        role2 = result.scalars().first()

        # Verify that the retrieved role
        # matches the added role
        assert role1.code == \
            role2.code

        # Update the role's code
        updated_code1 = uuid.uuid4()
        role1.code = updated_code1
        updated_role1 = await role_manager.update(
            role1)

        # Verify that the updated role
        # is of type Role
        # and has the updated code
        assert isinstance(updated_role1,
                          Role)

        assert updated_role1.code == updated_code1

        # Refresh the original role instance
        refreshed_role2 = await role_manager.refresh(
            role2)

        # Verify that the refreshed role
        # reflects the updated code
        assert refreshed_role2.code == updated_code1

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_role(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of refreshing a nonexistent role.

        Args:
            role_manager
            (RoleManager): The
                instance of the
                RoleManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If the role
            refresh operation raises an exception.

        Returns:
            None
        """
        role = Role(
            role_id=999)

        with pytest.raises(Exception):
            await role_manager.refresh(
                role)

        await session.rollback()

    @pytest.mark.asyncio
    async def test_exists_with_existing_role(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to check if a role
        exists using the manager function.

        Args:
            role_manager
            (RoleManager): The
                role manager instance.
            session (AsyncSession): The async session object.

        Returns:
            None
        """
        # Add a role
        role1 = await RoleFactory.create_async(
            session=session)

        # Check if the role exists
        # using the manager function
        assert await role_manager.exists(
            role1.role_id) is True

    @pytest.mark.asyncio
    async def test_is_equal_with_existing_role(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test if the is_equal method of the
        RoleManager class correctly compares two roles.

        Args:
            role_manager
            (RoleManager): An
                instance of the
                RoleManager class.
            session (AsyncSession): An instance of the AsyncSession class.

        Returns:
            None
        """
        # Add a role
        role1 = await \
            RoleFactory.create_async(
                session=session)

        role2 = await \
            role_manager.get_by_id(
                role_id=role1.role_id)

        assert role_manager.is_equal(
            role1, role2) is True

        role1_dict = \
            role_manager.to_dict(
                role1)

        role3 = await \
            role_manager.from_dict(
                role1_dict)

        assert role_manager.is_equal(
            role1, role3) is True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_role(
        self,
        role_manager: RoleManager
    ):
        """
        Test case to check if a role with a
        non-existent ID exists in the database.

        Args:
            role_manager
            (RoleManager): The
                instance of the RoleManager class.

        Returns:
            bool: True if the role exists,
                False otherwise.
        """
        non_existent_id = 999

        assert await role_manager.exists(non_existent_id) is False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
        Test case to check if the exists method raises
        an exception when an invalid ID type is provided.

        Args:
            role_manager
            (RoleManager): The instance
                of the RoleManager class.
            session (AsyncSession): The instance of the AsyncSession class.

        Raises:
            Exception: If an exception is not raised by the exists method.

        Returns:
            None
        """
        invalid_id = "invalid_id"

        with pytest.raises(Exception):
            await role_manager.exists(invalid_id)  # type: ignore  # noqa: E501

        await session.rollback()

