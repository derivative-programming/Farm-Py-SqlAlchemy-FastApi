# business/tests/dyna_flow_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
DynaFlowBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio

import models
from models.factory import (
    DynaFlowFactory)
from business.dyna_flow import (
    DynaFlowBusObj)
from helpers.session_context import SessionContext
from models import (
    DynaFlow)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def dyna_flow():
    """
    Fixture that returns a mock
    dyna_flow object.
    """
    return Mock(spec=DynaFlow)


@pytest.fixture
def obj_list():
    """
    Return a list of mock DynaFlow objects.
    """
    dyna_flows = []
    for _ in range(3):
        dyna_flow = Mock(spec=DynaFlow)
        dyna_flows.append(dyna_flow)
    return dyna_flows


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the DynaFlow class.
    """

    return await DynaFlowFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> DynaFlowBusObj:
    """
    Fixture that returns a new instance of
    the DynaFlow class.
    """

    session_context = SessionContext(dict(), session)
    dyna_flow_bus_obj = DynaFlowBusObj(session_context, new_obj)

    return dyna_flow_bus_obj


class TestDynaFlowBusObj:
    """
    Unit tests for the
    DynaFlowBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.dyna_flow"
                ".DynaFlowBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                DynaFlowBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, DynaFlowBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, dyna_flow in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(dyna_flow)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            DynaFlowBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # completedUTCDateTime
    # dependencyDynaFlowID,
    # description,
    # DynaFlowTypeID

    @pytest.mark.asyncio
    async def test_get_dyna_flow_type_id_obj(
        self, new_bus_obj: DynaFlowBusObj
    ):
        """
        Test the get_dyna_flow_type_id_obj method.
        """

        # Call the get_dyna_flow_type_id_obj method
        fk_obj: models.DynaFlowType = \
            await new_bus_obj.get_dyna_flow_type_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.DynaFlowType)

        assert fk_obj.dyna_flow_type_id == \
            new_bus_obj.dyna_flow_type_id

        assert fk_obj.code == \
            new_bus_obj.dyna_flow_type_code_peek

    @pytest.mark.asyncio
    async def test_get_dyna_flow_type_id_bus_obj(
        self, new_bus_obj: DynaFlowBusObj
    ):
        """
        Test the get_dyna_flow_type_id_bus_obj
        method.
        """

        from ..dyna_flow_type import (  # DynaFlowTypeID
            DynaFlowTypeBusObj)
        # Call the get_dyna_flow_type_id_bus_obj method
        fk_bus_obj: DynaFlowTypeBusObj = \
            await new_bus_obj.get_dyna_flow_type_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, DynaFlowTypeBusObj)

        assert fk_bus_obj.dyna_flow_type_id == \
            new_bus_obj.dyna_flow_type_id

        assert fk_bus_obj.code == \
            new_bus_obj.dyna_flow_type_code_peek
    # isBuildTaskDebugRequired,
    # isCanceled,
    # isCancelRequested,
    # isCompleted,
    # isPaused,
    # isResubmitted,
    # isRunTaskDebugRequired,
    # isStarted,
    # isSuccessful,
    # isTaskCreationStarted,
    # isTasksCreated,
    # minStartUTCDateTime
    # PacID

    @pytest.mark.asyncio
    async def test_get_pac_id_obj(
        self, new_bus_obj: DynaFlowBusObj
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
        self, new_bus_obj: DynaFlowBusObj
    ):
        """
        Test the get_pac_id_bus_obj method.
        """
        from ..pac import (  # PacID
            PacBusObj)
        # Call the get_pac_id_bus_obj method
        fk_bus_obj: PacBusObj = await \
            new_bus_obj.get_pac_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, PacBusObj)

        assert fk_bus_obj.pac_id == \
            new_bus_obj.pac_id

        assert fk_bus_obj.code == \
            new_bus_obj.pac_code_peek
    # param1,
    # parentDynaFlowID,
    # priorityLevel,
    # requestedUTCDateTime
    # resultValue,
    # rootDynaFlowID,
    # startedUTCDateTime
    # subjectCode,
    # taskCreationProcessorIdentifier,
