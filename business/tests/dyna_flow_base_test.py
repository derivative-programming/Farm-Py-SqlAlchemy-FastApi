# business/tests/dyna_flow_base_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=redefined-outer-name
# pylint: disable=too-few-public-methods

"""
This module contains unit tests for the
DynaFlowBusObj class.
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
from business.dyna_flow_base import DynaFlowBaseBusObj
from helpers.session_context import SessionContext
from managers.dyna_flow import DynaFlowManager
from models import DynaFlow
from models.factory import DynaFlowFactory
from services.logging_config import get_logger

from ..dyna_flow import DynaFlowBusObj


BUSINESS_DYNA_FLOW_BASE_MANAGER_PATCH = (
    "business.dyna_flow_base"
    ".DynaFlowManager"
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
def dyna_flow():
    """
    Fixture that returns a mock
    dyna_flow object.
    """
    return Mock(spec=DynaFlow)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, dyna_flow
):
    """
    Fixture that returns a
    DynaFlowBaseBusObj instance.
    """
    mock_sess_base_bus_obj = DynaFlowBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.dyna_flow = \
        dyna_flow
    return mock_sess_base_bus_obj


class TestDynaFlowBaseBusObj:
    """
    Unit tests for the
    DynaFlowBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        DynaFlowManager class.
        """
        session_context = SessionContext({}, session)
        return DynaFlowManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        DynaFlowBusObj class.
        """
        session_context = SessionContext({}, session)
        return DynaFlowBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the DynaFlow class.
        """

        return await DynaFlowFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_dyna_flow(
        self,
        new_bus_obj: DynaFlowBusObj
    ):
        """
        Test case for creating a new dyna_flow.
        """
        # Test creating a new dyna_flow

        assert new_bus_obj.dyna_flow_id == 0

        assert isinstance(new_bus_obj.dyna_flow_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.completed_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.dependency_dyna_flow_id,
                          int)
        assert isinstance(new_bus_obj.description,
                          str)
        assert isinstance(new_bus_obj.dyna_flow_type_id,
                          int)
        assert isinstance(new_bus_obj.is_build_task_debug_required,
                          bool)
        assert isinstance(new_bus_obj.is_canceled,
                          bool)
        assert isinstance(new_bus_obj.is_cancel_requested,
                          bool)
        assert isinstance(new_bus_obj.is_completed,
                          bool)
        assert isinstance(new_bus_obj.is_paused,
                          bool)
        assert isinstance(new_bus_obj.is_resubmitted,
                          bool)
        assert isinstance(new_bus_obj.is_run_task_debug_required,
                          bool)
        assert isinstance(new_bus_obj.is_started,
                          bool)
        assert isinstance(new_bus_obj.is_successful,
                          bool)
        assert isinstance(new_bus_obj.is_task_creation_started,
                          bool)
        assert isinstance(new_bus_obj.is_tasks_created,
                          bool)
        assert isinstance(new_bus_obj.min_start_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.pac_id,
                          int)
        assert isinstance(new_bus_obj.param_1,
                          str)
        assert isinstance(new_bus_obj.parent_dyna_flow_id,
                          int)
        assert isinstance(new_bus_obj.priority_level,
                          int)
        assert isinstance(new_bus_obj.requested_utc_date_time,
                          datetime)
        assert isinstance(new_bus_obj.result_value,
                          str)
        assert isinstance(new_bus_obj.root_dyna_flow_id,
                          int)
        assert isinstance(new_bus_obj.started_utc_date_time,
                          datetime)
        # subject_code
        assert isinstance(new_bus_obj.subject_code,
                          uuid.UUID)
        assert isinstance(new_bus_obj.task_creation_processor_identifier,
                          str)

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_obj(
        self,
        obj_manager: DynaFlowManager,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow
    ):
        """
        Test case for loading data from a
        dyna_flow object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_id(
        self,
        obj_manager: DynaFlowManager,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow
    ):
        """
        Test case for loading data from a
        dyna_flow ID.
        """

        new_obj_dyna_flow_id = \
            new_obj.dyna_flow_id

        await new_bus_obj.load_from_id(
            new_obj_dyna_flow_id)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_code(
        self,
        obj_manager: DynaFlowManager,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow
    ):
        """
        Test case for loading data from a
        dyna_flow code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_json(
        self,
        obj_manager: DynaFlowManager,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow
    ):
        """
        Test case for loading data from a
        dyna_flow JSON.
        """

        dyna_flow_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            dyna_flow_json)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_dict(
        self,
        obj_manager: DynaFlowManager,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow
    ):
        """
        Test case for loading data from a
        dyna_flow dictionary.
        """

        logger.info("test_load_with_dyna_flow_dict 1")

        dyna_flow_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(dyna_flow_dict)

        await new_bus_obj.load_from_dict(
            dyna_flow_dict)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_dyna_flow(
        self,
        new_bus_obj: DynaFlowBusObj
    ):
        """
        Test case for retrieving a nonexistent
        dyna_flow.
        """
        # Test retrieving a nonexistent
        # dyna_flow raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_dyna_flow(
        self,
        obj_manager: DynaFlowManager,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow
    ):
        """
        Test case for updating a dyna_flow's data.
        """
        # Test updating a dyna_flow's data

        new_obj_dyna_flow_id_value = \
            new_obj.dyna_flow_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_id_value)

        assert isinstance(new_obj,
                          DynaFlow)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_dyna_flow_id_value = \
            new_obj.dyna_flow_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_dyna_flow(
        self,
        obj_manager: DynaFlowManager,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow
    ):
        """
        Test case for deleting a dyna_flow.
        """

        assert new_bus_obj.dyna_flow is not None

        assert new_bus_obj.dyna_flow_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.dyna_flow_id is not None

        await new_bus_obj.delete()

        new_obj_dyna_flow_id_value = \
            new_obj.dyna_flow_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_id_value)

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
        dyna_flow
    ):
        """
        Test case for refreshing the dyna_flow data.
        """
        with patch(
            BUSINESS_DYNA_FLOW_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=dyna_flow)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .dyna_flow == dyna_flow
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(dyna_flow)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the dyna_flow data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.dyna_flow = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the dyna_flow
        data to a dictionary.
        """
        with patch(
            BUSINESS_DYNA_FLOW_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            dyna_flow_dict = mock_sess_base_bus_obj.to_dict()
            assert dyna_flow_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.dyna_flow)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the dyna_flow data to JSON.
        """
        with patch(
            BUSINESS_DYNA_FLOW_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            dyna_flow_json = mock_sess_base_bus_obj.to_json()
            assert dyna_flow_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.dyna_flow)

    def test_get_obj(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for getting the dyna_flow object.
        """
        assert mock_sess_base_bus_obj.get_obj() == dyna_flow

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "dyna_flow"

    def test_get_id(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for getting the dyna_flow ID.
        """
        dyna_flow.dyna_flow_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_dyna_flow_id(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the dyna_flow_id property.
        """
        dyna_flow.dyna_flow_id = 1
        assert mock_sess_base_bus_obj.dyna_flow_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        dyna_flow.code = test_uuid
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
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the DynaFlowBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (DynaFlowBaseBusiness):
                An instance of the
                DynaFlowBaseBusiness class.
            dyna_flow (DynaFlow):
                An instance of the
                DynaFlow class.

        Returns:
            None
        """
        dyna_flow.last_change_code = 123
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
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        dyna_flow.insert_user_id = test_uuid
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
    # completedUTCDateTime

    def test_completed_utc_date_time(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        completed_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow.completed_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .completed_utc_date_time == \
            test_datetime

    def test_completed_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        completed_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.completed_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .completed_utc_date_time == \
            test_datetime

    def test_completed_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        completed_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.completed_utc_date_time = \
                "not-a-datetime"
    # dependencyDynaFlowID

    def test_dependency_dyna_flow_id(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        dependency_dyna_flow_id property.
        """
        dyna_flow.dependency_dyna_flow_id = 1
        assert mock_sess_base_bus_obj \
            .dependency_dyna_flow_id == 1

    def test_dependency_dyna_flow_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        dependency_dyna_flow_id setter.
        """
        mock_sess_base_bus_obj.dependency_dyna_flow_id = 1
        assert mock_sess_base_bus_obj \
            .dependency_dyna_flow_id == 1

    def test_dependency_dyna_flow_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        dependency_dyna_flow_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.dependency_dyna_flow_id = \
                "not-an-int"
    # description

    def test_description(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        description property.
        """
        dyna_flow.description = \
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
    # DynaFlowTypeID
    # isBuildTaskDebugRequired

    def test_is_build_task_debug_required(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_build_task_debug_required property.
        """
        dyna_flow.is_build_task_debug_required = True
        assert mock_sess_base_bus_obj \
            .is_build_task_debug_required is True

    def test_is_build_task_debug_required_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_build_task_debug_required setter.
        """
        mock_sess_base_bus_obj.is_build_task_debug_required = \
            True
        assert mock_sess_base_bus_obj \
            .is_build_task_debug_required is True

    def test_is_build_task_debug_required_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_build_task_debug_required property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_build_task_debug_required = \
                "not-a-boolean"
    # isCanceled

    def test_is_canceled(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_canceled property.
        """
        dyna_flow.is_canceled = True
        assert mock_sess_base_bus_obj \
            .is_canceled is True

    def test_is_canceled_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_canceled setter.
        """
        mock_sess_base_bus_obj.is_canceled = \
            True
        assert mock_sess_base_bus_obj \
            .is_canceled is True

    def test_is_canceled_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_canceled property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_canceled = \
                "not-a-boolean"
    # isCancelRequested

    def test_is_cancel_requested(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_cancel_requested property.
        """
        dyna_flow.is_cancel_requested = True
        assert mock_sess_base_bus_obj \
            .is_cancel_requested is True

    def test_is_cancel_requested_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_cancel_requested setter.
        """
        mock_sess_base_bus_obj.is_cancel_requested = \
            True
        assert mock_sess_base_bus_obj \
            .is_cancel_requested is True

    def test_is_cancel_requested_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_cancel_requested property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_cancel_requested = \
                "not-a-boolean"
    # isCompleted

    def test_is_completed(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_completed property.
        """
        dyna_flow.is_completed = True
        assert mock_sess_base_bus_obj \
            .is_completed is True

    def test_is_completed_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_completed setter.
        """
        mock_sess_base_bus_obj.is_completed = \
            True
        assert mock_sess_base_bus_obj \
            .is_completed is True

    def test_is_completed_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_completed property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_completed = \
                "not-a-boolean"
    # isPaused

    def test_is_paused(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_paused property.
        """
        dyna_flow.is_paused = True
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
    # isResubmitted

    def test_is_resubmitted(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_resubmitted property.
        """
        dyna_flow.is_resubmitted = True
        assert mock_sess_base_bus_obj \
            .is_resubmitted is True

    def test_is_resubmitted_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_resubmitted setter.
        """
        mock_sess_base_bus_obj.is_resubmitted = \
            True
        assert mock_sess_base_bus_obj \
            .is_resubmitted is True

    def test_is_resubmitted_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_resubmitted property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_resubmitted = \
                "not-a-boolean"
    # isRunTaskDebugRequired

    def test_is_run_task_debug_required(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_run_task_debug_required property.
        """
        dyna_flow.is_run_task_debug_required = True
        assert mock_sess_base_bus_obj \
            .is_run_task_debug_required is True

    def test_is_run_task_debug_required_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_run_task_debug_required setter.
        """
        mock_sess_base_bus_obj.is_run_task_debug_required = \
            True
        assert mock_sess_base_bus_obj \
            .is_run_task_debug_required is True

    def test_is_run_task_debug_required_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_run_task_debug_required property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_run_task_debug_required = \
                "not-a-boolean"
    # isStarted

    def test_is_started(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_started property.
        """
        dyna_flow.is_started = True
        assert mock_sess_base_bus_obj \
            .is_started is True

    def test_is_started_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_started setter.
        """
        mock_sess_base_bus_obj.is_started = \
            True
        assert mock_sess_base_bus_obj \
            .is_started is True

    def test_is_started_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_started property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_started = \
                "not-a-boolean"
    # isSuccessful

    def test_is_successful(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_successful property.
        """
        dyna_flow.is_successful = True
        assert mock_sess_base_bus_obj \
            .is_successful is True

    def test_is_successful_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_successful setter.
        """
        mock_sess_base_bus_obj.is_successful = \
            True
        assert mock_sess_base_bus_obj \
            .is_successful is True

    def test_is_successful_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_successful property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_successful = \
                "not-a-boolean"
    # isTaskCreationStarted

    def test_is_task_creation_started(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_task_creation_started property.
        """
        dyna_flow.is_task_creation_started = True
        assert mock_sess_base_bus_obj \
            .is_task_creation_started is True

    def test_is_task_creation_started_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_task_creation_started setter.
        """
        mock_sess_base_bus_obj.is_task_creation_started = \
            True
        assert mock_sess_base_bus_obj \
            .is_task_creation_started is True

    def test_is_task_creation_started_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_task_creation_started property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_task_creation_started = \
                "not-a-boolean"
    # isTasksCreated

    def test_is_tasks_created(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        is_tasks_created property.
        """
        dyna_flow.is_tasks_created = True
        assert mock_sess_base_bus_obj \
            .is_tasks_created is True

    def test_is_tasks_created_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_tasks_created setter.
        """
        mock_sess_base_bus_obj.is_tasks_created = \
            True
        assert mock_sess_base_bus_obj \
            .is_tasks_created is True

    def test_is_tasks_created_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_tasks_created property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_tasks_created = \
                "not-a-boolean"
    # minStartUTCDateTime

    def test_min_start_utc_date_time(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        min_start_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow.min_start_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .min_start_utc_date_time == \
            test_datetime

    def test_min_start_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        min_start_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.min_start_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .min_start_utc_date_time == \
            test_datetime

    def test_min_start_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        min_start_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.min_start_utc_date_time = \
                "not-a-datetime"
    # PacID
    # param1

    def test_param_1(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        param_1 property.
        """
        dyna_flow.param_1 = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .param_1 == "Vanilla"

    def test_param_1_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        param_1 setter.
        """
        mock_sess_base_bus_obj.param_1 = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .param_1 == "Vanilla"

    def test_param_1_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        param_1 property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.param_1 = \
                123
    # parentDynaFlowID

    def test_parent_dyna_flow_id(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        parent_dyna_flow_id property.
        """
        dyna_flow.parent_dyna_flow_id = 1
        assert mock_sess_base_bus_obj \
            .parent_dyna_flow_id == 1

    def test_parent_dyna_flow_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        parent_dyna_flow_id setter.
        """
        mock_sess_base_bus_obj.parent_dyna_flow_id = 1
        assert mock_sess_base_bus_obj \
            .parent_dyna_flow_id == 1

    def test_parent_dyna_flow_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        parent_dyna_flow_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.parent_dyna_flow_id = \
                "not-an-int"
    # priorityLevel

    def test_priority_level(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        priority_level property.
        """
        dyna_flow.priority_level = 1
        assert mock_sess_base_bus_obj \
            .priority_level == 1

    def test_priority_level_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        priority_level setter.
        """
        mock_sess_base_bus_obj.priority_level = 1
        assert mock_sess_base_bus_obj \
            .priority_level == 1

    def test_priority_level_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        priority_level property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.priority_level = \
                "not-an-int"
    # requestedUTCDateTime

    def test_requested_utc_date_time(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        requested_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow.requested_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .requested_utc_date_time == \
            test_datetime

    def test_requested_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        requested_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.requested_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .requested_utc_date_time == \
            test_datetime

    def test_requested_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        requested_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.requested_utc_date_time = \
                "not-a-datetime"
    # resultValue

    def test_result_value(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        result_value property.
        """
        dyna_flow.result_value = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .result_value == "Vanilla"

    def test_result_value_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        result_value setter.
        """
        mock_sess_base_bus_obj.result_value = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .result_value == "Vanilla"

    def test_result_value_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        result_value property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.result_value = \
                123
    # rootDynaFlowID

    def test_root_dyna_flow_id(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        root_dyna_flow_id property.
        """
        dyna_flow.root_dyna_flow_id = 1
        assert mock_sess_base_bus_obj \
            .root_dyna_flow_id == 1

    def test_root_dyna_flow_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        root_dyna_flow_id setter.
        """
        mock_sess_base_bus_obj.root_dyna_flow_id = 1
        assert mock_sess_base_bus_obj \
            .root_dyna_flow_id == 1

    def test_root_dyna_flow_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        root_dyna_flow_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.root_dyna_flow_id = \
                "not-an-int"
    # startedUTCDateTime

    def test_started_utc_date_time(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        started_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow.started_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .started_utc_date_time == \
            test_datetime

    def test_started_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        started_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.started_utc_date_time = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .started_utc_date_time == \
            test_datetime

    def test_started_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        started_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.started_utc_date_time = \
                "not-a-datetime"
    # subjectCode

    def test_subject_code(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        subject_code property.
        """
        test_uuid = uuid.uuid4()
        dyna_flow.subject_code = \
            test_uuid
        assert mock_sess_base_bus_obj \
            .subject_code == \
            test_uuid

    def test_subject_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        subject_code setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.subject_code = \
            test_uuid
        assert mock_sess_base_bus_obj \
            .subject_code == \
            test_uuid

    def test_subject_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        subject_code property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.subject_code = \
                "not-a-uuid"
    # taskCreationProcessorIdentifier

    def test_task_creation_processor_identifier(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        task_creation_processor_identifier property.
        """
        dyna_flow.task_creation_processor_identifier = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .task_creation_processor_identifier == "Vanilla"

    def test_task_creation_processor_identifier_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        task_creation_processor_identifier setter.
        """
        mock_sess_base_bus_obj.task_creation_processor_identifier = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .task_creation_processor_identifier == "Vanilla"

    def test_task_creation_processor_identifier_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        task_creation_processor_identifier property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.task_creation_processor_identifier = \
                123
    # completedUTCDateTime
    # dependencyDynaFlowID
    # description
    # DynaFlowTypeID

    def test_dyna_flow_type_id(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the
        dyna_flow_type_id property.
        """
        dyna_flow.dyna_flow_type_id = 1
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
    # isBuildTaskDebugRequired
    # isCanceled
    # isCancelRequested
    # isCompleted
    # isPaused
    # isResubmitted
    # isRunTaskDebugRequired
    # isStarted
    # isSuccessful
    # isTaskCreationStarted
    # isTasksCreated
    # minStartUTCDateTime
    # PacID

    def test_pac_id(
            self, mock_sess_base_bus_obj, dyna_flow):
        """
        Test case for the pac_id property.
        """
        dyna_flow.pac_id = 1
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
    # param1
    # parentDynaFlowID
    # priorityLevel
    # requestedUTCDateTime
    # resultValue
    # rootDynaFlowID
    # startedUTCDateTime
    # subjectCode
    # taskCreationProcessorIdentifier

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            dyna_flow):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow.insert_utc_date_time = test_datetime
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
            dyna_flow):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow.last_update_utc_date_time = test_datetime
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


    @pytest.mark.asyncio
    async def test_build_dyna_flow_task(
        self,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext({}, session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.dyna_flow_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow_task()

        assert child_bus_obj.dyna_flow_id == new_bus_obj.dyna_flow_id
        assert child_bus_obj.dyna_flow_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.dyna_flow_task_id > 0

    @pytest.mark.asyncio
    async def test_get_all_dyna_flow_task(
        self,
        new_bus_obj: DynaFlowBusObj,
        new_obj: DynaFlow,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext({}, session)

        await current_runtime.initialize(session_context)

        new_obj_dyna_flow_id = (
            new_obj.dyna_flow_id
        )

        await new_bus_obj.load_from_id(
            new_obj_dyna_flow_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow_task()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_dyna_flow_task()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].dyna_flow_task_id > 0

        # Check if any item in the list has a matching
        # dyna_flow_task_id
        assert any(
            child.dyna_flow_task_id == (
                child_bus_obj.dyna_flow_task_id)
            for child in child_bus_obj_list
        ), "No matching dyna_flow_task_id found in the list"
