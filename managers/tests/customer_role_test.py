# models/managers/tests/customer_role_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    #TODO add comment
    #TODO file too big. split into separate test files
"""
import logging
from typing import List
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from helpers.session_context import SessionContext
from managers.customer_role import CustomerRoleManager
from models import CustomerRole
from models.factory import CustomerRoleFactory
from models.serialization_schema.customer_role import CustomerRoleSchema
class TestCustomerRoleManager:
    """
    #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def customer_role_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return CustomerRoleManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        # Define mock data for our customer_role
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        customer_role = await customer_role_manager.build(**mock_data)
        # Assert that the returned object is an instance of CustomerRole
        assert isinstance(customer_role, CustomerRole)
        # Assert that the attributes of the customer_role match our mock data
        assert customer_role.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await customer_role_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_customer_role_to_database(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer_role = await CustomerRoleFactory.build_async(session)
        assert test_customer_role.customer_role_id == 0
        # Add the customer_role using the manager's add method
        added_customer_role = await customer_role_manager.add(customer_role=test_customer_role)
        assert isinstance(added_customer_role, CustomerRole)
        assert str(added_customer_role.insert_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert str(added_customer_role.last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert added_customer_role.customer_role_id > 0
        # Fetch the customer_role from the database directly
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == added_customer_role.customer_role_id  # type: ignore
            )
        )
        fetched_customer_role = result.scalars().first()
        # Assert that the fetched customer_role is not None and matches the added customer_role
        assert fetched_customer_role is not None
        assert isinstance(fetched_customer_role, CustomerRole)
        assert fetched_customer_role.customer_role_id == added_customer_role.customer_role_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_customer_role_object(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Create a test customer_role using the CustomerRoleFactory
        # without persisting it to the database
        test_customer_role = await CustomerRoleFactory.build_async(session)
        assert test_customer_role.customer_role_id == 0
        test_customer_role.code = uuid.uuid4()
        # Add the customer_role using the manager's add method
        added_customer_role = await customer_role_manager.add(customer_role=test_customer_role)
        assert isinstance(added_customer_role, CustomerRole)
        assert str(added_customer_role.insert_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert str(added_customer_role.last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert added_customer_role.customer_role_id > 0
        # Assert that the returned customer_role matches the test customer_role
        assert added_customer_role.customer_role_id == test_customer_role.customer_role_id
        assert added_customer_role.code == test_customer_role.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        customer_role = await customer_role_manager.get_by_id(test_customer_role.customer_role_id)
        assert isinstance(customer_role, CustomerRole)
        assert test_customer_role.customer_role_id == customer_role.customer_role_id
        assert test_customer_role.code == customer_role.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_customer_role = await customer_role_manager.get_by_id(non_existent_id)
        assert retrieved_customer_role is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        customer_role = await customer_role_manager.get_by_code(test_customer_role.code)
        assert isinstance(customer_role, CustomerRole)
        assert test_customer_role.customer_role_id == customer_role.customer_role_id
        assert test_customer_role.code == customer_role.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any CustomerRole in the database
        random_code = uuid.uuid4()
        customer_role = await customer_role_manager.get_by_code(random_code)
        assert customer_role is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        test_customer_role.code = uuid.uuid4()
        updated_customer_role = await customer_role_manager.update(customer_role=test_customer_role)
        assert isinstance(updated_customer_role, CustomerRole)
        assert str(updated_customer_role.last_update_user_id) == str(
            customer_role_manager._session_context.customer_code)
        assert updated_customer_role.customer_role_id == test_customer_role.customer_role_id
        assert updated_customer_role.code == test_customer_role.code
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == test_customer_role.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert updated_customer_role.customer_role_id == fetched_customer_role.customer_role_id
        assert updated_customer_role.code == fetched_customer_role.code
        assert test_customer_role.customer_role_id == fetched_customer_role.customer_role_id
        assert test_customer_role.code == fetched_customer_role.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_customer_role = await customer_role_manager.update(
            customer_role=test_customer_role,
            code=new_code
        )
        assert isinstance(updated_customer_role, CustomerRole)
        assert str(updated_customer_role.last_update_user_id) == str(
            customer_role_manager._session_context.customer_code
        )
        assert updated_customer_role.customer_role_id == test_customer_role.customer_role_id
        assert updated_customer_role.code == new_code
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == test_customer_role.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert updated_customer_role.customer_role_id == fetched_customer_role.customer_role_id
        assert updated_customer_role.code == fetched_customer_role.code
        assert test_customer_role.customer_role_id == fetched_customer_role.customer_role_id
        assert new_code == fetched_customer_role.code
    @pytest.mark.asyncio
    async def test_update_invalid_customer_role(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        # None customer_role
        customer_role = None
        new_code = uuid.uuid4()
        updated_customer_role = await (
            customer_role_manager.update(customer_role, code=new_code))  # type: ignore
        # Assertions
        assert updated_customer_role is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer_role = await CustomerRoleFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await customer_role_manager.update(
                customer_role=test_customer_role,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role_data = await CustomerRoleFactory.create_async(session)
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == customer_role_data.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert isinstance(fetched_customer_role, CustomerRole)
        assert fetched_customer_role.customer_role_id == customer_role_data.customer_role_id
        await customer_role_manager.delete(
            customer_role_id=customer_role_data.customer_role_id)
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == customer_role_data.customer_role_id)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert fetched_customer_role is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await customer_role_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await customer_role_manager.delete("999") # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_roles = await customer_role_manager.get_list()
        assert len(customer_roles) == 0
        customer_roles_data = (
            [await CustomerRoleFactory.create_async(session) for _ in range(5)])
        assert isinstance(customer_roles_data, List)
        customer_roles = await customer_role_manager.get_list()
        assert len(customer_roles) == 5
        assert all(isinstance(customer_role, CustomerRole) for customer_role in customer_roles)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role = await CustomerRoleFactory.build_async(session)
        json_data = customer_role_manager.to_json(customer_role)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role = await CustomerRoleFactory.build_async(session)
        dict_data = customer_role_manager.to_dict(customer_role)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session)
        json_data = customer_role_manager.to_json(customer_role)
        deserialized_customer_role = customer_role_manager.from_json(json_data)
        assert isinstance(deserialized_customer_role, CustomerRole)
        assert deserialized_customer_role.code == customer_role.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role = await CustomerRoleFactory.create_async(session)
        schema = CustomerRoleSchema()
        customer_role_data = schema.dump(customer_role)
        deserialized_customer_role = customer_role_manager.from_dict(customer_role_data)
        assert isinstance(deserialized_customer_role, CustomerRole)
        assert deserialized_customer_role.code == customer_role.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_roles_data = [
            await CustomerRoleFactory.build_async(session) for _ in range(5)]
        customer_roles = await customer_role_manager.add_bulk(customer_roles_data)
        assert len(customer_roles) == 5
        for updated_customer_role in customer_roles:
            result = await session.execute(
                select(CustomerRole).filter(
                    CustomerRole._customer_role_id == updated_customer_role.customer_role_id  # type: ignore
                )
            )
            fetched_customer_role = result.scalars().first()
            assert isinstance(fetched_customer_role, CustomerRole)
            assert str(fetched_customer_role.insert_user_id) == (
                str(customer_role_manager._session_context.customer_code))
            assert str(fetched_customer_role.last_update_user_id) == (
                str(customer_role_manager._session_context.customer_code))
            assert fetched_customer_role.customer_role_id == updated_customer_role.customer_role_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking customer_role instances
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        customer_role2 = await CustomerRoleFactory.create_async(session=session)
        logging.info(customer_role1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update customer_roles
        updates = [
            {
                "customer_role_id": customer_role1.customer_role_id,
                "code": code_updated1
            },
            {
                "customer_role_id": customer_role2.customer_role_id,
                "code": code_updated2
            }
        ]
        updated_customer_roles = await customer_role_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_customer_roles) == 2
        logging.info(updated_customer_roles[0].__dict__)
        logging.info(updated_customer_roles[1].__dict__)
        logging.info('getall')
        customer_roles = await customer_role_manager.get_list()
        logging.info(customer_roles[0].__dict__)
        logging.info(customer_roles[1].__dict__)
        assert updated_customer_roles[0].code == code_updated1
        assert updated_customer_roles[1].code == code_updated2
        assert str(updated_customer_roles[0].last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        assert str(updated_customer_roles[1].last_update_user_id) == (
            str(customer_role_manager._session_context.customer_code))
        result = await session.execute(
            select(CustomerRole).filter(CustomerRole._customer_role_id == 1)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert isinstance(fetched_customer_role, CustomerRole)
        assert fetched_customer_role.code == code_updated1
        result = await session.execute(
            select(CustomerRole).filter(CustomerRole._customer_role_id == 2)  # type: ignore
        )
        fetched_customer_role = result.scalars().first()
        assert isinstance(fetched_customer_role, CustomerRole)
        assert fetched_customer_role.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_customer_role_id(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No customer_roles to update since customer_role_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await customer_role_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_customer_role_not_found(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update customer_roles
        updates = [{"customer_role_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await customer_role_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"customer_role_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await customer_role_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        customer_role2 = await CustomerRoleFactory.create_async(session=session)
        # Delete customer_roles
        customer_role_ids = [customer_role1.customer_role_id, customer_role2.customer_role_id]
        result = await customer_role_manager.delete_bulk(customer_role_ids)
        assert result is True
        for customer_role_id in customer_role_ids:
            execute_result = await session.execute(
                select(CustomerRole).filter(
                    CustomerRole._customer_role_id == customer_role_id)  # type: ignore
            )
            fetched_customer_role = execute_result.scalars().first()
            assert fetched_customer_role is None
    @pytest.mark.asyncio
    async def test_delete_bulk_customer_roles_not_found(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        assert isinstance(customer_role1, CustomerRole)
        # Delete customer_roles
        customer_role_ids = [1, 2]
        with pytest.raises(Exception):
            await customer_role_manager.delete_bulk(customer_role_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        # Delete customer_roles with an empty list
        customer_role_ids = []
        result = await customer_role_manager.delete_bulk(customer_role_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role_ids = ["1", 2]
        with pytest.raises(Exception):
            await customer_role_manager.delete_bulk(customer_role_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_roles_data = (
            [await CustomerRoleFactory.create_async(session) for _ in range(5)])
        assert isinstance(customer_roles_data, List)
        count = await customer_role_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        count = await customer_role_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add customer_roles
        customer_roles_data = (
            [await CustomerRoleFactory.create_async(session) for _ in range(5)])
        assert isinstance(customer_roles_data, List)
        sorted_customer_roles = await customer_role_manager.get_sorted_list(
            sort_by="_customer_role_id")
        assert [customer_role.customer_role_id for customer_role in sorted_customer_roles] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add customer_roles
        customer_roles_data = (
            [await CustomerRoleFactory.create_async(session) for _ in range(5)])
        assert isinstance(customer_roles_data, List)
        sorted_customer_roles = await customer_role_manager.get_sorted_list(
            sort_by="customer_role_id", order="desc")
        assert [customer_role.customer_role_id for customer_role in sorted_customer_roles] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await customer_role_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        sorted_customer_roles = await customer_role_manager.get_sorted_list(sort_by="customer_role_id")
        assert len(sorted_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a customer_role instance.
        This test performs the following steps:
        1. Creates a customer_role instance using the CustomerRoleFactory.
        2. Retrieves the customer_role from the database to ensure
            it was added correctly.
        3. Updates the customer_role's code and verifies the update.
        4. Refreshes the original customer_role instance and checks if
            it reflects the updated code.
        Args:
            customer_role_manager (CustomerRoleManager): The manager responsible
                for customer_role operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a customer_role
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        # Retrieve the customer_role from the database
        result = await session.execute(
            select(CustomerRole).filter(
                CustomerRole._customer_role_id == customer_role1.customer_role_id)  # type: ignore
        )  # type: ignore
        customer_role2 = result.scalars().first()
        # Verify that the retrieved customer_role matches the added customer_role
        assert customer_role1.code == customer_role2.code
        # Update the customer_role's code
        updated_code1 = uuid.uuid4()
        customer_role1.code = updated_code1
        updated_customer_role1 = await customer_role_manager.update(customer_role1)
        # Verify that the updated customer_role is of type CustomerRole
        # and has the updated code
        assert isinstance(updated_customer_role1, CustomerRole)
        assert updated_customer_role1.code == updated_code1
        # Refresh the original customer_role instance
        refreshed_customer_role2 = await customer_role_manager.refresh(customer_role2)
        # Verify that the refreshed customer_role reflects the updated code
        assert refreshed_customer_role2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_role = CustomerRole(customer_role_id=999)
        with pytest.raises(Exception):
            await customer_role_manager.refresh(customer_role)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a customer_role
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        # Check if the customer_role exists using the manager function
        assert await customer_role_manager.exists(customer_role1.customer_role_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_customer_role(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a customer_role
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        customer_role2 = await customer_role_manager.get_by_id(customer_role_id=customer_role1.customer_role_id)
        assert customer_role_manager.is_equal(customer_role1, customer_role2) is True
        customer_role1_dict = customer_role_manager.to_dict(customer_role1)
        customer_role3 = customer_role_manager.from_dict(customer_role1_dict)
        assert customer_role_manager.is_equal(customer_role1, customer_role3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_customer_role(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        assert await customer_role_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_role_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
    # CustomerID
    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a customer_role with a specific customer_id
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        # Fetch the customer_role using the manager function
        fetched_customer_roles = await customer_role_manager.get_by_customer_id(customer_role1.customer_id)
        assert len(fetched_customer_roles) == 1
        assert isinstance(fetched_customer_roles[0], CustomerRole)
        assert fetched_customer_roles[0].code == customer_role1.code
    @pytest.mark.asyncio
    async def test_get_by_customer_id_nonexistent(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        fetched_customer_roles = await customer_role_manager.get_by_customer_id(non_existent_id)
        assert len(fetched_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_get_by_customer_id_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_role_manager.get_by_customer_id(invalid_id) # type: ignore
        await session.rollback()
    # isPlaceholder,
    # placeholder,
    # RoleID
    @pytest.mark.asyncio
    async def test_get_by_role_id_existing(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a customer_role with a specific role_id
        customer_role1 = await CustomerRoleFactory.create_async(session=session)
        # Fetch the customer_role using the manager function
        fetched_customer_roles = await customer_role_manager.get_by_role_id(
            customer_role1.role_id)
        assert len(fetched_customer_roles) == 1
        assert isinstance(fetched_customer_roles[0], CustomerRole)
        assert fetched_customer_roles[0].code == customer_role1.code
        stmt = select(models.Role).where(
            models.Role._role_id == customer_role1.role_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        role = result.scalars().first()
        assert fetched_customer_roles[0].role_code_peek == role.code
    @pytest.mark.asyncio
    async def test_get_by_role_id_nonexistent(
        self,
        customer_role_manager: CustomerRoleManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        fetched_customer_roles = (
            await customer_role_manager.get_by_role_id(non_existent_id))
        assert len(fetched_customer_roles) == 0
    @pytest.mark.asyncio
    async def test_get_by_role_id_invalid_type(
        self,
        customer_role_manager: CustomerRoleManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_role_manager.get_by_role_id(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
