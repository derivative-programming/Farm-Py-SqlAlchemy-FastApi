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
from models import Base, DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
from managers.date_greater_than_filter import DateGreaterThanFilterManager
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
class TestDateGreaterThanFilterManager:
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
    async def date_greater_than_filter_manager(self, session:AsyncSession):
        return DateGreaterThanFilterManager(session)
    @pytest.mark.asyncio
    async def test_build(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Define some mock data for our date_greater_than_filter
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        date_greater_than_filter = await date_greater_than_filter_manager.build(**mock_data)
        # Assert that the returned object is an instance of DateGreaterThanFilter
        assert isinstance(date_greater_than_filter, DateGreaterThanFilter)
        # Assert that the attributes of the date_greater_than_filter match our mock data
        assert date_greater_than_filter.code == mock_data["code"]
        # Optionally, if the build method has some default values or computations:
        # assert date_greater_than_filter.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_date_greater_than_filter_to_database(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session)
        assert test_date_greater_than_filter.date_greater_than_filter_id is None
        # Add the date_greater_than_filter using the manager's add method
        added_date_greater_than_filter = await date_greater_than_filter_manager.add(date_greater_than_filter=test_date_greater_than_filter)
        assert isinstance(added_date_greater_than_filter, DateGreaterThanFilter)
        assert added_date_greater_than_filter.date_greater_than_filter_id > 0
        # Fetch the date_greater_than_filter from the database directly
        result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == added_date_greater_than_filter.date_greater_than_filter_id))
        fetched_date_greater_than_filter = result.scalars().first()
        # Assert that the fetched date_greater_than_filter is not None and matches the added date_greater_than_filter
        assert fetched_date_greater_than_filter is not None
        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
        assert fetched_date_greater_than_filter.date_greater_than_filter_id == added_date_greater_than_filter.date_greater_than_filter_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_date_greater_than_filter_object(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Create a test date_greater_than_filter using the DateGreaterThanFilterFactory without persisting it to the database
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session)
        assert test_date_greater_than_filter.date_greater_than_filter_id is None
        test_date_greater_than_filter.code = generate_uuid()
        # Add the date_greater_than_filter using the manager's add method
        added_date_greater_than_filter = await date_greater_than_filter_manager.add(date_greater_than_filter=test_date_greater_than_filter)
        assert isinstance(added_date_greater_than_filter, DateGreaterThanFilter)
        assert added_date_greater_than_filter.date_greater_than_filter_id > 0
        # Assert that the returned date_greater_than_filter matches the test date_greater_than_filter
        assert added_date_greater_than_filter.date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id
        assert added_date_greater_than_filter.code == test_date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_get_by_id(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(test_date_greater_than_filter.date_greater_than_filter_id)
        assert isinstance(date_greater_than_filter, DateGreaterThanFilter)
        assert test_date_greater_than_filter.date_greater_than_filter_id == date_greater_than_filter.date_greater_than_filter_id
        assert test_date_greater_than_filter.code == date_greater_than_filter.code
    async def test_get_by_id_not_found(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session: AsyncSession):
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(non_existent_id)
        assert retrieved_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_date_greater_than_filter(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        date_greater_than_filter = await date_greater_than_filter_manager.get_by_code(test_date_greater_than_filter.code)
        assert isinstance(date_greater_than_filter, DateGreaterThanFilter)
        assert test_date_greater_than_filter.date_greater_than_filter_id == date_greater_than_filter.date_greater_than_filter_id
        assert test_date_greater_than_filter.code == date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Generate a random UUID that doesn't correspond to any DateGreaterThanFilter in the database
        random_code = generate_uuid()
        date_greater_than_filter = await date_greater_than_filter_manager.get_by_code(random_code)
        assert date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_update(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        test_date_greater_than_filter.code = generate_uuid()
        updated_date_greater_than_filter = await date_greater_than_filter_manager.update(date_greater_than_filter=test_date_greater_than_filter)
        assert isinstance(updated_date_greater_than_filter, DateGreaterThanFilter)
        assert updated_date_greater_than_filter.date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id
        assert updated_date_greater_than_filter.code == test_date_greater_than_filter.code
        result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id))
        fetched_date_greater_than_filter = result.scalars().first()
        assert updated_date_greater_than_filter.date_greater_than_filter_id == fetched_date_greater_than_filter.date_greater_than_filter_id
        assert updated_date_greater_than_filter.code == fetched_date_greater_than_filter.code
        assert test_date_greater_than_filter.date_greater_than_filter_id == fetched_date_greater_than_filter.date_greater_than_filter_id
        assert test_date_greater_than_filter.code == fetched_date_greater_than_filter.code
    async def test_update_via_dict(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        new_code = generate_uuid()
        updated_date_greater_than_filter = await date_greater_than_filter_manager.update(date_greater_than_filter=test_date_greater_than_filter,code=new_code)
        assert isinstance(updated_date_greater_than_filter, DateGreaterThanFilter)
        assert updated_date_greater_than_filter.date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id
        assert updated_date_greater_than_filter.code == new_code
        result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id))
        fetched_date_greater_than_filter = result.scalars().first()
        assert updated_date_greater_than_filter.date_greater_than_filter_id == fetched_date_greater_than_filter.date_greater_than_filter_id
        assert updated_date_greater_than_filter.code == fetched_date_greater_than_filter.code
        assert test_date_greater_than_filter.date_greater_than_filter_id == fetched_date_greater_than_filter.date_greater_than_filter_id
        assert new_code == fetched_date_greater_than_filter.code
    async def test_update_invalid_date_greater_than_filter(self):
        # None date_greater_than_filter
        date_greater_than_filter = None
        new_code = generate_uuid()
        updated_date_greater_than_filter = await self.manager.update(date_greater_than_filter, code=new_code)
        # Assertions
        assert updated_date_greater_than_filter is None
    async def test_update_with_nonexistent_attribute(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        new_code = generate_uuid()
        # This should raise an AttributeError since 'color' is not an attribute of DateGreaterThanFilter
        with pytest.raises(AttributeError):
            updated_date_greater_than_filter = await date_greater_than_filter_manager.update(date_greater_than_filter=test_date_greater_than_filter,xxx=new_code)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filter_data = await DateGreaterThanFilterFactory.create_async(session)
        result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == date_greater_than_filter_data.date_greater_than_filter_id))
        fetched_date_greater_than_filter = result.scalars().first()
        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
        assert fetched_date_greater_than_filter.date_greater_than_filter_id == date_greater_than_filter_data.date_greater_than_filter_id
        deleted_date_greater_than_filter = await date_greater_than_filter_manager.delete(date_greater_than_filter_id=date_greater_than_filter_data.date_greater_than_filter_id)
        result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == date_greater_than_filter_data.date_greater_than_filter_id))
        fetched_date_greater_than_filter = result.scalars().first()
        assert fetched_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filters = await date_greater_than_filter_manager.get_list()
        assert len(date_greater_than_filters) == 0
        date_greater_than_filters_data = [await DateGreaterThanFilterFactory.create_async(session) for _ in range(5)]
        date_greater_than_filters = await date_greater_than_filter_manager.get_list()
        assert len(date_greater_than_filters) == 5
        assert all(isinstance(date_greater_than_filter, DateGreaterThanFilter) for date_greater_than_filter in date_greater_than_filters)
    @pytest.mark.asyncio
    async def test_to_json(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session)
        json_data = date_greater_than_filter_manager.to_json(date_greater_than_filter)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session)
        dict_data = date_greater_than_filter_manager.to_dict(date_greater_than_filter)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        json_data = date_greater_than_filter_manager.to_json(date_greater_than_filter)
        deserialized_date_greater_than_filter = date_greater_than_filter_manager.from_json(json_data)
        assert isinstance(deserialized_date_greater_than_filter, DateGreaterThanFilter)
        assert deserialized_date_greater_than_filter.code == date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_add_bulk(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filters_data = [await DateGreaterThanFilterFactory.build_async(session) for _ in range(5)]
        date_greater_than_filters = await date_greater_than_filter_manager.add_bulk(date_greater_than_filters_data)
        assert len(date_greater_than_filters) == 5
        for updated_date_greater_than_filter in date_greater_than_filters:
            result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == updated_date_greater_than_filter.date_greater_than_filter_id))
            fetched_date_greater_than_filter = result.scalars().first()
            assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
            assert fetched_date_greater_than_filter.date_greater_than_filter_id == updated_date_greater_than_filter.date_greater_than_filter_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Mocking date_greater_than_filter instances
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter2 = await DateGreaterThanFilterFactory.create_async(session=session)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        # Update date_greater_than_filters
        updates = [{"date_greater_than_filter_id": 1, "code": code_updated1}, {"date_greater_than_filter_id": 2, "code": code_updated2}]
        updated_date_greater_than_filters = await date_greater_than_filter_manager.update_bulk(updates)
        # Assertions
        assert len(updated_date_greater_than_filters) == 2
        assert updated_date_greater_than_filters[0].code == code_updated1
        assert updated_date_greater_than_filters[1].code == code_updated2
        result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == 1))
        fetched_date_greater_than_filter = result.scalars().first()
        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
        assert fetched_date_greater_than_filter.code == code_updated1
        result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == 2))
        fetched_date_greater_than_filter = result.scalars().first()
        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
        assert fetched_date_greater_than_filter.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_date_greater_than_filter_id(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # No date_greater_than_filters to update since date_greater_than_filter_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_date_greater_than_filters = await date_greater_than_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_date_greater_than_filter_not_found(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Update date_greater_than_filters
        updates = [{"date_greater_than_filter_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_date_greater_than_filters = await date_greater_than_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        updates = [{"date_greater_than_filter_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_date_greater_than_filters = await date_greater_than_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter2 = await DateGreaterThanFilterFactory.create_async(session=session)
        # Delete date_greater_than_filters
        date_greater_than_filter_ids = [1, 2]
        result = await date_greater_than_filter_manager.delete_bulk(date_greater_than_filter_ids)
        assert result is True
        for date_greater_than_filter_id in date_greater_than_filter_ids:
            execute_result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == date_greater_than_filter_id))
            fetched_date_greater_than_filter = execute_result.scalars().first()
            assert fetched_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_delete_bulk_some_date_greater_than_filters_not_found(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        # Delete date_greater_than_filters
        date_greater_than_filter_ids = [1, 2]
        with pytest.raises(Exception):
           result = await date_greater_than_filter_manager.delete_bulk(date_greater_than_filter_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Delete date_greater_than_filters with an empty list
        date_greater_than_filter_ids = []
        result = await date_greater_than_filter_manager.delete_bulk(date_greater_than_filter_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filter_ids = ["1", 2]
        with pytest.raises(Exception):
           result = await date_greater_than_filter_manager.delete_bulk(date_greater_than_filter_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filters_data = [await DateGreaterThanFilterFactory.create_async(session) for _ in range(5)]
        count = await date_greater_than_filter_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        count = await date_greater_than_filter_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Add date_greater_than_filters
        date_greater_than_filters_data = [await DateGreaterThanFilterFactory.create_async(session) for _ in range(5)]
        sorted_date_greater_than_filters = await date_greater_than_filter_manager.get_sorted_list(sort_by="date_greater_than_filter_id")
        assert [date_greater_than_filter.date_greater_than_filter_id for date_greater_than_filter in sorted_date_greater_than_filters] == [(i + 1) for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Add date_greater_than_filters
        date_greater_than_filters_data = [await DateGreaterThanFilterFactory.create_async(session) for _ in range(5)]
        sorted_date_greater_than_filters = await date_greater_than_filter_manager.get_sorted_list(sort_by="date_greater_than_filter_id", order="desc")
        assert [date_greater_than_filter.date_greater_than_filter_id for date_greater_than_filter in sorted_date_greater_than_filters] == [(i + 1) for i in reversed(range(5))]
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        with pytest.raises(AttributeError):
            await date_greater_than_filter_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        sorted_date_greater_than_filters = await date_greater_than_filter_manager.get_sorted_list(sort_by="date_greater_than_filter_id")
        assert len(sorted_date_greater_than_filters) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Add a date_greater_than_filter
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        result = await session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == date_greater_than_filter1.date_greater_than_filter_id))
        date_greater_than_filter2 = result.scalars().first()
        assert date_greater_than_filter1.code == date_greater_than_filter2.code
        updated_code1 = generate_uuid()
        date_greater_than_filter1.code = updated_code1
        updated_date_greater_than_filter1 = await date_greater_than_filter_manager.update(date_greater_than_filter1)
        assert updated_date_greater_than_filter1.code == updated_code1
        refreshed_date_greater_than_filter2 = await date_greater_than_filter_manager.refresh(date_greater_than_filter2)
        assert refreshed_date_greater_than_filter2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_date_greater_than_filter(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        date_greater_than_filter = DateGreaterThanFilter(date_greater_than_filter_id=999)
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.refresh(date_greater_than_filter)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_date_greater_than_filter(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Add a date_greater_than_filter
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        # Check if the date_greater_than_filter exists using the manager function
        assert await date_greater_than_filter_manager.exists(date_greater_than_filter1.date_greater_than_filter_id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_date_greater_than_filter(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        non_existent_id = 999
        assert await date_greater_than_filter_manager.exists(non_existent_id) == False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.exists(invalid_id)
        await session.rollback()
#endet
    #dayCount,
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        # Add a date_greater_than_filter with a specific pac_id
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        # Fetch the date_greater_than_filter using the manager function
        fetched_date_greater_than_filters = await date_greater_than_filter_manager.get_by_pac_id(date_greater_than_filter1.pac_id)
        assert len(fetched_date_greater_than_filters) == 1
        assert fetched_date_greater_than_filters[0].code == date_greater_than_filter1.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        non_existent_id = 999
        fetched_date_greater_than_filters = await date_greater_than_filter_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_date_greater_than_filters) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(self, date_greater_than_filter_manager:DateGreaterThanFilterManager, session:AsyncSession):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.get_by_pac_id(invalid_id)
        await session.rollback()
#endet
