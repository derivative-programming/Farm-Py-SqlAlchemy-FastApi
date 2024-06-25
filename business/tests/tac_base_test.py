# business/tests/tac_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the TacBusObj class.
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
from business.tac_base import TacBaseBusObj
from helpers.session_context import SessionContext
from managers.tac import TacManager
from models import Tac
from models.factory import TacFactory
from services.logging_config import get_logger

from ..tac import TacBusObj


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
def tac():
    """
    Fixture that returns a mock tac object.
    """
    return Mock(spec=Tac)


@pytest.fixture
def tac_base_bus_obj(fake_session_context, tac):
    """
    Fixture that returns a TacBaseBusObj instance.
    """
    tac_base = TacBaseBusObj(fake_session_context)
    tac_base.tac = tac
    return tac_base


class TestTacBaseBusObj:
    """
    Unit tests for the TacBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def tac_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the TacManager class.
        """
        session_context = SessionContext(dict(), session)
        return TacManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def tac_bus_obj(self, session):
        """
        Fixture that returns an instance of the TacBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return TacBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_tac(self, session):
        """
        Fixture that returns a new instance of
        the Tac class.
        """

        return await TacFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_tac(
        self,
        tac_bus_obj: TacBusObj
    ):
        """
        Test case for creating a new tac.
        """
        # Test creating a new tac

        assert tac_bus_obj.tac_id == 0

        # assert isinstance(tac_bus_obj.tac_id, int)
        assert isinstance(
            tac_bus_obj.code, uuid.UUID)

        assert isinstance(
            tac_bus_obj.last_change_code, int)

        assert tac_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert tac_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(tac_bus_obj.description, str)
        assert isinstance(tac_bus_obj.display_order, int)
        assert isinstance(tac_bus_obj.is_active, bool)
        assert isinstance(tac_bus_obj.lookup_enum_name, str)
        assert isinstance(tac_bus_obj.name, str)
        assert isinstance(tac_bus_obj.pac_id, int)

    @pytest.mark.asyncio
    async def test_load_with_tac_obj(
        self,
        tac_manager: TacManager,
        tac_bus_obj: TacBusObj,
        new_tac: Tac
    ):
        """
        Test case for loading data from a
        tac object instance.
        """

        tac_bus_obj.load_from_obj_instance(
            new_tac)

        assert tac_manager.is_equal(
            tac_bus_obj.tac, new_tac) is True

    @pytest.mark.asyncio
    async def test_load_with_tac_id(
        self,
        tac_manager: TacManager,
        tac_bus_obj: TacBusObj,
        new_tac: Tac
    ):
        """
        Test case for loading data from a
        tac ID.
        """

        new_tac_tac_id = new_tac.tac_id

        await tac_bus_obj.load_from_id(
            new_tac_tac_id)

        assert tac_manager.is_equal(
            tac_bus_obj.tac, new_tac) is True

    @pytest.mark.asyncio
    async def test_load_with_tac_code(
        self,
        tac_manager: TacManager,
        tac_bus_obj: TacBusObj,
        new_tac: Tac
    ):
        """
        Test case for loading data from a
        tac code.
        """

        await tac_bus_obj.load_from_code(
            new_tac.code)

        assert tac_manager.is_equal(
            tac_bus_obj.tac, new_tac) is True

    @pytest.mark.asyncio
    async def test_load_with_tac_json(
        self,
        tac_manager: TacManager,
        tac_bus_obj: TacBusObj,
        new_tac: Tac
    ):
        """
        Test case for loading data from a
        tac JSON.
        """

        tac_json = tac_manager.to_json(new_tac)

        await tac_bus_obj.load_from_json(
            tac_json)

        assert tac_manager.is_equal(
            tac_bus_obj.tac, new_tac) is True

    @pytest.mark.asyncio
    async def test_load_with_tac_dict(
        self,
        tac_manager: TacManager,
        tac_bus_obj: TacBusObj,
        new_tac: Tac
    ):
        """
        Test case for loading data from a
        tac dictionary.
        """

        logger.info("test_load_with_tac_dict 1")

        tac_dict = tac_manager.to_dict(new_tac)

        logger.info(tac_dict)

        await tac_bus_obj.load_from_dict(
            tac_dict)

        assert tac_manager.is_equal(
            tac_bus_obj.tac,
            new_tac) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_tac(
        self,
        tac_bus_obj: TacBusObj
    ):
        """
        Test case for retrieving a nonexistent tac.
        """
        # Test retrieving a nonexistent
        # tac raises an exception
        await tac_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert tac_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_tac(
        self,
        tac_manager: TacManager,
        tac_bus_obj: TacBusObj,
        new_tac: Tac
    ):
        """
        Test case for updating a tac's data.
        """
        # Test updating a tac's data

        new_tac_tac_id_value = new_tac.tac_id

        new_tac = await tac_manager.get_by_id(
            new_tac_tac_id_value)

        assert isinstance(new_tac, Tac)

        new_code = uuid.uuid4()

        tac_bus_obj.load_from_obj_instance(
            new_tac)

        assert tac_manager.is_equal(
            tac_bus_obj.tac,
            new_tac) is True

        tac_bus_obj.code = new_code

        await tac_bus_obj.save()

        new_tac_tac_id_value = new_tac.tac_id

        new_tac = await tac_manager.get_by_id(
            new_tac_tac_id_value)

        assert tac_manager.is_equal(
            tac_bus_obj.tac,
            new_tac) is True

    @pytest.mark.asyncio
    async def test_delete_tac(
        self,
        tac_manager: TacManager,
        tac_bus_obj: TacBusObj,
        new_tac: Tac
    ):
        """
        Test case for deleting a tac.
        """

        assert tac_bus_obj.tac is not None

        assert tac_bus_obj.tac_id == 0

        tac_bus_obj.load_from_obj_instance(
            new_tac)

        assert tac_bus_obj.tac_id is not None

        await tac_bus_obj.delete()

        new_tac_tac_id_value = new_tac.tac_id

        new_tac = await tac_manager.get_by_id(
            new_tac_tac_id_value)

        assert new_tac is None

    def test_get_session_context(
        self,
        tac_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert tac_base_bus_obj.get_session_context() == fake_session_context

    @pytest.mark.asyncio
    async def test_refresh(self, tac_base_bus_obj, tac):
        """
        Test case for refreshing the tac data.
        """
        with patch(
            'business.tac_base.TacManager',
            autospec=True
        ) as mock_tac_manager:
            mock_tac_manager_instance = mock_tac_manager.return_value
            mock_tac_manager_instance.refresh = AsyncMock(return_value=tac)

            refreshed_tac_base = await tac_base_bus_obj.refresh()
            assert refreshed_tac_base.tac == tac
            mock_tac_manager_instance.refresh.assert_called_once_with(tac)

    def test_is_valid(self, tac_base_bus_obj):
        """
        Test case for checking if the tac data is valid.
        """
        assert tac_base_bus_obj.is_valid() is True

        tac_base_bus_obj.tac = None
        assert tac_base_bus_obj.is_valid() is False

    def test_to_dict(self, tac_base_bus_obj):
        """
        Test case for converting the tac data to a dictionary.
        """
        with patch(
            'business.tac_base.TacManager',
            autospec=True
        ) as mock_tac_manager:
            mock_tac_manager_instance = mock_tac_manager.return_value
            mock_tac_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            tac_dict = tac_base_bus_obj.to_dict()
            assert tac_dict == {"key": "value"}
            mock_tac_manager_instance.to_dict.assert_called_once_with(
                tac_base_bus_obj.tac)

    def test_to_json(self, tac_base_bus_obj):
        """
        Test case for converting the tac data to JSON.
        """
        with patch(
            'business.tac_base.TacManager',
            autospec=True
        ) as mock_tac_manager:
            mock_tac_manager_instance = mock_tac_manager.return_value
            mock_tac_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            tac_json = tac_base_bus_obj.to_json()
            assert tac_json == '{"key": "value"}'
            mock_tac_manager_instance.to_json.assert_called_once_with(
                tac_base_bus_obj.tac)

    def test_get_obj(self, tac_base_bus_obj, tac):
        """
        Test case for getting the tac object.
        """
        assert tac_base_bus_obj.get_obj() == tac

    def test_get_object_name(self, tac_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert tac_base_bus_obj.get_object_name() == "tac"

    def test_get_id(self, tac_base_bus_obj, tac):
        """
        Test case for getting the tac ID.
        """
        tac.tac_id = 1
        assert tac_base_bus_obj.get_id() == 1

    def test_tac_id(self, tac_base_bus_obj, tac):
        """
        Test case for the tac_id property.
        """
        tac.tac_id = 1
        assert tac_base_bus_obj.tac_id == 1

    def test_code(self, tac_base_bus_obj, tac):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        tac.code = test_uuid
        assert tac_base_bus_obj.code == test_uuid

    def test_code_setter(self, tac_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        tac_base_bus_obj.code = test_uuid
        assert tac_base_bus_obj.code == test_uuid

    def test_code_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            tac_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(self, tac_base_bus_obj, tac):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the TacBaseBusiness class.

        Args:
            tac_base_bus_obj (TacBaseBusiness):
                An instance of the
                TacBaseBusiness class.
            tac (Tac): An instance of the Tac class.

        Returns:
            None
        """
        tac.last_change_code = 123
        assert tac_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(self, tac_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        tac_base_bus_obj.last_change_code = 123
        assert tac_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            tac_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(self, tac_base_bus_obj, tac):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        tac.insert_user_id = test_uuid
        assert tac_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_setter(self, tac_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        tac_base_bus_obj.insert_user_id = test_uuid
        assert tac_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            tac_base_bus_obj.insert_user_id = "not-a-uuid"
    # description

    def test_description(self, tac_base_bus_obj, tac):
        """
        Test case for the description property.
        """
        tac.description = "Vanilla"
        assert tac_base_bus_obj.description == "Vanilla"

    def test_description_setter(self, tac_base_bus_obj):
        """
        Test case for the description setter.
        """
        tac_base_bus_obj.description = "Vanilla"
        assert tac_base_bus_obj.description == "Vanilla"

    def test_description_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        description property.
        """
        with pytest.raises(AssertionError):
            tac_base_bus_obj.description = 123
    # displayOrder

    def test_display_order(self, tac_base_bus_obj, tac):
        """
        Test case for the display_order property.
        """
        tac.display_order = 1
        assert tac_base_bus_obj.display_order == 1

    def test_display_order_setter(self, tac_base_bus_obj):
        """
        Test case for the display_order setter.
        """
        tac_base_bus_obj.display_order = 1
        assert tac_base_bus_obj.display_order == 1

    def test_display_order_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        display_order property.
        """
        with pytest.raises(AssertionError):
            tac_base_bus_obj.display_order = "not-an-int"
    # isActive

    def test_is_active(self, tac_base_bus_obj, tac):
        """
        Test case for the is_active property.
        """
        tac.is_active = True
        assert tac_base_bus_obj.is_active is True

    def test_is_active_setter(self, tac_base_bus_obj):
        """
        Test case for the is_active setter.
        """
        tac_base_bus_obj.is_active = True
        assert tac_base_bus_obj.is_active is True

    def test_is_active_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            tac_base_bus_obj.is_active = "not-a-boolean"
    # lookupEnumName

    def test_lookup_enum_name(self, tac_base_bus_obj, tac):
        """
        Test case for the lookup_enum_name property.
        """
        tac.lookup_enum_name = "Vanilla"
        assert tac_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_setter(self, tac_base_bus_obj):
        """
        Test case for the lookup_enum_name setter.
        """
        tac_base_bus_obj.lookup_enum_name = "Vanilla"
        assert tac_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        lookup_enum_name property.
        """
        with pytest.raises(AssertionError):
            tac_base_bus_obj.lookup_enum_name = 123
    # name

    def test_name(self, tac_base_bus_obj, tac):
        """
        Test case for the name property.
        """
        tac.name = "Vanilla"
        assert tac_base_bus_obj.name == "Vanilla"

    def test_name_setter(self, tac_base_bus_obj):
        """
        Test case for the name setter.
        """
        tac_base_bus_obj.name = "Vanilla"
        assert tac_base_bus_obj.name == "Vanilla"

    def test_name_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            tac_base_bus_obj.name = 123
    # PacID
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_pac_id(self, tac_base_bus_obj, tac):
        """
        Test case for the pac_id property.
        """
        tac.pac_id = 1
        assert tac_base_bus_obj.pac_id == 1

    def test_pac_id_setter(self, tac_base_bus_obj):
        """
        Test case for the pac_id setter.
        """
        tac_base_bus_obj.pac_id = 1
        assert tac_base_bus_obj.pac_id == 1

    def test_pac_id_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        pac_id property.
        """
        with pytest.raises(AssertionError):
            tac_base_bus_obj.pac_id = "not-an-int"

    def test_insert_utc_date_time(self, tac_base_bus_obj, tac):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        tac.insert_utc_date_time = test_datetime
        assert tac_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_setter(self, tac_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        tac_base_bus_obj.insert_utc_date_time = test_datetime
        assert tac_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            tac_base_bus_obj.insert_utc_date_time = "not-a-datetime"

    def test_last_update_utc_date_time(self, tac_base_bus_obj, tac):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        tac.last_update_utc_date_time = test_datetime
        assert tac_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_setter(self, tac_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        tac_base_bus_obj.last_update_utc_date_time = test_datetime
        assert tac_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_invalid_value(self, tac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            tac_base_bus_obj.last_update_utc_date_time = "not-a-datetime"


    @pytest.mark.asyncio
    async def test_build_organization(
        self,
        tac_bus_obj: TacBusObj,
        new_tac: Tac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await tac_bus_obj.load_from_id(
            new_tac.tac_id
        )

        organization_bus_obj = await tac_bus_obj.build_organization()

        assert organization_bus_obj.tac_id == tac_bus_obj.tac_id
        assert organization_bus_obj.tac_code_peek == tac_bus_obj.code

        await organization_bus_obj.save()

        assert organization_bus_obj.organization_id > 0


    @pytest.mark.asyncio
    async def test_get_all_organization(
        self,
        tac_bus_obj: TacBusObj,
        new_tac: Tac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_tac_tac_id = (
            new_tac.tac_id
        )

        await tac_bus_obj.load_from_id(
            new_tac_tac_id
        )

        organization_bus_obj = await tac_bus_obj.build_organization()

        await organization_bus_obj.save()

        organization_list = await tac_bus_obj.get_all_organization()

        assert len(organization_list) >= 1

        #assert organization_list[0].organization_id > 0

        #assert organization_list[0].organization_id == organization_bus_obj.organization_id


    @pytest.mark.asyncio
    async def test_build_customer(
        self,
        tac_bus_obj: TacBusObj,
        new_tac: Tac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await tac_bus_obj.load_from_id(
            new_tac.tac_id
        )

        customer_bus_obj = await tac_bus_obj.build_customer()

        assert customer_bus_obj.tac_id == tac_bus_obj.tac_id
        assert customer_bus_obj.tac_code_peek == tac_bus_obj.code

        await customer_bus_obj.save()

        assert customer_bus_obj.customer_id > 0


    @pytest.mark.asyncio
    async def test_get_all_customer(
        self,
        tac_bus_obj: TacBusObj,
        new_tac: Tac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_tac_tac_id = (
            new_tac.tac_id
        )

        await tac_bus_obj.load_from_id(
            new_tac_tac_id
        )

        customer_bus_obj = await tac_bus_obj.build_customer()

        await customer_bus_obj.save()

        customer_list = await tac_bus_obj.get_all_customer()

        assert len(customer_list) >= 1

        #assert customer_list[0].customer_id > 0

        #assert customer_list[0].customer_id == customer_bus_obj.customer_id

