# models/managers/tests/org_customer_test.py
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
from managers.org_customer import OrgCustomerManager
from models import OrgCustomer
from models.factory import OrgCustomerFactory
from models.serialization_schema.org_customer import OrgCustomerSchema
class TestOrgCustomerManager:
    """
    #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def org_customer_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return OrgCustomerManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        # Define mock data for our org_customer
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        org_customer = await org_customer_manager.build(**mock_data)
        # Assert that the returned object is an instance of OrgCustomer
        assert isinstance(org_customer, OrgCustomer)
        # Assert that the attributes of the org_customer match our mock data
        assert org_customer.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        org_customer_manager: OrgCustomerManager,
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
            await org_customer_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_org_customer_to_database(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_org_customer = await OrgCustomerFactory.build_async(session)
        assert test_org_customer.org_customer_id == 0
        # Add the org_customer using the manager's add method
        added_org_customer = await org_customer_manager.add(org_customer=test_org_customer)
        assert isinstance(added_org_customer, OrgCustomer)
        assert str(added_org_customer.insert_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert str(added_org_customer.last_update_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert added_org_customer.org_customer_id > 0
        # Fetch the org_customer from the database directly
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == added_org_customer.org_customer_id  # type: ignore
            )
        )
        fetched_org_customer = result.scalars().first()
        # Assert that the fetched org_customer is not None and matches the added org_customer
        assert fetched_org_customer is not None
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.org_customer_id == added_org_customer.org_customer_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_org_customer_object(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Create a test org_customer using the OrgCustomerFactory
        # without persisting it to the database
        test_org_customer = await OrgCustomerFactory.build_async(session)
        assert test_org_customer.org_customer_id == 0
        test_org_customer.code = uuid.uuid4()
        # Add the org_customer using the manager's add method
        added_org_customer = await org_customer_manager.add(org_customer=test_org_customer)
        assert isinstance(added_org_customer, OrgCustomer)
        assert str(added_org_customer.insert_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert str(added_org_customer.last_update_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert added_org_customer.org_customer_id > 0
        # Assert that the returned org_customer matches the test org_customer
        assert added_org_customer.org_customer_id == test_org_customer.org_customer_id
        assert added_org_customer.code == test_org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_org_customer = await OrgCustomerFactory.create_async(session)
        org_customer = await org_customer_manager.get_by_id(test_org_customer.org_customer_id)
        assert isinstance(org_customer, OrgCustomer)
        assert test_org_customer.org_customer_id == org_customer.org_customer_id
        assert test_org_customer.code == org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_org_customer = await org_customer_manager.get_by_id(non_existent_id)
        assert retrieved_org_customer is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_org_customer = await OrgCustomerFactory.create_async(session)
        org_customer = await org_customer_manager.get_by_code(test_org_customer.code)
        assert isinstance(org_customer, OrgCustomer)
        assert test_org_customer.org_customer_id == org_customer.org_customer_id
        assert test_org_customer.code == org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any OrgCustomer in the database
        random_code = uuid.uuid4()
        org_customer = await org_customer_manager.get_by_code(random_code)
        assert org_customer is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_org_customer = await OrgCustomerFactory.create_async(session)
        test_org_customer.code = uuid.uuid4()
        updated_org_customer = await org_customer_manager.update(org_customer=test_org_customer)
        assert isinstance(updated_org_customer, OrgCustomer)
        assert str(updated_org_customer.last_update_user_id) == str(
            org_customer_manager._session_context.customer_code)
        assert updated_org_customer.org_customer_id == test_org_customer.org_customer_id
        assert updated_org_customer.code == test_org_customer.code
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == test_org_customer.org_customer_id)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert updated_org_customer.org_customer_id == fetched_org_customer.org_customer_id
        assert updated_org_customer.code == fetched_org_customer.code
        assert test_org_customer.org_customer_id == fetched_org_customer.org_customer_id
        assert test_org_customer.code == fetched_org_customer.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_org_customer = await OrgCustomerFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_org_customer = await org_customer_manager.update(
            org_customer=test_org_customer,
            code=new_code
        )
        assert isinstance(updated_org_customer, OrgCustomer)
        assert str(updated_org_customer.last_update_user_id) == str(
            org_customer_manager._session_context.customer_code
        )
        assert updated_org_customer.org_customer_id == test_org_customer.org_customer_id
        assert updated_org_customer.code == new_code
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == test_org_customer.org_customer_id)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert updated_org_customer.org_customer_id == fetched_org_customer.org_customer_id
        assert updated_org_customer.code == fetched_org_customer.code
        assert test_org_customer.org_customer_id == fetched_org_customer.org_customer_id
        assert new_code == fetched_org_customer.code
    @pytest.mark.asyncio
    async def test_update_invalid_org_customer(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        # None org_customer
        org_customer = None
        new_code = uuid.uuid4()
        updated_org_customer = await (
            org_customer_manager.update(org_customer, code=new_code))  # type: ignore
        # Assertions
        assert updated_org_customer is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_org_customer = await OrgCustomerFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await org_customer_manager.update(
                org_customer=test_org_customer,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer_data = await OrgCustomerFactory.create_async(session)
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == org_customer_data.org_customer_id)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.org_customer_id == org_customer_data.org_customer_id
        await org_customer_manager.delete(
            org_customer_id=org_customer_data.org_customer_id)
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == org_customer_data.org_customer_id)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert fetched_org_customer is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await org_customer_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await org_customer_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customers = await org_customer_manager.get_list()
        assert len(org_customers) == 0
        org_customers_data = (
            [await OrgCustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_customers_data, List)
        org_customers = await org_customer_manager.get_list()
        assert len(org_customers) == 5
        assert all(isinstance(org_customer, OrgCustomer) for org_customer in org_customers)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer = await OrgCustomerFactory.build_async(session)
        json_data = org_customer_manager.to_json(org_customer)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer = await OrgCustomerFactory.build_async(session)
        dict_data = org_customer_manager.to_dict(org_customer)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer = await OrgCustomerFactory.create_async(session)
        json_data = org_customer_manager.to_json(org_customer)
        deserialized_org_customer = org_customer_manager.from_json(json_data)
        assert isinstance(deserialized_org_customer, OrgCustomer)
        assert deserialized_org_customer.code == org_customer.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer = await OrgCustomerFactory.create_async(session)
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        deserialized_org_customer = org_customer_manager.from_dict(org_customer_data)
        assert isinstance(deserialized_org_customer, OrgCustomer)
        assert deserialized_org_customer.code == org_customer.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customers_data = [
            await OrgCustomerFactory.build_async(session) for _ in range(5)]
        org_customers = await org_customer_manager.add_bulk(org_customers_data)
        assert len(org_customers) == 5
        for updated_org_customer in org_customers:
            result = await session.execute(
                select(OrgCustomer).filter(
                    OrgCustomer._org_customer_id == updated_org_customer.org_customer_id  # type: ignore
                )
            )
            fetched_org_customer = result.scalars().first()
            assert isinstance(fetched_org_customer, OrgCustomer)
            assert str(fetched_org_customer.insert_user_id) == (
                str(org_customer_manager._session_context.customer_code))
            assert str(fetched_org_customer.last_update_user_id) == (
                str(org_customer_manager._session_context.customer_code))
            assert fetched_org_customer.org_customer_id == updated_org_customer.org_customer_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking org_customer instances
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        org_customer2 = await OrgCustomerFactory.create_async(session=session)
        logging.info(org_customer1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update org_customers
        updates = [
            {
                "org_customer_id": org_customer1.org_customer_id,
                "code": code_updated1
            },
            {
                "org_customer_id": org_customer2.org_customer_id,
                "code": code_updated2
            }
        ]
        updated_org_customers = await org_customer_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_org_customers) == 2
        logging.info(updated_org_customers[0].__dict__)
        logging.info(updated_org_customers[1].__dict__)
        logging.info('getall')
        org_customers = await org_customer_manager.get_list()
        logging.info(org_customers[0].__dict__)
        logging.info(org_customers[1].__dict__)
        assert updated_org_customers[0].code == code_updated1
        assert updated_org_customers[1].code == code_updated2
        assert str(updated_org_customers[0].last_update_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        assert str(updated_org_customers[1].last_update_user_id) == (
            str(org_customer_manager._session_context.customer_code))
        result = await session.execute(
            select(OrgCustomer).filter(OrgCustomer._org_customer_id == 1)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.code == code_updated1
        result = await session.execute(
            select(OrgCustomer).filter(OrgCustomer._org_customer_id == 2)  # type: ignore
        )
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_org_customer_id(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No org_customers to update since org_customer_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_org_customer_not_found(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update org_customers
        updates = [{"org_customer_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"org_customer_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        org_customer2 = await OrgCustomerFactory.create_async(session=session)
        # Delete org_customers
        org_customer_ids = [org_customer1.org_customer_id, org_customer2.org_customer_id]
        result = await org_customer_manager.delete_bulk(org_customer_ids)
        assert result is True
        for org_customer_id in org_customer_ids:
            execute_result = await session.execute(
                select(OrgCustomer).filter(
                    OrgCustomer._org_customer_id == org_customer_id)  # type: ignore
            )
            fetched_org_customer = execute_result.scalars().first()
            assert fetched_org_customer is None
    @pytest.mark.asyncio
    async def test_delete_bulk_org_customers_not_found(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        assert isinstance(org_customer1, OrgCustomer)
        # Delete org_customers
        org_customer_ids = [1, 2]
        with pytest.raises(Exception):
            await org_customer_manager.delete_bulk(org_customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        # Delete org_customers with an empty list
        org_customer_ids = []
        result = await org_customer_manager.delete_bulk(org_customer_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer_ids = ["1", 2]
        with pytest.raises(Exception):
            await org_customer_manager.delete_bulk(org_customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customers_data = (
            [await OrgCustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_customers_data, List)
        count = await org_customer_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        count = await org_customer_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add org_customers
        org_customers_data = (
            [await OrgCustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_customers_data, List)
        sorted_org_customers = await org_customer_manager.get_sorted_list(
            sort_by="_org_customer_id")
        assert [org_customer.org_customer_id for org_customer in sorted_org_customers] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add org_customers
        org_customers_data = (
            [await OrgCustomerFactory.create_async(session) for _ in range(5)])
        assert isinstance(org_customers_data, List)
        sorted_org_customers = await org_customer_manager.get_sorted_list(
            sort_by="org_customer_id", order="desc")
        assert [org_customer.org_customer_id for org_customer in sorted_org_customers] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await org_customer_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        sorted_org_customers = await org_customer_manager.get_sorted_list(sort_by="org_customer_id")
        assert len(sorted_org_customers) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a org_customer instance.
        This test performs the following steps:
        1. Creates a org_customer instance using the OrgCustomerFactory.
        2. Retrieves the org_customer from the database to ensure
            it was added correctly.
        3. Updates the org_customer's code and verifies the update.
        4. Refreshes the original org_customer instance and checks if
            it reflects the updated code.
        Args:
            org_customer_manager (OrgCustomerManager): The manager responsible
                for org_customer operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a org_customer
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        # Retrieve the org_customer from the database
        result = await session.execute(
            select(OrgCustomer).filter(
                OrgCustomer._org_customer_id == org_customer1.org_customer_id)  # type: ignore
        )  # type: ignore
        org_customer2 = result.scalars().first()
        # Verify that the retrieved org_customer matches the added org_customer
        assert org_customer1.code == org_customer2.code
        # Update the org_customer's code
        updated_code1 = uuid.uuid4()
        org_customer1.code = updated_code1
        updated_org_customer1 = await org_customer_manager.update(org_customer1)
        # Verify that the updated org_customer is of type OrgCustomer
        # and has the updated code
        assert isinstance(updated_org_customer1, OrgCustomer)
        assert updated_org_customer1.code == updated_code1
        # Refresh the original org_customer instance
        refreshed_org_customer2 = await org_customer_manager.refresh(org_customer2)
        # Verify that the refreshed org_customer reflects the updated code
        assert refreshed_org_customer2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        org_customer = OrgCustomer(org_customer_id=999)
        with pytest.raises(Exception):
            await org_customer_manager.refresh(org_customer)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a org_customer
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        # Check if the org_customer exists using the manager function
        assert await org_customer_manager.exists(org_customer1.org_customer_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_org_customer(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a org_customer
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        org_customer2 = await org_customer_manager.get_by_id(org_customer_id=org_customer1.org_customer_id)
        assert org_customer_manager.is_equal(org_customer1, org_customer2) is True
        org_customer1_dict = org_customer_manager.to_dict(org_customer1)
        org_customer3 = org_customer_manager.from_dict(org_customer1_dict)
        assert org_customer_manager.is_equal(org_customer1, org_customer3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_org_customer(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        assert await org_customer_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.exists(invalid_id)
        await session.rollback()
# endset
    # CustomerID
    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a org_customer with a specific customer_id
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        # Fetch the org_customer using the manager function
        fetched_org_customers = await org_customer_manager.get_by_customer_id(
            org_customer1.customer_id)
        assert len(fetched_org_customers) == 1
        assert isinstance(fetched_org_customers[0], OrgCustomer)
        assert fetched_org_customers[0].code == org_customer1.code
        stmt = select(models.Customer).where(
            models.Customer._customer_id == org_customer1.customer_id)
        result = await session.execute(stmt)
        customer = result.scalars().first()
        assert fetched_org_customers[0].customer_code_peek == customer.code
    @pytest.mark.asyncio
    async def test_get_by_customer_id_nonexistent(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        fetched_org_customers = (
            await org_customer_manager.get_by_customer_id(non_existent_id))
        assert len(fetched_org_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_customer_id_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.get_by_customer_id(invalid_id)
        await session.rollback()
    # email,
    # OrganizationID
    @pytest.mark.asyncio
    async def test_get_by_organization_id_existing(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a org_customer with a specific organization_id
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        # Fetch the org_customer using the manager function
        fetched_org_customers = await org_customer_manager.get_by_organization_id(org_customer1.organization_id)
        assert len(fetched_org_customers) == 1
        assert isinstance(fetched_org_customers[0], OrgCustomer)
        assert fetched_org_customers[0].code == org_customer1.code
    @pytest.mark.asyncio
    async def test_get_by_organization_id_nonexistent(
        self,
        org_customer_manager: OrgCustomerManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        fetched_org_customers = await org_customer_manager.get_by_organization_id(non_existent_id)
        assert len(fetched_org_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_organization_id_invalid_type(
        self,
        org_customer_manager: OrgCustomerManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.get_by_organization_id(invalid_id)
        await session.rollback()
# endset
