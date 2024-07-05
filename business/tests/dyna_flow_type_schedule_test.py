# business/tests/dyna_flow_type_schedule_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
DynaFlowTypeScheduleBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio

import models
from models.factory import (
    DynaFlowTypeScheduleFactory)
from business.dyna_flow_type_schedule import (
    DynaFlowTypeScheduleBusObj)
from helpers.session_context import SessionContext
from models import (
    DynaFlowTypeSchedule)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def dyna_flow_type_schedule():
    """
    Fixture that returns a mock
    dyna_flow_type_schedule object.
    """
    return Mock(spec=DynaFlowTypeSchedule)


@pytest.fixture
def obj_list():
    """
    Return a list of mock DynaFlowTypeSchedule objects.
    """
    dyna_flow_type_schedules = []
    for _ in range(3):
        dyna_flow_type_schedule = Mock(spec=DynaFlowTypeSchedule)
        dyna_flow_type_schedules.append(dyna_flow_type_schedule)
    return dyna_flow_type_schedules


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the DynaFlowTypeSchedule class.
    """

    return await DynaFlowTypeScheduleFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> DynaFlowTypeScheduleBusObj:
    """
    Fixture that returns a new instance of
    the DynaFlowTypeSchedule class.
    """

    session_context = SessionContext({}, session)
    dyna_flow_type_schedule_bus_obj = DynaFlowTypeScheduleBusObj(session_context, new_obj)

    return dyna_flow_type_schedule_bus_obj


class TestDynaFlowTypeScheduleBusObj:
    """
    Unit tests for the
    DynaFlowTypeScheduleBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.dyna_flow_type_schedule"
                ".DynaFlowTypeScheduleBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                DynaFlowTypeScheduleBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, DynaFlowTypeScheduleBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, dyna_flow_type_schedule in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(dyna_flow_type_schedule)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            DynaFlowTypeScheduleBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # DynaFlowTypeID

    @pytest.mark.asyncio
    async def test_get_dyna_flow_type_id_obj(
        self, new_bus_obj: DynaFlowTypeScheduleBusObj
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
        self, new_bus_obj: DynaFlowTypeScheduleBusObj
    ):
        """
        Test the get_dyna_flow_type_id_bus_obj
        method.
        """

        from business.dyna_flow_type import (  # DynaFlowTypeID
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
    # frequencyInHours,
    # isActive,
    # lastUTCDateTime
    # nextUTCDateTime
    # PacID

    @pytest.mark.asyncio
    async def test_get_pac_id_obj(
        self, new_bus_obj: DynaFlowTypeScheduleBusObj
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
        self, new_bus_obj: DynaFlowTypeScheduleBusObj
    ):
        """
        Test the get_pac_id_bus_obj method.
        """
        from business.pac import (  # PacID
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
