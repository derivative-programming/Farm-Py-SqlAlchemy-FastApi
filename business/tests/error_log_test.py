# business/tests/error_log_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-lines
"""
Unit tests for the
ErrorLogBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.error_log import ErrorLogBusObj
from helpers.session_context import SessionContext
from models import ErrorLog
from models.factory import ErrorLogFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def error_log():
    """
    Fixture that returns a mock
    error_log object.
    """
    return Mock(spec=ErrorLog)


@pytest.fixture
def obj_list():
    """
    Return a list of mock ErrorLog objects.
    """
    error_logs = []
    for _ in range(3):
        error_log = Mock(spec=ErrorLog)
        error_logs.append(error_log)
    return error_logs


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the ErrorLog class.
    """

    return await ErrorLogFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> ErrorLogBusObj:
    """
    Fixture that returns a new instance of
    the ErrorLog class.
    """

    session_context = SessionContext({}, session)
    error_log_bus_obj = ErrorLogBusObj(
        session_context, new_obj)

    return error_log_bus_obj


class TestErrorLogBusObj:
    """
    Unit tests for the
    ErrorLogBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.error_log"
                ".ErrorLogBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                ErrorLogBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, ErrorLogBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, error_log in \
                    zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(error_log)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            ErrorLogBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # browserCode
    # contextCode
    # createdUTCDateTime
    # description
    # isClientSideError
    # isResolved
    # PacID

    @pytest.mark.asyncio
    async def test_get_pac_id_obj(
        self, new_bus_obj: ErrorLogBusObj
    ):
        """
        Test the get_pac_id_obj method.
        """

        # Call the get_pac_id_bus_obj method
        fk_obj: models.Pac = await \
            new_bus_obj.get_pac_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Pac)

        assert fk_obj.pac_id == \
            new_bus_obj.pac_id

        assert fk_obj.code == \
            new_bus_obj.pac_code_peek

    @pytest.mark.asyncio
    async def test_get_pac_id_bus_obj(
        self, new_bus_obj: ErrorLogBusObj
    ):
        """
        Test the get_pac_id_bus_obj method.
        """
        from business.pac import PacBusObj  # PacID

        # Call the get_pac_id_bus_obj method
        fk_bus_obj: PacBusObj = await \
            new_bus_obj.get_pac_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, PacBusObj)

        assert fk_bus_obj.pac_id == \
            new_bus_obj.pac_id

        assert fk_bus_obj.code == \
            new_bus_obj.pac_code_peek
    # url
