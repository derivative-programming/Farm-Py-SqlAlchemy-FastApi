import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio
import time
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, OrgCustomer
from models.factory import OrgCustomerFactory
from managers.org_customer import OrgCustomerManager
from models.serialization_schema.org_customer import OrgCustomerSchema
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestOrgCustomerManager:
    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    @pytest.fixture(scope="function")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=True)
        yield engine
        engine.sync_engine.dispose()
    @pytest_asyncio.fixture(scope="function")
    async def session(self,engine) -> AsyncSession:
        @event.listens_for(engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        async with engine.begin() as connection:
            await connection.begin_nested()
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
            TestingSessionLocal = sessionmaker(
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with TestingSessionLocal(bind=connection) as session:
                @event.listens_for(
                    session.sync_session, "after_transaction_end"
                )
                def end_savepoint(session, transaction):
                    if connection.closed:
                        return
                    if not connection.in_nested_transaction():
                        connection.sync_connection.begin_nested()
                yield session
                await session.flush()
                await session.rollback()
    @pytest_asyncio.fixture(scope="function")
    async def org_customer_manager(self, session:AsyncSession):
        return OrgCustomerManager(session)
    @pytest.mark.asyncio
    async def test_build(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Define some mock data for our org_customer
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        org_customer = await org_customer_manager.build(**mock_data)
        # Assert that the returned object is an instance of OrgCustomer
        assert isinstance(org_customer, OrgCustomer)
        # Assert that the attributes of the org_customer match our mock data
        assert org_customer.code == mock_data["code"]
        # Optionally, if the build method has some default values or computations:
        # assert org_customer.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await org_customer_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_org_customer_to_database(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        test_org_customer = await OrgCustomerFactory.build_async(session)
        assert test_org_customer.org_customer_id is None
        # Add the org_customer using the manager's add method
        added_org_customer = await org_customer_manager.add(org_customer=test_org_customer)
        assert isinstance(added_org_customer, OrgCustomer)
        assert added_org_customer.org_customer_id > 0
        # Fetch the org_customer from the database directly
        result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == added_org_customer.org_customer_id))
        fetched_org_customer = result.scalars().first()
        # Assert that the fetched org_customer is not None and matches the added org_customer
        assert fetched_org_customer is not None
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.org_customer_id == added_org_customer.org_customer_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_org_customer_object(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Create a test org_customer using the OrgCustomerFactory without persisting it to the database
        test_org_customer = await OrgCustomerFactory.build_async(session)
        assert test_org_customer.org_customer_id is None
        test_org_customer.code = generate_uuid()
        # Add the org_customer using the manager's add method
        added_org_customer = await org_customer_manager.add(org_customer=test_org_customer)
        assert isinstance(added_org_customer, OrgCustomer)
        assert added_org_customer.org_customer_id > 0
        # Assert that the returned org_customer matches the test org_customer
        assert added_org_customer.org_customer_id == test_org_customer.org_customer_id
        assert added_org_customer.code == test_org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_id(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        test_org_customer = await OrgCustomerFactory.create_async(session)
        org_customer = await org_customer_manager.get_by_id(test_org_customer.org_customer_id)
        assert isinstance(org_customer, OrgCustomer)
        assert test_org_customer.org_customer_id == org_customer.org_customer_id
        assert test_org_customer.code == org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, org_customer_manager:OrgCustomerManager, session: AsyncSession):
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_org_customer = await org_customer_manager.get_by_id(non_existent_id)
        assert retrieved_org_customer is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_org_customer(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        test_org_customer = await OrgCustomerFactory.create_async(session)
        org_customer = await org_customer_manager.get_by_code(test_org_customer.code)
        assert isinstance(org_customer, OrgCustomer)
        assert test_org_customer.org_customer_id == org_customer.org_customer_id
        assert test_org_customer.code == org_customer.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Generate a random UUID that doesn't correspond to any OrgCustomer in the database
        random_code = generate_uuid()
        org_customer = await org_customer_manager.get_by_code(random_code)
        assert org_customer is None
    @pytest.mark.asyncio
    async def test_update(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        test_org_customer = await OrgCustomerFactory.create_async(session)
        test_org_customer.code = generate_uuid()
        updated_org_customer = await org_customer_manager.update(org_customer=test_org_customer)
        assert isinstance(updated_org_customer, OrgCustomer)
        assert updated_org_customer.org_customer_id == test_org_customer.org_customer_id
        assert updated_org_customer.code == test_org_customer.code
        result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == test_org_customer.org_customer_id))
        fetched_org_customer = result.scalars().first()
        assert updated_org_customer.org_customer_id == fetched_org_customer.org_customer_id
        assert updated_org_customer.code == fetched_org_customer.code
        assert test_org_customer.org_customer_id == fetched_org_customer.org_customer_id
        assert test_org_customer.code == fetched_org_customer.code
    @pytest.mark.asyncio
    async def test_update_via_dict(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        test_org_customer = await OrgCustomerFactory.create_async(session)
        new_code = generate_uuid()
        updated_org_customer = await org_customer_manager.update(org_customer=test_org_customer,code=new_code)
        assert isinstance(updated_org_customer, OrgCustomer)
        assert updated_org_customer.org_customer_id == test_org_customer.org_customer_id
        assert updated_org_customer.code == new_code
        result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == test_org_customer.org_customer_id))
        fetched_org_customer = result.scalars().first()
        assert updated_org_customer.org_customer_id == fetched_org_customer.org_customer_id
        assert updated_org_customer.code == fetched_org_customer.code
        assert test_org_customer.org_customer_id == fetched_org_customer.org_customer_id
        assert new_code == fetched_org_customer.code
    @pytest.mark.asyncio
    async def test_update_invalid_org_customer(self, org_customer_manager:OrgCustomerManager):
        # None org_customer
        org_customer = None
        new_code = generate_uuid()
        updated_org_customer = await org_customer_manager.update(org_customer, code=new_code)
        # Assertions
        assert updated_org_customer is None
    #todo fix test
    # @pytest.mark.asyncio
    # async def test_update_with_nonexistent_attribute(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
    #     test_org_customer = await OrgCustomerFactory.create_async(session)
    #     new_code = generate_uuid()
    #     # This should raise an AttributeError since 'color' is not an attribute of OrgCustomer
    #     with pytest.raises(Exception):
    #         updated_org_customer = await org_customer_manager.update(org_customer=test_org_customer,xxx=new_code)
    #     await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer_data = await OrgCustomerFactory.create_async(session)
        result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == org_customer_data.org_customer_id))
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.org_customer_id == org_customer_data.org_customer_id
        deleted_org_customer = await org_customer_manager.delete(org_customer_id=org_customer_data.org_customer_id)
        result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == org_customer_data.org_customer_id))
        fetched_org_customer = result.scalars().first()
        assert fetched_org_customer is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        with pytest.raises(Exception):
            await org_customer_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        with pytest.raises(Exception):
            await org_customer_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customers = await org_customer_manager.get_list()
        assert len(org_customers) == 0
        org_customers_data = [await OrgCustomerFactory.create_async(session) for _ in range(5)]
        org_customers = await org_customer_manager.get_list()
        assert len(org_customers) == 5
        assert all(isinstance(org_customer, OrgCustomer) for org_customer in org_customers)
    @pytest.mark.asyncio
    async def test_to_json(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer = await OrgCustomerFactory.build_async(session)
        json_data = org_customer_manager.to_json(org_customer)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer = await OrgCustomerFactory.build_async(session)
        dict_data = org_customer_manager.to_dict(org_customer)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer = await OrgCustomerFactory.create_async(session)
        json_data = org_customer_manager.to_json(org_customer)
        deserialized_org_customer = org_customer_manager.from_json(json_data)
        assert isinstance(deserialized_org_customer, OrgCustomer)
        assert deserialized_org_customer.code == org_customer.code
    @pytest.mark.asyncio
    async def test_from_dict(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer = await OrgCustomerFactory.create_async(session)
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        deserialized_org_customer = org_customer_manager.from_dict(org_customer_data)
        assert isinstance(deserialized_org_customer, OrgCustomer)
        assert deserialized_org_customer.code == org_customer.code
    @pytest.mark.asyncio
    async def test_add_bulk(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customers_data = [await OrgCustomerFactory.build_async(session) for _ in range(5)]
        org_customers = await org_customer_manager.add_bulk(org_customers_data)
        assert len(org_customers) == 5
        for updated_org_customer in org_customers:
            result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == updated_org_customer.org_customer_id))
            fetched_org_customer = result.scalars().first()
            assert isinstance(fetched_org_customer, OrgCustomer)
            assert fetched_org_customer.org_customer_id == updated_org_customer.org_customer_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Mocking org_customer instances
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        org_customer2 = await OrgCustomerFactory.create_async(session=session)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        # Update org_customers
        updates = [{"org_customer_id": 1, "code": code_updated1}, {"org_customer_id": 2, "code": code_updated2}]
        updated_org_customers = await org_customer_manager.update_bulk(updates)
        # Assertions
        assert len(updated_org_customers) == 2
        assert updated_org_customers[0].code == code_updated1
        assert updated_org_customers[1].code == code_updated2
        result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == 1))
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.code == code_updated1
        result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == 2))
        fetched_org_customer = result.scalars().first()
        assert isinstance(fetched_org_customer, OrgCustomer)
        assert fetched_org_customer.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_org_customer_id(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # No org_customers to update since org_customer_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_org_customers = await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_org_customer_not_found(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Update org_customers
        updates = [{"org_customer_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_org_customers = await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        updates = [{"org_customer_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_org_customers = await org_customer_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        org_customer2 = await OrgCustomerFactory.create_async(session=session)
        # Delete org_customers
        org_customer_ids = [1, 2]
        result = await org_customer_manager.delete_bulk(org_customer_ids)
        assert result is True
        for org_customer_id in org_customer_ids:
            execute_result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == org_customer_id))
            fetched_org_customer = execute_result.scalars().first()
            assert fetched_org_customer is None
    @pytest.mark.asyncio
    async def test_delete_bulk_some_org_customers_not_found(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        # Delete org_customers
        org_customer_ids = [1, 2]
        with pytest.raises(Exception):
           result = await org_customer_manager.delete_bulk(org_customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Delete org_customers with an empty list
        org_customer_ids = []
        result = await org_customer_manager.delete_bulk(org_customer_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer_ids = ["1", 2]
        with pytest.raises(Exception):
           result = await org_customer_manager.delete_bulk(org_customer_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customers_data = [await OrgCustomerFactory.create_async(session) for _ in range(5)]
        count = await org_customer_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        count = await org_customer_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Add org_customers
        org_customers_data = [await OrgCustomerFactory.create_async(session) for _ in range(5)]
        sorted_org_customers = await org_customer_manager.get_sorted_list(sort_by="org_customer_id")
        assert [org_customer.org_customer_id for org_customer in sorted_org_customers] == [(i + 1) for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Add org_customers
        org_customers_data = [await OrgCustomerFactory.create_async(session) for _ in range(5)]
        sorted_org_customers = await org_customer_manager.get_sorted_list(sort_by="org_customer_id", order="desc")
        assert [org_customer.org_customer_id for org_customer in sorted_org_customers] == [(i + 1) for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        with pytest.raises(AttributeError):
            await org_customer_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        sorted_org_customers = await org_customer_manager.get_sorted_list(sort_by="org_customer_id")
        assert len(sorted_org_customers) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Add a org_customer
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        result = await session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == org_customer1.org_customer_id))
        org_customer2 = result.scalars().first()
        assert org_customer1.code == org_customer2.code
        updated_code1 = generate_uuid()
        org_customer1.code = updated_code1
        updated_org_customer1 = await org_customer_manager.update(org_customer1)
        assert updated_org_customer1.code == updated_code1
        refreshed_org_customer2 = await org_customer_manager.refresh(org_customer2)
        assert refreshed_org_customer2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_org_customer(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        org_customer = OrgCustomer(org_customer_id=999)
        with pytest.raises(Exception):
            await org_customer_manager.refresh(org_customer)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_org_customer(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Add a org_customer
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        # Check if the org_customer exists using the manager function
        assert await org_customer_manager.exists(org_customer1.org_customer_id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_org_customer(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        non_existent_id = 999
        assert await org_customer_manager.exists(non_existent_id) == False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.exists(invalid_id)
        await session.rollback()
#endet
    #CustomerID
    @pytest.mark.asyncio
    async def test_get_by_customer_id_existing(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Add a org_customer with a specific customer_id
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        # Fetch the org_customer using the manager function
        fetched_org_customers = await org_customer_manager.get_by_customer_id(org_customer1.customer_id)
        assert len(fetched_org_customers) == 1
        assert fetched_org_customers[0].code == org_customer1.code
    @pytest.mark.asyncio
    async def test_get_by_customer_id_nonexistent(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        non_existent_id = 999
        fetched_org_customers = await org_customer_manager.get_by_customer_id(non_existent_id)
        assert len(fetched_org_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_customer_id_invalid_type(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.get_by_customer_id(invalid_id)
        await session.rollback()
    #email,
    #OrganizationID
    @pytest.mark.asyncio
    async def test_get_by_organization_id_existing(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        # Add a org_customer with a specific organization_id
        org_customer1 = await OrgCustomerFactory.create_async(session=session)
        # Fetch the org_customer using the manager function
        fetched_org_customers = await org_customer_manager.get_by_organization_id(org_customer1.organization_id)
        assert len(fetched_org_customers) == 1
        assert fetched_org_customers[0].code == org_customer1.code
    @pytest.mark.asyncio
    async def test_get_by_organization_id_nonexistent(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        non_existent_id = 999
        fetched_org_customers = await org_customer_manager.get_by_organization_id(non_existent_id)
        assert len(fetched_org_customers) == 0
    @pytest.mark.asyncio
    async def test_get_by_organization_id_invalid_type(self, org_customer_manager:OrgCustomerManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await org_customer_manager.get_by_organization_id(invalid_id)
        await session.rollback()
#endet
##todo test for is_equal
