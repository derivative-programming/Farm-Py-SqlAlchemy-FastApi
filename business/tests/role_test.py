# business/tests/role_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-lines
"""
Unit tests for the
RoleBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.role import RoleBusObj
from helpers.session_context import SessionContext
from models import Role
from models.factory import RoleFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def role():
    """
    Fixture that returns a mock
    role object.
    """
    return Mock(spec=Role)


@pytest.fixture
def obj_list():
    """
    Return a list of mock Role objects.
    """
    roles = []
    for _ in range(3):
        role = Mock(spec=Role)
        roles.append(role)
    return roles


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the Role class.
    """

    return await RoleFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> RoleBusObj:
    """
    Fixture that returns a new instance of
    the Role class.
    """

    session_context = SessionContext({}, session)
    role_bus_obj = RoleBusObj(
        session_context, new_obj)

    return role_bus_obj


class TestRoleBusObj:
    """
    Unit tests for the
    RoleBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.role"
                ".RoleBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                RoleBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, RoleBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, role in \
                    zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(role)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            RoleBusObj.to_bus_obj_list(
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
        self, new_bus_obj: RoleBusObj
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
        self, new_bus_obj: RoleBusObj
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
