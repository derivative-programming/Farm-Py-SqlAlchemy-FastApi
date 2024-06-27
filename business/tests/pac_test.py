# business/tests/pac_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
PacBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio

import models
from models.factory import (
    PacFactory)
from business.pac import (
    PacBusObj)
from helpers.session_context import SessionContext
from models import (
    Pac)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def pac():
    """
    Fixture that returns a mock
    pac object.
    """
    return Mock(spec=Pac)


@pytest.fixture
def obj_list():
    """
    Return a list of mock Pac objects.
    """
    pacs = []
    for _ in range(3):
        pac = Mock(spec=Pac)
        pacs.append(pac)
    return pacs


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the Pac class.
    """

    return await PacFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> PacBusObj:
    """
    Fixture that returns a new instance of
    the Pac class.
    """

    session_context = SessionContext(dict(), session)
    pac_bus_obj = PacBusObj(session_context, new_obj)

    return pac_bus_obj


class TestPacBusObj:
    """
    Unit tests for the
    PacBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.pac"
                ".PacBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                PacBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, PacBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, pac in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(pac)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            PacBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
