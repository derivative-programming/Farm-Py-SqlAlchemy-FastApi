# business/tests/date_greater_than_filter_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-lines
"""
Unit tests for the
DateGreaterThanFilterBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.date_greater_than_filter import DateGreaterThanFilterBusObj
from helpers.session_context import SessionContext
from models import DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def date_greater_than_filter():
    """
    Fixture that returns a mock
    date_greater_than_filter object.
    """
    return Mock(spec=DateGreaterThanFilter)


@pytest.fixture
def obj_list():
    """
    Return a list of mock DateGreaterThanFilter objects.
    """
    date_greater_than_filters = []
    for _ in range(3):
        date_greater_than_filter = Mock(spec=DateGreaterThanFilter)
        date_greater_than_filters.append(date_greater_than_filter)
    return date_greater_than_filters


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the DateGreaterThanFilter class.
    """

    return await DateGreaterThanFilterFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> DateGreaterThanFilterBusObj:
    """
    Fixture that returns a new instance of
    the DateGreaterThanFilter class.
    """

    session_context = SessionContext({}, session)
    date_greater_than_filter_bus_obj = DateGreaterThanFilterBusObj(
        session_context, new_obj)

    return date_greater_than_filter_bus_obj


class TestDateGreaterThanFilterBusObj:
    """
    Unit tests for the
    DateGreaterThanFilterBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.date_greater_than_filter"
                ".DateGreaterThanFilterBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                DateGreaterThanFilterBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, DateGreaterThanFilterBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, date_greater_than_filter in \
                    zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(date_greater_than_filter)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            DateGreaterThanFilterBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # dayCount
    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    @pytest.mark.asyncio
    async def test_get_pac_id_obj(
        self, new_bus_obj: DateGreaterThanFilterBusObj
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
        self, new_bus_obj: DateGreaterThanFilterBusObj
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
