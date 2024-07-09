# business/tests/dyna_flow_type_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-lines
"""
Unit tests for the
DynaFlowTypeBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.dyna_flow_type import DynaFlowTypeBusObj
from helpers.session_context import SessionContext
from models import DynaFlowType
from models.factory import DynaFlowTypeFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def dyna_flow_type():
    """
    Fixture that returns a mock
    dyna_flow_type object.
    """
    return Mock(spec=DynaFlowType)


@pytest.fixture
def obj_list():
    """
    Return a list of mock DynaFlowType objects.
    """
    dyna_flow_types = []
    for _ in range(3):
        dyna_flow_type = Mock(spec=DynaFlowType)
        dyna_flow_types.append(dyna_flow_type)
    return dyna_flow_types


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the DynaFlowType class.
    """

    return await DynaFlowTypeFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> DynaFlowTypeBusObj:
    """
    Fixture that returns a new instance of
    the DynaFlowType class.
    """

    session_context = SessionContext({}, session)
    dyna_flow_type_bus_obj = DynaFlowTypeBusObj(
        session_context, new_obj)

    return dyna_flow_type_bus_obj


class TestDynaFlowTypeBusObj:
    """
    Unit tests for the
    DynaFlowTypeBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.dyna_flow_type"
                ".DynaFlowTypeBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                DynaFlowTypeBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, DynaFlowTypeBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, dyna_flow_type in \
                    zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(dyna_flow_type)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            DynaFlowTypeBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    @pytest.mark.asyncio
    async def test_get_pac_id_obj(
        self, new_bus_obj: DynaFlowTypeBusObj
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
        self, new_bus_obj: DynaFlowTypeBusObj
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
    # priorityLevel
