# business/tests/pac_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the PacBusObj class.
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
from business.pac_base import PacBaseBusObj
from helpers.session_context import SessionContext
from managers.pac import PacManager
from models import Pac
from models.factory import PacFactory
from services.logging_config import get_logger

from ..pac import PacBusObj


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
def pac():
    """
    Fixture that returns a mock pac object.
    """
    return Mock(spec=Pac)


@pytest.fixture
def pac_base_bus_obj(fake_session_context, pac):
    """
    Fixture that returns a PacBaseBusObj instance.
    """
    pac_base = PacBaseBusObj(fake_session_context)
    pac_base.pac = pac
    return pac_base


class TestPacBaseBusObj:
    """
    Unit tests for the PacBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def pac_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the PacManager class.
        """
        session_context = SessionContext(dict(), session)
        return PacManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def pac_bus_obj(self, session):
        """
        Fixture that returns an instance of the PacBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return PacBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_pac(self, session):
        """
        Fixture that returns a new instance of
        the Pac class.
        """

        return await PacFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_pac(
        self,
        pac_bus_obj: PacBusObj
    ):
        """
        Test case for creating a new pac.
        """
        # Test creating a new pac

        assert pac_bus_obj.pac_id == 0

        # assert isinstance(pac_bus_obj.pac_id, int)
        assert isinstance(
            pac_bus_obj.code, uuid.UUID)

        assert isinstance(
            pac_bus_obj.last_change_code, int)

        assert pac_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert pac_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(pac_bus_obj.description, str)
        assert isinstance(pac_bus_obj.display_order, int)
        assert isinstance(pac_bus_obj.is_active, bool)
        assert isinstance(pac_bus_obj.lookup_enum_name, str)
        assert isinstance(pac_bus_obj.name, str)

    @pytest.mark.asyncio
    async def test_load_with_pac_obj(
        self,
        pac_manager: PacManager,
        pac_bus_obj: PacBusObj,
        new_pac: Pac
    ):
        """
        Test case for loading data from a
        pac object instance.
        """

        pac_bus_obj.load_from_obj_instance(
            new_pac)

        assert pac_manager.is_equal(
            pac_bus_obj.pac, new_pac) is True

    @pytest.mark.asyncio
    async def test_load_with_pac_id(
        self,
        pac_manager: PacManager,
        pac_bus_obj: PacBusObj,
        new_pac: Pac
    ):
        """
        Test case for loading data from a
        pac ID.
        """

        new_pac_pac_id = new_pac.pac_id

        await pac_bus_obj.load_from_id(
            new_pac_pac_id)

        assert pac_manager.is_equal(
            pac_bus_obj.pac, new_pac) is True

    @pytest.mark.asyncio
    async def test_load_with_pac_code(
        self,
        pac_manager: PacManager,
        pac_bus_obj: PacBusObj,
        new_pac: Pac
    ):
        """
        Test case for loading data from a
        pac code.
        """

        await pac_bus_obj.load_from_code(
            new_pac.code)

        assert pac_manager.is_equal(
            pac_bus_obj.pac, new_pac) is True

    @pytest.mark.asyncio
    async def test_load_with_pac_json(
        self,
        pac_manager: PacManager,
        pac_bus_obj: PacBusObj,
        new_pac: Pac
    ):
        """
        Test case for loading data from a
        pac JSON.
        """

        pac_json = pac_manager.to_json(new_pac)

        await pac_bus_obj.load_from_json(
            pac_json)

        assert pac_manager.is_equal(
            pac_bus_obj.pac, new_pac) is True

    @pytest.mark.asyncio
    async def test_load_with_pac_dict(
        self,
        pac_manager: PacManager,
        pac_bus_obj: PacBusObj,
        new_pac: Pac
    ):
        """
        Test case for loading data from a
        pac dictionary.
        """

        logger.info("test_load_with_pac_dict 1")

        pac_dict = pac_manager.to_dict(new_pac)

        logger.info(pac_dict)

        await pac_bus_obj.load_from_dict(
            pac_dict)

        assert pac_manager.is_equal(
            pac_bus_obj.pac,
            new_pac) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_pac(
        self,
        pac_bus_obj: PacBusObj
    ):
        """
        Test case for retrieving a nonexistent pac.
        """
        # Test retrieving a nonexistent
        # pac raises an exception
        await pac_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert pac_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_pac(
        self,
        pac_manager: PacManager,
        pac_bus_obj: PacBusObj,
        new_pac: Pac
    ):
        """
        Test case for updating a pac's data.
        """
        # Test updating a pac's data

        new_pac_pac_id_value = new_pac.pac_id

        new_pac = await pac_manager.get_by_id(
            new_pac_pac_id_value)

        assert isinstance(new_pac, Pac)

        new_code = uuid.uuid4()

        pac_bus_obj.load_from_obj_instance(
            new_pac)

        assert pac_manager.is_equal(
            pac_bus_obj.pac,
            new_pac) is True

        pac_bus_obj.code = new_code

        await pac_bus_obj.save()

        new_pac_pac_id_value = new_pac.pac_id

        new_pac = await pac_manager.get_by_id(
            new_pac_pac_id_value)

        assert pac_manager.is_equal(
            pac_bus_obj.pac,
            new_pac) is True

    @pytest.mark.asyncio
    async def test_delete_pac(
        self,
        pac_manager: PacManager,
        pac_bus_obj: PacBusObj,
        new_pac: Pac
    ):
        """
        Test case for deleting a pac.
        """

        assert pac_bus_obj.pac is not None

        assert pac_bus_obj.pac_id == 0

        pac_bus_obj.load_from_obj_instance(
            new_pac)

        assert pac_bus_obj.pac_id is not None

        await pac_bus_obj.delete()

        new_pac_pac_id_value = new_pac.pac_id

        new_pac = await pac_manager.get_by_id(
            new_pac_pac_id_value)

        assert new_pac is None

    def test_get_session_context(
        self,
        pac_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert pac_base_bus_obj.get_session_context() == fake_session_context

    @pytest.mark.asyncio
    async def test_refresh(self, pac_base_bus_obj, pac):
        """
        Test case for refreshing the pac data.
        """
        with patch(
            'business.pac_base.PacManager',
            autospec=True
        ) as mock_pac_manager:
            mock_pac_manager_instance = mock_pac_manager.return_value
            mock_pac_manager_instance.refresh = AsyncMock(return_value=pac)

            refreshed_pac_base = await pac_base_bus_obj.refresh()
            assert refreshed_pac_base.pac == pac
            mock_pac_manager_instance.refresh.assert_called_once_with(pac)

    def test_is_valid(self, pac_base_bus_obj):
        """
        Test case for checking if the pac data is valid.
        """
        assert pac_base_bus_obj.is_valid() is True

        pac_base_bus_obj.pac = None
        assert pac_base_bus_obj.is_valid() is False

    def test_to_dict(self, pac_base_bus_obj):
        """
        Test case for converting the pac data to a dictionary.
        """
        with patch(
            'business.pac_base.PacManager',
            autospec=True
        ) as mock_pac_manager:
            mock_pac_manager_instance = mock_pac_manager.return_value
            mock_pac_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            pac_dict = pac_base_bus_obj.to_dict()
            assert pac_dict == {"key": "value"}
            mock_pac_manager_instance.to_dict.assert_called_once_with(
                pac_base_bus_obj.pac)

    def test_to_json(self, pac_base_bus_obj):
        """
        Test case for converting the pac data to JSON.
        """
        with patch(
            'business.pac_base.PacManager',
            autospec=True
        ) as mock_pac_manager:
            mock_pac_manager_instance = mock_pac_manager.return_value
            mock_pac_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            pac_json = pac_base_bus_obj.to_json()
            assert pac_json == '{"key": "value"}'
            mock_pac_manager_instance.to_json.assert_called_once_with(
                pac_base_bus_obj.pac)

    def test_get_obj(self, pac_base_bus_obj, pac):
        """
        Test case for getting the pac object.
        """
        assert pac_base_bus_obj.get_obj() == pac

    def test_get_object_name(self, pac_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert pac_base_bus_obj.get_object_name() == "pac"

    def test_get_id(self, pac_base_bus_obj, pac):
        """
        Test case for getting the pac ID.
        """
        pac.pac_id = 1
        assert pac_base_bus_obj.get_id() == 1

    def test_pac_id(self, pac_base_bus_obj, pac):
        """
        Test case for the pac_id property.
        """
        pac.pac_id = 1
        assert pac_base_bus_obj.pac_id == 1

    def test_code(self, pac_base_bus_obj, pac):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        pac.code = test_uuid
        assert pac_base_bus_obj.code == test_uuid

    def test_code_setter(self, pac_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        pac_base_bus_obj.code = test_uuid
        assert pac_base_bus_obj.code == test_uuid

    def test_code_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            pac_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(self, pac_base_bus_obj, pac):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the PacBaseBusiness class.

        Args:
            pac_base_bus_obj (PacBaseBusiness):
                An instance of the
                PacBaseBusiness class.
            pac (Pac): An instance of the Pac class.

        Returns:
            None
        """
        pac.last_change_code = 123
        assert pac_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(self, pac_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        pac_base_bus_obj.last_change_code = 123
        assert pac_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            pac_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(self, pac_base_bus_obj, pac):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        pac.insert_user_id = test_uuid
        assert pac_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_setter(self, pac_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        pac_base_bus_obj.insert_user_id = test_uuid
        assert pac_base_bus_obj.insert_user_id == test_uuid

    def test_insert_user_id_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            pac_base_bus_obj.insert_user_id = "not-a-uuid"
    # description

    def test_description(self, pac_base_bus_obj, pac):
        """
        Test case for the description property.
        """
        pac.description = "Vanilla"
        assert pac_base_bus_obj.description == "Vanilla"

    def test_description_setter(self, pac_base_bus_obj):
        """
        Test case for the description setter.
        """
        pac_base_bus_obj.description = "Vanilla"
        assert pac_base_bus_obj.description == "Vanilla"

    def test_description_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        description property.
        """
        with pytest.raises(AssertionError):
            pac_base_bus_obj.description = 123
    # displayOrder

    def test_display_order(self, pac_base_bus_obj, pac):
        """
        Test case for the display_order property.
        """
        pac.display_order = 1
        assert pac_base_bus_obj.display_order == 1

    def test_display_order_setter(self, pac_base_bus_obj):
        """
        Test case for the display_order setter.
        """
        pac_base_bus_obj.display_order = 1
        assert pac_base_bus_obj.display_order == 1

    def test_display_order_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        display_order property.
        """
        with pytest.raises(AssertionError):
            pac_base_bus_obj.display_order = "not-an-int"
    # isActive

    def test_is_active(self, pac_base_bus_obj, pac):
        """
        Test case for the is_active property.
        """
        pac.is_active = True
        assert pac_base_bus_obj.is_active is True

    def test_is_active_setter(self, pac_base_bus_obj):
        """
        Test case for the is_active setter.
        """
        pac_base_bus_obj.is_active = True
        assert pac_base_bus_obj.is_active is True

    def test_is_active_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_active property.
        """
        with pytest.raises(ValueError):
            pac_base_bus_obj.is_active = "not-a-boolean"
    # lookupEnumName

    def test_lookup_enum_name(self, pac_base_bus_obj, pac):
        """
        Test case for the lookup_enum_name property.
        """
        pac.lookup_enum_name = "Vanilla"
        assert pac_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_setter(self, pac_base_bus_obj):
        """
        Test case for the lookup_enum_name setter.
        """
        pac_base_bus_obj.lookup_enum_name = "Vanilla"
        assert pac_base_bus_obj.lookup_enum_name == "Vanilla"

    def test_lookup_enum_name_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        lookup_enum_name property.
        """
        with pytest.raises(AssertionError):
            pac_base_bus_obj.lookup_enum_name = 123
    # name

    def test_name(self, pac_base_bus_obj, pac):
        """
        Test case for the name property.
        """
        pac.name = "Vanilla"
        assert pac_base_bus_obj.name == "Vanilla"

    def test_name_setter(self, pac_base_bus_obj):
        """
        Test case for the name setter.
        """
        pac_base_bus_obj.name = "Vanilla"
        assert pac_base_bus_obj.name == "Vanilla"

    def test_name_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            pac_base_bus_obj.name = 123
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,

    def test_insert_utc_date_time(self, pac_base_bus_obj, pac):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        pac.insert_utc_date_time = test_datetime
        assert pac_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_setter(self, pac_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        pac_base_bus_obj.insert_utc_date_time = test_datetime
        assert pac_base_bus_obj.insert_utc_date_time == test_datetime

    def test_insert_utc_date_time_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            pac_base_bus_obj.insert_utc_date_time = "not-a-datetime"

    def test_last_update_utc_date_time(self, pac_base_bus_obj, pac):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        pac.last_update_utc_date_time = test_datetime
        assert pac_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_setter(self, pac_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        pac_base_bus_obj.last_update_utc_date_time = test_datetime
        assert pac_base_bus_obj.last_update_utc_date_time == test_datetime

    def test_last_update_utc_date_time_invalid_value(self, pac_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            pac_base_bus_obj.last_update_utc_date_time = "not-a-datetime"


    @pytest.mark.asyncio
    async def test_build_tri_state_filter(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await pac_bus_obj.load_from_id(
            new_pac.pac_id
        )

        tri_state_filter_bus_obj = await pac_bus_obj.build_tri_state_filter()

        assert tri_state_filter_bus_obj.pac_id == pac_bus_obj.pac_id
        assert tri_state_filter_bus_obj.pac_code_peek == pac_bus_obj.code

        await tri_state_filter_bus_obj.save()

        assert tri_state_filter_bus_obj.tri_state_filter_id > 0

    @pytest.mark.asyncio
    async def test_get_all_tri_state_filter(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_pac_pac_id = (
            new_pac.pac_id
        )

        await pac_bus_obj.load_from_id(
            new_pac_pac_id
        )

        tri_state_filter_bus_obj = await pac_bus_obj.build_tri_state_filter()

        await tri_state_filter_bus_obj.save()

        tri_state_filter_list = await pac_bus_obj.get_all_tri_state_filter()

        assert len(tri_state_filter_list) >= 1

        #assert tri_state_filter_list[0].tri_state_filter_id > 0

        #assert tri_state_filter_list[0].tri_state_filter_id == tri_state_filter_bus_obj.tri_state_filter_id


    @pytest.mark.asyncio
    async def test_build_tac(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await pac_bus_obj.load_from_id(
            new_pac.pac_id
        )

        tac_bus_obj = await pac_bus_obj.build_tac()

        assert tac_bus_obj.pac_id == pac_bus_obj.pac_id
        assert tac_bus_obj.pac_code_peek == pac_bus_obj.code

        await tac_bus_obj.save()

        assert tac_bus_obj.tac_id > 0

    @pytest.mark.asyncio
    async def test_get_all_tac(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_pac_pac_id = (
            new_pac.pac_id
        )

        await pac_bus_obj.load_from_id(
            new_pac_pac_id
        )

        tac_bus_obj = await pac_bus_obj.build_tac()

        await tac_bus_obj.save()

        tac_list = await pac_bus_obj.get_all_tac()

        assert len(tac_list) >= 1

        #assert tac_list[0].tac_id > 0

        #assert tac_list[0].tac_id == tac_bus_obj.tac_id


    @pytest.mark.asyncio
    async def test_build_role(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await pac_bus_obj.load_from_id(
            new_pac.pac_id
        )

        role_bus_obj = await pac_bus_obj.build_role()

        assert role_bus_obj.pac_id == pac_bus_obj.pac_id
        assert role_bus_obj.pac_code_peek == pac_bus_obj.code

        await role_bus_obj.save()

        assert role_bus_obj.role_id > 0

    @pytest.mark.asyncio
    async def test_get_all_role(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_pac_pac_id = (
            new_pac.pac_id
        )

        await pac_bus_obj.load_from_id(
            new_pac_pac_id
        )

        role_bus_obj = await pac_bus_obj.build_role()

        await role_bus_obj.save()

        role_list = await pac_bus_obj.get_all_role()

        assert len(role_list) >= 1

        #assert role_list[0].role_id > 0

        #assert role_list[0].role_id == role_bus_obj.role_id


    @pytest.mark.asyncio
    async def test_build_land(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await pac_bus_obj.load_from_id(
            new_pac.pac_id
        )

        land_bus_obj = await pac_bus_obj.build_land()

        assert land_bus_obj.pac_id == pac_bus_obj.pac_id
        assert land_bus_obj.pac_code_peek == pac_bus_obj.code

        await land_bus_obj.save()

        assert land_bus_obj.land_id > 0

    @pytest.mark.asyncio
    async def test_get_all_land(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_pac_pac_id = (
            new_pac.pac_id
        )

        await pac_bus_obj.load_from_id(
            new_pac_pac_id
        )

        land_bus_obj = await pac_bus_obj.build_land()

        await land_bus_obj.save()

        land_list = await pac_bus_obj.get_all_land()

        assert len(land_list) >= 1

        #assert land_list[0].land_id > 0

        #assert land_list[0].land_id == land_bus_obj.land_id


    @pytest.mark.asyncio
    async def test_build_flavor(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await pac_bus_obj.load_from_id(
            new_pac.pac_id
        )

        flavor_bus_obj = await pac_bus_obj.build_flavor()

        assert flavor_bus_obj.pac_id == pac_bus_obj.pac_id
        assert flavor_bus_obj.pac_code_peek == pac_bus_obj.code

        await flavor_bus_obj.save()

        assert flavor_bus_obj.flavor_id > 0

    @pytest.mark.asyncio
    async def test_get_all_flavor(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_pac_pac_id = (
            new_pac.pac_id
        )

        await pac_bus_obj.load_from_id(
            new_pac_pac_id
        )

        flavor_bus_obj = await pac_bus_obj.build_flavor()

        await flavor_bus_obj.save()

        flavor_list = await pac_bus_obj.get_all_flavor()

        assert len(flavor_list) >= 1

        #assert flavor_list[0].flavor_id > 0

        #assert flavor_list[0].flavor_id == flavor_bus_obj.flavor_id


    @pytest.mark.asyncio
    async def test_build_error_log(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await pac_bus_obj.load_from_id(
            new_pac.pac_id
        )

        error_log_bus_obj = await pac_bus_obj.build_error_log()

        assert error_log_bus_obj.pac_id == pac_bus_obj.pac_id
        assert error_log_bus_obj.pac_code_peek == pac_bus_obj.code

        await error_log_bus_obj.save()

        assert error_log_bus_obj.error_log_id > 0

    @pytest.mark.asyncio
    async def test_get_all_error_log(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_pac_pac_id = (
            new_pac.pac_id
        )

        await pac_bus_obj.load_from_id(
            new_pac_pac_id
        )

        error_log_bus_obj = await pac_bus_obj.build_error_log()

        await error_log_bus_obj.save()

        error_log_list = await pac_bus_obj.get_all_error_log()

        assert len(error_log_list) >= 1

        #assert error_log_list[0].error_log_id > 0

        #assert error_log_list[0].error_log_id == error_log_bus_obj.error_log_id


    @pytest.mark.asyncio
    async def test_build_date_greater_than_filter(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await pac_bus_obj.load_from_id(
            new_pac.pac_id
        )

        date_greater_than_filter_bus_obj = await pac_bus_obj.build_date_greater_than_filter()

        assert date_greater_than_filter_bus_obj.pac_id == pac_bus_obj.pac_id
        assert date_greater_than_filter_bus_obj.pac_code_peek == pac_bus_obj.code

        await date_greater_than_filter_bus_obj.save()

        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id > 0

    @pytest.mark.asyncio
    async def test_get_all_date_greater_than_filter(
        self,
        pac_bus_obj: PacBusObj,
        new_pac: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_pac_pac_id = (
            new_pac.pac_id
        )

        await pac_bus_obj.load_from_id(
            new_pac_pac_id
        )

        date_greater_than_filter_bus_obj = await pac_bus_obj.build_date_greater_than_filter()

        await date_greater_than_filter_bus_obj.save()

        date_greater_than_filter_list = await pac_bus_obj.get_all_date_greater_than_filter()

        assert len(date_greater_than_filter_list) >= 1

        #assert date_greater_than_filter_list[0].date_greater_than_filter_id > 0

        #assert date_greater_than_filter_list[0].date_greater_than_filter_id == date_greater_than_filter_bus_obj.date_greater_than_filter_id

