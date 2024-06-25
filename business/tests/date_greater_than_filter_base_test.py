# business/tests/date_greater_than_filter_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
DateGreaterThanFilterBusObj class.
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
from business.date_greater_than_filter_base import (
    DateGreaterThanFilterBaseBusObj)
from helpers.session_context import SessionContext
from managers.date_greater_than_filter import (
    DateGreaterThanFilterManager)
from models import DateGreaterThanFilter
from models.factory import (
    DateGreaterThanFilterFactory)
from services.logging_config import get_logger

from ..date_greater_than_filter import DateGreaterThanFilterBusObj


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
def date_greater_than_filter():
    """
    Fixture that returns a mock date_greater_than_filter object.
    """
    return Mock(spec=DateGreaterThanFilter)


@pytest.fixture
def date_greater_than_filter_base_bus_obj(
    fake_session_context, date_greater_than_filter
):
    """
    Fixture that returns a DateGreaterThanFilterBaseBusObj instance.
    """
    date_greater_than_filter_base = DateGreaterThanFilterBaseBusObj(
        fake_session_context)
    date_greater_than_filter_base.date_greater_than_filter = date_greater_than_filter
    return date_greater_than_filter_base


class TestDateGreaterThanFilterBaseBusObj:
    """
    Unit tests for the
    DateGreaterThanFilterBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        DateGreaterThanFilterManager class.
        """
        session_context = SessionContext(dict(), session)
        return DateGreaterThanFilterManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        DateGreaterThanFilterBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return DateGreaterThanFilterBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_date_greater_than_filter(self, session):
        """
        Fixture that returns a new instance of
        the DateGreaterThanFilter class.
        """

        return await DateGreaterThanFilterFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_date_greater_than_filter(
        self,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj
    ):
        """
        Test case for creating a new date_greater_than_filter.
        """
        # Test creating a new date_greater_than_filter

        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id == 0

        # assert isinstance(date_greater_than_filter_bus_obj.date_greater_than_filter_id, int)
        assert isinstance(
            date_greater_than_filter_bus_obj.code, uuid.UUID)

        assert isinstance(
            date_greater_than_filter_bus_obj.last_change_code, int)

        assert date_greater_than_filter_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert date_greater_than_filter_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(date_greater_than_filter_bus_obj.day_count,
                          int)
        assert isinstance(date_greater_than_filter_bus_obj.description,
                          str)
        assert isinstance(date_greater_than_filter_bus_obj.display_order,
                          int)
        assert isinstance(date_greater_than_filter_bus_obj.is_active,
                          bool)
        assert isinstance(date_greater_than_filter_bus_obj.lookup_enum_name,
                          str)
        assert isinstance(date_greater_than_filter_bus_obj.name,
                          str)
        assert isinstance(date_greater_than_filter_bus_obj.pac_id,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_obj(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter object instance.
        """

        date_greater_than_filter_bus_obj.load_from_obj_instance(
            new_date_greater_than_filter)

        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_id(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter ID.
        """

        new_date_greater_than_filter_date_greater_than_filter_id = \
            new_date_greater_than_filter.date_greater_than_filter_id

        await date_greater_than_filter_bus_obj.load_from_id(
            new_date_greater_than_filter_date_greater_than_filter_id)

        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_code(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter code.
        """

        await date_greater_than_filter_bus_obj.load_from_code(
            new_date_greater_than_filter.code)

        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_json(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter JSON.
        """

        date_greater_than_filter_json = \
            date_greater_than_filter_manager.to_json(
                new_date_greater_than_filter)

        await date_greater_than_filter_bus_obj.load_from_json(
            date_greater_than_filter_json)

        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter, new_date_greater_than_filter) is True

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_dict(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter dictionary.
        """

        logger.info("test_load_with_date_greater_than_filter_dict 1")

        date_greater_than_filter_dict = \
            date_greater_than_filter_manager.to_dict(
                new_date_greater_than_filter)

        logger.info(date_greater_than_filter_dict)

        await date_greater_than_filter_bus_obj.load_from_dict(
            date_greater_than_filter_dict)

        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter,
            new_date_greater_than_filter) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_date_greater_than_filter(
        self,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj
    ):
        """
        Test case for retrieving a nonexistent date_greater_than_filter.
        """
        # Test retrieving a nonexistent
        # date_greater_than_filter raises an exception
        await date_greater_than_filter_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert date_greater_than_filter_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for updating a date_greater_than_filter's data.
        """
        # Test updating a date_greater_than_filter's data

        new_date_greater_than_filter_date_greater_than_filter_id_value = new_date_greater_than_filter.date_greater_than_filter_id

        new_date_greater_than_filter = await \
            date_greater_than_filter_manager.get_by_id(
                new_date_greater_than_filter_date_greater_than_filter_id_value)

        assert isinstance(new_date_greater_than_filter,
                          DateGreaterThanFilter)

        new_code = uuid.uuid4()

        date_greater_than_filter_bus_obj.load_from_obj_instance(
            new_date_greater_than_filter)

        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter,
            new_date_greater_than_filter) is True

        date_greater_than_filter_bus_obj.code = new_code

        await date_greater_than_filter_bus_obj.save()

        new_date_greater_than_filter_date_greater_than_filter_id_value = new_date_greater_than_filter.date_greater_than_filter_id

        new_date_greater_than_filter = await \
            date_greater_than_filter_manager.get_by_id(
                new_date_greater_than_filter_date_greater_than_filter_id_value)

        assert date_greater_than_filter_manager.is_equal(
            date_greater_than_filter_bus_obj.date_greater_than_filter,
            new_date_greater_than_filter) is True

    @pytest.mark.asyncio
    async def test_delete_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        date_greater_than_filter_bus_obj: DateGreaterThanFilterBusObj,
        new_date_greater_than_filter: DateGreaterThanFilter
    ):
        """
        Test case for deleting a date_greater_than_filter.
        """

        assert date_greater_than_filter_bus_obj.date_greater_than_filter is not None

        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id == 0

        date_greater_than_filter_bus_obj.load_from_obj_instance(
            new_date_greater_than_filter)

        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id is not None

        await date_greater_than_filter_bus_obj.delete()

        new_date_greater_than_filter_date_greater_than_filter_id_value = new_date_greater_than_filter.date_greater_than_filter_id

        new_date_greater_than_filter = await \
            date_greater_than_filter_manager.get_by_id(
                new_date_greater_than_filter_date_greater_than_filter_id_value)

        assert new_date_greater_than_filter is None

    def test_get_session_context(
        self,
        date_greater_than_filter_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert date_greater_than_filter_base_bus_obj.get_session_context() == fake_session_context

    @pytest.mark.asyncio
    async def test_refresh(
        self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for refreshing the date_greater_than_filter data.
        """
        with patch(
            'business.date_greater_than_filter_base.DateGreaterThanFilterManager',
            autospec=True
        ) as mock_date_greater_than_filter_manager:
            mock_date_greater_than_filter_manager_instance = \
                mock_date_greater_than_filter_manager.return_value
            mock_date_greater_than_filter_manager_instance.refresh =\
                AsyncMock(return_value=date_greater_than_filter)

            refreshed_date_greater_than_filter_base = await date_greater_than_filter_base_bus_obj.refresh()
            assert refreshed_date_greater_than_filter_base.date_greater_than_filter == date_greater_than_filter
            mock_date_greater_than_filter_manager_instance.refresh.assert_called_once_with(date_greater_than_filter)

    def test_is_valid(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for checking if the date_greater_than_filter data is valid.
        """
        assert date_greater_than_filter_base_bus_obj.is_valid() is True

        date_greater_than_filter_base_bus_obj.date_greater_than_filter = None
        assert date_greater_than_filter_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for converting the date_greater_than_filter data to a dictionary.
        """
        with patch(
            'business.date_greater_than_filter_base.DateGreaterThanFilterManager',
            autospec=True
        ) as mock_date_greater_than_filter_manager:
            mock_date_greater_than_filter_manager_instance = \
                mock_date_greater_than_filter_manager.return_value
            mock_date_greater_than_filter_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            date_greater_than_filter_dict = date_greater_than_filter_base_bus_obj.to_dict()
            assert date_greater_than_filter_dict == {"key": "value"}
            mock_date_greater_than_filter_manager_instance.to_dict.assert_called_once_with(
                date_greater_than_filter_base_bus_obj.date_greater_than_filter)

    def test_to_json(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for converting the date_greater_than_filter data to JSON.
        """
        with patch(
            'business.date_greater_than_filter_base.DateGreaterThanFilterManager',
            autospec=True
        ) as mock_date_greater_than_filter_manager:
            mock_date_greater_than_filter_manager_instance = \
                mock_date_greater_than_filter_manager.return_value
            mock_date_greater_than_filter_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            date_greater_than_filter_json = date_greater_than_filter_base_bus_obj.to_json()
            assert date_greater_than_filter_json == '{"key": "value"}'
            mock_date_greater_than_filter_manager_instance.to_json.assert_called_once_with(
                date_greater_than_filter_base_bus_obj.date_greater_than_filter)

    def test_get_obj(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for getting the date_greater_than_filter object.
        """
        assert date_greater_than_filter_base_bus_obj.get_obj() == date_greater_than_filter

    def test_get_object_name(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert date_greater_than_filter_base_bus_obj.get_object_name() == "date_greater_than_filter"

    def test_get_id(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for getting the date_greater_than_filter ID.
        """
        date_greater_than_filter.date_greater_than_filter_id = 1
        assert date_greater_than_filter_base_bus_obj.get_id() == 1

    def test_date_greater_than_filter_id(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the date_greater_than_filter_id property.
        """
        date_greater_than_filter.date_greater_than_filter_id = 1
        assert date_greater_than_filter_base_bus_obj.date_greater_than_filter_id == 1

    def test_code(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        date_greater_than_filter.code = test_uuid
        assert date_greater_than_filter_base_bus_obj.code == test_uuid

    def test_code_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        date_greater_than_filter_base_bus_obj.code = test_uuid
        assert date_greater_than_filter_base_bus_obj.code == test_uuid

    def test_code_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            date_greater_than_filter_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the DateGreaterThanFilterBaseBusiness class.

        Args:
            date_greater_than_filter_base_bus_obj (DateGreaterThanFilterBaseBusiness):
                An instance of the
                DateGreaterThanFilterBaseBusiness class.
            date_greater_than_filter (DateGreaterThanFilter): An instance of the
                DateGreaterThanFilter class.

        Returns:
            None
        """
        date_greater_than_filter.last_change_code = 123
        assert date_greater_than_filter_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        date_greater_than_filter_base_bus_obj.last_change_code = 123
        assert date_greater_than_filter_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            date_greater_than_filter_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        date_greater_than_filter.insert_user_id = test_uuid
        assert date_greater_than_filter_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        date_greater_than_filter_base_bus_obj.insert_user_id = test_uuid
        assert date_greater_than_filter_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            date_greater_than_filter_base_bus_obj.insert_user_id = "not-a-uuid"
    # dayCount

    def test_day_count(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the day_count property.
        """
        date_greater_than_filter.day_count = 1
        assert date_greater_than_filter_base_bus_obj.day_count == 1

    def test_day_count_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the day_count setter.
        """
        date_greater_than_filter_base_bus_obj.day_count = 1
        assert date_greater_than_filter_base_bus_obj.day_count == 1

    def test_day_count_invalid_value(self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        day_count property.
        """
        with pytest.raises(AssertionError):
            date_greater_than_filter_base_bus_obj.day_count = "not-an-int"
    # description

    def test_description(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the description property.
        """
        date_greater_than_filter.description = "Vanilla"
        assert date_greater_than_filter_base_bus_obj.description == "Vanilla"

    def test_description_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the description setter.
        """
        date_greater_than_filter_base_bus_obj.description = "Vanilla"
        assert date_greater_than_filter_base_bus_obj.description == "Vanilla"

    def test_description_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        description property.
        """
        with pytest.raises(AssertionError):
            date_greater_than_filter_base_bus_obj.description = 123
    # displayOrder

    def test_display_order(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the display_order property.
        """
        date_greater_than_filter.display_order = 1
        assert date_greater_than_filter_base_bus_obj.display_order == 1

    def test_display_order_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the display_order setter.
        """
        date_greater_than_filter_base_bus_obj.display_order = 1
        assert date_greater_than_filter_base_bus_obj.display_order == 1

    def test_display_order_invalid_value(self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        display_order property.
        """
        with pytest.raises(AssertionError):
            date_greater_than_filter_base_bus_obj.display_order = "not-an-int"
    # isActive

    def test_is_active(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the is_active property.
        """
        date_greater_than_filter.is_active = True
        assert date_greater_than_filter_base_bus_obj.is_active is True

    def test_is_active_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the is_active setter.
        """
        date_greater_than_filter_base_bus_obj.is_active = True
        assert date_greater_than_filter_base_bus_obj.is_active is True

    def test_is_active_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            date_greater_than_filter_base_bus_obj.is_active = "not-a-boolean"
    # lookupEnumName

    def test_lookup_enum_name(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the lookup_enum_name property.
        """
        date_greater_than_filter.lookup_enum_name = "Vanilla"
        assert date_greater_than_filter_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the lookup_enum_name setter.
        """
        date_greater_than_filter_base_bus_obj.lookup_enum_name = "Vanilla"
        assert date_greater_than_filter_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        lookup_enum_name property.
        """
        with pytest.raises(AssertionError):
            date_greater_than_filter_base_bus_obj.lookup_enum_name = 123
    # name

    def test_name(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the name property.
        """
        date_greater_than_filter.name = "Vanilla"
        assert date_greater_than_filter_base_bus_obj.name == "Vanilla"

    def test_name_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the name setter.
        """
        date_greater_than_filter_base_bus_obj.name = "Vanilla"
        assert date_greater_than_filter_base_bus_obj.name == "Vanilla"

    def test_name_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            date_greater_than_filter_base_bus_obj.name = 123
    # PacID
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_pac_id(
            self, date_greater_than_filter_base_bus_obj, date_greater_than_filter):
        """
        Test case for the pac_id property.
        """
        date_greater_than_filter.pac_id = 1
        assert date_greater_than_filter_base_bus_obj.pac_id == 1

    def test_pac_id_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the pac_id setter.
        """
        date_greater_than_filter_base_bus_obj.pac_id = 1
        assert date_greater_than_filter_base_bus_obj.pac_id == 1

    def test_pac_id_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        pac_id property.
        """
        with pytest.raises(AssertionError):
            date_greater_than_filter_base_bus_obj.pac_id = "not-an-int"

    def test_insert_utc_date_time(
            self,
            date_greater_than_filter_base_bus_obj,
            date_greater_than_filter):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        date_greater_than_filter.insert_utc_date_time = test_datetime
        assert date_greater_than_filter_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        date_greater_than_filter_base_bus_obj.insert_utc_date_time = test_datetime
        assert date_greater_than_filter_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            date_greater_than_filter_base_bus_obj.insert_utc_date_time = "not-a-datetime"

    def test_last_update_utc_date_time(
            self,
            date_greater_than_filter_base_bus_obj,
            date_greater_than_filter):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        date_greater_than_filter.last_update_utc_date_time = test_datetime
        assert date_greater_than_filter_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_setter(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        date_greater_than_filter_base_bus_obj.last_update_utc_date_time = test_datetime
        assert date_greater_than_filter_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_invalid_value(
            self, date_greater_than_filter_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            date_greater_than_filter_base_bus_obj.last_update_utc_date_time = "not-a-datetime"

