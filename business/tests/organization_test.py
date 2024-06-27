# business/tests/organization_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
OrganizationBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio

import models
from models.factory import (
    OrganizationFactory)
from business.organization import (
    OrganizationBusObj)
from helpers.session_context import SessionContext
from models import (
    Organization)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def organization():
    """
    Fixture that returns a mock
    organization object.
    """
    return Mock(spec=Organization)


@pytest.fixture
def obj_list():
    """
    Return a list of mock Organization objects.
    """
    organizations = []
    for _ in range(3):
        organization = Mock(spec=Organization)
        organizations.append(organization)
    return organizations


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the Organization class.
    """

    return await OrganizationFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> OrganizationBusObj:
    """
    Fixture that returns a new instance of
    the Organization class.
    """

    session_context = SessionContext(dict(), session)
    organization_bus_obj = OrganizationBusObj(session_context, new_obj)

    return organization_bus_obj


class TestOrganizationBusObj:
    """
    Unit tests for the
    OrganizationBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.organization"
                ".OrganizationBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                OrganizationBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, OrganizationBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, organization in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(organization)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            OrganizationBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # name,
    # TacID

    @pytest.mark.asyncio
    async def test_get_tac_id_obj(
        self, new_bus_obj: OrganizationBusObj
    ):
        """
        Test the get_tac_id_obj method.
        """

        # Call the get_tac_id_bus_obj method
        fk_obj: models.Tac = await \
            new_bus_obj.get_tac_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Tac)

        assert fk_obj.tac_id == \
            new_bus_obj.tac_id

        assert fk_obj.code == \
            new_bus_obj.tac_code_peek

    @pytest.mark.asyncio
    async def test_get_tac_id_bus_obj(
        self, new_bus_obj: OrganizationBusObj
    ):
        """
        Test the get_tac_id_bus_obj method.
        """
        from ..tac import (  # TacID
            TacBusObj)
        # Call the get_tac_id_bus_obj method
        fk_bus_obj: TacBusObj = await \
            new_bus_obj.get_tac_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, TacBusObj)

        assert fk_bus_obj.tac_id == \
            new_bus_obj.tac_id

        assert fk_bus_obj.code == \
            new_bus_obj.tac_code_peek
