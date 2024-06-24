# business/tests/flavor_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
"""
This module contains unit tests for the FlavorBusObj class.
"""
import uuid
from datetime import date, datetime  # noqa: F401
from decimal import Decimal
from unittest.mock import AsyncMock, Mock, patch
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import current_runtime  # noqa: F401
from business.flavor_base import FlavorBaseBusObj
from helpers.session_context import SessionContext
from managers.flavor import FlavorManager
from models import Flavor
from models.factory import FlavorFactory
from services.logging_config import get_logger
from ..flavor import FlavorBusObj

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
def flavor():
    """
    Fixture that returns a mock flavor object.
    """
    return Mock(spec=Flavor)
@pytest.fixture
def flavor_base_bus_obj(fake_session_context, flavor):
    """
    Fixture that returns a FlavorBaseBusObj instance.
    """
    flavor_base = FlavorBaseBusObj(fake_session_context)
    flavor_base.flavor = flavor
    return flavor_base
class TestFlavorBaseBusObj:
    """
    Unit tests for the FlavorBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def flavor_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the FlavorManager class.
        """
        session_context = SessionContext(dict(), session)
        return FlavorManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def flavor_bus_obj(self, session):
        """
        Fixture that returns an instance of the FlavorBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return FlavorBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_flavor(self, session):
        """
        Fixture that returns a new instance of
        the Flavor class.
        """
        return await FlavorFactory.create_async(
            session)
    @pytest.mark.asyncio
    async def test_create_flavor(
        self,
        flavor_bus_obj: FlavorBusObj
    ):
        """
        Test case for creating a new flavor.
        """
        # Test creating a new flavor
        assert flavor_bus_obj.flavor_id == 0
        # assert isinstance(flavor_bus_obj.flavor_id, int)
        assert isinstance(
            flavor_bus_obj.code, uuid.UUID)
        assert isinstance(
            flavor_bus_obj.last_change_code, int)
        assert flavor_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert flavor_bus_obj.last_update_user_id == uuid.UUID(int=0)
# endset
        assert isinstance(flavor_bus_obj.description, str)
        assert isinstance(flavor_bus_obj.display_order, int)
        assert isinstance(flavor_bus_obj.is_active, bool)
        assert isinstance(flavor_bus_obj.lookup_enum_name, str)
        assert isinstance(flavor_bus_obj.name, str)
        assert isinstance(flavor_bus_obj.pac_id, int)
# endset
    @pytest.mark.asyncio
    async def test_load_with_flavor_obj(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
        Test case for loading data from a
        flavor object instance.
        """
        await flavor_bus_obj.load_from_obj_instance(
            new_flavor)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor, new_flavor) is True
    @pytest.mark.asyncio
    async def test_load_with_flavor_id(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
        Test case for loading data from a
        flavor ID.
        """
        new_flavor_flavor_id = new_flavor.flavor_id
        await flavor_bus_obj.load_from_id(
            new_flavor_flavor_id)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor, new_flavor) is True
    @pytest.mark.asyncio
    async def test_load_with_flavor_code(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
        Test case for loading data from a
        flavor code.
        """
        await flavor_bus_obj.load_from_code(
            new_flavor.code)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor, new_flavor) is True
    @pytest.mark.asyncio
    async def test_load_with_flavor_json(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
        Test case for loading data from a
        flavor JSON.
        """
        flavor_json = flavor_manager.to_json(new_flavor)
        await flavor_bus_obj.load_from_json(
            flavor_json)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor, new_flavor) is True
    @pytest.mark.asyncio
    async def test_load_with_flavor_dict(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
        Test case for loading data from a
        flavor dictionary.
        """
        logger.info("test_load_with_flavor_dict 1")
        flavor_dict = flavor_manager.to_dict(new_flavor)
        logger.info(flavor_dict)
        await flavor_bus_obj.load_from_dict(
            flavor_dict)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor,
            new_flavor) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_flavor(
        self,
        flavor_bus_obj: FlavorBusObj
    ):
        """
        Test case for retrieving a nonexistent flavor.
        """
        # Test retrieving a nonexistent
        # flavor raises an exception
        await flavor_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert flavor_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_flavor(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
        Test case for updating a flavor's data.
        """
        # Test updating a flavor's data
        new_flavor_flavor_id_value = new_flavor.flavor_id
        new_flavor = await flavor_manager.get_by_id(
            new_flavor_flavor_id_value)
        assert isinstance(new_flavor, Flavor)
        new_code = uuid.uuid4()
        await flavor_bus_obj.load_from_obj_instance(
            new_flavor)
        flavor_bus_obj.code = new_code
        await flavor_bus_obj.save()
        new_flavor_flavor_id_value = new_flavor.flavor_id
        new_flavor = await flavor_manager.get_by_id(
            new_flavor_flavor_id_value)
        assert flavor_manager.is_equal(
            flavor_bus_obj.flavor,
            new_flavor) is True
    @pytest.mark.asyncio
    async def test_delete_flavor(
        self,
        flavor_manager: FlavorManager,
        flavor_bus_obj: FlavorBusObj,
        new_flavor: Flavor
    ):
        """
        Test case for deleting a flavor.
        """
        assert new_flavor.flavor_id is not None
        assert flavor_bus_obj.flavor_id == 0
        new_flavor_flavor_id_value = new_flavor.flavor_id
        await flavor_bus_obj.load_from_id(
            new_flavor_flavor_id_value)
        assert flavor_bus_obj.flavor_id is not None
        await flavor_bus_obj.delete()
        new_flavor_flavor_id_value = new_flavor.flavor_id
        new_flavor = await flavor_manager.get_by_id(
            new_flavor_flavor_id_value)
        assert new_flavor is None
    def test_get_session_context(
        self,
        flavor_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert flavor_base_bus_obj.get_session_context() == fake_session_context
    @pytest.mark.asyncio
    async def test_refresh(self, flavor_base_bus_obj, flavor):
        """
        Test case for refreshing the flavor data.
        """
        with patch(
            'business.flavor_base.FlavorManager',
            autospec=True
        ) as mock_flavor_manager:
            mock_flavor_manager_instance = mock_flavor_manager.return_value
            mock_flavor_manager_instance.refresh = AsyncMock(return_value=flavor)
            refreshed_flavor_base = await flavor_base_bus_obj.refresh()
            assert refreshed_flavor_base.flavor == flavor
            mock_flavor_manager_instance.refresh.assert_called_once_with(flavor)
    def test_is_valid(self, flavor_base_bus_obj):
        """
        Test case for checking if the flavor data is valid.
        """
        assert flavor_base_bus_obj.is_valid() is True
        flavor_base_bus_obj.flavor = None
        assert flavor_base_bus_obj.is_valid() is False
    def test_to_dict(self, flavor_base_bus_obj):
        """
        Test case for converting the flavor data to a dictionary.
        """
        with patch(
            'business.flavor_base.FlavorManager',
            autospec=True
        ) as mock_flavor_manager:
            mock_flavor_manager_instance = mock_flavor_manager.return_value
            mock_flavor_manager_instance.to_dict = Mock(
                return_value={"key": "value"})
            flavor_dict = flavor_base_bus_obj.to_dict()
            assert flavor_dict == {"key": "value"}
            mock_flavor_manager_instance.to_dict.assert_called_once_with(
                flavor_base_bus_obj.flavor)
    def test_to_json(self, flavor_base_bus_obj):
        """
        Test case for converting the flavor data to JSON.
        """
        with patch(
            'business.flavor_base.FlavorManager',
            autospec=True
        ) as mock_flavor_manager:
            mock_flavor_manager_instance = mock_flavor_manager.return_value
            mock_flavor_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')
            flavor_json = flavor_base_bus_obj.to_json()
            assert flavor_json == '{"key": "value"}'
            mock_flavor_manager_instance.to_json.assert_called_once_with(
                flavor_base_bus_obj.flavor)
    def test_get_obj(self, flavor_base_bus_obj, flavor):
        """
        Test case for getting the flavor object.
        """
        assert flavor_base_bus_obj.get_obj() == flavor
    def test_get_object_name(self, flavor_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert flavor_base_bus_obj.get_object_name() == "flavor"
    def test_get_id(self, flavor_base_bus_obj, flavor):
        """
        Test case for getting the flavor ID.
        """
        flavor.flavor_id = 1
        assert flavor_base_bus_obj.get_id() == 1
    def test_flavor_id(self, flavor_base_bus_obj, flavor):
        """
        Test case for the flavor_id property.
        """
        flavor.flavor_id = 1
        assert flavor_base_bus_obj.flavor_id == 1
    def test_code(self, flavor_base_bus_obj, flavor):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        flavor.code = test_uuid
        assert flavor_base_bus_obj.code == test_uuid
    def test_code_setter(self, flavor_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        flavor_base_bus_obj.code = test_uuid
        assert flavor_base_bus_obj.code == test_uuid
    def test_code_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            flavor_base_bus_obj.code = "not-a-uuid"
    def test_last_change_code(self, flavor_base_bus_obj, flavor):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the FlavorBaseBusiness class.
        Args:
            flavor_base_bus_obj (FlavorBaseBusiness):
                An instance of the
                FlavorBaseBusiness class.
            flavor (Flavor): An instance of the Flavor class.
        Returns:
            None
        """
        flavor.last_change_code = 123
        assert flavor_base_bus_obj.last_change_code == 123
    def test_last_change_code_setter(self, flavor_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        flavor_base_bus_obj.last_change_code = 123
        assert flavor_base_bus_obj.last_change_code == 123
    def test_last_change_code_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            flavor_base_bus_obj.last_change_code = "not-an-int"
    def test_insert_user_id(self, flavor_base_bus_obj, flavor):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        flavor.insert_user_id = test_uuid
        assert flavor_base_bus_obj.insert_user_id == test_uuid
    def test_insert_user_id_setter(self, flavor_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        flavor_base_bus_obj.insert_user_id = test_uuid
        assert flavor_base_bus_obj.insert_user_id == test_uuid
    def test_insert_user_id_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            flavor_base_bus_obj.insert_user_id = "not-a-uuid"
# endset
    # description,
    def test_description(self, flavor_base_bus_obj, flavor):
        """
        Test case for the description property.
        """
        flavor.description = "Vanilla"
        assert flavor_base_bus_obj.description == "Vanilla"
    def test_description_setter(self, flavor_base_bus_obj):
        """
        Test case for the description setter.
        """
        flavor_base_bus_obj.description = "Vanilla"
        assert flavor_base_bus_obj.description == "Vanilla"
    def test_description_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        description property.
        """
        with pytest.raises(AssertionError):
            flavor_base_bus_obj.description = 123
    # displayOrder,
    def test_display_order(self, flavor_base_bus_obj, flavor):
        """
        Test case for the display_order property.
        """
        flavor.display_order = 1
        assert flavor_base_bus_obj.display_order == 1
    def test_display_order_setter(self, flavor_base_bus_obj):
        """
        Test case for the display_order setter.
        """
        flavor_base_bus_obj.display_order = 1
        assert flavor_base_bus_obj.display_order == 1
    def test_display_order_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        display_order property.
        """
        with pytest.raises(AssertionError):
            flavor_base_bus_obj.display_order = "not-an-int"
    # isActive,
    def test_is_active(self, flavor_base_bus_obj, flavor):
        """
        Test case for the is_active property.
        """
        flavor.is_active = True
        assert flavor_base_bus_obj.is_active is True
    def test_is_active_setter(self, flavor_base_bus_obj):
        """
        Test case for the is_active setter.
        """
        flavor_base_bus_obj.is_active = True
        assert flavor_base_bus_obj.is_active is True
    def test_is_active_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            flavor_base_bus_obj.is_active = "not-a-boolean"
    # lookupEnumName,
    def test_lookup_enum_name(self, flavor_base_bus_obj, flavor):
        """
        Test case for the lookup_enum_name property.
        """
        flavor.lookup_enum_name = "Vanilla"
        assert flavor_base_bus_obj.lookup_enum_name == "Vanilla"
    def test_lookup_enum_name_setter(self, flavor_base_bus_obj):
        """
        Test case for the lookup_enum_name setter.
        """
        flavor_base_bus_obj.lookup_enum_name = "Vanilla"
        assert flavor_base_bus_obj.lookup_enum_name == "Vanilla"
    def test_lookup_enum_name_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        lookup_enum_name property.
        """
        with pytest.raises(AssertionError):
            flavor_base_bus_obj.lookup_enum_name = 123
    # name,
    def test_name(self, flavor_base_bus_obj, flavor):
        """
        Test case for the name property.
        """
        flavor.name = "Vanilla"
        assert flavor_base_bus_obj.name == "Vanilla"
    def test_name_setter(self, flavor_base_bus_obj):
        """
        Test case for the name setter.
        """
        flavor_base_bus_obj.name = "Vanilla"
        assert flavor_base_bus_obj.name == "Vanilla"
    def test_name_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            flavor_base_bus_obj.name = 123
    # PacID
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    def test_pac_id(self, flavor_base_bus_obj, flavor):
        """
        Test case for the pac_id property.
        """
        flavor.pac_id = 1
        assert flavor_base_bus_obj.pac_id == 1
    def test_pac_id_setter(self, flavor_base_bus_obj):
        """
        Test case for the pac_id setter.
        """
        flavor_base_bus_obj.pac_id = 1
        assert flavor_base_bus_obj.pac_id == 1
    def test_pac_id_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        pac_id property.
        """
        with pytest.raises(AssertionError):
            flavor_base_bus_obj.pac_id = "not-an-int"
# endset
    def test_insert_utc_date_time(self, flavor_base_bus_obj, flavor):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        flavor.insert_utc_date_time = test_datetime
        assert flavor_base_bus_obj.insert_utc_date_time == test_datetime
    def test_insert_utc_date_time_setter(self, flavor_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        flavor_base_bus_obj.insert_utc_date_time = test_datetime
        assert flavor_base_bus_obj.insert_utc_date_time == test_datetime
    def test_insert_utc_date_time_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            flavor_base_bus_obj.insert_utc_date_time = "not-a-datetime"
    def test_last_update_utc_date_time(self, flavor_base_bus_obj, flavor):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        flavor.last_update_utc_date_time = test_datetime
        assert flavor_base_bus_obj.last_update_utc_date_time == test_datetime
    def test_last_update_utc_date_time_setter(self, flavor_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        flavor_base_bus_obj.last_update_utc_date_time = test_datetime
        assert flavor_base_bus_obj.last_update_utc_date_time == test_datetime
    def test_last_update_utc_date_time_invalid_value(self, flavor_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            flavor_base_bus_obj.last_update_utc_date_time = "not-a-datetime"

