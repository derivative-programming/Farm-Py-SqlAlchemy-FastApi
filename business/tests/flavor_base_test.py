# business/tests/flavor_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
FlavorBusObj class.
"""

import uuid  # noqa: F401
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
from business.flavor_base import (
    FlavorBaseBusObj)
from helpers.session_context import SessionContext
from managers.flavor import (
    FlavorManager)
from models import Flavor
from models.factory import (
    FlavorFactory)
from services.logging_config import get_logger

from ..flavor import FlavorBusObj


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
def flavor():
    """
    Fixture that returns a mock
    flavor object.
    """
    return Mock(spec=Flavor)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, flavor
):
    """
    Fixture that returns a
    FlavorBaseBusObj instance.
    """
    mock_sess_base_bus_obj = FlavorBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.flavor = \
        flavor
    return mock_sess_base_bus_obj


class TestFlavorBaseBusObj:
    """
    Unit tests for the
    FlavorBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        FlavorManager class.
        """
        session_context = SessionContext(dict(), session)
        return FlavorManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        FlavorBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return FlavorBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the Flavor class.
        """

        return await FlavorFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_flavor(
        self,
        new_bus_obj: FlavorBusObj
    ):
        """
        Test case for creating a new flavor.
        """
        # Test creating a new flavor

        assert new_bus_obj.flavor_id == 0

        assert isinstance(new_bus_obj.flavor_id, int)
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

    @pytest.mark.asyncio
    async def test_load_with_flavor_obj(
        self,
        obj_manager: FlavorManager,
        new_bus_obj: FlavorBusObj,
        new_obj: Flavor
    ):
        """
        Test case for loading data from a
        flavor object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.flavor, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_flavor_id(
        self,
        obj_manager: FlavorManager,
        new_bus_obj: FlavorBusObj,
        new_obj: Flavor
    ):
        """
        Test case for loading data from a
        flavor ID.
        """

        new_obj_flavor_id = \
            new_obj.flavor_id

        await new_bus_obj.load_from_id(
            new_obj_flavor_id)

        assert obj_manager.is_equal(
            new_bus_obj.flavor, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_flavor_code(
        self,
        obj_manager: FlavorManager,
        new_bus_obj: FlavorBusObj,
        new_obj: Flavor
    ):
        """
        Test case for loading data from a
        flavor code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.flavor, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_flavor_json(
        self,
        obj_manager: FlavorManager,
        new_bus_obj: FlavorBusObj,
        new_obj: Flavor
    ):
        """
        Test case for loading data from a
        flavor JSON.
        """

        flavor_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            flavor_json)

        assert obj_manager.is_equal(
            new_bus_obj.flavor, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_flavor_dict(
        self,
        obj_manager: FlavorManager,
        new_bus_obj: FlavorBusObj,
        new_obj: Flavor
    ):
        """
        Test case for loading data from a
        flavor dictionary.
        """

        logger.info("test_load_with_flavor_dict 1")

        flavor_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(flavor_dict)

        await new_bus_obj.load_from_dict(
            flavor_dict)

        assert obj_manager.is_equal(
            new_bus_obj.flavor,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_flavor(
        self,
        new_bus_obj: FlavorBusObj
    ):
        """
        Test case for retrieving a nonexistent
        flavor.
        """
        # Test retrieving a nonexistent
        # flavor raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_flavor(
        self,
        obj_manager: FlavorManager,
        new_bus_obj: FlavorBusObj,
        new_obj: Flavor
    ):
        """
        Test case for updating a flavor's data.
        """
        # Test updating a flavor's data

        new_obj_flavor_id_value = \
            new_obj.flavor_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_flavor_id_value)

        assert isinstance(new_obj,
                          Flavor)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.flavor,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_flavor_id_value = \
            new_obj.flavor_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_flavor_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.flavor,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_flavor(
        self,
        obj_manager: FlavorManager,
        new_bus_obj: FlavorBusObj,
        new_obj: Flavor
    ):
        """
        Test case for deleting a flavor.
        """

        assert new_bus_obj.flavor is not None

        assert new_bus_obj.flavor_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.flavor_id is not None

        await new_bus_obj.delete()

        new_obj_flavor_id_value = \
            new_obj.flavor_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_flavor_id_value)

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
        flavor
    ):
        """
        Test case for refreshing the flavor data.
        """
        with patch(
            "business.flavor_base"
            ".FlavorManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=flavor)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .flavor == flavor
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(flavor)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the flavor data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.flavor = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the flavor
        data to a dictionary.
        """
        with patch(
            "business.flavor_base"
            ".FlavorManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            flavor_dict = mock_sess_base_bus_obj.to_dict()
            assert flavor_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.flavor)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the flavor data to JSON.
        """
        with patch(
            "business.flavor_base"
            ".FlavorManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            flavor_json = mock_sess_base_bus_obj.to_json()
            assert flavor_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.flavor)

    def test_get_obj(
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for getting the flavor object.
        """
        assert mock_sess_base_bus_obj.get_obj() == flavor

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "flavor"

    def test_get_id(
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for getting the flavor ID.
        """
        flavor.flavor_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_flavor_id(
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the flavor_id property.
        """
        flavor.flavor_id = 1
        assert mock_sess_base_bus_obj.flavor_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        flavor.code = test_uuid
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
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the FlavorBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (FlavorBaseBusiness):
                An instance of the
                FlavorBaseBusiness class.
            flavor (Flavor):
                An instance of the
                Flavor class.

        Returns:
            None
        """
        flavor.last_change_code = 123
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
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        flavor.insert_user_id = test_uuid
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
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the
        description property.
        """
        flavor.description = \
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
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the
        display_order property.
        """
        flavor.display_order = 1
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
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the
        is_active property.
        """
        flavor.is_active = True
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
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the
        lookup_enum_name property.
        """
        flavor.lookup_enum_name = \
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
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the
        name property.
        """
        flavor.name = \
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
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_pac_id(
            self, mock_sess_base_bus_obj, flavor):
        """
        Test case for the pac_id property.
        """
        flavor.pac_id = 1
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
            flavor):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        flavor.insert_utc_date_time = test_datetime
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
            flavor):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        flavor.last_update_utc_date_time = test_datetime
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
