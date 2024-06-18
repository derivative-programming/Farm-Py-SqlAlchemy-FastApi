# models/managers/tests/customer_test.py
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
from managers.customer import CustomerManager
from models import Customer
from models.factory import CustomerFactory
from models.serialization_schema.customer import CustomerSchema
class TestCustomerManager:
    """
    #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def customer_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return CustomerManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        # Define mock data for our customer
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        customer = await customer_manager.build(**mock_data)
        # Assert that the returned object is an instance of Customer
        assert isinstance(customer, Customer)
        # Assert that the attributes of the customer match our mock data
        assert customer.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        customer_manager: CustomerManager,
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
            await customer_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_customer_to_database(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer = await CustomerFactory.build_async(session)
        assert test_customer.customer_id == 0
        # Add the customer using the manager's add method
        added_customer = await customer_manager.add(customer=test_customer)
        assert isinstance(added_customer, Customer)
        assert str(added_customer.insert_user_id) == (
            str(customer_manager._session_context.customer_code))
        assert str(added_customer.last_update_user_id) == (
            str(customer_manager._session_context.customer_code))
        assert added_customer.customer_id > 0
        # Fetch the customer from the database directly
        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == added_customer.customer_id  # type: ignore
            )
        )
        fetched_customer = result.scalars().first()
        # Assert that the fetched customer is not None and matches the added customer
        assert fetched_customer is not None
        assert isinstance(fetched_customer, Customer)
        assert fetched_customer.customer_id == added_customer.customer_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_customer_object(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Create a test customer using the CustomerFactory
        # without persisting it to the database
        test_customer = await CustomerFactory.build_async(session)
        assert test_customer.customer_id == 0
        test_customer.code = uuid.uuid4()
        # Add the customer using the manager's add method
        added_customer = await customer_manager.add(customer=test_customer)
        assert isinstance(added_customer, Customer)
        assert str(added_customer.insert_user_id) == (
            str(customer_manager._session_context.customer_code))
        assert str(added_customer.last_update_user_id) == (
            str(customer_manager._session_context.customer_code))
        assert added_customer.customer_id > 0
        # Assert that the returned customer matches the test customer
        assert added_customer.customer_id == test_customer.customer_id
        assert added_customer.code == test_customer.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer = await CustomerFactory.create_async(session)
        customer = await customer_manager.get_by_id(test_customer.customer_id)
        assert isinstance(customer, Customer)
        assert test_customer.customer_id == customer.customer_id
        assert test_customer.code == customer.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_customer = await customer_manager.get_by_id(non_existent_id)
        assert retrieved_customer is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_customer(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer = await CustomerFactory.create_async(session)
        customer = await customer_manager.get_by_code(test_customer.code)
        assert isinstance(customer, Customer)
        assert test_customer.customer_id == customer.customer_id
        assert test_customer.code == customer.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any Customer in the database
        random_code = uuid.uuid4()
        customer = await customer_manager.get_by_code(random_code)
        assert customer is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer = await CustomerFactory.create_async(session)
        test_customer.code = uuid.uuid4()
        updated_customer = await customer_manager.update(customer=test_customer)
        assert isinstance(updated_customer, Customer)
        assert str(updated_customer.last_update_user_id) == str(
            customer_manager._session_context.customer_code)
        assert updated_customer.customer_id == test_customer.customer_id
        assert updated_customer.code == test_customer.code
        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == test_customer.customer_id)  # type: ignore
        )
        fetched_customer = result.scalars().first()
        assert updated_customer.customer_id == fetched_customer.customer_id
        assert updated_customer.code == fetched_customer.code
        assert test_customer.customer_id == fetched_customer.customer_id
        assert test_customer.code == fetched_customer.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer = await CustomerFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_customer = await customer_manager.update(
            customer=test_customer,
            code=new_code
        )
        assert isinstance(updated_customer, Customer)
        assert str(updated_customer.last_update_user_id) == str(
            customer_manager._session_context.customer_code
        )
        assert updated_customer.customer_id == test_customer.customer_id
        assert updated_customer.code == new_code
        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == test_customer.customer_id)  # type: ignore
        )
        fetched_customer = result.scalars().first()
        assert updated_customer.customer_id == fetched_customer.customer_id
        assert updated_customer.code == fetched_customer.code
        assert test_customer.customer_id == fetched_customer.customer_id
        assert new_code == fetched_customer.code
    @pytest.mark.asyncio
    async def test_update_invalid_customer(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        # None customer
        customer = None
        new_code = uuid.uuid4()
        updated_customer = await (
            customer_manager.update(customer, code=new_code))  # type: ignore
        # Assertions
        assert updated_customer is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_customer = await CustomerFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await customer_manager.update(
                customer=test_customer,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_data = await CustomerFactory.create_async(session)
        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == customer_data.customer_id)  # type: ignore
        )
        fetched_customer = result.scalars().first()
        assert isinstance(fetched_customer, Customer)
        assert fetched_customer.customer_id == customer_data.customer_id
        await customer_manager.delete(
            customer_id=customer_data.customer_id)
        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == customer_data.customer_id)  # type: ignore
        )
        fetched_customer = result.scalars().first()
        assert fetched_customer is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await customer_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await customer_manager.delete("999") # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customers = await customer_manager.get_list()
        assert len(customers) == 0
        customers_data = (
            [await CustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(customers_data, List)
        customers = await customer_manager.get_list()
        assert len(customers) == 5
        assert all(isinstance(customer, Customer) for customer in customers)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer = await CustomerFactory.build_async(session)
        json_data = customer_manager.to_json(customer)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer = await CustomerFactory.build_async(session)
        dict_data = customer_manager.to_dict(customer)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer = await CustomerFactory.create_async(session)
        json_data = customer_manager.to_json(customer)
        deserialized_customer = customer_manager.from_json(json_data)
        assert isinstance(deserialized_customer, Customer)
        assert deserialized_customer.code == customer.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer = await CustomerFactory.create_async(session)
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        deserialized_customer = customer_manager.from_dict(customer_data)
        assert isinstance(deserialized_customer, Customer)
        assert deserialized_customer.code == customer.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customers_data = [
            await CustomerFactory.build_async(session) for _ in range(5)]
        customers = await customer_manager.add_bulk(customers_data)
        assert len(customers) == 5
        for updated_customer in customers:
            result = await session.execute(
                select(Customer).filter(
                    Customer._customer_id == updated_customer.customer_id  # type: ignore
                )
            )
            fetched_customer = result.scalars().first()
            assert isinstance(fetched_customer, Customer)
            assert str(fetched_customer.insert_user_id) == (
                str(customer_manager._session_context.customer_code))
            assert str(fetched_customer.last_update_user_id) == (
                str(customer_manager._session_context.customer_code))
            assert fetched_customer.customer_id == updated_customer.customer_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking customer instances
        customer1 = await CustomerFactory.create_async(session=session)
        customer2 = await CustomerFactory.create_async(session=session)
        logging.info(customer1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update customers
        updates = [
            {
                "customer_id": customer1.customer_id,
                "code": code_updated1
            },
            {
                "customer_id": customer2.customer_id,
                "code": code_updated2
            }
        ]
        updated_customers = await customer_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_customers) == 2
        logging.info(updated_customers[0].__dict__)
        logging.info(updated_customers[1].__dict__)
        logging.info('getall')
        customers = await customer_manager.get_list()
        logging.info(customers[0].__dict__)
        logging.info(customers[1].__dict__)
        assert updated_customers[0].code == code_updated1
        assert updated_customers[1].code == code_updated2
        assert str(updated_customers[0].last_update_user_id) == (
            str(customer_manager._session_context.customer_code))
        assert str(updated_customers[1].last_update_user_id) == (
            str(customer_manager._session_context.customer_code))
        result = await session.execute(
            select(Customer).filter(Customer._customer_id == 1)  # type: ignore
        )
        fetched_customer = result.scalars().first()
        assert isinstance(fetched_customer, Customer)
        assert fetched_customer.code == code_updated1
        result = await session.execute(
            select(Customer).filter(Customer._customer_id == 2)  # type: ignore
        )
        fetched_customer = result.scalars().first()
        assert isinstance(fetched_customer, Customer)
        assert fetched_customer.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_customer_id(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No customers to update since customer_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_customer_not_found(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update customers
        updates = [{"customer_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"customer_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer1 = await CustomerFactory.create_async(session=session)
        customer2 = await CustomerFactory.create_async(session=session)
        # Delete customers
        customer_ids = [customer1.customer_id, customer2.customer_id]
        result = await customer_manager.delete_bulk(customer_ids)
        assert result is True
        for customer_id in customer_ids:
            execute_result = await session.execute(
                select(Customer).filter(
                    Customer._customer_id == customer_id)  # type: ignore
            )
            fetched_customer = execute_result.scalars().first()
            assert fetched_customer is None
    @pytest.mark.asyncio
    async def test_delete_bulk_customers_not_found(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer1 = await CustomerFactory.create_async(session=session)
        assert isinstance(customer1, Customer)
        # Delete customers
        customer_ids = [1, 2]
        with pytest.raises(Exception):
            await customer_manager.delete_bulk(customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        # Delete customers with an empty list
        customer_ids = []
        result = await customer_manager.delete_bulk(customer_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer_ids = ["1", 2]
        with pytest.raises(Exception):
            await customer_manager.delete_bulk(customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customers_data = (
            [await CustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(customers_data, List)
        count = await customer_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        count = await customer_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add customers
        customers_data = (
            [await CustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(customers_data, List)
        sorted_customers = await customer_manager.get_sorted_list(
            sort_by="_customer_id")
        assert [customer.customer_id for customer in sorted_customers] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add customers
        customers_data = (
            [await CustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(customers_data, List)
        sorted_customers = await customer_manager.get_sorted_list(
            sort_by="customer_id", order="desc")
        assert [customer.customer_id for customer in sorted_customers] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await customer_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        sorted_customers = await customer_manager.get_sorted_list(sort_by="customer_id")
        assert len(sorted_customers) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a customer instance.
        This test performs the following steps:
        1. Creates a customer instance using the CustomerFactory.
        2. Retrieves the customer from the database to ensure
            it was added correctly.
        3. Updates the customer's code and verifies the update.
        4. Refreshes the original customer instance and checks if
            it reflects the updated code.
        Args:
            customer_manager (CustomerManager): The manager responsible
                for customer operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a customer
        customer1 = await CustomerFactory.create_async(session=session)
        # Retrieve the customer from the database
        result = await session.execute(
            select(Customer).filter(
                Customer._customer_id == customer1.customer_id)  # type: ignore
        )  # type: ignore
        customer2 = result.scalars().first()
        # Verify that the retrieved customer matches the added customer
        assert customer1.code == customer2.code
        # Update the customer's code
        updated_code1 = uuid.uuid4()
        customer1.code = updated_code1
        updated_customer1 = await customer_manager.update(customer1)
        # Verify that the updated customer is of type Customer
        # and has the updated code
        assert isinstance(updated_customer1, Customer)
        assert updated_customer1.code == updated_code1
        # Refresh the original customer instance
        refreshed_customer2 = await customer_manager.refresh(customer2)
        # Verify that the refreshed customer reflects the updated code
        assert refreshed_customer2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_customer(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        customer = Customer(customer_id=999)
        with pytest.raises(Exception):
            await customer_manager.refresh(customer)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_customer(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a customer
        customer1 = await CustomerFactory.create_async(session=session)
        # Check if the customer exists using the manager function
        assert await customer_manager.exists(customer1.customer_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_customer(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a customer
        customer1 = await CustomerFactory.create_async(session=session)
        customer2 = await customer_manager.get_by_id(customer_id=customer1.customer_id)
        assert customer_manager.is_equal(customer1, customer2) is True
        customer1_dict = customer_manager.to_dict(customer1)
        customer3 = customer_manager.from_dict(customer1_dict)
        assert customer_manager.is_equal(customer1, customer3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_customer(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        assert await customer_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
    # activeOrganizationID,
    # email,
    # emailConfirmedUTCDateTime
    # firstName,
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue,
    # fSUserCodeValue,
    # isActive,
    # isEmailAllowed,
    # isEmailConfirmed,
    # isEmailMarketingAllowed,
    # isLocked,
    # isMultipleOrganizationsAllowed,
    # isVerboseLoggingForced,
    # lastLoginUTCDateTime
    # lastName,
    # password,
    # phone,
    # province,
    # registrationUTCDateTime
    # TacID
    @pytest.mark.asyncio
    async def test_get_by_tac_id_existing(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a customer with a specific tac_id
        customer1 = await CustomerFactory.create_async(session=session)
        # Fetch the customer using the manager function
        fetched_customers = await customer_manager.get_by_tac_id(customer1.tac_id)
        assert len(fetched_customers) == 1
        assert isinstance(fetched_customers[0], Customer)
        assert fetched_customers[0].code == customer1.code
    @pytest.mark.asyncio
    async def test_get_by_tac_id_nonexistent(
        self,
        customer_manager: CustomerManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        fetched_customers = await customer_manager.get_by_tac_id(non_existent_id)
        assert len(fetched_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_tac_id_invalid_type(
        self,
        customer_manager: CustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await customer_manager.get_by_tac_id(invalid_id) # type: ignore
        await session.rollback()
    # uTCOffsetInMinutes,
    # zip,
# endset
