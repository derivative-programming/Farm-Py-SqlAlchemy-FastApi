# business/tests/tri_state_filter_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
TriStateFilterBusObj class.
"""

import uuid  # noqa: F401
import math
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
def fake_session_context():
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
    Fixture that returns a mock tri_state_filter object.
    """
    return Mock(spec=TriStateFilter)


@pytest.fixture
def tri_state_filter_base_bus_obj(
    fake_session_context, tri_state_filter
):
    """
    Fixture that returns a TriStateFilterBaseBusObj instance.
    """
    tri_state_filter_base = TriStateFilterBaseBusObj(
        fake_session_context)
    tri_state_filter_base.tri_state_filter = tri_state_filter
    return tri_state_filter_base


class TestTriStateFilterBaseBusObj:
    """
    Unit tests for the
    TriStateFilterBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def tri_state_filter_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        TriStateFilterManager class.
        """
        session_context = SessionContext(dict(), session)
        return TriStateFilterManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def tri_state_filter_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        TriStateFilterBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return TriStateFilterBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_tri_state_filter(self, session):
        """
        Fixture that returns a new instance of
        the TriStateFilter class.
        """

        return await TriStateFilterFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_tri_state_filter(
        self,
        tri_state_filter_bus_obj: TriStateFilterBusObj
    ):
        """
        Test case for creating a new tri_state_filter.
        """
        # Test creating a new tri_state_filter

        assert tri_state_filter_bus_obj.tri_state_filter_id == 0

        # assert isinstance(tri_state_filter_bus_obj.tri_state_filter_id, int)
        assert isinstance(
            tri_state_filter_bus_obj.code, uuid.UUID)

        assert isinstance(
            tri_state_filter_bus_obj.last_change_code, int)

        assert tri_state_filter_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert tri_state_filter_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(tri_state_filter_bus_obj.description,
                          str)
        assert isinstance(tri_state_filter_bus_obj.display_order,
                          int)
        assert isinstance(tri_state_filter_bus_obj.is_active,
                          bool)
        assert isinstance(tri_state_filter_bus_obj.lookup_enum_name,
                          str)
        assert isinstance(tri_state_filter_bus_obj.name,
                          str)
        assert isinstance(tri_state_filter_bus_obj.pac_id,
                          int)
        assert isinstance(tri_state_filter_bus_obj.state_int_value,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_obj(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter object instance.
        """

        tri_state_filter_bus_obj.load_from_obj_instance(
            new_tri_state_filter)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter, new_tri_state_filter) is True

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_id(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter ID.
        """

        new_tri_state_filter_tri_state_filter_id = \
            new_tri_state_filter.tri_state_filter_id

        await tri_state_filter_bus_obj.load_from_id(
            new_tri_state_filter_tri_state_filter_id)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter, new_tri_state_filter) is True

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_code(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter code.
        """

        await tri_state_filter_bus_obj.load_from_code(
            new_tri_state_filter.code)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter, new_tri_state_filter) is True

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_json(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter JSON.
        """

        tri_state_filter_json = \
            tri_state_filter_manager.to_json(
                new_tri_state_filter)

        await tri_state_filter_bus_obj.load_from_json(
            tri_state_filter_json)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter, new_tri_state_filter) is True

    @pytest.mark.asyncio
    async def test_load_with_tri_state_filter_dict(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for loading data from a
        tri_state_filter dictionary.
        """

        logger.info("test_load_with_tri_state_filter_dict 1")

        tri_state_filter_dict = \
            tri_state_filter_manager.to_dict(
                new_tri_state_filter)

        logger.info(tri_state_filter_dict)

        await tri_state_filter_bus_obj.load_from_dict(
            tri_state_filter_dict)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter,
            new_tri_state_filter) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_tri_state_filter(
        self,
        tri_state_filter_bus_obj: TriStateFilterBusObj
    ):
        """
        Test case for retrieving a nonexistent tri_state_filter.
        """
        # Test retrieving a nonexistent
        # tri_state_filter raises an exception
        await tri_state_filter_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert tri_state_filter_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for updating a tri_state_filter's data.
        """
        # Test updating a tri_state_filter's data

        new_tri_state_filter_tri_state_filter_id_value = new_tri_state_filter.tri_state_filter_id

        new_tri_state_filter = await \
            tri_state_filter_manager.get_by_id(
                new_tri_state_filter_tri_state_filter_id_value)

        assert isinstance(new_tri_state_filter,
                          TriStateFilter)

        new_code = uuid.uuid4()

        tri_state_filter_bus_obj.load_from_obj_instance(
            new_tri_state_filter)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter,
            new_tri_state_filter) is True

        tri_state_filter_bus_obj.code = new_code

        await tri_state_filter_bus_obj.save()

        new_tri_state_filter_tri_state_filter_id_value = new_tri_state_filter.tri_state_filter_id

        new_tri_state_filter = await \
            tri_state_filter_manager.get_by_id(
                new_tri_state_filter_tri_state_filter_id_value)

        assert tri_state_filter_manager.is_equal(
            tri_state_filter_bus_obj.tri_state_filter,
            new_tri_state_filter) is True

    @pytest.mark.asyncio
    async def test_delete_tri_state_filter(
        self,
        tri_state_filter_manager: TriStateFilterManager,
        tri_state_filter_bus_obj: TriStateFilterBusObj,
        new_tri_state_filter: TriStateFilter
    ):
        """
        Test case for deleting a tri_state_filter.
        """

        assert tri_state_filter_bus_obj.tri_state_filter is not None

        assert tri_state_filter_bus_obj.tri_state_filter_id == 0

        tri_state_filter_bus_obj.load_from_obj_instance(
            new_tri_state_filter)

        assert tri_state_filter_bus_obj.tri_state_filter_id is not None

        await tri_state_filter_bus_obj.delete()

        new_tri_state_filter_tri_state_filter_id_value = new_tri_state_filter.tri_state_filter_id

        new_tri_state_filter = await \
            tri_state_filter_manager.get_by_id(
                new_tri_state_filter_tri_state_filter_id_value)

        assert new_tri_state_filter is None

    def test_get_session_context(
        self,
        tri_state_filter_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert tri_state_filter_base_bus_obj.get_session_context() == fake_session_context

    @pytest.mark.asyncio
    async def test_refresh(
        self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for refreshing the tri_state_filter data.
        """
        with patch(
            'business.tri_state_filter_base.TriStateFilterManager',
            autospec=True
        ) as mock_tri_state_filter_manager:
            mock_tri_state_filter_manager_instance = \
                mock_tri_state_filter_manager.return_value
            mock_tri_state_filter_manager_instance.refresh =\
                AsyncMock(return_value=tri_state_filter)

            refreshed_tri_state_filter_base = await tri_state_filter_base_bus_obj.refresh()
            assert refreshed_tri_state_filter_base.tri_state_filter == tri_state_filter
            mock_tri_state_filter_manager_instance.refresh.assert_called_once_with(tri_state_filter)

    def test_is_valid(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for checking if the tri_state_filter data is valid.
        """
        assert tri_state_filter_base_bus_obj.is_valid() is True

        tri_state_filter_base_bus_obj.tri_state_filter = None
        assert tri_state_filter_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for converting the tri_state_filter data to a dictionary.
        """
        with patch(
            'business.tri_state_filter_base.TriStateFilterManager',
            autospec=True
        ) as mock_tri_state_filter_manager:
            mock_tri_state_filter_manager_instance = \
                mock_tri_state_filter_manager.return_value
            mock_tri_state_filter_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            tri_state_filter_dict = tri_state_filter_base_bus_obj.to_dict()
            assert tri_state_filter_dict == {"key": "value"}
            mock_tri_state_filter_manager_instance.to_dict.assert_called_once_with(
                tri_state_filter_base_bus_obj.tri_state_filter)

    def test_to_json(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for converting the tri_state_filter data to JSON.
        """
        with patch(
            'business.tri_state_filter_base.TriStateFilterManager',
            autospec=True
        ) as mock_tri_state_filter_manager:
            mock_tri_state_filter_manager_instance = \
                mock_tri_state_filter_manager.return_value
            mock_tri_state_filter_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            tri_state_filter_json = tri_state_filter_base_bus_obj.to_json()
            assert tri_state_filter_json == '{"key": "value"}'
            mock_tri_state_filter_manager_instance.to_json.assert_called_once_with(
                tri_state_filter_base_bus_obj.tri_state_filter)

    def test_get_obj(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for getting the tri_state_filter object.
        """
        assert tri_state_filter_base_bus_obj.get_obj() == tri_state_filter

    def test_get_object_name(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert tri_state_filter_base_bus_obj.get_object_name() == "tri_state_filter"

    def test_get_id(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for getting the tri_state_filter ID.
        """
        tri_state_filter.tri_state_filter_id = 1
        assert tri_state_filter_base_bus_obj.get_id() == 1

    def test_tri_state_filter_id(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the tri_state_filter_id property.
        """
        tri_state_filter.tri_state_filter_id = 1
        assert tri_state_filter_base_bus_obj.tri_state_filter_id == 1

    def test_code(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        tri_state_filter.code = test_uuid
        assert tri_state_filter_base_bus_obj.code == test_uuid

    def test_code_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        tri_state_filter_base_bus_obj.code = test_uuid
        assert tri_state_filter_base_bus_obj.code == test_uuid

    def test_code_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            tri_state_filter_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the TriStateFilterBaseBusiness class.

        Args:
            tri_state_filter_base_bus_obj (TriStateFilterBaseBusiness):
                An instance of the
                TriStateFilterBaseBusiness class.
            tri_state_filter (TriStateFilter): An instance of the
                TriStateFilter class.

        Returns:
            None
        """
        tri_state_filter.last_change_code = 123
        assert tri_state_filter_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        tri_state_filter_base_bus_obj.last_change_code = 123
        assert tri_state_filter_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            tri_state_filter_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        tri_state_filter.insert_user_id = test_uuid
        assert tri_state_filter_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        tri_state_filter_base_bus_obj.insert_user_id = test_uuid
        assert tri_state_filter_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            tri_state_filter_base_bus_obj.insert_user_id = "not-a-uuid"
    # description

    def test_description(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the description property.
        """
        tri_state_filter.description = "Vanilla"
        assert tri_state_filter_base_bus_obj.description == "Vanilla"

    def test_description_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the description setter.
        """
        tri_state_filter_base_bus_obj.description = "Vanilla"
        assert tri_state_filter_base_bus_obj.description == "Vanilla"

    def test_description_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        description property.
        """
        with pytest.raises(AssertionError):
            tri_state_filter_base_bus_obj.description = 123
    # displayOrder

    def test_display_order(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the display_order property.
        """
        tri_state_filter.display_order = 1
        assert tri_state_filter_base_bus_obj.display_order == 1

    def test_display_order_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the display_order setter.
        """
        tri_state_filter_base_bus_obj.display_order = 1
        assert tri_state_filter_base_bus_obj.display_order == 1

    def test_display_order_invalid_value(self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        display_order property.
        """
        with pytest.raises(AssertionError):
            tri_state_filter_base_bus_obj.display_order = "not-an-int"
    # isActive

    def test_is_active(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the is_active property.
        """
        tri_state_filter.is_active = True
        assert tri_state_filter_base_bus_obj.is_active is True

    def test_is_active_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the is_active setter.
        """
        tri_state_filter_base_bus_obj.is_active = True
        assert tri_state_filter_base_bus_obj.is_active is True

    def test_is_active_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            tri_state_filter_base_bus_obj.is_active = "not-a-boolean"
    # lookupEnumName

    def test_lookup_enum_name(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the lookup_enum_name property.
        """
        tri_state_filter.lookup_enum_name = "Vanilla"
        assert tri_state_filter_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the lookup_enum_name setter.
        """
        tri_state_filter_base_bus_obj.lookup_enum_name = "Vanilla"
        assert tri_state_filter_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        lookup_enum_name property.
        """
        with pytest.raises(AssertionError):
            tri_state_filter_base_bus_obj.lookup_enum_name = 123
    # name

    def test_name(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the name property.
        """
        tri_state_filter.name = "Vanilla"
        assert tri_state_filter_base_bus_obj.name == "Vanilla"

    def test_name_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the name setter.
        """
        tri_state_filter_base_bus_obj.name = "Vanilla"
        assert tri_state_filter_base_bus_obj.name == "Vanilla"

    def test_name_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            tri_state_filter_base_bus_obj.name = 123
    # PacID
    # stateIntValue

    def test_state_int_value(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the state_int_value property.
        """
        tri_state_filter.state_int_value = 1
        assert tri_state_filter_base_bus_obj.state_int_value == 1

    def test_state_int_value_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the state_int_value setter.
        """
        tri_state_filter_base_bus_obj.state_int_value = 1
        assert tri_state_filter_base_bus_obj.state_int_value == 1

    def test_state_int_value_invalid_value(self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        state_int_value property.
        """
        with pytest.raises(AssertionError):
            tri_state_filter_base_bus_obj.state_int_value = "not-an-int"
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_pac_id(
            self, tri_state_filter_base_bus_obj, tri_state_filter):
        """
        Test case for the pac_id property.
        """
        tri_state_filter.pac_id = 1
        assert tri_state_filter_base_bus_obj.pac_id == 1

    def test_pac_id_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the pac_id setter.
        """
        tri_state_filter_base_bus_obj.pac_id = 1
        assert tri_state_filter_base_bus_obj.pac_id == 1

    def test_pac_id_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        pac_id property.
        """
        with pytest.raises(AssertionError):
            tri_state_filter_base_bus_obj.pac_id = "not-an-int"
    # stateIntValue,

    def test_insert_utc_date_time(
            self,
            tri_state_filter_base_bus_obj,
            tri_state_filter):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        tri_state_filter.insert_utc_date_time = test_datetime
        assert tri_state_filter_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        tri_state_filter_base_bus_obj.insert_utc_date_time = test_datetime
        assert tri_state_filter_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            tri_state_filter_base_bus_obj.insert_utc_date_time = "not-a-datetime"

    def test_last_update_utc_date_time(
            self,
            tri_state_filter_base_bus_obj,
            tri_state_filter):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        tri_state_filter.last_update_utc_date_time = test_datetime
        assert tri_state_filter_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_setter(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        tri_state_filter_base_bus_obj.last_update_utc_date_time = test_datetime
        assert tri_state_filter_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_invalid_value(
            self, tri_state_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            tri_state_filter_base_bus_obj.last_update_utc_date_time = "not-a-datetime"

