# business/tests/date_greater_than_filter_base_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=redefined-outer-name
# pylint: disable=too-few-public-methods

"""
This module contains unit tests for the
DateGreaterThanFilterBusObj class.
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
from business.date_greater_than_filter_base import DateGreaterThanFilterBaseBusObj
from helpers.session_context import SessionContext
from managers.date_greater_than_filter import DateGreaterThanFilterManager
from models import DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
from services.logging_config import get_logger

from ..date_greater_than_filter import DateGreaterThanFilterBusObj


BUSINESS_DATE_GREATER_THAN_FILTER_BASE_MANAGER_PATCH = (
    "business.date_greater_than_filter_base"
    ".DateGreaterThanFilterManager"
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
def date_greater_than_filter():
    """
    Fixture that returns a mock
    date_greater_than_filter object.
    """
    return Mock(spec=DateGreaterThanFilter)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, date_greater_than_filter
):
    """
    Fixture that returns a
    DateGreaterThanFilterBaseBusObj instance.
    """
    mock_sess_base_bus_obj = DateGreaterThanFilterBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.date_greater_than_filter = \
        date_greater_than_filter
    return mock_sess_base_bus_obj


class TestDateGreaterThanFilterBaseBusObj:
    """
    Unit tests for the
    DateGreaterThanFilterBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        DateGreaterThanFilterManager class.
        """
        session_context = SessionContext({}, session)
        return DateGreaterThanFilterManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        DateGreaterThanFilterBusObj class.
        """
        session_context = SessionContext({}, session)
        return DateGreaterThanFilterBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the DateGreaterThanFilter class.
        """

        return await DateGreaterThanFilterFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_date_greater_than_filter(
        self,
        new_bus_obj: DateGreaterThanFilterBusObj
    ):
        """
        Test case for creating a new date_greater_than_filter.
        """
        # Test creating a new date_greater_than_filter

        assert new_bus_obj.date_greater_than_filter_id == 0

        assert isinstance(new_bus_obj.date_greater_than_filter_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.day_count,
                          int)
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

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_obj(
        self,
        obj_manager: DateGreaterThanFilterManager,
        new_bus_obj: DateGreaterThanFilterBusObj,
        new_obj: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.date_greater_than_filter, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_id(
        self,
        obj_manager: DateGreaterThanFilterManager,
        new_bus_obj: DateGreaterThanFilterBusObj,
        new_obj: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter ID.
        """

        new_obj_date_greater_than_filter_id = \
            new_obj.date_greater_than_filter_id

        await new_bus_obj.load_from_id(
            new_obj_date_greater_than_filter_id)

        assert obj_manager.is_equal(
            new_bus_obj.date_greater_than_filter, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_code(
        self,
        obj_manager: DateGreaterThanFilterManager,
        new_bus_obj: DateGreaterThanFilterBusObj,
        new_obj: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.date_greater_than_filter, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_json(
        self,
        obj_manager: DateGreaterThanFilterManager,
        new_bus_obj: DateGreaterThanFilterBusObj,
        new_obj: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter JSON.
        """

        date_greater_than_filter_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            date_greater_than_filter_json)

        assert obj_manager.is_equal(
            new_bus_obj.date_greater_than_filter, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_date_greater_than_filter_dict(
        self,
        obj_manager: DateGreaterThanFilterManager,
        new_bus_obj: DateGreaterThanFilterBusObj,
        new_obj: DateGreaterThanFilter
    ):
        """
        Test case for loading data from a
        date_greater_than_filter dictionary.
        """

        logger.info("test_load_with_date_greater_than_filter_dict 1")

        date_greater_than_filter_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(date_greater_than_filter_dict)

        await new_bus_obj.load_from_dict(
            date_greater_than_filter_dict)

        assert obj_manager.is_equal(
            new_bus_obj.date_greater_than_filter,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_date_greater_than_filter(
        self,
        new_bus_obj: DateGreaterThanFilterBusObj
    ):
        """
        Test case for retrieving a nonexistent
        date_greater_than_filter.
        """
        # Test retrieving a nonexistent
        # date_greater_than_filter raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_date_greater_than_filter(
        self,
        obj_manager: DateGreaterThanFilterManager,
        new_bus_obj: DateGreaterThanFilterBusObj,
        new_obj: DateGreaterThanFilter
    ):
        """
        Test case for updating a date_greater_than_filter's data.
        """
        # Test updating a date_greater_than_filter's data

        new_obj_date_greater_than_filter_id_value = \
            new_obj.date_greater_than_filter_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_date_greater_than_filter_id_value)

        assert isinstance(new_obj,
                          DateGreaterThanFilter)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.date_greater_than_filter,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_date_greater_than_filter_id_value = \
            new_obj.date_greater_than_filter_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_date_greater_than_filter_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.date_greater_than_filter,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_date_greater_than_filter(
        self,
        obj_manager: DateGreaterThanFilterManager,
        new_bus_obj: DateGreaterThanFilterBusObj,
        new_obj: DateGreaterThanFilter
    ):
        """
        Test case for deleting a date_greater_than_filter.
        """

        assert new_bus_obj.date_greater_than_filter is not None

        assert new_bus_obj.date_greater_than_filter_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.date_greater_than_filter_id is not None

        await new_bus_obj.delete()

        new_obj_date_greater_than_filter_id_value = \
            new_obj.date_greater_than_filter_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_date_greater_than_filter_id_value)

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
        date_greater_than_filter
    ):
        """
        Test case for refreshing the date_greater_than_filter data.
        """
        with patch(
            BUSINESS_DATE_GREATER_THAN_FILTER_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=date_greater_than_filter)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .date_greater_than_filter == date_greater_than_filter
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(date_greater_than_filter)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the date_greater_than_filter data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.date_greater_than_filter = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the date_greater_than_filter
        data to a dictionary.
        """
        with patch(
            BUSINESS_DATE_GREATER_THAN_FILTER_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            date_greater_than_filter_dict = mock_sess_base_bus_obj.to_dict()
            assert date_greater_than_filter_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.date_greater_than_filter)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the date_greater_than_filter data to JSON.
        """
        with patch(
            BUSINESS_DATE_GREATER_THAN_FILTER_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            date_greater_than_filter_json = mock_sess_base_bus_obj.to_json()
            assert date_greater_than_filter_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.date_greater_than_filter)

    def test_get_obj(
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for getting the date_greater_than_filter object.
        """
        assert mock_sess_base_bus_obj.get_obj() == date_greater_than_filter

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "date_greater_than_filter"

    def test_get_id(
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for getting the date_greater_than_filter ID.
        """
        date_greater_than_filter.date_greater_than_filter_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_date_greater_than_filter_id(
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the date_greater_than_filter_id property.
        """
        date_greater_than_filter.date_greater_than_filter_id = 1
        assert mock_sess_base_bus_obj.date_greater_than_filter_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        date_greater_than_filter.code = test_uuid
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
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the DateGreaterThanFilterBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (DateGreaterThanFilterBaseBusiness):
                An instance of the
                DateGreaterThanFilterBaseBusiness class.
            date_greater_than_filter (DateGreaterThanFilter):
                An instance of the
                DateGreaterThanFilter class.

        Returns:
            None
        """
        date_greater_than_filter.last_change_code = 123
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
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        date_greater_than_filter.insert_user_id = test_uuid
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
    # dayCount

    def test_day_count(
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the
        day_count property.
        """
        date_greater_than_filter.day_count = 1
        assert mock_sess_base_bus_obj \
            .day_count == 1

    def test_day_count_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        day_count setter.
        """
        mock_sess_base_bus_obj.day_count = 1
        assert mock_sess_base_bus_obj \
            .day_count == 1

    def test_day_count_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        day_count property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.day_count = \
                "not-an-int"
    # description

    def test_description(
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the
        description property.
        """
        date_greater_than_filter.description = \
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
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the
        display_order property.
        """
        date_greater_than_filter.display_order = 1
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
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the
        is_active property.
        """
        date_greater_than_filter.is_active = True
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
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the
        lookup_enum_name property.
        """
        date_greater_than_filter.lookup_enum_name = \
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
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the
        name property.
        """
        date_greater_than_filter.name = \
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
    # dayCount
    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    def test_pac_id(
            self, mock_sess_base_bus_obj, date_greater_than_filter):
        """
        Test case for the pac_id property.
        """
        date_greater_than_filter.pac_id = 1
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

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            date_greater_than_filter):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        date_greater_than_filter.insert_utc_date_time = test_datetime
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
            date_greater_than_filter):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        date_greater_than_filter.last_update_utc_date_time = test_datetime
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
