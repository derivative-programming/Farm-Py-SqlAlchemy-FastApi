# business/tests/tri_state_filter_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
TriStateFilterBusObj class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
from business.tri_state_filter_base import (
    TriStateFilterBaseBusObj)
from helpers.session_context import SessionContext
from managers.tri_state_filter import (
    TriStateFilterManager)
from models import TriStateFilter
from models.factory import (
    TriStateFilterFactory)
from services.logging_config import get_logger

from ..tri_state_filter import TriStateFilterBusObj


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
def tri_state_filter():
    """
    Fixture that returns a mock
    tri_state_filter object.
    """
    return Mock(spec=TriStateFilter)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, tri_state_filter
):
    """
    Fixture that returns a
    TriStateFilterBaseBusObj instance.
    """
    mock_sess_base_bus_obj = TriStateFilterBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.tri_state_filter = \
        tri_state_filter
    return mock_sess_base_bus_obj


class TestTriStateFilterBaseBusObj:
    """
    Unit tests for the
    TriStateFilterBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        TriStateFilterManager class.
        """
        session_context = SessionContext(dict(), session)
        return TriStateFilterManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        TriStateFilterBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return TriStateFilterBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the TriStateFilter class.
        """

        return await TriStateFilterFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_tri_state_filter(
        self,
        new_bus_obj: TriStateFilterBusObj
    ):
        """
        Test case for creating a new tri_state_filter.
        """
        # Test creating a new tri_state_filter

        assert new_bus_obj.tri_state_filter_id == 0

        # assert isinstance(new_bus_obj.tri_state_filter_id, int)
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
        assert isinstance(new_bus_obj.state_int_value,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_obj(
        self,
        obj_manager: TriStateFilterManager,
        new_bus_obj: TriStateFilterBusObj,
        new_obj: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.tri_state_filter, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_id(
        self,
        obj_manager: TriStateFilterManager,
        new_bus_obj: TriStateFilterBusObj,
        new_obj: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter ID.
        """

        new_obj_tri_state_filter_id = \
            new_obj.tri_state_filter_id

        await new_bus_obj.load_from_id(
            new_obj_tri_state_filter_id)

        assert obj_manager.is_equal(
            new_bus_obj.tri_state_filter, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_code(
        self,
        obj_manager: TriStateFilterManager,
        new_bus_obj: TriStateFilterBusObj,
        new_obj: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.tri_state_filter, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_json(
        self,
        obj_manager: TriStateFilterManager,
        new_bus_obj: TriStateFilterBusObj,
        new_obj: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter JSON.
        """

        tri_state_filter_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            tri_state_filter_json)

        assert obj_manager.is_equal(
            new_bus_obj.tri_state_filter, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_dict(
        self,
        obj_manager: TriStateFilterManager,
        new_bus_obj: TriStateFilterBusObj,
        new_obj: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter dictionary.
        """

        logger.info("test_load_with_tri_state_filter_dict 1")

        tri_state_filter_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(tri_state_filter_dict)

        await new_bus_obj.load_from_dict(
            tri_state_filter_dict)

        assert obj_manager.is_equal(
            new_bus_obj.tri_state_filter,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_tri_state_filter(
        self,
        new_bus_obj: TriStateFilterBusObj
    ):
        """
        Test case for retrieving a nonexistent
        tri_state_filter.
        """
        # Test retrieving a nonexistent
        # tri_state_filter raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_tri_state_filter(
        self,
        obj_manager: TriStateFilterManager,
        new_bus_obj: TriStateFilterBusObj,
        new_obj: TriStateFilter
    ):
        """
        Test case for updating a tri_state_filter's data.
        """
        # Test updating a tri_state_filter's data

        new_obj_tri_state_filter_id_value = \
            new_obj.tri_state_filter_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_tri_state_filter_id_value)

        assert isinstance(new_obj,
                          TriStateFilter)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.tri_state_filter,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_tri_state_filter_id_value = \
            new_obj.tri_state_filter_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_tri_state_filter_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.tri_state_filter,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_tri_state_filter(
        self,
        obj_manager: TriStateFilterManager,
        new_bus_obj: TriStateFilterBusObj,
        new_obj: TriStateFilter
    ):
        """
        Test case for deleting a tri_state_filter.
        """

        assert new_bus_obj.tri_state_filter is not None

        assert new_bus_obj.tri_state_filter_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.tri_state_filter_id is not None

        await new_bus_obj.delete()

        new_obj_tri_state_filter_id_value = \
            new_obj.tri_state_filter_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_tri_state_filter_id_value)

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
        tri_state_filter
    ):
        """
        Test case for refreshing the tri_state_filter data.
        """
        with patch(
            "business.tri_state_filter_base"
            ".TriStateFilterManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=tri_state_filter)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .tri_state_filter == tri_state_filter
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(tri_state_filter)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the tri_state_filter data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.tri_state_filter = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the tri_state_filter
        data to a dictionary.
        """
        with patch(
            "business.tri_state_filter_base"
            ".TriStateFilterManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            tri_state_filter_dict = mock_sess_base_bus_obj.to_dict()
            assert tri_state_filter_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.tri_state_filter)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the tri_state_filter data to JSON.
        """
        with patch(
            "business.tri_state_filter_base"
            ".TriStateFilterManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            tri_state_filter_json = mock_sess_base_bus_obj.to_json()
            assert tri_state_filter_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.tri_state_filter)

    def test_get_obj(
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for getting the tri_state_filter object.
        """
        assert mock_sess_base_bus_obj.get_obj() == tri_state_filter

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "tri_state_filter"

    def test_get_id(
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for getting the tri_state_filter ID.
        """
        tri_state_filter.tri_state_filter_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_tri_state_filter_id(
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the tri_state_filter_id property.
        """
        tri_state_filter.tri_state_filter_id = 1
        assert mock_sess_base_bus_obj.tri_state_filter_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        tri_state_filter.code = test_uuid
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
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the TriStateFilterBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (TriStateFilterBaseBusiness):
                An instance of the
                TriStateFilterBaseBusiness class.
            tri_state_filter (TriStateFilter):
                An instance of the
                TriStateFilter class.

        Returns:
            None
        """
        tri_state_filter.last_change_code = 123
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
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        tri_state_filter.insert_user_id = test_uuid
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
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the
        description property.
        """
        tri_state_filter.description = \
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
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the
        display_order property.
        """
        tri_state_filter.display_order = 1
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
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the
        is_active property.
        """
        tri_state_filter.is_active = True
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
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the
        lookup_enum_name property.
        """
        tri_state_filter.lookup_enum_name = \
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
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the
        name property.
        """
        tri_state_filter.name = \
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
    # stateIntValue

    def test_state_int_value(
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the
        state_int_value property.
        """
        tri_state_filter.state_int_value = 1
        assert mock_sess_base_bus_obj \
            .state_int_value == 1

    def test_state_int_value_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        state_int_value setter.
        """
        mock_sess_base_bus_obj.state_int_value = 1
        assert mock_sess_base_bus_obj \
            .state_int_value == 1

    def test_state_int_value_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        state_int_value property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.state_int_value = \
                "not-an-int"
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_pac_id(
            self, mock_sess_base_bus_obj, tri_state_filter):
        """
        Test case for the pac_id property.
        """
        tri_state_filter.pac_id = 1
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
    # stateIntValue,

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            tri_state_filter):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        tri_state_filter.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
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
            tri_state_filter):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        tri_state_filter.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
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
