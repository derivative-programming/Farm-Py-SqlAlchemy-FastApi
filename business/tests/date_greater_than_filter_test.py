# business/tests/date_greater_than_filter_test.py
"""
    #TODO add comment
"""
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
from managers.date_greater_than_filter import DateGreaterThanFilterManager
from business.date_greater_than_filter import DateGreaterThanFilterBusObj
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
DB_DIALECT = "sqlite"  # noqa: F811
class TestDateGreaterThanFilterBusObj:
    """
        #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_manager(self, session: AsyncSession):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return DateGreaterThanFilterManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_bus_obj(self, session):
        """
            #TODO add comment
        """
        session_context = SessionContext(dict(), session)
        return DateGreaterThanFilterBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_date_greater_than_filter(self, session):
        """
            #TODO add comment
        """
        # Use the DateGreaterThanFilterFactory to create a new date_greater_than_filter instance
        # Assuming DateGreaterThanFilterFactory.create() is an async function
        return await DateGreaterThanFilterFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        # Test creating a new date_greater_than_filter
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id is None
        # assert isinstance(date_greater_than_filter_bus_obj.date_greater_than_filter_id, int)
        if DB_DIALECT == 'postgresql':
            assert isinstance(date_greater_than_filter_bus_obj.code, UUID)
        elif DB_DIALECT == 'mssql':
            assert isinstance(date_greater_than_filter_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(date_greater_than_filter_bus_obj.code, str)
        assert isinstance(date_greater_than_filter_bus_obj.last_change_code, int)
        assert date_greater_than_filter_bus_obj.insert_user_id is None
        assert date_greater_than_filter_bus_obj.last_update_user_id is None
        assert isinstance(date_greater_than_filter_bus_obj.day_count, int)
        assert date_greater_than_filter_bus_obj.description == "" or isinstance(
            date_greater_than_filter_bus_obj.description, str)
        assert isinstance(date_greater_than_filter_bus_obj.display_order, int)
        assert isinstance(date_greater_than_filter_bus_obj.is_active, bool)
        assert date_greater_than_filter_bus_obj.lookup_enum_name == "" or isinstance(
            date_greater_than_filter_bus_obj.lookup_enum_name, str)
        assert date_greater_than_filter_bus_obj.name == "" or isinstance(
            date_greater_than_filter_bus_obj.name, str)
        assert isinstance(date_greater_than_filter_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_obj(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_obj_instance=new_date_greater_than_filter)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_id(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_id=new_date_greater_than_filter.date_greater_than_filter_id)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_code(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        await date_greater_than_filter_bus_obj.load(code=new_date_greater_than_filter.code)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_json(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter_json = date_greater_than_filter_manager.to_json(new_date_greater_than_filter)
        await date_greater_than_filter_bus_obj.load(json_data=date_greater_than_filter_json)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_dict(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        logger.info("test_load_with_date_greater_than_filter_dict 1")
        date_greater_than_filter_dict = date_greater_than_filter_manager.to_dict(new_date_greater_than_filter)
        logger.info(date_greater_than_filter_dict)
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_dict=date_greater_than_filter_dict)
        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter,
            new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        # Test retrieving a nonexistent date_greater_than_filter raises an exception
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_id=-1)
        assert date_greater_than_filter_bus_obj.is_valid() is False  # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        # Test updating a date_greater_than_filter's data
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(new_date_greater_than_filter.date_greater_than_filter_id)
        new_code = generate_uuid()
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_obj_instance=new_date_greater_than_filter)
        date_greater_than_filter_bus_obj.code = new_code
        await date_greater_than_filter_bus_obj.save()
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(new_date_greater_than_filter.date_greater_than_filter_id)
        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter,
            new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_delete_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
            #TODO add comment
        """
        assert new_date_greater_than_filter.date_greater_than_filter_id is not None
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id is None
        await date_greater_than_filter_bus_obj.load(date_greater_than_filter_id=new_date_greater_than_filter.date_greater_than_filter_id)
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id is not None
        await date_greater_than_filter_bus_obj.delete()
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(new_date_greater_than_filter.date_greater_than_filter_id)
        assert new_date_greater_than_filter is None

