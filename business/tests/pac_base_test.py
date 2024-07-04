# business/tests/pac_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
PacBusObj class.
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
from business.pac_base import (
    PacBaseBusObj)
from helpers.session_context import SessionContext
from managers.pac import (
    PacManager)
from models import Pac
from models.factory import (
    PacFactory)
from services.logging_config import get_logger

from ..pac import PacBusObj


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
def pac():
    """
    Fixture that returns a mock
    pac object.
    """
    return Mock(spec=Pac)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, pac
):
    """
    Fixture that returns a
    PacBaseBusObj instance.
    """
    mock_sess_base_bus_obj = PacBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.pac = \
        pac
    return mock_sess_base_bus_obj


class TestPacBaseBusObj:
    """
    Unit tests for the
    PacBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        PacManager class.
        """
        session_context = SessionContext(dict(), session)
        return PacManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        PacBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return PacBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the Pac class.
        """

        return await PacFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_pac(
        self,
        new_bus_obj: PacBusObj
    ):
        """
        Test case for creating a new pac.
        """
        # Test creating a new pac

        assert new_bus_obj.pac_id == 0

        assert isinstance(new_bus_obj.pac_id, int)
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

    @pytest.mark.asyncio
    async def test_load_with_pac_obj(
        self,
        obj_manager: PacManager,
        new_bus_obj: PacBusObj,
        new_obj: Pac
    ):
        """
        Test case for loading data from a
        pac object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.pac, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_pac_id(
        self,
        obj_manager: PacManager,
        new_bus_obj: PacBusObj,
        new_obj: Pac
    ):
        """
        Test case for loading data from a
        pac ID.
        """

        new_obj_pac_id = \
            new_obj.pac_id

        await new_bus_obj.load_from_id(
            new_obj_pac_id)

        assert obj_manager.is_equal(
            new_bus_obj.pac, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_pac_code(
        self,
        obj_manager: PacManager,
        new_bus_obj: PacBusObj,
        new_obj: Pac
    ):
        """
        Test case for loading data from a
        pac code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.pac, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_pac_json(
        self,
        obj_manager: PacManager,
        new_bus_obj: PacBusObj,
        new_obj: Pac
    ):
        """
        Test case for loading data from a
        pac JSON.
        """

        pac_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            pac_json)

        assert obj_manager.is_equal(
            new_bus_obj.pac, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_pac_dict(
        self,
        obj_manager: PacManager,
        new_bus_obj: PacBusObj,
        new_obj: Pac
    ):
        """
        Test case for loading data from a
        pac dictionary.
        """

        logger.info("test_load_with_pac_dict 1")

        pac_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(pac_dict)

        await new_bus_obj.load_from_dict(
            pac_dict)

        assert obj_manager.is_equal(
            new_bus_obj.pac,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_pac(
        self,
        new_bus_obj: PacBusObj
    ):
        """
        Test case for retrieving a nonexistent
        pac.
        """
        # Test retrieving a nonexistent
        # pac raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_pac(
        self,
        obj_manager: PacManager,
        new_bus_obj: PacBusObj,
        new_obj: Pac
    ):
        """
        Test case for updating a pac's data.
        """
        # Test updating a pac's data

        new_obj_pac_id_value = \
            new_obj.pac_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_pac_id_value)

        assert isinstance(new_obj,
                          Pac)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.pac,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_pac_id_value = \
            new_obj.pac_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_pac_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.pac,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_pac(
        self,
        obj_manager: PacManager,
        new_bus_obj: PacBusObj,
        new_obj: Pac
    ):
        """
        Test case for deleting a pac.
        """

        assert new_bus_obj.pac is not None

        assert new_bus_obj.pac_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.pac_id is not None

        await new_bus_obj.delete()

        new_obj_pac_id_value = \
            new_obj.pac_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_pac_id_value)

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
        pac
    ):
        """
        Test case for refreshing the pac data.
        """
        with patch(
            "business.pac_base"
            ".PacManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=pac)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .pac == pac
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(pac)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the pac data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.pac = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the pac
        data to a dictionary.
        """
        with patch(
            "business.pac_base"
            ".PacManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            pac_dict = mock_sess_base_bus_obj.to_dict()
            assert pac_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.pac)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the pac data to JSON.
        """
        with patch(
            "business.pac_base"
            ".PacManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            pac_json = mock_sess_base_bus_obj.to_json()
            assert pac_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.pac)

    def test_get_obj(
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for getting the pac object.
        """
        assert mock_sess_base_bus_obj.get_obj() == pac

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "pac"

    def test_get_id(
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for getting the pac ID.
        """
        pac.pac_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_pac_id(
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for the pac_id property.
        """
        pac.pac_id = 1
        assert mock_sess_base_bus_obj.pac_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        pac.code = test_uuid
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
            self, mock_sess_base_bus_obj, pac):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the PacBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (PacBaseBusiness):
                An instance of the
                PacBaseBusiness class.
            pac (Pac):
                An instance of the
                Pac class.

        Returns:
            None
        """
        pac.last_change_code = 123
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
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        pac.insert_user_id = test_uuid
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
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for the
        description property.
        """
        pac.description = \
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
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for the
        display_order property.
        """
        pac.display_order = 1
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
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for the
        is_active property.
        """
        pac.is_active = True
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
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for the
        lookup_enum_name property.
        """
        pac.lookup_enum_name = \
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
            self, mock_sess_base_bus_obj, pac):
        """
        Test case for the
        name property.
        """
        pac.name = \
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
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            pac):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        pac.insert_utc_date_time = test_datetime
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
            pac):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        pac.last_update_utc_date_time = test_datetime
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


    @pytest.mark.asyncio
    async def test_build_tri_state_filter(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_tri_state_filter()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.tri_state_filter_id > 0

    @pytest.mark.asyncio
    async def test_get_all_tri_state_filter(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_tri_state_filter()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_tri_state_filter()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].tri_state_filter_id > 0

        # Check if any item in the list has a matching
        # tri_state_filter_id
        assert any(
            child.tri_state_filter_id == (
                child_bus_obj.tri_state_filter_id)
            for child in child_bus_obj_list
        ), "No matching tri_state_filter_id found in the list"


    @pytest.mark.asyncio
    async def test_build_tac(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_tac()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.tac_id > 0

    @pytest.mark.asyncio
    async def test_get_all_tac(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_tac()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_tac()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].tac_id > 0

        # Check if any item in the list has a matching
        # tac_id
        assert any(
            child.tac_id == (
                child_bus_obj.tac_id)
            for child in child_bus_obj_list
        ), "No matching tac_id found in the list"


    @pytest.mark.asyncio
    async def test_build_role(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_role()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.role_id > 0

    @pytest.mark.asyncio
    async def test_get_all_role(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_role()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_role()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].role_id > 0

        # Check if any item in the list has a matching
        # role_id
        assert any(
            child.role_id == (
                child_bus_obj.role_id)
            for child in child_bus_obj_list
        ), "No matching role_id found in the list"


    @pytest.mark.asyncio
    async def test_build_land(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_land()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.land_id > 0

    @pytest.mark.asyncio
    async def test_get_all_land(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_land()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_land()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].land_id > 0

        # Check if any item in the list has a matching
        # land_id
        assert any(
            child.land_id == (
                child_bus_obj.land_id)
            for child in child_bus_obj_list
        ), "No matching land_id found in the list"


    @pytest.mark.asyncio
    async def test_build_flavor(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_flavor()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.flavor_id > 0

    @pytest.mark.asyncio
    async def test_get_all_flavor(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_flavor()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_flavor()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].flavor_id > 0

        # Check if any item in the list has a matching
        # flavor_id
        assert any(
            child.flavor_id == (
                child_bus_obj.flavor_id)
            for child in child_bus_obj_list
        ), "No matching flavor_id found in the list"


    @pytest.mark.asyncio
    async def test_build_error_log(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_error_log()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.error_log_id > 0

    @pytest.mark.asyncio
    async def test_get_all_error_log(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_error_log()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_error_log()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].error_log_id > 0

        # Check if any item in the list has a matching
        # error_log_id
        assert any(
            child.error_log_id == (
                child_bus_obj.error_log_id)
            for child in child_bus_obj_list
        ), "No matching error_log_id found in the list"


    @pytest.mark.asyncio
    async def test_build_dyna_flow_type_schedule(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow_type_schedule()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.dyna_flow_type_schedule_id > 0

    @pytest.mark.asyncio
    async def test_get_all_dyna_flow_type_schedule(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow_type_schedule()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_dyna_flow_type_schedule()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].dyna_flow_type_schedule_id > 0

        # Check if any item in the list has a matching
        # dyna_flow_type_schedule_id
        assert any(
            child.dyna_flow_type_schedule_id == (
                child_bus_obj.dyna_flow_type_schedule_id)
            for child in child_bus_obj_list
        ), "No matching dyna_flow_type_schedule_id found in the list"


    @pytest.mark.asyncio
    async def test_build_dyna_flow_type(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow_type()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.dyna_flow_type_id > 0

    @pytest.mark.asyncio
    async def test_get_all_dyna_flow_type(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow_type()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_dyna_flow_type()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].dyna_flow_type_id > 0

        # Check if any item in the list has a matching
        # dyna_flow_type_id
        assert any(
            child.dyna_flow_type_id == (
                child_bus_obj.dyna_flow_type_id)
            for child in child_bus_obj_list
        ), "No matching dyna_flow_type_id found in the list"


    @pytest.mark.asyncio
    async def test_build_dyna_flow_task_type(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow_task_type()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.dyna_flow_task_type_id > 0

    @pytest.mark.asyncio
    async def test_get_all_dyna_flow_task_type(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow_task_type()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_dyna_flow_task_type()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].dyna_flow_task_type_id > 0

        # Check if any item in the list has a matching
        # dyna_flow_task_type_id
        assert any(
            child.dyna_flow_task_type_id == (
                child_bus_obj.dyna_flow_task_type_id)
            for child in child_bus_obj_list
        ), "No matching dyna_flow_task_type_id found in the list"


    @pytest.mark.asyncio
    async def test_build_dyna_flow(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.dyna_flow_id > 0

    @pytest.mark.asyncio
    async def test_get_all_dyna_flow(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_dyna_flow()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_dyna_flow()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].dyna_flow_id > 0

        # Check if any item in the list has a matching
        # dyna_flow_id
        assert any(
            child.dyna_flow_id == (
                child_bus_obj.dyna_flow_id)
            for child in child_bus_obj_list
        ), "No matching dyna_flow_id found in the list"


    @pytest.mark.asyncio
    async def test_build_df_maintenance(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_df_maintenance()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.df_maintenance_id > 0

    @pytest.mark.asyncio
    async def test_get_all_df_maintenance(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_df_maintenance()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_df_maintenance()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].df_maintenance_id > 0

        # Check if any item in the list has a matching
        # df_maintenance_id
        assert any(
            child.df_maintenance_id == (
                child_bus_obj.df_maintenance_id)
            for child in child_bus_obj_list
        ), "No matching df_maintenance_id found in the list"


    @pytest.mark.asyncio
    async def test_build_date_greater_than_filter(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        await new_bus_obj.load_from_id(
            new_obj.pac_id
        )

        child_bus_obj = await new_bus_obj.build_date_greater_than_filter()

        assert child_bus_obj.pac_id == new_bus_obj.pac_id
        assert child_bus_obj.pac_code_peek == new_bus_obj.code

        await child_bus_obj.save()

        assert child_bus_obj.date_greater_than_filter_id > 0

    @pytest.mark.asyncio
    async def test_get_all_date_greater_than_filter(
        self,
        new_bus_obj: PacBusObj,
        new_obj: Pac,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """

        session_context = SessionContext(dict(), session)

        await current_runtime.initialize(session_context)

        new_obj_pac_id = (
            new_obj.pac_id
        )

        await new_bus_obj.load_from_id(
            new_obj_pac_id
        )

        child_bus_obj = await new_bus_obj.build_date_greater_than_filter()

        await child_bus_obj.save()

        child_bus_obj_list = await new_bus_obj.get_all_date_greater_than_filter()

        assert len(child_bus_obj_list) >= 1

        assert child_bus_obj_list[0].date_greater_than_filter_id > 0

        # Check if any item in the list has a matching
        # date_greater_than_filter_id
        assert any(
            child.date_greater_than_filter_id == (
                child_bus_obj.date_greater_than_filter_id)
            for child in child_bus_obj_list
        ), "No matching date_greater_than_filter_id found in the list"
