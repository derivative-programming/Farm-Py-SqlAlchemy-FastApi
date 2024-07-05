# business/tests/error_log_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
ErrorLogBusObj class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
from business.error_log_base import (
    ErrorLogBaseBusObj)
from helpers.session_context import SessionContext
from managers.error_log import (
    ErrorLogManager)
from models import ErrorLog
from models.factory import (
    ErrorLogFactory)
from services.logging_config import get_logger

from ..error_log import ErrorLogBusObj


logger = get_logger(__name__)


@pytest.fixture
def mock_session_context():
    """
    Fixture that returns a fake session context.
    """
    session = Mock()
    session_context = Mock(spec=SessionContext)
    session_context.session = session
    return session_context


@pytest.fixture
def error_log():
    """
    Fixture that returns a mock
    error_log object.
    """
    return Mock(spec=ErrorLog)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, error_log
):
    """
    Fixture that returns a
    ErrorLogBaseBusObj instance.
    """
    mock_sess_base_bus_obj = ErrorLogBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.error_log = \
        error_log
    return mock_sess_base_bus_obj


class TestErrorLogBaseBusObj:
    """
    Unit tests for the
    ErrorLogBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        ErrorLogManager class.
        """
        session_context = SessionContext({}, session)
        return ErrorLogManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        ErrorLogBusObj class.
        """
        session_context = SessionContext({}, session)
        return ErrorLogBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the ErrorLog class.
        """

        return await ErrorLogFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_error_log(
        self,
        new_bus_obj: ErrorLogBusObj
    ):
        """
        Test case for creating a new error_log.
        """
        # Test creating a new error_log

        assert new_bus_obj.error_log_id == 0

        assert isinstance(new_bus_obj.error_log_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        # browser_code
        assert isinstance(new_bus_obj.browser_code,
                          uuid.UUID)
        # context_code
        assert isinstance(new_bus_obj.context_code,
                          uuid.UUID)
        assert isinstance(new_bus_obj.created_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.description,
                          str)
        assert isinstance(new_bus_obj.is_client_side_error,
                          bool)
        assert isinstance(new_bus_obj.is_resolved,
                          bool)
        assert isinstance(new_bus_obj.pac_id,
                          int)
        assert isinstance(new_bus_obj.url,
                          str)

    @pytest.mark.asyncio
    async def test_load_with_error_log_obj(
        self,
        obj_manager: ErrorLogManager,
        new_bus_obj: ErrorLogBusObj,
        new_obj: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.error_log, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_error_log_id(
        self,
        obj_manager: ErrorLogManager,
        new_bus_obj: ErrorLogBusObj,
        new_obj: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log ID.
        """

        new_obj_error_log_id = \
            new_obj.error_log_id

        await new_bus_obj.load_from_id(
            new_obj_error_log_id)

        assert obj_manager.is_equal(
            new_bus_obj.error_log, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_error_log_code(
        self,
        obj_manager: ErrorLogManager,
        new_bus_obj: ErrorLogBusObj,
        new_obj: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.error_log, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_error_log_json(
        self,
        obj_manager: ErrorLogManager,
        new_bus_obj: ErrorLogBusObj,
        new_obj: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log JSON.
        """

        error_log_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            error_log_json)

        assert obj_manager.is_equal(
            new_bus_obj.error_log, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_error_log_dict(
        self,
        obj_manager: ErrorLogManager,
        new_bus_obj: ErrorLogBusObj,
        new_obj: ErrorLog
    ):
        """
        Test case for loading data from a
        error_log dictionary.
        """

        logger.info("test_load_with_error_log_dict 1")

        error_log_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(error_log_dict)

        await new_bus_obj.load_from_dict(
            error_log_dict)

        assert obj_manager.is_equal(
            new_bus_obj.error_log,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_error_log(
        self,
        new_bus_obj: ErrorLogBusObj
    ):
        """
        Test case for retrieving a nonexistent
        error_log.
        """
        # Test retrieving a nonexistent
        # error_log raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_error_log(
        self,
        obj_manager: ErrorLogManager,
        new_bus_obj: ErrorLogBusObj,
        new_obj: ErrorLog
    ):
        """
        Test case for updating a error_log's data.
        """
        # Test updating a error_log's data

        new_obj_error_log_id_value = \
            new_obj.error_log_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_error_log_id_value)

        assert isinstance(new_obj,
                          ErrorLog)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.error_log,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_error_log_id_value = \
            new_obj.error_log_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_error_log_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.error_log,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_error_log(
        self,
        obj_manager: ErrorLogManager,
        new_bus_obj: ErrorLogBusObj,
        new_obj: ErrorLog
    ):
        """
        Test case for deleting a error_log.
        """

        assert new_bus_obj.error_log is not None

        assert new_bus_obj.error_log_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.error_log_id is not None

        await new_bus_obj.delete()

        new_obj_error_log_id_value = \
            new_obj.error_log_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_error_log_id_value)

        assert new_obj is None

    def test_get_session_context(
        self,
        mock_sess_base_bus_obj,
        mock_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert mock_sess_base_bus_obj.get_session_context() == \
            mock_session_context

    @pytest.mark.asyncio
    async def test_refresh(
        self,
        mock_sess_base_bus_obj,
        error_log
    ):
        """
        Test case for refreshing the error_log data.
        """
        with patch(
            "business.error_log_base"
            ".ErrorLogManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=error_log)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .error_log == error_log
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(error_log)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the error_log data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.error_log = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the error_log
        data to a dictionary.
        """
        with patch(
            "business.error_log_base"
            ".ErrorLogManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            error_log_dict = mock_sess_base_bus_obj.to_dict()
            assert error_log_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.error_log)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the error_log data to JSON.
        """
        with patch(
            "business.error_log_base"
            ".ErrorLogManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            error_log_json = mock_sess_base_bus_obj.to_json()
            assert error_log_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.error_log)

    def test_get_obj(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for getting the error_log object.
        """
        assert mock_sess_base_bus_obj.get_obj() == error_log

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "error_log"

    def test_get_id(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for getting the error_log ID.
        """
        error_log.error_log_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_error_log_id(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the error_log_id property.
        """
        error_log.error_log_id = 1
        assert mock_sess_base_bus_obj.error_log_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        error_log.code = test_uuid
        assert mock_sess_base_bus_obj.code == \
            test_uuid

    def test_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.code = test_uuid
        assert mock_sess_base_bus_obj.code == \
            test_uuid

    def test_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the ErrorLogBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (ErrorLogBaseBusiness):
                An instance of the
                ErrorLogBaseBusiness class.
            error_log (ErrorLog):
                An instance of the
                ErrorLog class.

        Returns:
            None
        """
        error_log.last_change_code = 123
        assert mock_sess_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_change_code setter.
        """
        mock_sess_base_bus_obj.last_change_code = 123
        assert mock_sess_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        error_log.insert_user_id = test_uuid
        assert mock_sess_base_bus_obj.insert_user_id == \
            test_uuid

    def test_insert_user_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.insert_user_id = test_uuid
        assert mock_sess_base_bus_obj.insert_user_id == \
            test_uuid

    def test_insert_user_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.insert_user_id = "not-a-uuid"
    # browserCode

    def test_browser_code(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the
        browser_code property.
        """
        test_uuid = uuid.uuid4()
        error_log.browser_code = \
            test_uuid
        assert mock_sess_base_bus_obj \
            .browser_code == \
            test_uuid

    def test_browser_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        browser_code setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.browser_code = \
            test_uuid
        assert mock_sess_base_bus_obj \
            .browser_code == \
            test_uuid

    def test_browser_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        browser_code property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.browser_code = \
                "not-a-uuid"
    # contextCode

    def test_context_code(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the
        context_code property.
        """
        test_uuid = uuid.uuid4()
        error_log.context_code = \
            test_uuid
        assert mock_sess_base_bus_obj \
            .context_code == \
            test_uuid

    def test_context_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        context_code setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.context_code = \
            test_uuid
        assert mock_sess_base_bus_obj \
            .context_code == \
            test_uuid

    def test_context_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        context_code property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.context_code = \
                "not-a-uuid"
    # createdUTCDateTime

    def test_created_utc_date_time(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the
        created_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        error_log.created_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .created_utc_date_time == \
            test_datetime

    def test_created_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        created_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.created_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .created_utc_date_time == \
            test_datetime

    def test_created_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        created_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.created_utc_date_time = \
                "not-a-datetime"
    # description

    def test_description(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the
        description property.
        """
        error_log.description = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .description == "Vanilla"

    def test_description_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        description setter.
        """
        mock_sess_base_bus_obj.description = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .description == "Vanilla"

    def test_description_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        description property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.description = \
                123
    # isClientSideError

    def test_is_client_side_error(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the
        is_client_side_error property.
        """
        error_log.is_client_side_error = True
        assert mock_sess_base_bus_obj \
            .is_client_side_error is True

    def test_is_client_side_error_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_client_side_error setter.
        """
        mock_sess_base_bus_obj.is_client_side_error = \
            True
        assert mock_sess_base_bus_obj \
            .is_client_side_error is True

    def test_is_client_side_error_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_client_side_error property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_client_side_error = \
                "not-a-boolean"
    # isResolved

    def test_is_resolved(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the
        is_resolved property.
        """
        error_log.is_resolved = True
        assert mock_sess_base_bus_obj \
            .is_resolved is True

    def test_is_resolved_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_resolved setter.
        """
        mock_sess_base_bus_obj.is_resolved = \
            True
        assert mock_sess_base_bus_obj \
            .is_resolved is True

    def test_is_resolved_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_resolved property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_resolved = \
                "not-a-boolean"
    # PacID
    # url

    def test_url(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the
        url property.
        """
        error_log.url = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .url == "Vanilla"

    def test_url_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        url setter.
        """
        mock_sess_base_bus_obj.url = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .url == "Vanilla"

    def test_url_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        url property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.url = \
                123
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID

    def test_pac_id(
            self, mock_sess_base_bus_obj, error_log):
        """
        Test case for the pac_id property.
        """
        error_log.pac_id = 1
        assert mock_sess_base_bus_obj \
            .pac_id == 1

    def test_pac_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the pac_id setter.
        """
        mock_sess_base_bus_obj.pac_id = 1
        assert mock_sess_base_bus_obj \
            .pac_id == 1

    def test_pac_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        pac_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.pac_id = \
                "not-an-int"
    # url,

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            error_log):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        error_log.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.insert_utc_date_time = \
                "not-a-datetime"

    def test_last_update_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            error_log):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        error_log.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_update_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.last_update_utc_date_time = \
                "not-a-datetime"
