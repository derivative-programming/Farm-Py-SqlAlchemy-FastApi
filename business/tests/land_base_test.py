# business/tests/land_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the LandBusObj class.
"""

import uuid
import math
from datetime import date, datetime  # noqa: F401
from decimal import Decimal
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
from business.land_base import LandBaseBusObj
from helpers.session_context import SessionContext
from managers.land import LandManager
from models import Land
from models.factory import LandFactory
from services.logging_config import get_logger

from ..land import LandBusObj


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
def land():
    """
    Fixture that returns a mock land object.
    """
    return Mock(spec=Land)


@pytest.fixture
def land_base_bus_obj(fake_session_context, land):
    """
    Fixture that returns a LandBaseBusObj instance.
    """
    land_base = LandBaseBusObj(fake_session_context)
    land_base.land = land
    return land_base


class TestLandBaseBusObj:
    """
    Unit tests for the LandBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def land_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the LandManager class.
        """
        session_context = SessionContext(dict(), session)
        return LandManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def land_bus_obj(self, session):
        """
        Fixture that returns an instance of the LandBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return LandBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_land(self, session):
        """
        Fixture that returns a new instance of
        the Land class.
        """

        return await LandFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_land(
        self,
        land_bus_obj: LandBusObj
    ):
        """
        Test case for creating a new land.
        """
        # Test creating a new land

        assert land_bus_obj.land_id == 0

        # assert isinstance(land_bus_obj.land_id, int)
        assert isinstance(
            land_bus_obj.code, uuid.UUID)

        assert isinstance(
            land_bus_obj.last_change_code, int)

        assert land_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert land_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(land_bus_obj.description, str)
        assert isinstance(land_bus_obj.display_order, int)
        assert isinstance(land_bus_obj.is_active, bool)
        assert isinstance(land_bus_obj.lookup_enum_name, str)
        assert isinstance(land_bus_obj.name, str)
        assert isinstance(land_bus_obj.pac_id, int)

    @pytest.mark.asyncio
    async def test_load_with_land_obj(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
        Test case for loading data from a
        land object instance.
        """

        land_bus_obj.load_from_obj_instance(
            new_land)

        assert land_manager.is_equal(
            land_bus_obj.land, new_land) is True

    @pytest.mark.asyncio
    async def test_load_with_land_id(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
        Test case for loading data from a
        land ID.
        """

        new_land_land_id = new_land.land_id

        await land_bus_obj.load_from_id(
            new_land_land_id)

        assert land_manager.is_equal(
            land_bus_obj.land, new_land) is True

    @pytest.mark.asyncio
    async def test_load_with_land_code(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
        Test case for loading data from a
        land code.
        """

        await land_bus_obj.load_from_code(
            new_land.code)

        assert land_manager.is_equal(
            land_bus_obj.land, new_land) is True

    @pytest.mark.asyncio
    async def test_load_with_land_json(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
        Test case for loading data from a
        land JSON.
        """

        land_json = land_manager.to_json(new_land)

        await land_bus_obj.load_from_json(
            land_json)

        assert land_manager.is_equal(
            land_bus_obj.land, new_land) is True

    @pytest.mark.asyncio
    async def test_load_with_land_dict(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
        Test case for loading data from a
        land dictionary.
        """

        logger.info("test_load_with_land_dict 1")

        land_dict = land_manager.to_dict(new_land)

        logger.info(land_dict)

        await land_bus_obj.load_from_dict(
            land_dict)

        assert land_manager.is_equal(
            land_bus_obj.land,
            new_land) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_land(
        self,
        land_bus_obj: LandBusObj
    ):
        """
        Test case for retrieving a nonexistent land.
        """
        # Test retrieving a nonexistent
        # land raises an exception
        await land_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert land_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_land(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
        Test case for updating a land's data.
        """
        # Test updating a land's data

        new_land_land_id_value = new_land.land_id

        new_land = await land_manager.get_by_id(
            new_land_land_id_value)

        assert isinstance(new_land, Land)

        new_code = uuid.uuid4()

        land_bus_obj.load_from_obj_instance(
            new_land)

        assert land_manager.is_equal(
            land_bus_obj.land,
            new_land) is True

        land_bus_obj.code = new_code

        await land_bus_obj.save()

        new_land_land_id_value = new_land.land_id

        new_land = await land_manager.get_by_id(
            new_land_land_id_value)

        assert land_manager.is_equal(
            land_bus_obj.land,
            new_land) is True

    @pytest.mark.asyncio
    async def test_delete_land(
        self,
        land_manager: LandManager,
        land_bus_obj: LandBusObj,
        new_land: Land
    ):
        """
        Test case for deleting a land.
        """

        assert land_bus_obj.land is not None

        assert land_bus_obj.land_id == 0

        land_bus_obj.load_from_obj_instance(
            new_land)

        assert land_bus_obj.land_id is not None

        await land_bus_obj.delete()

        new_land_land_id_value = new_land.land_id

        new_land = await land_manager.get_by_id(
            new_land_land_id_value)

        assert new_land is None

    def test_get_session_context(
        self,
        land_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert land_base_bus_obj.get_session_context() == fake_session_context

    @pytest.mark.asyncio
    async def test_refresh(self, land_base_bus_obj, land):
        """
        Test case for refreshing the land data.
        """
        with patch(
            'business.land_base.LandManager',
            autospec=True
        ) as mock_land_manager:
            mock_land_manager_instance = mock_land_manager.return_value
            mock_land_manager_instance.refresh = AsyncMock(return_value=land)

            refreshed_land_base = await land_base_bus_obj.refresh()
            assert refreshed_land_base.land == land
            mock_land_manager_instance.refresh.assert_called_once_with(land)

    def test_is_valid(self, land_base_bus_obj):
        """
        Test case for checking if the land data is valid.
        """
        assert land_base_bus_obj.is_valid() is True

        land_base_bus_obj.land = None
        assert land_base_bus_obj.is_valid() is False

    def test_to_dict(self, land_base_bus_obj):
        """
        Test case for converting the land data to a dictionary.
        """
        with patch(
            'business.land_base.LandManager',
            autospec=True
        ) as mock_land_manager:
            mock_land_manager_instance = mock_land_manager.return_value
            mock_land_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            land_dict = land_base_bus_obj.to_dict()
            assert land_dict == {"key": "value"}
            mock_land_manager_instance.to_dict.assert_called_once_with(
                land_base_bus_obj.land)

    def test_to_json(self, land_base_bus_obj):
        """
        Test case for converting the land data to JSON.
        """
        with patch(
            'business.land_base.LandManager',
            autospec=True
        ) as mock_land_manager:
            mock_land_manager_instance = mock_land_manager.return_value
            mock_land_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            land_json = land_base_bus_obj.to_json()
            assert land_json == '{"key": "value"}'
            mock_land_manager_instance.to_json.assert_called_once_with(
                land_base_bus_obj.land)

    def test_get_obj(self, land_base_bus_obj, land):
        """
        Test case for getting the land object.
        """
        assert land_base_bus_obj.get_obj() == land

    def test_get_object_name(self, land_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert land_base_bus_obj.get_object_name() == "land"

    def test_get_id(self, land_base_bus_obj, land):
        """
        Test case for getting the land ID.
        """
        land.land_id = 1
        assert land_base_bus_obj.get_id() == 1

    def test_land_id(self, land_base_bus_obj, land):
        """
        Test case for the land_id property.
        """
        land.land_id = 1
        assert land_base_bus_obj.land_id == 1

    def test_code(self, land_base_bus_obj, land):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        land.code = test_uuid
        assert land_base_bus_obj.code == test_uuid

    def test_code_setter(self, land_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        land_base_bus_obj.code = test_uuid
        assert land_base_bus_obj.code == test_uuid

    def test_code_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            land_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(self, land_base_bus_obj, land):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the LandBaseBusiness class.

        Args:
            land_base_bus_obj (LandBaseBusiness):
                An instance of the
                LandBaseBusiness class.
            land (Land): An instance of the Land class.

        Returns:
            None
        """
        land.last_change_code = 123
        assert land_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(self, land_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        land_base_bus_obj.last_change_code = 123
        assert land_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            land_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(self, land_base_bus_obj, land):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        land.insert_user_id = test_uuid
        assert land_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_setter(self, land_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        land_base_bus_obj.insert_user_id = test_uuid
        assert land_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            land_base_bus_obj.insert_user_id = "not-a-uuid"
    # description

    def test_description(self, land_base_bus_obj, land):
        """
        Test case for the description property.
        """
        land.description = "Vanilla"
        assert land_base_bus_obj.description == "Vanilla"

    def test_description_setter(self, land_base_bus_obj):
        """
        Test case for the description setter.
        """
        land_base_bus_obj.description = "Vanilla"
        assert land_base_bus_obj.description == "Vanilla"

    def test_description_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        description property.
        """
        with pytest.raises(AssertionError):
            land_base_bus_obj.description = 123
    # displayOrder

    def test_display_order(self, land_base_bus_obj, land):
        """
        Test case for the display_order property.
        """
        land.display_order = 1
        assert land_base_bus_obj.display_order == 1

    def test_display_order_setter(self, land_base_bus_obj):
        """
        Test case for the display_order setter.
        """
        land_base_bus_obj.display_order = 1
        assert land_base_bus_obj.display_order == 1

    def test_display_order_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        display_order property.
        """
        with pytest.raises(AssertionError):
            land_base_bus_obj.display_order = "not-an-int"
    # isActive

    def test_is_active(self, land_base_bus_obj, land):
        """
        Test case for the is_active property.
        """
        land.is_active = True
        assert land_base_bus_obj.is_active is True

    def test_is_active_setter(self, land_base_bus_obj):
        """
        Test case for the is_active setter.
        """
        land_base_bus_obj.is_active = True
        assert land_base_bus_obj.is_active is True

    def test_is_active_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            land_base_bus_obj.is_active = "not-a-boolean"
    # lookupEnumName

    def test_lookup_enum_name(self, land_base_bus_obj, land):
        """
        Test case for the lookup_enum_name property.
        """
        land.lookup_enum_name = "Vanilla"
        assert land_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_setter(self, land_base_bus_obj):
        """
        Test case for the lookup_enum_name setter.
        """
        land_base_bus_obj.lookup_enum_name = "Vanilla"
        assert land_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        lookup_enum_name property.
        """
        with pytest.raises(AssertionError):
            land_base_bus_obj.lookup_enum_name = 123
    # name

    def test_name(self, land_base_bus_obj, land):
        """
        Test case for the name property.
        """
        land.name = "Vanilla"
        assert land_base_bus_obj.name == "Vanilla"

    def test_name_setter(self, land_base_bus_obj):
        """
        Test case for the name setter.
        """
        land_base_bus_obj.name = "Vanilla"
        assert land_base_bus_obj.name == "Vanilla"

    def test_name_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            land_base_bus_obj.name = 123
    # PacID
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_pac_id(self, land_base_bus_obj, land):
        """
        Test case for the pac_id property.
        """
        land.pac_id = 1
        assert land_base_bus_obj.pac_id == 1

    def test_pac_id_setter(self, land_base_bus_obj):
        """
        Test case for the pac_id setter.
        """
        land_base_bus_obj.pac_id = 1
        assert land_base_bus_obj.pac_id == 1

    def test_pac_id_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        pac_id property.
        """
        with pytest.raises(AssertionError):
            land_base_bus_obj.pac_id = "not-an-int"

    def test_insert_utc_date_time(self, land_base_bus_obj, land):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        land.insert_utc_date_time = test_datetime
        assert land_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_setter(self, land_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        land_base_bus_obj.insert_utc_date_time = test_datetime
        assert land_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            land_base_bus_obj.insert_utc_date_time = "not-a-datetime"

    def test_last_update_utc_date_time(self, land_base_bus_obj, land):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        land.last_update_utc_date_time = test_datetime
        assert land_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_setter(self, land_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        land_base_bus_obj.last_update_utc_date_time = test_datetime
        assert land_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_invalid_value(self, land_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            land_base_bus_obj.last_update_utc_date_time = "not-a-datetime"


    @pytest.mark.asyncio
    async def test_build_plant(
        self,
        land_bus_obj: LandBusObj,
        new_land: Land,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await land_bus_obj.load_from_id(
            new_land.land_id
        )

        plant_bus_obj = await land_bus_obj.build_plant()

        assert plant_bus_obj.land_id == land_bus_obj.land_id
        assert plant_bus_obj.land_code_peek == land_bus_obj.code

        await plant_bus_obj.save()

        assert plant_bus_obj.plant_id > 0


    @pytest.mark.asyncio
    async def test_get_all_plant(
        self,
        land_bus_obj: LandBusObj,
        new_land: Land,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_land_land_id = (
            new_land.land_id
        )

        await land_bus_obj.load_from_id(
            new_land_land_id
        )

        plant_bus_obj = await land_bus_obj.build_plant()

        await plant_bus_obj.save()

        plant_list = await land_bus_obj.get_all_plant()

        assert len(plant_list) >= 1

        #assert plant_list[0].plant_id > 0

        #assert plant_list[0].plant_id == plant_bus_obj.plant_id

