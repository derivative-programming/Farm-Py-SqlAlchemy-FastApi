# business/tests/dyna_flow_type_base_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
DynaFlowTypeBusObj class.
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
from business.dyna_flow_type_base import DynaFlowTypeBaseBusObj
from helpers.session_context import SessionContext
from managers.dyna_flow_type import DynaFlowTypeManager
from models import DynaFlowType
from models.factory import DynaFlowTypeFactory
from services.logging_config import get_logger

from ..dyna_flow_type import DynaFlowTypeBusObj


BUSINESS_DYNA_FLOW_TYPE_BASE_MANAGER_PATCH = (
    "business.dyna_flow_type_base"
    ".DynaFlowTypeManager"
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
def dyna_flow_type():
    """
    Fixture that returns a mock
    dyna_flow_type object.
    """
    return Mock(spec=DynaFlowType)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, dyna_flow_type
):
    """
    Fixture that returns a
    DynaFlowTypeBaseBusObj instance.
    """
    mock_sess_base_bus_obj = DynaFlowTypeBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.dyna_flow_type = \
        dyna_flow_type
    return mock_sess_base_bus_obj


class TestDynaFlowTypeBaseBusObj:
    """
    Unit tests for the
    DynaFlowTypeBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        DynaFlowTypeManager class.
        """
        session_context = SessionContext({}, session)
        return DynaFlowTypeManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        DynaFlowTypeBusObj class.
        """
        session_context = SessionContext({}, session)
        return DynaFlowTypeBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the DynaFlowType class.
        """

        return await DynaFlowTypeFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_dyna_flow_type(
        self,
        new_bus_obj: DynaFlowTypeBusObj
    ):
        """
        Test case for creating a new dyna_flow_type.
        """
        # Test creating a new dyna_flow_type

        assert new_bus_obj.dyna_flow_type_id == 0

        assert isinstance(new_bus_obj.dyna_flow_type_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.description,
                          str)
        assert isinstance(new_bus_obj.display_order,
                          int)
        assert isinstance(new_bus_obj.is_active,
                          bool)
        assert isinstance(new_bus_obj.lookup_enum_name,
                          str)
        assert isinstance(new_bus_obj.name,
                          str)
        assert isinstance(new_bus_obj.pac_id,
                          int)
        assert isinstance(new_bus_obj.priority_level,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_obj(
        self,
        obj_manager: DynaFlowTypeManager,
        new_bus_obj: DynaFlowTypeBusObj,
        new_obj: DynaFlowType
    ):
        """
        Test case for loading data from a
        dyna_flow_type object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_id(
        self,
        obj_manager: DynaFlowTypeManager,
        new_bus_obj: DynaFlowTypeBusObj,
        new_obj: DynaFlowType
    ):
        """
        Test case for loading data from a
        dyna_flow_type ID.
        """

        new_obj_dyna_flow_type_id = \
            new_obj.dyna_flow_type_id

        await new_bus_obj.load_from_id(
            new_obj_dyna_flow_type_id)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_code(
        self,
        obj_manager: DynaFlowTypeManager,
        new_bus_obj: DynaFlowTypeBusObj,
        new_obj: DynaFlowType
    ):
        """
        Test case for loading data from a
        dyna_flow_type code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_json(
        self,
        obj_manager: DynaFlowTypeManager,
        new_bus_obj: DynaFlowTypeBusObj,
        new_obj: DynaFlowType
    ):
        """
        Test case for loading data from a
        dyna_flow_type JSON.
        """

        dyna_flow_type_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            dyna_flow_type_json)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_dyna_flow_type_dict(
        self,
        obj_manager: DynaFlowTypeManager,
        new_bus_obj: DynaFlowTypeBusObj,
        new_obj: DynaFlowType
    ):
        """
        Test case for loading data from a
        dyna_flow_type dictionary.
        """

        logger.info("test_load_with_dyna_flow_type_dict 1")

        dyna_flow_type_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(dyna_flow_type_dict)

        await new_bus_obj.load_from_dict(
            dyna_flow_type_dict)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_dyna_flow_type(
        self,
        new_bus_obj: DynaFlowTypeBusObj
    ):
        """
        Test case for retrieving a nonexistent
        dyna_flow_type.
        """
        # Test retrieving a nonexistent
        # dyna_flow_type raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_dyna_flow_type(
        self,
        obj_manager: DynaFlowTypeManager,
        new_bus_obj: DynaFlowTypeBusObj,
        new_obj: DynaFlowType
    ):
        """
        Test case for updating a dyna_flow_type's data.
        """
        # Test updating a dyna_flow_type's data

        new_obj_dyna_flow_type_id_value = \
            new_obj.dyna_flow_type_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_type_id_value)

        assert isinstance(new_obj,
                          DynaFlowType)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_dyna_flow_type_id_value = \
            new_obj.dyna_flow_type_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_type_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.dyna_flow_type,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_dyna_flow_type(
        self,
        obj_manager: DynaFlowTypeManager,
        new_bus_obj: DynaFlowTypeBusObj,
        new_obj: DynaFlowType
    ):
        """
        Test case for deleting a dyna_flow_type.
        """

        assert new_bus_obj.dyna_flow_type is not None

        assert new_bus_obj.dyna_flow_type_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.dyna_flow_type_id is not None

        await new_bus_obj.delete()

        new_obj_dyna_flow_type_id_value = \
            new_obj.dyna_flow_type_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_dyna_flow_type_id_value)

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
        dyna_flow_type
    ):
        """
        Test case for refreshing the dyna_flow_type data.
        """
        with patch(
            BUSINESS_DYNA_FLOW_TYPE_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=dyna_flow_type)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .dyna_flow_type == dyna_flow_type
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(dyna_flow_type)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the dyna_flow_type data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.dyna_flow_type = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the dyna_flow_type
        data to a dictionary.
        """
        with patch(
            BUSINESS_DYNA_FLOW_TYPE_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            dyna_flow_type_dict = mock_sess_base_bus_obj.to_dict()
            assert dyna_flow_type_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.dyna_flow_type)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the dyna_flow_type data to JSON.
        """
        with patch(
            BUSINESS_DYNA_FLOW_TYPE_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            dyna_flow_type_json = mock_sess_base_bus_obj.to_json()
            assert dyna_flow_type_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.dyna_flow_type)

    def test_get_obj(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for getting the dyna_flow_type object.
        """
        assert mock_sess_base_bus_obj.get_obj() == dyna_flow_type

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "dyna_flow_type"

    def test_get_id(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for getting the dyna_flow_type ID.
        """
        dyna_flow_type.dyna_flow_type_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_dyna_flow_type_id(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the dyna_flow_type_id property.
        """
        dyna_flow_type.dyna_flow_type_id = 1
        assert mock_sess_base_bus_obj.dyna_flow_type_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        dyna_flow_type.code = test_uuid
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
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the DynaFlowTypeBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (DynaFlowTypeBaseBusiness):
                An instance of the
                DynaFlowTypeBaseBusiness class.
            dyna_flow_type (DynaFlowType):
                An instance of the
                DynaFlowType class.

        Returns:
            None
        """
        dyna_flow_type.last_change_code = 123
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
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        dyna_flow_type.insert_user_id = test_uuid
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
    # description

    def test_description(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the
        description property.
        """
        dyna_flow_type.description = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .description == "Vanilla"

    def test_description_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        description setter.
        """
        mock_sess_base_bus_obj.description = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .description == "Vanilla"

    def test_description_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        description property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.description = \
                123
    # displayOrder

    def test_display_order(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the
        display_order property.
        """
        dyna_flow_type.display_order = 1
        assert mock_sess_base_bus_obj \
            .display_order == 1

    def test_display_order_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        display_order setter.
        """
        mock_sess_base_bus_obj.display_order = 1
        assert mock_sess_base_bus_obj \
            .display_order == 1

    def test_display_order_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        display_order property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.display_order = \
                "not-an-int"
    # isActive

    def test_is_active(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the
        is_active property.
        """
        dyna_flow_type.is_active = True
        assert mock_sess_base_bus_obj \
            .is_active is True

    def test_is_active_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_active setter.
        """
        mock_sess_base_bus_obj.is_active = \
            True
        assert mock_sess_base_bus_obj \
            .is_active is True

    def test_is_active_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_active = \
                "not-a-boolean"
    # lookupEnumName

    def test_lookup_enum_name(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the
        lookup_enum_name property.
        """
        dyna_flow_type.lookup_enum_name = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        lookup_enum_name setter.
        """
        mock_sess_base_bus_obj.lookup_enum_name = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        lookup_enum_name property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.lookup_enum_name = \
                123
    # name

    def test_name(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the
        name property.
        """
        dyna_flow_type.name = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .name == "Vanilla"

    def test_name_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        name setter.
        """
        mock_sess_base_bus_obj.name = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .name == "Vanilla"

    def test_name_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.name = \
                123
    # PacID
    # priorityLevel

    def test_priority_level(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the
        priority_level property.
        """
        dyna_flow_type.priority_level = 1
        assert mock_sess_base_bus_obj \
            .priority_level == 1

    def test_priority_level_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        priority_level setter.
        """
        mock_sess_base_bus_obj.priority_level = 1
        assert mock_sess_base_bus_obj \
            .priority_level == 1

    def test_priority_level_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        priority_level property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.priority_level = \
                "not-an-int"
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_pac_id(
            self, mock_sess_base_bus_obj, dyna_flow_type):
        """
        Test case for the pac_id property.
        """
        dyna_flow_type.pac_id = 1
        assert mock_sess_base_bus_obj \
            .pac_id == 1

    def test_pac_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the pac_id setter.
        """
        mock_sess_base_bus_obj.pac_id = 1
        assert mock_sess_base_bus_obj \
            .pac_id == 1

    def test_pac_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        pac_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.pac_id = \
                "not-an-int"
    # priorityLevel,

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            dyna_flow_type):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow_type.insert_utc_date_time = test_datetime
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
            dyna_flow_type):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        dyna_flow_type.last_update_utc_date_time = test_datetime
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
