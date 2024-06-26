# business/tests/organization_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name

"""
This module contains unit tests for the
OrganizationBusObj class.
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
from business.organization_base import (
    OrganizationBaseBusObj)
from helpers.session_context import SessionContext
from managers.organization import (
    OrganizationManager)
from models import Organization
from models.factory import (
    OrganizationFactory)
from services.logging_config import get_logger

from ..organization import OrganizationBusObj


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
def organization():
    """
    Fixture that returns a mock
    organization object.
    """
    return Mock(spec=Organization)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, organization
):
    """
    Fixture that returns a
    OrganizationBaseBusObj instance.
    """
    mock_sess_base_bus_obj = OrganizationBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.organization = \
        organization
    return mock_sess_base_bus_obj


class TestOrganizationBaseBusObj:
    """
    Unit tests for the
    OrganizationBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        OrganizationManager class.
        """
        session_context = SessionContext(dict(), session)
        return OrganizationManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        OrganizationBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return OrganizationBusObj(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the Organization class.
        """

        return await OrganizationFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_organization(
        self,
        new_bus_obj: OrganizationBusObj
    ):
        """
        Test case for creating a new organization.
        """
        # Test creating a new organization

        assert new_bus_obj.organization_id == 0

        # assert isinstance(new_bus_obj.organization_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

        assert isinstance(new_bus_obj.name,
                          str)
        assert isinstance(new_bus_obj.tac_id,
                          int)

    @pytest.mark.asyncio
    async def test_load_with_organization_obj(
        self,
        obj_manager: OrganizationManager,
        new_bus_obj: OrganizationBusObj,
        new_obj: Organization
    ):
        """
        Test case for loading data from a
        organization object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.organization, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_organization_id(
        self,
        obj_manager: OrganizationManager,
        new_bus_obj: OrganizationBusObj,
        new_obj: Organization
    ):
        """
        Test case for loading data from a
        organization ID.
        """

        new_obj_organization_id = \
            new_obj.organization_id

        await new_bus_obj.load_from_id(
            new_obj_organization_id)

        assert obj_manager.is_equal(
            new_bus_obj.organization, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_organization_code(
        self,
        obj_manager: OrganizationManager,
        new_bus_obj: OrganizationBusObj,
        new_obj: Organization
    ):
        """
        Test case for loading data from a
        organization code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.organization, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_organization_json(
        self,
        obj_manager: OrganizationManager,
        new_bus_obj: OrganizationBusObj,
        new_obj: Organization
    ):
        """
        Test case for loading data from a
        organization JSON.
        """

        organization_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            organization_json)

        assert obj_manager.is_equal(
            new_bus_obj.organization, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_organization_dict(
        self,
        obj_manager: OrganizationManager,
        new_bus_obj: OrganizationBusObj,
        new_obj: Organization
    ):
        """
        Test case for loading data from a
        organization dictionary.
        """

        logger.info("test_load_with_organization_dict 1")

        organization_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(organization_dict)

        await new_bus_obj.load_from_dict(
            organization_dict)

        assert obj_manager.is_equal(
            new_bus_obj.organization,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_organization(
        self,
        new_bus_obj: OrganizationBusObj
    ):
        """
        Test case for retrieving a nonexistent
        organization.
        """
        # Test retrieving a nonexistent
        # organization raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_organization(
        self,
        obj_manager: OrganizationManager,
        new_bus_obj: OrganizationBusObj,
        new_obj: Organization
    ):
        """
        Test case for updating a organization's data.
        """
        # Test updating a organization's data

        new_obj_organization_id_value = \
            new_obj.organization_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_organization_id_value)

        assert isinstance(new_obj,
                          Organization)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.organization,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_organization_id_value = \
            new_obj.organization_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_organization_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.organization,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_organization(
        self,
        obj_manager: OrganizationManager,
        new_bus_obj: OrganizationBusObj,
        new_obj: Organization
    ):
        """
        Test case for deleting a organization.
        """

        assert new_bus_obj.organization is not None

        assert new_bus_obj.organization_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.organization_id is not None

        await new_bus_obj.delete()

        new_obj_organization_id_value = \
            new_obj.organization_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_organization_id_value)

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
        organization
    ):
        """
        Test case for refreshing the organization data.
        """
        with patch(
            "business.organization_base"
            ".OrganizationManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=organization)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .organization == organization
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(organization)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the organization data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.organization = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the organization
        data to a dictionary.
        """
        with patch(
            "business.organization_base"
            ".OrganizationManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            organization_dict = mock_sess_base_bus_obj.to_dict()
            assert organization_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.organization)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the organization data to JSON.
        """
        with patch(
            "business.organization_base"
            ".OrganizationManager",
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            organization_json = mock_sess_base_bus_obj.to_json()
            assert organization_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.organization)

    def test_get_obj(
            self, mock_sess_base_bus_obj, organization):
        """
        Test case for getting the organization object.
        """
        assert mock_sess_base_bus_obj.get_obj() == organization

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "organization"

    def test_get_id(
            self, mock_sess_base_bus_obj, organization):
        """
        Test case for getting the organization ID.
        """
        organization.organization_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_organization_id(
            self, mock_sess_base_bus_obj, organization):
        """
        Test case for the organization_id property.
        """
        organization.organization_id = 1
        assert mock_sess_base_bus_obj.organization_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, organization):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        organization.code = test_uuid
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
            self, mock_sess_base_bus_obj, organization):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the OrganizationBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (OrganizationBaseBusiness):
                An instance of the
                OrganizationBaseBusiness class.
            organization (Organization):
                An instance of the
                Organization class.

        Returns:
            None
        """
        organization.last_change_code = 123
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
            self, mock_sess_base_bus_obj, organization):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        organization.insert_user_id = test_uuid
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
    # name

    def test_name(
            self, mock_sess_base_bus_obj, organization):
        """
        Test case for the
        name property.
        """
        organization.name = \
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
    # TacID
    # name,
    # TacID

    def test_tac_id(
            self, mock_sess_base_bus_obj, organization):
        """
        Test case for the tac_id property.
        """
        organization.tac_id = 1
        assert mock_sess_base_bus_obj \
            .tac_id == 1

    def test_tac_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the tac_id setter.
        """
        mock_sess_base_bus_obj.tac_id = 1
        assert mock_sess_base_bus_obj \
            .tac_id == 1

    def test_tac_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        tac_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.tac_id = \
                "not-an-int"

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            organization):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        organization.insert_utc_date_time = test_datetime
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
            organization):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        organization.last_update_utc_date_time = test_datetime
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
