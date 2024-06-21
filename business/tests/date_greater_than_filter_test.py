# business/tests/date_greater_than_filter_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the DateGreaterThanFilterBusObj class.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
from managers.date_greater_than_filter import DateGreaterThanFilterManager
from business.date_greater_than_filter import DateGreaterThanFilterBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401

logger = get_logger(__name__)
class TestDateGreaterThanFilterBusObj:
    """
    Unit tests for the DateGreaterThanFilterBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the DateGreaterThanFilterManager class.
        """
        session_context = SessionContext(dict(), session)
        return DateGreaterThanFilterManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_bus_obj(self, session):
        """
        Fixture that returns an instance of the DateGreaterThanFilterBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return DateGreaterThanFilterBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_date_greater_than_filter(self, session):
        """
        Fixture that returns a new instance of
        the DateGreaterThanFilter class.
        """
        return await DateGreaterThanFilterFactory.create_async(
            session)
    @pytest.mark.asyncio
    async def test_create_date_greater_than_filter(
        self,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj
    ):
        """
        Test case for creating a new date_greater_than_filter.
        """
        # Test creating a new date_greater_than_filter
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id == 0
        # assert isinstance(date_greater_than_filter_bus_obj.date_greater_than_filter_id, int)
        assert isinstance(
            date_greater_than_filter_bus_obj.code, uuid.UUID)
        assert isinstance(
            date_greater_than_filter_bus_obj.last_change_code, int)
        assert date_greater_than_filter_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert date_greater_than_filter_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(date_greater_than_filter_bus_obj.day_count, int)
        assert isinstance(date_greater_than_filter_bus_obj.description, str)
        assert isinstance(date_greater_than_filter_bus_obj.display_order, int)
        assert isinstance(date_greater_than_filter_bus_obj.is_active, bool)
        assert isinstance(date_greater_than_filter_bus_obj.lookup_enum_name, str)
        assert isinstance(date_greater_than_filter_bus_obj.name, str)
        assert isinstance(date_greater_than_filter_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_obj(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter object instance.
        """
        await date_greater_than_filter_bus_obj.load_from_obj_instance(
            new_date_greater_than_filter)
        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_id(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter ID.
        """
        new_date_greater_than_filter_date_greater_than_filter_id = new_date_greater_than_filter.date_greater_than_filter_id
        await date_greater_than_filter_bus_obj.load_from_id(
            new_date_greater_than_filter_date_greater_than_filter_id)
        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_code(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter code.
        """
        await date_greater_than_filter_bus_obj.load_from_code(
            new_date_greater_than_filter.code)
        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_json(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter JSON.
        """
        date_greater_than_filter_json = date_greater_than_filter_manager.to_json(new_date_greater_than_filter)
        await date_greater_than_filter_bus_obj.load_from_json(
            date_greater_than_filter_json)
        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_dict(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter dictionary.
        """
        logger.info("test_load_with_date_greater_than_filter_dict 1")
        date_greater_than_filter_dict = date_greater_than_filter_manager.to_dict(new_date_greater_than_filter)
        logger.info(date_greater_than_filter_dict)
        await date_greater_than_filter_bus_obj.load_from_dict(
            date_greater_than_filter_dict)
        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter,
            new_date_greater_than_filter) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_date_greater_than_filter(
        self,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj
    ):
        """
        Test case for retrieving a nonexistent date_greater_than_filter.
        """
        # Test retrieving a nonexistent
        # date_greater_than_filter raises an exception
        await date_greater_than_filter_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert date_greater_than_filter_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for updating a date_greater_than_filter's data.
        """
        # Test updating a date_greater_than_filter's data
        new_date_greater_than_filter_date_greater_than_filter_id_value = new_date_greater_than_filter.date_greater_than_filter_id
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(
            new_date_greater_than_filter_date_greater_than_filter_id_value)
        assert isinstance(new_date_greater_than_filter, DateGreaterThanFilter)
        new_code = uuid.uuid4()
        await date_greater_than_filter_bus_obj.load_from_obj_instance(
            new_date_greater_than_filter)
        date_greater_than_filter_bus_obj.code = new_code
        await date_greater_than_filter_bus_obj.save()
        new_date_greater_than_filter_date_greater_than_filter_id_value = new_date_greater_than_filter.date_greater_than_filter_id
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(
            new_date_greater_than_filter_date_greater_than_filter_id_value)
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
        Test case for deleting a date_greater_than_filter.
        """
        assert new_date_greater_than_filter.date_greater_than_filter_id is not None
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id == 0
        new_date_greater_than_filter_date_greater_than_filter_id_value = new_date_greater_than_filter.date_greater_than_filter_id
        await date_greater_than_filter_bus_obj.load_from_id(
            new_date_greater_than_filter_date_greater_than_filter_id_value)
        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id is not None
        await date_greater_than_filter_bus_obj.delete()
        new_date_greater_than_filter_date_greater_than_filter_id_value = new_date_greater_than_filter.date_greater_than_filter_id
        new_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(
            new_date_greater_than_filter_date_greater_than_filter_id_value)
        assert new_date_greater_than_filter is None

