# business/tests/tri_state_filter_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the TriStateFilterBusObj class.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import TriStateFilter
from models.factory import TriStateFilterFactory
from managers.tri_state_filter import TriStateFilterManager
from business.tri_state_filter import TriStateFilterBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401

logger = get_logger(__name__)
class TestTriStateFilterBusObj:
    """
    Unit tests for the TriStateFilterBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def tri_state_filter_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the TriStateFilterManager class.
        """
        session_context = SessionContext(dict(), session)
        return TriStateFilterManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def tri_state_filter_bus_obj(self, session):
        """
        Fixture that returns an instance of the TriStateFilterBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return TriStateFilterBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_tri_state_filter(self, session):
        """
        Fixture that returns a new instance of the TriStateFilter class.
        """
        # Use the TriStateFilterFactory to create a new tri_state_filter instance
        # Assuming TriStateFilterFactory.create() is an async function
        return await TriStateFilterFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_tri_state_filter(
        self,
        tri_state_filter_bus_obj: TriStateFilterBusObj
    ):
        """
        Test case for creating a new tri_state_filter.
        """
        # Test creating a new tri_state_filter
        assert tri_state_filter_bus_obj.tri_state_filter_id == 0
        # assert isinstance(tri_state_filter_bus_obj.tri_state_filter_id, int)
        assert isinstance(tri_state_filter_bus_obj.code, uuid.UUID)
        assert isinstance(tri_state_filter_bus_obj.last_change_code, int)
        assert tri_state_filter_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert tri_state_filter_bus_obj.last_update_user_id == uuid.UUID(int=0)
        assert isinstance(tri_state_filter_bus_obj.description, str)
        assert isinstance(tri_state_filter_bus_obj.display_order, int)
        assert isinstance(tri_state_filter_bus_obj.is_active, bool)
        assert isinstance(tri_state_filter_bus_obj.lookup_enum_name, str)
        assert isinstance(tri_state_filter_bus_obj.name, str)
        assert isinstance(tri_state_filter_bus_obj.pac_id, int)
        assert isinstance(tri_state_filter_bus_obj.state_int_value, int)
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_obj(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a tri_state_filter object instance.
        """
        await tri_state_filter_bus_obj.load_from_obj_instance(new_tri_state_filter)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter, new_tri_state_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_id(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a tri_state_filter ID.
        """
        new_tri_state_filter_tri_state_filter_id = new_tri_state_filter.tri_state_filter_id
        await tri_state_filter_bus_obj.load_from_id(new_tri_state_filter_tri_state_filter_id)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter, new_tri_state_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_code(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a tri_state_filter code.
        """
        await tri_state_filter_bus_obj.load_from_code(new_tri_state_filter.code)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter, new_tri_state_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_json(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a tri_state_filter JSON.
        """
        tri_state_filter_json = tri_state_filter_manager.to_json(new_tri_state_filter)
        await tri_state_filter_bus_obj.load_from_json(tri_state_filter_json)
        assert tri_state_filter_manager.is_equal(tri_state_filter_bus_obj.tri_state_filter, new_tri_state_filter) is True
    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_dict(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a tri_state_filter dictionary.
        """
        logger.info("test_load_with_tri_state_filter_dict 1")
        tri_state_filter_dict = tri_state_filter_manager.to_dict(new_tri_state_filter)
        logger.info(tri_state_filter_dict)
        await tri_state_filter_bus_obj.load_from_dict(tri_state_filter_dict)
        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter,
            new_tri_state_filter) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_tri_state_filter(
        self,
        tri_state_filter_bus_obj: TriStateFilterBusObj
    ):
        """
        Test case for retrieving a nonexistent tri_state_filter.
        """
        # Test retrieving a nonexistent tri_state_filter raises an exception
        await tri_state_filter_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert tri_state_filter_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for updating a tri_state_filter's data.
        """
        # Test updating a tri_state_filter's data
        new_tri_state_filter_tri_state_filter_id_value = new_tri_state_filter.tri_state_filter_id
        new_tri_state_filter = await tri_state_filter_manager.get_by_id(new_tri_state_filter_tri_state_filter_id_value)
        assert isinstance(new_tri_state_filter, TriStateFilter)
        new_code = uuid.uuid4()
        await tri_state_filter_bus_obj.load_from_obj_instance(new_tri_state_filter)
        tri_state_filter_bus_obj.code = new_code
        await tri_state_filter_bus_obj.save()
        new_tri_state_filter_tri_state_filter_id_value = new_tri_state_filter.tri_state_filter_id
        new_tri_state_filter = await tri_state_filter_manager.get_by_id(new_tri_state_filter_tri_state_filter_id_value)
        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter,
            new_tri_state_filter) is True
    @pytest.mark.asyncio
    async def test_delete_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for deleting a tri_state_filter.
        """
        assert new_tri_state_filter.tri_state_filter_id is not None
        assert tri_state_filter_bus_obj.tri_state_filter_id == 0
        new_tri_state_filter_tri_state_filter_id_value = new_tri_state_filter.tri_state_filter_id
        await tri_state_filter_bus_obj.load_from_id(new_tri_state_filter_tri_state_filter_id_value)
        assert tri_state_filter_bus_obj.tri_state_filter_id is not None
        await tri_state_filter_bus_obj.delete()
        new_tri_state_filter_tri_state_filter_id_value = new_tri_state_filter.tri_state_filter_id
        new_tri_state_filter = await tri_state_filter_manager.get_by_id(new_tri_state_filter_tri_state_filter_id_value)
        assert new_tri_state_filter is None

