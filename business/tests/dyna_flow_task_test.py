# business/tests/dyna_flow_task_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-lines
"""
Unit tests for the
DynaFlowTaskBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.dyna_flow_task import DynaFlowTaskBusObj
from helpers.session_context import SessionContext
from models import DynaFlowTask
from models.factory import DynaFlowTaskFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def dyna_flow_task():
    """
    Fixture that returns a mock
    dyna_flow_task object.
    """
    return Mock(spec=DynaFlowTask)


@pytest.fixture
def obj_list():
    """
    Return a list of mock DynaFlowTask objects.
    """
    dyna_flow_tasks = []
    for _ in range(3):
        dyna_flow_task = Mock(spec=DynaFlowTask)
        dyna_flow_tasks.append(dyna_flow_task)
    return dyna_flow_tasks


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the DynaFlowTask class.
    """

    return await DynaFlowTaskFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> DynaFlowTaskBusObj:
    """
    Fixture that returns a new instance of
    the DynaFlowTask class.
    """

    session_context = SessionContext({}, session)
    dyna_flow_task_bus_obj = DynaFlowTaskBusObj(
        session_context, new_obj)

    return dyna_flow_task_bus_obj


class TestDynaFlowTaskBusObj:
    """
    Unit tests for the
    DynaFlowTaskBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.dyna_flow_task"
                ".DynaFlowTaskBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                DynaFlowTaskBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, DynaFlowTaskBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, dyna_flow_task in \
                    zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(dyna_flow_task)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            DynaFlowTaskBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # completedUTCDateTime
    # dependencyDynaFlowTaskID
    # description
    # DynaFlowID

    @pytest.mark.asyncio
    async def test_get_dyna_flow_id_obj(
        self, new_bus_obj: DynaFlowTaskBusObj
    ):
        """
        Test the get_dyna_flow_id_obj method.
        """

        # Call the get_dyna_flow_id_bus_obj method
        fk_obj: models.DynaFlow = await \
            new_bus_obj.get_dyna_flow_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.DynaFlow)

        assert fk_obj.dyna_flow_id == \
            new_bus_obj.dyna_flow_id

        assert fk_obj.code == \
            new_bus_obj.dyna_flow_code_peek

    @pytest.mark.asyncio
    async def test_get_dyna_flow_id_bus_obj(
        self, new_bus_obj: DynaFlowTaskBusObj
    ):
        """
        Test the get_dyna_flow_id_bus_obj method.
        """
        from business.dyna_flow import DynaFlowBusObj  # DynaFlowID

        # Call the get_dyna_flow_id_bus_obj method
        fk_bus_obj: DynaFlowBusObj = await \
            new_bus_obj.get_dyna_flow_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, DynaFlowBusObj)

        assert fk_bus_obj.dyna_flow_id == \
            new_bus_obj.dyna_flow_id

        assert fk_bus_obj.code == \
            new_bus_obj.dyna_flow_code_peek
    # dynaFlowSubjectCode
    # DynaFlowTaskTypeID

    @pytest.mark.asyncio
    async def test_get_dyna_flow_task_type_id_obj(
        self, new_bus_obj: DynaFlowTaskBusObj
    ):
        """
        Test the get_dyna_flow_task_type_id_obj method.
        """

        # Call the get_dyna_flow_task_type_id_obj method
        fk_obj: models.DynaFlowTaskType = \
            await new_bus_obj.get_dyna_flow_task_type_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.DynaFlowTaskType)

        assert fk_obj.dyna_flow_task_type_id == \
            new_bus_obj.dyna_flow_task_type_id

        assert fk_obj.code == \
            new_bus_obj.dyna_flow_task_type_code_peek

    @pytest.mark.asyncio
    async def test_get_dyna_flow_task_type_id_bus_obj(
        self, new_bus_obj: DynaFlowTaskBusObj
    ):
        """
        Test the get_dyna_flow_task_type_id_bus_obj
        method.
        """

        from business.dyna_flow_task_type import DynaFlowTaskTypeBusObj  # DynaFlowTaskTypeID

        # Call the get_dyna_flow_task_type_id_bus_obj method
        fk_bus_obj: DynaFlowTaskTypeBusObj = \
            await new_bus_obj.get_dyna_flow_task_type_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, DynaFlowTaskTypeBusObj)

        assert fk_bus_obj.dyna_flow_task_type_id == \
            new_bus_obj.dyna_flow_task_type_id

        assert fk_bus_obj.code == \
            new_bus_obj.dyna_flow_task_type_code_peek
    # isCanceled
    # isCancelRequested
    # isCompleted
    # isParallelRunAllowed
    # isRunTaskDebugRequired
    # isStarted
    # isSuccessful
    # maxRetryCount
    # minStartUTCDateTime
    # param1
    # param2
    # processorIdentifier
    # requestedUTCDateTime
    # resultValue
    # retryCount
    # startedUTCDateTime
