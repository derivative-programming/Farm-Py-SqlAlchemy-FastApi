# models/managers/tests/role_test.py
"""
    #TODO add comment
"""
import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from sqlalchemy.future import select
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import Role
import models
from models.factory import RoleFactory
from managers.role import RoleManager
from models.serialization_schema.role import RoleSchema
from services.db_config import DB_DIALECT, generate_uuid
DB_DIALECT = "sqlite"  # noqa: F811
class TestRoleManager:
    """
    #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def role_manager(self, session: AsyncSession):
        session_context = SessionContext(dict(), session)
        session_context.customer_code = generate_uuid()
        return RoleManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        role_manager: RoleManager
    ):
        """
            #TODO add comment
        """
        # Define mock data for our role
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        role = await role_manager.build(**mock_data)
        # Assert that the returned object is an instance of Role
        assert isinstance(role, Role)
        # Assert that the attributes of the role match our mock data
        assert role.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await role_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_role_to_database(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_role = await RoleFactory.build_async(session)
        assert test_role.role_id is None
        # Add the role using the manager's add method
        added_role = await role_manager.add(role=test_role)
        assert isinstance(added_role, Role)
        assert str(added_role.insert_user_id) == (
            str(role_manager._session_context.customer_code))
        assert str(added_role.last_update_user_id) == (
            str(role_manager._session_context.customer_code))
        assert added_role.role_id > 0
        # Fetch the role from the database directly
        result = await session.execute(
            select(Role).filter(Role.role_id == added_role.role_id))
        fetched_role = result.scalars().first()
        # Assert that the fetched role is not None and matches the added role
        assert fetched_role is not None
        assert isinstance(fetched_role, Role)
        assert fetched_role.role_id == added_role.role_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_role_object(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Create a test role using the RoleFactory without persisting it to the database
        test_role = await RoleFactory.build_async(session)
        assert test_role.role_id is None
        test_role.code = generate_uuid()
        # Add the role using the manager's add method
        added_role = await role_manager.add(role=test_role)
        assert isinstance(added_role, Role)
        assert str(added_role.insert_user_id) == (
            str(role_manager._session_context.customer_code))
        assert str(added_role.last_update_user_id) == (
            str(role_manager._session_context.customer_code))
        assert added_role.role_id > 0
        # Assert that the returned role matches the test role
        assert added_role.role_id == test_role.role_id
        assert added_role.code == test_role.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_role = await RoleFactory.create_async(session)
        role = await role_manager.get_by_id(test_role.role_id)
        assert isinstance(role, Role)
        assert test_role.role_id == role.role_id
        assert test_role.code == role.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        role_manager: RoleManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_role = await role_manager.get_by_id(non_existent_id)
        assert retrieved_role is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_role(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_role = await RoleFactory.create_async(session)
        role = await role_manager.get_by_code(test_role.code)
        assert isinstance(role, Role)
        assert test_role.role_id == role.role_id
        assert test_role.code == role.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        role_manager: RoleManager
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any Role in the database
        random_code = generate_uuid()
        role = await role_manager.get_by_code(random_code)
        assert role is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_role = await RoleFactory.create_async(session)
        test_role.code = generate_uuid()
        updated_role = await role_manager.update(role=test_role)
        assert isinstance(updated_role, Role)
        assert str(updated_role.last_update_user_id) == str(
            role_manager._session_context.customer_code)
        assert updated_role.role_id == test_role.role_id
        assert updated_role.code == test_role.code
        result = await session.execute(
            select(Role).filter(
                Role.role_id == test_role.role_id)
        )
        fetched_role = result.scalars().first()
        assert updated_role.role_id == fetched_role.role_id
        assert updated_role.code == fetched_role.code
        assert test_role.role_id == fetched_role.role_id
        assert test_role.code == fetched_role.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_role = await RoleFactory.create_async(session)
        new_code = generate_uuid()
        updated_role = await role_manager.update(
            role=test_role,
            code=new_code
        )
        assert isinstance(updated_role, Role)
        assert str(updated_role.last_update_user_id) == str(
            role_manager._session_context.customer_code
        )
        assert updated_role.role_id == test_role.role_id
        assert updated_role.code == new_code
        result = await session.execute(
            select(Role).filter(
                Role.role_id == test_role.role_id)
        )
        fetched_role = result.scalars().first()
        assert updated_role.role_id == fetched_role.role_id
        assert updated_role.code == fetched_role.code
        assert test_role.role_id == fetched_role.role_id
        assert new_code == fetched_role.code
    @pytest.mark.asyncio
    async def test_update_invalid_role(self, role_manager: RoleManager):
        # None role
        role = None
        new_code = generate_uuid()
        updated_role = await role_manager.update(role, code=new_code)
        # Assertions
        assert updated_role is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_role = await RoleFactory.create_async(session)
        new_code = generate_uuid()
        with pytest.raises(ValueError):
            updated_role = await role_manager.update(
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
            #TODO add comment
        """
        role_data = await RoleFactory.create_async(session)
        result = await session.execute(
            select(Role).filter(Role.role_id == role_data.role_id))
        fetched_role = result.scalars().first()
        assert isinstance(fetched_role, Role)
        assert fetched_role.role_id == role_data.role_id
        deleted_role = await role_manager.delete(
            role_id=role_data.role_id)
        result = await session.execute(
            select(Role).filter(Role.role_id == role_data.role_id))
        fetched_role = result.scalars().first()
        assert fetched_role is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        with pytest.raises(Exception):
            await role_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        roles = await role_manager.get_list()
        assert len(roles) == 0
        roles_data = (
            [await RoleFactory.create_async(session) for _ in range(5)])
        roles = await role_manager.get_list()
        assert len(roles) == 5
        assert all(isinstance(role, Role) for role in roles)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        role = await RoleFactory.build_async(session)
        json_data = role_manager.to_json(role)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        role = await RoleFactory.build_async(session)
        dict_data = role_manager.to_dict(role)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        role = await RoleFactory.create_async(session)
        json_data = role_manager.to_json(role)
        deserialized_role = role_manager.from_json(json_data)
        assert isinstance(deserialized_role, Role)
        assert deserialized_role.code == role.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        role = await RoleFactory.create_async(session)
        schema = RoleSchema()
        role_data = schema.dump(role)
        deserialized_role = role_manager.from_dict(role_data)
        assert isinstance(deserialized_role, Role)
        assert deserialized_role.code == role.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        roles_data = [await RoleFactory.build_async(session) for _ in range(5)]
        roles = await role_manager.add_bulk(roles_data)
        assert len(roles) == 5
        for updated_role in roles:
            result = await session.execute(select(Role).filter(Role.role_id == updated_role.role_id))
            fetched_role = result.scalars().first()
            assert isinstance(fetched_role, Role)
            assert str(fetched_role.insert_user_id) == (
                str(role_manager._session_context.customer_code))
            assert str(fetched_role.last_update_user_id) == (
                str(role_manager._session_context.customer_code))
            assert fetched_role.role_id == updated_role.role_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking role instances
        role1 = await RoleFactory.create_async(session=session)
        role2 = await RoleFactory.create_async(session=session)
        logging.info(role1.__dict__)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update roles
        updates = [
            {
                "role_id": 1,
                "code": code_updated1
            },
            {
                "role_id": 2,
                "code": code_updated2
            }
        ]
        updated_roles = await role_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_roles) == 2
        logging.info(updated_roles[0].__dict__)
        logging.info(updated_roles[1].__dict__)
        logging.info('getall')
        roles = await role_manager.get_list()
        logging.info(roles[0].__dict__)
        logging.info(roles[1].__dict__)
        assert updated_roles[0].code == code_updated1
        assert updated_roles[1].code == code_updated2
        assert str(updated_roles[0].last_update_user_id) == (
            str(role_manager._session_context.customer_code))
        assert str(updated_roles[1].last_update_user_id) == (
            str(role_manager._session_context.customer_code))
        result = await session.execute(select(Role).filter(Role.role_id == 1))
        fetched_role = result.scalars().first()
        assert isinstance(fetched_role, Role)
        assert fetched_role.code == code_updated1
        result = await session.execute(select(Role).filter(Role.role_id == 2))
        fetched_role = result.scalars().first()
        assert isinstance(fetched_role, Role)
        assert fetched_role.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_role_id(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No roles to update since role_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_roles = await role_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_role_not_found(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update roles
        updates = [{"role_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_roles = await role_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"role_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_roles = await role_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        role1 = await RoleFactory.create_async(session=session)
        role2 = await RoleFactory.create_async(session=session)
        # Delete roles
        role_ids = [1, 2]
        result = await role_manager.delete_bulk(role_ids)
        assert result is True
        for role_id in role_ids:
            execute_result = await session.execute(
                select(Role).filter(Role.role_id == role_id))
            fetched_role = execute_result.scalars().first()
            assert fetched_role is None
    @pytest.mark.asyncio
    async def test_delete_bulk_roles_not_found(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        role1 = await RoleFactory.create_async(session=session)
        # Delete roles
        role_ids = [1, 2]
        with pytest.raises(Exception):
            result = await role_manager.delete_bulk(role_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        role_manager: RoleManager
    ):
        """
            #TODO add comment
        """
        # Delete roles with an empty list
        role_ids = []
        result = await role_manager.delete_bulk(role_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        role_ids = ["1", 2]
        with pytest.raises(Exception):
            result = await role_manager.delete_bulk(role_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        roles_data = (
            [await RoleFactory.create_async(session) for _ in range(5)])
        count = await role_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        role_manager: RoleManager
    ):
        """
            #TODO add comment
        """
        count = await role_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add roles
        roles_data = (
            [await RoleFactory.create_async(session) for _ in range(5)])
        sorted_roles = await role_manager.get_sorted_list(sort_by="role_id")
        assert [role.role_id for role in sorted_roles] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add roles
        roles_data = (
            [await RoleFactory.create_async(session) for _ in range(5)])
        sorted_roles = await role_manager.get_sorted_list(
            sort_by="role_id", order="desc")
        assert [role.role_id for role in sorted_roles] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await role_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        role_manager: RoleManager
    ):
        """
            #TODO add comment
        """
        sorted_roles = await role_manager.get_sorted_list(sort_by="role_id")
        assert len(sorted_roles) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a role
        role1 = await RoleFactory.create_async(session=session)
        result = await session.execute(select(Role).filter(Role.role_id == role1.role_id))
        role2 = result.scalars().first()
        assert role1.code == role2.code
        updated_code1 = generate_uuid()
        role1.code = updated_code1
        updated_role1 = await role_manager.update(role1)
        assert updated_role1.code == updated_code1
        refreshed_role2 = await role_manager.refresh(role2)
        assert refreshed_role2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_role(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        role = Role(role_id=999)
        with pytest.raises(Exception):
            await role_manager.refresh(role)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_role(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a role
        role1 = await RoleFactory.create_async(session=session)
        # Check if the role exists using the manager function
        assert await role_manager.exists(role1.role_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_role(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a role
        role1 = await RoleFactory.create_async(session=session)
        role2 = await role_manager.get_by_id(role_id=role1.role_id)
        assert role_manager.is_equal(role1, role2) is True
        role1_dict = role_manager.to_dict(role1)
        role3 = role_manager.from_dict(role1_dict)
        assert role_manager.is_equal(role1, role3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_role(
        self,
        role_manager: RoleManager
    ):
        """
            #TODO add comment
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
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await role_manager.exists(invalid_id)
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
        role_manager: RoleManager,
        session: AsyncSession
    ):
        # Add a role with a specific pac_id
        role1 = await RoleFactory.create_async(session=session)
        # Fetch the role using the manager function
        fetched_roles = await role_manager.get_by_pac_id(role1.pac_id)
        assert len(fetched_roles) == 1
        assert isinstance(fetched_roles[0], Role)
        assert fetched_roles[0].code == role1.code
        stmt = select(models.Pac).where(
            models.Pac.pac_id == role1.pac_id)
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert fetched_roles[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        role_manager: RoleManager
    ):
        non_existent_id = 999
        fetched_roles = await role_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_roles) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        role_manager: RoleManager,
        session: AsyncSession
    ):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await role_manager.get_by_pac_id(invalid_id)
        await session.rollback()
# endset
