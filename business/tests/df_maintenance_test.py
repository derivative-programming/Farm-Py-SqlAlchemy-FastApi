# business/tests/df_maintenance_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-lines
"""
Unit tests for the
DFMaintenanceBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.df_maintenance import DFMaintenanceBusObj
from helpers.session_context import SessionContext
from models import DFMaintenance
from models.factory import DFMaintenanceFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def df_maintenance():
    """
    Fixture that returns a mock
    df_maintenance object.
    """
    return Mock(spec=DFMaintenance)


@pytest.fixture
def obj_list():
    """
    Return a list of mock DFMaintenance objects.
    """
    df_maintenances = []
    for _ in range(3):
        df_maintenance = Mock(spec=DFMaintenance)
        df_maintenances.append(df_maintenance)
    return df_maintenances


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the DFMaintenance class.
    """

    return await DFMaintenanceFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> DFMaintenanceBusObj:
    """
    Fixture that returns a new instance of
    the DFMaintenance class.
    """

    session_context = SessionContext({}, session)
    df_maintenance_bus_obj = DFMaintenanceBusObj(
        session_context, new_obj)

    return df_maintenance_bus_obj


class TestDFMaintenanceBusObj:
    """
    Unit tests for the
    DFMaintenanceBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.df_maintenance"
                ".DFMaintenanceBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                DFMaintenanceBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, DFMaintenanceBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, df_maintenance in \
                    zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(df_maintenance)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            DFMaintenanceBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # isPaused
    # isScheduledDFProcessRequestCompleted
    # isScheduledDFProcessRequestStarted
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
    # PacID

    @pytest.mark.asyncio
    async def test_get_pac_id_obj(
        self, new_bus_obj: DFMaintenanceBusObj
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
        self, new_bus_obj: DFMaintenanceBusObj
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
    # pausedByUsername
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier
