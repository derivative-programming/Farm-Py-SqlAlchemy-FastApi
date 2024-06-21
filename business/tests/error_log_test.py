# business/tests/error_log_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the ErrorLogBusObj class.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio
from helpers.session_context import SessionContext
from models import ErrorLog
from models.factory import ErrorLogFactory
from managers.error_log import ErrorLogManager
from business.error_log import ErrorLogBusObj
from services.logging_config import get_logger
import current_runtime  # noqa: F401

logger = get_logger(__name__)
class TestErrorLogBusObj:
    """
    Unit tests for the ErrorLogBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def error_log_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the ErrorLogManager class.
        """
        session_context = SessionContext(dict(), session)
        return ErrorLogManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def error_log_bus_obj(self, session):
        """
        Fixture that returns an instance of the ErrorLogBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return ErrorLogBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_error_log(self, session):
        """
        Fixture that returns a new instance of
        the ErrorLog class.
        """
        return await ErrorLogFactory.create_async(
            session)
    @pytest.mark.asyncio
    async def test_create_error_log(
        self,
        error_log_bus_obj: ErrorLogBusObj
    ):
        """
        Test case for creating a new error_log.
        """
        # Test creating a new error_log
        assert error_log_bus_obj.error_log_id == 0
        # assert isinstance(error_log_bus_obj.error_log_id, int)
        assert isinstance(
            error_log_bus_obj.code, uuid.UUID)
        assert isinstance(
            error_log_bus_obj.last_change_code, int)
        assert error_log_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert error_log_bus_obj.last_update_user_id == uuid.UUID(int=0)
        # browser_code
        assert isinstance(error_log_bus_obj.browser_code, uuid.UUID)
        # context_code
        assert isinstance(error_log_bus_obj.context_code, uuid.UUID)
        assert isinstance(error_log_bus_obj.created_utc_date_time, datetime)
        assert isinstance(error_log_bus_obj.description, str)
        assert isinstance(error_log_bus_obj.is_client_side_error, bool)
        assert isinstance(error_log_bus_obj.is_resolved, bool)
        assert isinstance(error_log_bus_obj.pac_id, int)
        assert isinstance(error_log_bus_obj.url, str)
    @pytest.mark.asyncio
    async def test_load_with_error_log_obj(
        self,
        error_log_manager: ErrorLogManager,
        error_log_bus_obj: ErrorLogBusObj,
        new_error_log: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log object instance.
        """
        await error_log_bus_obj.load_from_obj_instance(
            new_error_log)
        assert error_log_manager.is_equal(
            error_log_bus_obj.error_log, new_error_log) is True
    @pytest.mark.asyncio
    async def test_load_with_error_log_id(
        self,
        error_log_manager: ErrorLogManager,
        error_log_bus_obj: ErrorLogBusObj,
        new_error_log: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log ID.
        """
        new_error_log_error_log_id = new_error_log.error_log_id
        await error_log_bus_obj.load_from_id(
            new_error_log_error_log_id)
        assert error_log_manager.is_equal(
            error_log_bus_obj.error_log, new_error_log) is True
    @pytest.mark.asyncio
    async def test_load_with_error_log_code(
        self,
        error_log_manager: ErrorLogManager,
        error_log_bus_obj: ErrorLogBusObj,
        new_error_log: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log code.
        """
        await error_log_bus_obj.load_from_code(
            new_error_log.code)
        assert error_log_manager.is_equal(
            error_log_bus_obj.error_log, new_error_log) is True
    @pytest.mark.asyncio
    async def test_load_with_error_log_json(
        self,
        error_log_manager: ErrorLogManager,
        error_log_bus_obj: ErrorLogBusObj,
        new_error_log: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log JSON.
        """
        error_log_json = error_log_manager.to_json(new_error_log)
        await error_log_bus_obj.load_from_json(
            error_log_json)
        assert error_log_manager.is_equal(
            error_log_bus_obj.error_log, new_error_log) is True
    @pytest.mark.asyncio
    async def test_load_with_error_log_dict(
        self,
        error_log_manager: ErrorLogManager,
        error_log_bus_obj: ErrorLogBusObj,
        new_error_log: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log dictionary.
        """
        logger.info("test_load_with_error_log_dict 1")
        error_log_dict = error_log_manager.to_dict(new_error_log)
        logger.info(error_log_dict)
        await error_log_bus_obj.load_from_dict(
            error_log_dict)
        assert error_log_manager.is_equal(
            error_log_bus_obj.error_log,
            new_error_log) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_error_log(
        self,
        error_log_bus_obj: ErrorLogBusObj
    ):
        """
        Test case for retrieving a nonexistent error_log.
        """
        # Test retrieving a nonexistent
        # error_log raises an exception
        await error_log_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert error_log_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_error_log(
        self,
        error_log_manager: ErrorLogManager,
        error_log_bus_obj: ErrorLogBusObj,
        new_error_log: ErrorLog
    ):
        """
        Test case for updating a error_log's data.
        """
        # Test updating a error_log's data
        new_error_log_error_log_id_value = new_error_log.error_log_id
        new_error_log = await error_log_manager.get_by_id(
            new_error_log_error_log_id_value)
        assert isinstance(new_error_log, ErrorLog)
        new_code = uuid.uuid4()
        await error_log_bus_obj.load_from_obj_instance(
            new_error_log)
        error_log_bus_obj.code = new_code
        await error_log_bus_obj.save()
        new_error_log_error_log_id_value = new_error_log.error_log_id
        new_error_log = await error_log_manager.get_by_id(
            new_error_log_error_log_id_value)
        assert error_log_manager.is_equal(
            error_log_bus_obj.error_log,
            new_error_log) is True
    @pytest.mark.asyncio
    async def test_delete_error_log(
        self,
        error_log_manager: ErrorLogManager,
        error_log_bus_obj: ErrorLogBusObj,
        new_error_log: ErrorLog
    ):
        """
        Test case for deleting a error_log.
        """
        assert new_error_log.error_log_id is not None
        assert error_log_bus_obj.error_log_id == 0
        new_error_log_error_log_id_value = new_error_log.error_log_id
        await error_log_bus_obj.load_from_id(
            new_error_log_error_log_id_value)
        assert error_log_bus_obj.error_log_id is not None
        await error_log_bus_obj.delete()
        new_error_log_error_log_id_value = new_error_log.error_log_id
        new_error_log = await error_log_manager.get_by_id(
            new_error_log_error_log_id_value)
        assert new_error_log is None

