# business/tests/dft_dependency_base_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
DFTDependencyBusObj class.
"""

import math  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
import pytest
from business.dft_dependency_base import DFTDependencyBaseBusObj
from helpers.session_context import SessionContext
from managers.dft_dependency import DFTDependencyManager
from models import DFTDependency
from models.factory import DFTDependencyFactory
from services.logging_config import get_logger

from ..dft_dependency import DFTDependencyBusObj


BUSINESS_DFT_DEPENDENCY_BASE_MANAGER_PATCH = (
    "business.dft_dependency_base"
    ".DFTDependencyManager"
)

logger = get_logger(__name__)


@pytest.fixture
def mock_session_context():
    """
    Fixture that returns a fake session context.
    """
    session = Mock()
    session_context = Mock(spec=SessionContext)
    session_context.session = session
    return session_context


@pytest.fixture
def dft_dependency():
    """
    Fixture that returns a mock
    dft_dependency object.
    """
    return Mock(spec=DFTDependency)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, dft_dependency
):
    """
    Fixture that returns a
    DFTDependencyBaseBusObj instance.
    """
    mock_sess_base_bus_obj = DFTDependencyBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.dft_dependency = \
        dft_dependency
    return mock_sess_base_bus_obj


class TestDFTDependencyBaseBusObj:
    """
    Unit tests for the
    DFTDependencyBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        DFTDependencyManager class.
        """
        session_context = SessionContext({}, session)
        return DFTDependencyManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        DFTDependencyBusObj class.
        """
        session_context = SessionContext({}, session)
        return DFTDependencyBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the DFTDependency class.
        """

        return await DFTDependencyFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_dft_dependency(
        self,
        new_bus_obj: DFTDependencyBusObj
    ):
        """
        Test case for creating a new dft_dependency.
        """
        # Test creating a new dft_dependency

        assert new_bus_obj.dft_dependency_id == 0

        assert isinstance(new_bus_obj.dft_dependency_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.dependency_df_task_id,
                          int)
        assert isinstance(new_bus_obj.dyna_flow_task_id,
                          int)
        assert isinstance(new_bus_obj.is_placeholder,
                          bool)

    @pytest.mark.asyncio
    async def test_load_with_dft_dependency_obj(
        self,
        obj_manager: DFTDependencyManager,
        new_bus_obj: DFTDependencyBusObj,
        new_obj: DFTDependency
    ):
        """
        Test case for loading data from a
        dft_dependency object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.dft_dependency, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dft_dependency_id(
        self,
        obj_manager: DFTDependencyManager,
        new_bus_obj: DFTDependencyBusObj,
        new_obj: DFTDependency
    ):
        """
        Test case for loading data from a
        dft_dependency ID.
        """

        new_obj_dft_dependency_id = \
            new_obj.dft_dependency_id

        await new_bus_obj.load_from_id(
            new_obj_dft_dependency_id)

        assert obj_manager.is_equal(
            new_bus_obj.dft_dependency, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dft_dependency_code(
        self,
        obj_manager: DFTDependencyManager,
        new_bus_obj: DFTDependencyBusObj,
        new_obj: DFTDependency
    ):
        """
        Test case for loading data from a
        dft_dependency code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.dft_dependency, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dft_dependency_json(
        self,
        obj_manager: DFTDependencyManager,
        new_bus_obj: DFTDependencyBusObj,
        new_obj: DFTDependency
    ):
        """
        Test case for loading data from a
        dft_dependency JSON.
        """

        dft_dependency_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            dft_dependency_json)

        assert obj_manager.is_equal(
            new_bus_obj.dft_dependency, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dft_dependency_dict(
        self,
        obj_manager: DFTDependencyManager,
        new_bus_obj: DFTDependencyBusObj,
        new_obj: DFTDependency
    ):
        """
        Test case for loading data from a
        dft_dependency dictionary.
        """

        logger.info("test_load_with_dft_dependency_dict 1")

        dft_dependency_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(dft_dependency_dict)

        await new_bus_obj.load_from_dict(
            dft_dependency_dict)

        assert obj_manager.is_equal(
            new_bus_obj.dft_dependency,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_dft_dependency(
        self,
        new_bus_obj: DFTDependencyBusObj
    ):
        """
        Test case for retrieving a nonexistent
        dft_dependency.
        """
        # Test retrieving a nonexistent
        # dft_dependency raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_dft_dependency(
        self,
        obj_manager: DFTDependencyManager,
        new_bus_obj: DFTDependencyBusObj,
        new_obj: DFTDependency
    ):
        """
        Test case for updating a dft_dependency's data.
        """
        # Test updating a dft_dependency's data

        new_obj_dft_dependency_id_value = \
            new_obj.dft_dependency_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dft_dependency_id_value)

        assert isinstance(new_obj,
                          DFTDependency)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.dft_dependency,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_dft_dependency_id_value = \
            new_obj.dft_dependency_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dft_dependency_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.dft_dependency,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_dft_dependency(
        self,
        obj_manager: DFTDependencyManager,
        new_bus_obj: DFTDependencyBusObj,
        new_obj: DFTDependency
    ):
        """
        Test case for deleting a dft_dependency.
        """

        assert new_bus_obj.dft_dependency is not None

        assert new_bus_obj.dft_dependency_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.dft_dependency_id is not None

        await new_bus_obj.delete()

        new_obj_dft_dependency_id_value = \
            new_obj.dft_dependency_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dft_dependency_id_value)

        assert new_obj is None

    def test_get_session_context(
        self,
        mock_sess_base_bus_obj,
        mock_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert mock_sess_base_bus_obj.get_session_context() == \
            mock_session_context

    @pytest.mark.asyncio
    async def test_refresh(
        self,
        mock_sess_base_bus_obj,
        dft_dependency
    ):
        """
        Test case for refreshing the dft_dependency data.
        """
        with patch(
            BUSINESS_DFT_DEPENDENCY_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=dft_dependency)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .dft_dependency == dft_dependency
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(dft_dependency)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the dft_dependency data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.dft_dependency = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the dft_dependency
        data to a dictionary.
        """
        with patch(
            BUSINESS_DFT_DEPENDENCY_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            dft_dependency_dict = mock_sess_base_bus_obj.to_dict()
            assert dft_dependency_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.dft_dependency)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the dft_dependency data to JSON.
        """
        with patch(
            BUSINESS_DFT_DEPENDENCY_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            dft_dependency_json = mock_sess_base_bus_obj.to_json()
            assert dft_dependency_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.dft_dependency)

    def test_get_obj(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case for getting the dft_dependency object.
        """
        assert mock_sess_base_bus_obj.get_obj() == dft_dependency

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "dft_dependency"

    def test_get_id(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case for getting the dft_dependency ID.
        """
        dft_dependency.dft_dependency_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_dft_dependency_id(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case for the dft_dependency_id property.
        """
        dft_dependency.dft_dependency_id = 1
        assert mock_sess_base_bus_obj.dft_dependency_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        dft_dependency.code = test_uuid
        assert mock_sess_base_bus_obj.code == \
            test_uuid

    def test_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.code = test_uuid
        assert mock_sess_base_bus_obj.code == \
            test_uuid

    def test_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the DFTDependencyBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (DFTDependencyBaseBusiness):
                An instance of the
                DFTDependencyBaseBusiness class.
            dft_dependency (DFTDependency):
                An instance of the
                DFTDependency class.

        Returns:
            None
        """
        dft_dependency.last_change_code = 123
        assert mock_sess_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_change_code setter.
        """
        mock_sess_base_bus_obj.last_change_code = 123
        assert mock_sess_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        dft_dependency.insert_user_id = test_uuid
        assert mock_sess_base_bus_obj.insert_user_id == \
            test_uuid

    def test_insert_user_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.insert_user_id = test_uuid
        assert mock_sess_base_bus_obj.insert_user_id == \
            test_uuid

    def test_insert_user_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.insert_user_id = "not-a-uuid"
    # dependencyDFTaskID

    def test_dependency_df_task_id(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case for the
        dependency_df_task_id property.
        """
        dft_dependency.dependency_df_task_id = 1
        assert mock_sess_base_bus_obj \
            .dependency_df_task_id == 1

    def test_dependency_df_task_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        dependency_df_task_id setter.
        """
        mock_sess_base_bus_obj.dependency_df_task_id = 1
        assert mock_sess_base_bus_obj \
            .dependency_df_task_id == 1

    def test_dependency_df_task_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        dependency_df_task_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.dependency_df_task_id = \
                "not-an-int"
    # DynaFlowTaskID
    # isPlaceholder

    def test_is_placeholder(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case for the
        is_placeholder property.
        """
        dft_dependency.is_placeholder = True
        assert mock_sess_base_bus_obj \
            .is_placeholder is True

    def test_is_placeholder_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_placeholder setter.
        """
        mock_sess_base_bus_obj.is_placeholder = \
            True
        assert mock_sess_base_bus_obj \
            .is_placeholder is True

    def test_is_placeholder_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_placeholder property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_placeholder = \
                "not-a-boolean"
    # dependencyDFTaskID,
    # DynaFlowTaskID

    def test_dyna_flow_task_id(
            self, mock_sess_base_bus_obj, dft_dependency):
        """
        Test case for the dyna_flow_task_id property.
        """
        dft_dependency.dyna_flow_task_id = 1
        assert mock_sess_base_bus_obj \
            .dyna_flow_task_id == 1

    def test_dyna_flow_task_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the dyna_flow_task_id setter.
        """
        mock_sess_base_bus_obj.dyna_flow_task_id = 1
        assert mock_sess_base_bus_obj \
            .dyna_flow_task_id == 1

    def test_dyna_flow_task_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        dyna_flow_task_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.dyna_flow_task_id = \
                "not-an-int"
    # isPlaceholder,

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            dft_dependency):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dft_dependency.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.insert_utc_date_time = \
                "not-a-datetime"

    def test_last_update_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            dft_dependency):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dft_dependency.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_update_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.last_update_utc_date_time = \
                "not-a-datetime"
