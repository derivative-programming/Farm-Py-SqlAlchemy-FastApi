# business/tests/tri_state_filter_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
"""
Unit tests for the
TriStateFilterBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.tri_state_filter import TriStateFilterBusObj
from helpers.session_context import SessionContext
from models import TriStateFilter
from models.factory import TriStateFilterFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def tri_state_filter():
    """
    Fixture that returns a mock
    tri_state_filter object.
    """
    return Mock(spec=TriStateFilter)


@pytest.fixture
def obj_list():
    """
    Return a list of mock TriStateFilter objects.
    """
    tri_state_filters = []
    for _ in range(3):
        tri_state_filter = Mock(spec=TriStateFilter)
        tri_state_filters.append(tri_state_filter)
    return tri_state_filters


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the TriStateFilter class.
    """

    return await TriStateFilterFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> TriStateFilterBusObj:
    """
    Fixture that returns a new instance of
    the TriStateFilter class.
    """

    session_context = SessionContext({}, session)
    tri_state_filter_bus_obj = TriStateFilterBusObj(session_context, new_obj)

    return tri_state_filter_bus_obj


class TestTriStateFilterBusObj:
    """
    Unit tests for the
    TriStateFilterBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.tri_state_filter"
                ".TriStateFilterBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                TriStateFilterBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, TriStateFilterBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, tri_state_filter in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(tri_state_filter)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            TriStateFilterBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    @pytest.mark.asyncio
    async def test_get_pac_id_obj(
        self, new_bus_obj: TriStateFilterBusObj
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
        self, new_bus_obj: TriStateFilterBusObj
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
    # stateIntValue,
