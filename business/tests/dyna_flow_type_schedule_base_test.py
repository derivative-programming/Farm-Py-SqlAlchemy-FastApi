# business/tests/dyna_flow_type_schedule_base_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
DynaFlowTypeScheduleBusObj class.
"""

import math  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
import pytest
from business.dyna_flow_type_schedule_base import DynaFlowTypeScheduleBaseBusObj
from helpers.session_context import SessionContext
from managers.dyna_flow_type_schedule import DynaFlowTypeScheduleManager
from models import DynaFlowTypeSchedule
from models.factory import DynaFlowTypeScheduleFactory
from services.logging_config import get_logger

from ..dyna_flow_type_schedule import DynaFlowTypeScheduleBusObj


BUSINESS_DYNA_FLOW_TYPE_SCHEDULE_BASE_MANAGER_PATCH = (
    "business.dyna_flow_type_schedule_base"
    ".DynaFlowTypeScheduleManager"
)

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
def dyna_flow_type_schedule():
    """
    Fixture that returns a mock
    dyna_flow_type_schedule object.
    """
    return Mock(spec=DynaFlowTypeSchedule)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, dyna_flow_type_schedule
):
    """
    Fixture that returns a
    DynaFlowTypeScheduleBaseBusObj instance.
    """
    mock_sess_base_bus_obj = DynaFlowTypeScheduleBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.dyna_flow_type_schedule = \
        dyna_flow_type_schedule
    return mock_sess_base_bus_obj


class TestDynaFlowTypeScheduleBaseBusObj:
    """
    Unit tests for the
    DynaFlowTypeScheduleBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        DynaFlowTypeScheduleManager class.
        """
        session_context = SessionContext({}, session)
        return DynaFlowTypeScheduleManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        DynaFlowTypeScheduleBusObj class.
        """
        session_context = SessionContext({}, session)
        return DynaFlowTypeScheduleBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the DynaFlowTypeSchedule class.
        """

        return await DynaFlowTypeScheduleFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_dyna_flow_type_schedule(
        self,
        new_bus_obj: DynaFlowTypeScheduleBusObj
    ):
        """
        Test case for creating a new dyna_flow_type_schedule.
        """
        # Test creating a new dyna_flow_type_schedule

        assert new_bus_obj.dyna_flow_type_schedule_id == 0

        assert isinstance(new_bus_obj.dyna_flow_type_schedule_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.dyna_flow_type_id,
                          int)
        assert isinstance(new_bus_obj.frequency_in_hours,
                          int)
        assert isinstance(new_bus_obj.is_active,
                          bool)
        assert isinstance(new_bus_obj.last_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.next_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.pac_id,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_schedule_obj(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        new_bus_obj: DynaFlowTypeScheduleBusObj,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test case for loading data from a
        dyna_flow_type_schedule object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type_schedule, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_schedule_id(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        new_bus_obj: DynaFlowTypeScheduleBusObj,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test case for loading data from a
        dyna_flow_type_schedule ID.
        """

        new_obj_dyna_flow_type_schedule_id = \
            new_obj.dyna_flow_type_schedule_id

        await new_bus_obj.load_from_id(
            new_obj_dyna_flow_type_schedule_id)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type_schedule, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_schedule_code(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        new_bus_obj: DynaFlowTypeScheduleBusObj,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test case for loading data from a
        dyna_flow_type_schedule code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type_schedule, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_schedule_json(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        new_bus_obj: DynaFlowTypeScheduleBusObj,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test case for loading data from a
        dyna_flow_type_schedule JSON.
        """

        dyna_flow_type_schedule_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            dyna_flow_type_schedule_json)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type_schedule, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_schedule_dict(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        new_bus_obj: DynaFlowTypeScheduleBusObj,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test case for loading data from a
        dyna_flow_type_schedule dictionary.
        """

        logger.info("test_load_with_dyna_flow_type_schedule_dict 1")

        dyna_flow_type_schedule_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(dyna_flow_type_schedule_dict)

        await new_bus_obj.load_from_dict(
            dyna_flow_type_schedule_dict)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type_schedule,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_dyna_flow_type_schedule(
        self,
        new_bus_obj: DynaFlowTypeScheduleBusObj
    ):
        """
        Test case for retrieving a nonexistent
        dyna_flow_type_schedule.
        """
        # Test retrieving a nonexistent
        # dyna_flow_type_schedule raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_dyna_flow_type_schedule(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        new_bus_obj: DynaFlowTypeScheduleBusObj,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test case for updating a dyna_flow_type_schedule's data.
        """
        # Test updating a dyna_flow_type_schedule's data

        new_obj_dyna_flow_type_schedule_id_value = \
            new_obj.dyna_flow_type_schedule_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_type_schedule_id_value)

        assert isinstance(new_obj,
                          DynaFlowTypeSchedule)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type_schedule,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_dyna_flow_type_schedule_id_value = \
            new_obj.dyna_flow_type_schedule_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_type_schedule_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type_schedule,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_dyna_flow_type_schedule(
        self,
        obj_manager: DynaFlowTypeScheduleManager,
        new_bus_obj: DynaFlowTypeScheduleBusObj,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test case for deleting a dyna_flow_type_schedule.
        """

        assert new_bus_obj.dyna_flow_type_schedule is not None

        assert new_bus_obj.dyna_flow_type_schedule_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.dyna_flow_type_schedule_id is not None

        await new_bus_obj.delete()

        new_obj_dyna_flow_type_schedule_id_value = \
            new_obj.dyna_flow_type_schedule_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_type_schedule_id_value)

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
        dyna_flow_type_schedule
    ):
        """
        Test case for refreshing the dyna_flow_type_schedule data.
        """
        with patch(
            BUSINESS_DYNA_FLOW_TYPE_SCHEDULE_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=dyna_flow_type_schedule)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .dyna_flow_type_schedule == dyna_flow_type_schedule
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(dyna_flow_type_schedule)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the dyna_flow_type_schedule data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.dyna_flow_type_schedule = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the dyna_flow_type_schedule
        data to a dictionary.
        """
        with patch(
            BUSINESS_DYNA_FLOW_TYPE_SCHEDULE_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            dyna_flow_type_schedule_dict = mock_sess_base_bus_obj.to_dict()
            assert dyna_flow_type_schedule_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.dyna_flow_type_schedule)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the dyna_flow_type_schedule data to JSON.
        """
        with patch(
            BUSINESS_DYNA_FLOW_TYPE_SCHEDULE_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            dyna_flow_type_schedule_json = mock_sess_base_bus_obj.to_json()
            assert dyna_flow_type_schedule_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.dyna_flow_type_schedule)

    def test_get_obj(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for getting the dyna_flow_type_schedule object.
        """
        assert mock_sess_base_bus_obj.get_obj() == dyna_flow_type_schedule

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "dyna_flow_type_schedule"

    def test_get_id(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for getting the dyna_flow_type_schedule ID.
        """
        dyna_flow_type_schedule.dyna_flow_type_schedule_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_dyna_flow_type_schedule_id(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the dyna_flow_type_schedule_id property.
        """
        dyna_flow_type_schedule.dyna_flow_type_schedule_id = 1
        assert mock_sess_base_bus_obj.dyna_flow_type_schedule_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        dyna_flow_type_schedule.code = test_uuid
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
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the DynaFlowTypeScheduleBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (DynaFlowTypeScheduleBaseBusiness):
                An instance of the
                DynaFlowTypeScheduleBaseBusiness class.
            dyna_flow_type_schedule (DynaFlowTypeSchedule):
                An instance of the
                DynaFlowTypeSchedule class.

        Returns:
            None
        """
        dyna_flow_type_schedule.last_change_code = 123
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
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        dyna_flow_type_schedule.insert_user_id = test_uuid
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
    # DynaFlowTypeID
    # frequencyInHours

    def test_frequency_in_hours(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the
        frequency_in_hours property.
        """
        dyna_flow_type_schedule.frequency_in_hours = 1
        assert mock_sess_base_bus_obj \
            .frequency_in_hours == 1

    def test_frequency_in_hours_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        frequency_in_hours setter.
        """
        mock_sess_base_bus_obj.frequency_in_hours = 1
        assert mock_sess_base_bus_obj \
            .frequency_in_hours == 1

    def test_frequency_in_hours_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        frequency_in_hours property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.frequency_in_hours = \
                "not-an-int"
    # isActive

    def test_is_active(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the
        is_active property.
        """
        dyna_flow_type_schedule.is_active = True
        assert mock_sess_base_bus_obj \
            .is_active is True

    def test_is_active_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_active setter.
        """
        mock_sess_base_bus_obj.is_active = \
            True
        assert mock_sess_base_bus_obj \
            .is_active is True

    def test_is_active_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_active = \
                "not-a-boolean"
    # lastUTCDateTime

    def test_last_utc_date_time(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the
        last_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow_type_schedule.last_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .last_utc_date_time == \
            test_datetime

    def test_last_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.last_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .last_utc_date_time == \
            test_datetime

    def test_last_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.last_utc_date_time = \
                "not-a-datetime"
    # nextUTCDateTime

    def test_next_utc_date_time(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the
        next_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow_type_schedule.next_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .next_utc_date_time == \
            test_datetime

    def test_next_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        next_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.next_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .next_utc_date_time == \
            test_datetime

    def test_next_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        next_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.next_utc_date_time = \
                "not-a-datetime"
    # PacID
    # DynaFlowTypeID

    def test_dyna_flow_type_id(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the
        dyna_flow_type_id property.
        """
        dyna_flow_type_schedule.dyna_flow_type_id = 1
        assert mock_sess_base_bus_obj \
            .dyna_flow_type_id == 1

    def test_dyna_flow_type_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        dyna_flow_type_id setter.
        """
        mock_sess_base_bus_obj.dyna_flow_type_id = 1
        assert mock_sess_base_bus_obj \
            .dyna_flow_type_id == 1

    def test_dyna_flow_type_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        dyna_flow_type_id property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.dyna_flow_type_id = \
                "not-an-int"
    # frequencyInHours,
    # isActive,
    # lastUTCDateTime
    # nextUTCDateTime
    # PacID

    def test_pac_id(
            self, mock_sess_base_bus_obj, dyna_flow_type_schedule):
        """
        Test case for the pac_id property.
        """
        dyna_flow_type_schedule.pac_id = 1
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

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            dyna_flow_type_schedule):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow_type_schedule.insert_utc_date_time = test_datetime
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
            dyna_flow_type_schedule):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow_type_schedule.last_update_utc_date_time = test_datetime
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
