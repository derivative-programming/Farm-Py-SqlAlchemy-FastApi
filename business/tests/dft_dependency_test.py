# business/tests/dft_dependency_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import
"""
Unit tests for the
DFTDependencyBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio

import models
import pytest
from business.dft_dependency import DFTDependencyBusObj
from helpers.session_context import SessionContext
from models import DFTDependency
from models.factory import DFTDependencyFactory


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def dft_dependency():
    """
    Fixture that returns a mock
    dft_dependency object.
    """
    return Mock(spec=DFTDependency)


@pytest.fixture
def obj_list():
    """
    Return a list of mock DFTDependency objects.
    """
    dft_dependencys = []
    for _ in range(3):
        dft_dependency = Mock(spec=DFTDependency)
        dft_dependencys.append(dft_dependency)
    return dft_dependencys


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the DFTDependency class.
    """

    return await DFTDependencyFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> DFTDependencyBusObj:
    """
    Fixture that returns a new instance of
    the DFTDependency class.
    """

    session_context = SessionContext({}, session)
    dft_dependency_bus_obj = DFTDependencyBusObj(session_context, new_obj)

    return dft_dependency_bus_obj


class TestDFTDependencyBusObj:
    """
    Unit tests for the
    DFTDependencyBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.dft_dependency"
                ".DFTDependencyBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                DFTDependencyBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, DFTDependencyBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, dft_dependency in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(dft_dependency)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            DFTDependencyBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # dependencyDFTaskID,
    # DynaFlowTaskID

    @pytest.mark.asyncio
    async def test_get_dyna_flow_task_id_obj(
        self, new_bus_obj: DFTDependencyBusObj
    ):
        """
        Test the get_dyna_flow_task_id_obj method.
        """

        # Call the get_dyna_flow_task_id_bus_obj method
        fk_obj: models.DynaFlowTask = await \
            new_bus_obj.get_dyna_flow_task_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.DynaFlowTask)

        assert fk_obj.dyna_flow_task_id == \
            new_bus_obj.dyna_flow_task_id

        assert fk_obj.code == \
            new_bus_obj.dyna_flow_task_code_peek

    @pytest.mark.asyncio
    async def test_get_dyna_flow_task_id_bus_obj(
        self, new_bus_obj: DFTDependencyBusObj
    ):
        """
        Test the get_dyna_flow_task_id_bus_obj method.
        """
        from business.dyna_flow_task import DynaFlowTaskBusObj  # DynaFlowTaskID

        # Call the get_dyna_flow_task_id_bus_obj method
        fk_bus_obj: DynaFlowTaskBusObj = await \
            new_bus_obj.get_dyna_flow_task_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, DynaFlowTaskBusObj)

        assert fk_bus_obj.dyna_flow_task_id == \
            new_bus_obj.dyna_flow_task_id

        assert fk_bus_obj.code == \
            new_bus_obj.dyna_flow_task_code_peek
    # isPlaceholder,
