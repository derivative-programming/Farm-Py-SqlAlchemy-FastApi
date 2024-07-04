# business/tests/df_maintenance_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
DFMaintenanceBusObj class.
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
from business.df_maintenance_base import (
    DFMaintenanceBaseBusObj)
from helpers.session_context import SessionContext
from managers.df_maintenance import (
    DFMaintenanceManager)
from models import DFMaintenance
from models.factory import (
    DFMaintenanceFactory)
from services.logging_config import get_logger

from ..df_maintenance import DFMaintenanceBusObj


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
def df_maintenance():
    """
    Fixture that returns a mock
    df_maintenance object.
    """
    return Mock(spec=DFMaintenance)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, df_maintenance
):
    """
    Fixture that returns a
    DFMaintenanceBaseBusObj instance.
    """
    mock_sess_base_bus_obj = DFMaintenanceBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.df_maintenance = \
        df_maintenance
    return mock_sess_base_bus_obj


class TestDFMaintenanceBaseBusObj:
    """
    Unit tests for the
    DFMaintenanceBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        DFMaintenanceManager class.
        """
        session_context = SessionContext(dict(), session)
        return DFMaintenanceManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        DFMaintenanceBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return DFMaintenanceBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the DFMaintenance class.
        """

        return await DFMaintenanceFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_df_maintenance(
        self,
        new_bus_obj: DFMaintenanceBusObj
    ):
        """
        Test case for creating a new df_maintenance.
        """
        # Test creating a new df_maintenance

        assert new_bus_obj.df_maintenance_id == 0

        assert isinstance(new_bus_obj.df_maintenance_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.is_paused,
                          bool)
        assert isinstance(new_bus_obj.is_scheduled_df_process_request_completed,
                          bool)
        assert isinstance(new_bus_obj.is_scheduled_df_process_request_started,
                          bool)
        assert isinstance(new_bus_obj.last_scheduled_df_process_request_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.next_scheduled_df_process_request_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.pac_id,
                          int)
        assert isinstance(new_bus_obj.paused_by_username,
                          str)
        assert isinstance(new_bus_obj.paused_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.scheduled_df_process_request_processor_identifier,
                          str)

    @pytest.mark.asyncio
    async def test_load_with_df_maintenance_obj(
        self,
        obj_manager: DFMaintenanceManager,
        new_bus_obj: DFMaintenanceBusObj,
        new_obj: DFMaintenance
    ):
        """
        Test case for loading data from a
        df_maintenance object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.df_maintenance, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_df_maintenance_id(
        self,
        obj_manager: DFMaintenanceManager,
        new_bus_obj: DFMaintenanceBusObj,
        new_obj: DFMaintenance
    ):
        """
        Test case for loading data from a
        df_maintenance ID.
        """

        new_obj_df_maintenance_id = \
            new_obj.df_maintenance_id

        await new_bus_obj.load_from_id(
            new_obj_df_maintenance_id)

        assert obj_manager.is_equal(
            new_bus_obj.df_maintenance, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_df_maintenance_code(
        self,
        obj_manager: DFMaintenanceManager,
        new_bus_obj: DFMaintenanceBusObj,
        new_obj: DFMaintenance
    ):
        """
        Test case for loading data from a
        df_maintenance code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.df_maintenance, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_df_maintenance_json(
        self,
        obj_manager: DFMaintenanceManager,
        new_bus_obj: DFMaintenanceBusObj,
        new_obj: DFMaintenance
    ):
        """
        Test case for loading data from a
        df_maintenance JSON.
        """

        df_maintenance_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            df_maintenance_json)

        assert obj_manager.is_equal(
            new_bus_obj.df_maintenance, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_df_maintenance_dict(
        self,
        obj_manager: DFMaintenanceManager,
        new_bus_obj: DFMaintenanceBusObj,
        new_obj: DFMaintenance
    ):
        """
        Test case for loading data from a
        df_maintenance dictionary.
        """

        logger.info("test_load_with_df_maintenance_dict 1")

        df_maintenance_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(df_maintenance_dict)

        await new_bus_obj.load_from_dict(
            df_maintenance_dict)

        assert obj_manager.is_equal(
            new_bus_obj.df_maintenance,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_df_maintenance(
        self,
        new_bus_obj: DFMaintenanceBusObj
    ):
        """
        Test case for retrieving a nonexistent
        df_maintenance.
        """
        # Test retrieving a nonexistent
        # df_maintenance raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_df_maintenance(
        self,
        obj_manager: DFMaintenanceManager,
        new_bus_obj: DFMaintenanceBusObj,
        new_obj: DFMaintenance
    ):
        """
        Test case for updating a df_maintenance's data.
        """
        # Test updating a df_maintenance's data

        new_obj_df_maintenance_id_value = \
            new_obj.df_maintenance_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_df_maintenance_id_value)

        assert isinstance(new_obj,
                          DFMaintenance)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.df_maintenance,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_df_maintenance_id_value = \
            new_obj.df_maintenance_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_df_maintenance_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.df_maintenance,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_df_maintenance(
        self,
        obj_manager: DFMaintenanceManager,
        new_bus_obj: DFMaintenanceBusObj,
        new_obj: DFMaintenance
    ):
        """
        Test case for deleting a df_maintenance.
        """

        assert new_bus_obj.df_maintenance is not None

        assert new_bus_obj.df_maintenance_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.df_maintenance_id is not None

        await new_bus_obj.delete()

        new_obj_df_maintenance_id_value = \
            new_obj.df_maintenance_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_df_maintenance_id_value)

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
        df_maintenance
    ):
        """
        Test case for refreshing the df_maintenance data.
        """
        with patch(
            "business.df_maintenance_base"
            ".DFMaintenanceManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=df_maintenance)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .df_maintenance == df_maintenance
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(df_maintenance)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the df_maintenance data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.df_maintenance = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the df_maintenance
        data to a dictionary.
        """
        with patch(
            "business.df_maintenance_base"
            ".DFMaintenanceManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            df_maintenance_dict = mock_sess_base_bus_obj.to_dict()
            assert df_maintenance_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.df_maintenance)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the df_maintenance data to JSON.
        """
        with patch(
            "business.df_maintenance_base"
            ".DFMaintenanceManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            df_maintenance_json = mock_sess_base_bus_obj.to_json()
            assert df_maintenance_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.df_maintenance)

    def test_get_obj(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for getting the df_maintenance object.
        """
        assert mock_sess_base_bus_obj.get_obj() == df_maintenance

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "df_maintenance"

    def test_get_id(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for getting the df_maintenance ID.
        """
        df_maintenance.df_maintenance_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_df_maintenance_id(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the df_maintenance_id property.
        """
        df_maintenance.df_maintenance_id = 1
        assert mock_sess_base_bus_obj.df_maintenance_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        df_maintenance.code = test_uuid
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
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the DFMaintenanceBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (DFMaintenanceBaseBusiness):
                An instance of the
                DFMaintenanceBaseBusiness class.
            df_maintenance (DFMaintenance):
                An instance of the
                DFMaintenance class.

        Returns:
            None
        """
        df_maintenance.last_change_code = 123
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
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        df_maintenance.insert_user_id = test_uuid
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
    # isPaused

    def test_is_paused(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        is_paused property.
        """
        df_maintenance.is_paused = True
        assert mock_sess_base_bus_obj \
            .is_paused is True

    def test_is_paused_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_paused setter.
        """
        mock_sess_base_bus_obj.is_paused = \
            True
        assert mock_sess_base_bus_obj \
            .is_paused is True

    def test_is_paused_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_paused property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_paused = \
                "not-a-boolean"
    # isScheduledDFProcessRequestCompleted

    def test_is_scheduled_df_process_request_completed(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        is_scheduled_df_process_request_completed property.
        """
        df_maintenance.is_scheduled_df_process_request_completed = True
        assert mock_sess_base_bus_obj \
            .is_scheduled_df_process_request_completed is True

    def test_is_scheduled_df_process_request_completed_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_scheduled_df_process_request_completed setter.
        """
        mock_sess_base_bus_obj.is_scheduled_df_process_request_completed = \
            True
        assert mock_sess_base_bus_obj \
            .is_scheduled_df_process_request_completed is True

    def test_is_scheduled_df_process_request_completed_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_scheduled_df_process_request_completed property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_scheduled_df_process_request_completed = \
                "not-a-boolean"
    # isScheduledDFProcessRequestStarted

    def test_is_scheduled_df_process_request_started(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        is_scheduled_df_process_request_started property.
        """
        df_maintenance.is_scheduled_df_process_request_started = True
        assert mock_sess_base_bus_obj \
            .is_scheduled_df_process_request_started is True

    def test_is_scheduled_df_process_request_started_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_scheduled_df_process_request_started setter.
        """
        mock_sess_base_bus_obj.is_scheduled_df_process_request_started = \
            True
        assert mock_sess_base_bus_obj \
            .is_scheduled_df_process_request_started is True

    def test_is_scheduled_df_process_request_started_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_scheduled_df_process_request_started property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_scheduled_df_process_request_started = \
                "not-a-boolean"
    # lastScheduledDFProcessRequestUTCDateTime

    def test_last_scheduled_df_process_request_utc_date_time(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        last_scheduled_df_process_request_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        df_maintenance.last_scheduled_df_process_request_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .last_scheduled_df_process_request_utc_date_time == \
            test_datetime

    def test_last_scheduled_df_process_request_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_scheduled_df_process_request_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.last_scheduled_df_process_request_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .last_scheduled_df_process_request_utc_date_time == \
            test_datetime

    def test_last_scheduled_df_process_request_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_scheduled_df_process_request_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.last_scheduled_df_process_request_utc_date_time = \
                "not-a-datetime"
    # nextScheduledDFProcessRequestUTCDateTime

    def test_next_scheduled_df_process_request_utc_date_time(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        next_scheduled_df_process_request_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        df_maintenance.next_scheduled_df_process_request_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .next_scheduled_df_process_request_utc_date_time == \
            test_datetime

    def test_next_scheduled_df_process_request_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        next_scheduled_df_process_request_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.next_scheduled_df_process_request_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .next_scheduled_df_process_request_utc_date_time == \
            test_datetime

    def test_next_scheduled_df_process_request_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        next_scheduled_df_process_request_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.next_scheduled_df_process_request_utc_date_time = \
                "not-a-datetime"
    # PacID
    # pausedByUsername

    def test_paused_by_username(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        paused_by_username property.
        """
        df_maintenance.paused_by_username = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .paused_by_username == "Vanilla"

    def test_paused_by_username_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        paused_by_username setter.
        """
        mock_sess_base_bus_obj.paused_by_username = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .paused_by_username == "Vanilla"

    def test_paused_by_username_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        paused_by_username property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.paused_by_username = \
                123
    # pausedUTCDateTime

    def test_paused_utc_date_time(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        paused_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        df_maintenance.paused_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .paused_utc_date_time == \
            test_datetime

    def test_paused_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        paused_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.paused_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .paused_utc_date_time == \
            test_datetime

    def test_paused_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        paused_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.paused_utc_date_time = \
                "not-a-datetime"
    # scheduledDFProcessRequestProcessorIdentifier

    def test_scheduled_df_process_request_processor_identifier(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the
        scheduled_df_process_request_processor_identifier property.
        """
        df_maintenance.scheduled_df_process_request_processor_identifier = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .scheduled_df_process_request_processor_identifier == "Vanilla"

    def test_scheduled_df_process_request_processor_identifier_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        scheduled_df_process_request_processor_identifier setter.
        """
        mock_sess_base_bus_obj.scheduled_df_process_request_processor_identifier = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .scheduled_df_process_request_processor_identifier == "Vanilla"

    def test_scheduled_df_process_request_processor_identifier_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        scheduled_df_process_request_processor_identifier property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.scheduled_df_process_request_processor_identifier = \
                123
    # isPaused,
    # isScheduledDFProcessRequestCompleted,
    # isScheduledDFProcessRequestStarted,
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
    # PacID

    def test_pac_id(
            self, mock_sess_base_bus_obj, df_maintenance):
        """
        Test case for the pac_id property.
        """
        df_maintenance.pac_id = 1
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
    # pausedByUsername,
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier,

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            df_maintenance):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        df_maintenance.insert_utc_date_time = test_datetime
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
            df_maintenance):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        df_maintenance.last_update_utc_date_time = test_datetime
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
