# business/tests/organization_base_test.py
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
"""
This module contains unit tests for the OrganizationBusObj class.
"""
import uuid
from datetime import date, datetime  # noqa: F401
from decimal import Decimal
from unittest.mock import AsyncMock, Mock, patch
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import current_runtime  # noqa: F401
from business.organization_base import OrganizationBaseBusObj
from helpers.session_context import SessionContext
from managers.organization import OrganizationManager
from models import Organization
from models.factory import OrganizationFactory
from services.logging_config import get_logger
from ..organization import OrganizationBusObj

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
def organization():
    """
    Fixture that returns a mock organization object.
    """
    return Mock(spec=Organization)
@pytest.fixture
def organization_base_bus_obj(fake_session_context, organization):
    """
    Fixture that returns a OrganizationBaseBusObj instance.
    """
    organization_base = OrganizationBaseBusObj(fake_session_context)
    organization_base.organization = organization
    return organization_base
class TestOrganizationBaseBusObj:
    """
    Unit tests for the OrganizationBusObj class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def organization_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the OrganizationManager class.
        """
        session_context = SessionContext(dict(), session)
        return OrganizationManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def organization_bus_obj(self, session):
        """
        Fixture that returns an instance of the OrganizationBusObj class.
        """
        session_context = SessionContext(dict(), session)
        return OrganizationBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_organization(self, session):
        """
        Fixture that returns a new instance of
        the Organization class.
        """
        return await OrganizationFactory.create_async(
            session)
    @pytest.mark.asyncio
    async def test_create_organization(
        self,
        organization_bus_obj: OrganizationBusObj
    ):
        """
        Test case for creating a new organization.
        """
        # Test creating a new organization
        assert organization_bus_obj.organization_id == 0
        # assert isinstance(organization_bus_obj.organization_id, int)
        assert isinstance(
            organization_bus_obj.code, uuid.UUID)
        assert isinstance(
            organization_bus_obj.last_change_code, int)
        assert organization_bus_obj.insert_user_id == uuid.UUID(int=0)
        assert organization_bus_obj.last_update_user_id == uuid.UUID(int=0)
# endset
        assert isinstance(organization_bus_obj.name, str)
        assert isinstance(organization_bus_obj.tac_id, int)
# endset
    @pytest.mark.asyncio
    async def test_load_with_organization_obj(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
        Test case for loading data from a
        organization object instance.
        """
        await organization_bus_obj.load_from_obj_instance(
            new_organization)
        assert organization_manager.is_equal(
            organization_bus_obj.organization, new_organization) is True
    @pytest.mark.asyncio
    async def test_load_with_organization_id(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
        Test case for loading data from a
        organization ID.
        """
        new_organization_organization_id = new_organization.organization_id
        await organization_bus_obj.load_from_id(
            new_organization_organization_id)
        assert organization_manager.is_equal(
            organization_bus_obj.organization, new_organization) is True
    @pytest.mark.asyncio
    async def test_load_with_organization_code(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
        Test case for loading data from a
        organization code.
        """
        await organization_bus_obj.load_from_code(
            new_organization.code)
        assert organization_manager.is_equal(
            organization_bus_obj.organization, new_organization) is True
    @pytest.mark.asyncio
    async def test_load_with_organization_json(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
        Test case for loading data from a
        organization JSON.
        """
        organization_json = organization_manager.to_json(new_organization)
        await organization_bus_obj.load_from_json(
            organization_json)
        assert organization_manager.is_equal(
            organization_bus_obj.organization, new_organization) is True
    @pytest.mark.asyncio
    async def test_load_with_organization_dict(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
        Test case for loading data from a
        organization dictionary.
        """
        logger.info("test_load_with_organization_dict 1")
        organization_dict = organization_manager.to_dict(new_organization)
        logger.info(organization_dict)
        await organization_bus_obj.load_from_dict(
            organization_dict)
        assert organization_manager.is_equal(
            organization_bus_obj.organization,
            new_organization) is True
    @pytest.mark.asyncio
    async def test_get_nonexistent_organization(
        self,
        organization_bus_obj: OrganizationBusObj
    ):
        """
        Test case for retrieving a nonexistent organization.
        """
        # Test retrieving a nonexistent
        # organization raises an exception
        await organization_bus_obj.load_from_id(-1)
        # Assuming -1 is an id that wouldn't exist
        assert organization_bus_obj.is_valid() is False
    @pytest.mark.asyncio
    async def test_update_organization(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
        Test case for updating a organization's data.
        """
        # Test updating a organization's data
        new_organization_organization_id_value = new_organization.organization_id
        new_organization = await organization_manager.get_by_id(
            new_organization_organization_id_value)
        assert isinstance(new_organization, Organization)
        new_code = uuid.uuid4()
        await organization_bus_obj.load_from_obj_instance(
            new_organization)
        organization_bus_obj.code = new_code
        await organization_bus_obj.save()
        new_organization_organization_id_value = new_organization.organization_id
        new_organization = await organization_manager.get_by_id(
            new_organization_organization_id_value)
        assert organization_manager.is_equal(
            organization_bus_obj.organization,
            new_organization) is True
    @pytest.mark.asyncio
    async def test_delete_organization(
        self,
        organization_manager: OrganizationManager,
        organization_bus_obj: OrganizationBusObj,
        new_organization: Organization
    ):
        """
        Test case for deleting a organization.
        """
        assert new_organization.organization_id is not None
        assert organization_bus_obj.organization_id == 0
        new_organization_organization_id_value = new_organization.organization_id
        await organization_bus_obj.load_from_id(
            new_organization_organization_id_value)
        assert organization_bus_obj.organization_id is not None
        await organization_bus_obj.delete()
        new_organization_organization_id_value = new_organization.organization_id
        new_organization = await organization_manager.get_by_id(
            new_organization_organization_id_value)
        assert new_organization is None
    def test_get_session_context(
        self,
        organization_base_bus_obj,
        fake_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert organization_base_bus_obj.get_session_context() == fake_session_context
    @pytest.mark.asyncio
    async def test_refresh(self, organization_base_bus_obj, organization):
        """
        Test case for refreshing the organization data.
        """
        with patch(
            'business.organization_base.OrganizationManager',
            autospec=True
        ) as mock_organization_manager:
            mock_organization_manager_instance = mock_organization_manager.return_value
            mock_organization_manager_instance.refresh = AsyncMock(return_value=organization)
            refreshed_organization_base = await organization_base_bus_obj.refresh()
            assert refreshed_organization_base.organization == organization
            mock_organization_manager_instance.refresh.assert_called_once_with(organization)
    def test_is_valid(self, organization_base_bus_obj):
        """
        Test case for checking if the organization data is valid.
        """
        assert organization_base_bus_obj.is_valid() is True
        organization_base_bus_obj.organization = None
        assert organization_base_bus_obj.is_valid() is False
    def test_to_dict(self, organization_base_bus_obj):
        """
        Test case for converting the organization data to a dictionary.
        """
        with patch(
            'business.organization_base.OrganizationManager',
            autospec=True
        ) as mock_organization_manager:
            mock_organization_manager_instance = mock_organization_manager.return_value
            mock_organization_manager_instance.to_dict = Mock(
                return_value={"key": "value"})
            organization_dict = organization_base_bus_obj.to_dict()
            assert organization_dict == {"key": "value"}
            mock_organization_manager_instance.to_dict.assert_called_once_with(
                organization_base_bus_obj.organization)
    def test_to_json(self, organization_base_bus_obj):
        """
        Test case for converting the organization data to JSON.
        """
        with patch(
            'business.organization_base.OrganizationManager',
            autospec=True
        ) as mock_organization_manager:
            mock_organization_manager_instance = mock_organization_manager.return_value
            mock_organization_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')
            organization_json = organization_base_bus_obj.to_json()
            assert organization_json == '{"key": "value"}'
            mock_organization_manager_instance.to_json.assert_called_once_with(
                organization_base_bus_obj.organization)
    def test_get_obj(self, organization_base_bus_obj, organization):
        """
        Test case for getting the organization object.
        """
        assert organization_base_bus_obj.get_obj() == organization
    def test_get_object_name(self, organization_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert organization_base_bus_obj.get_object_name() == "organization"
    def test_get_id(self, organization_base_bus_obj, organization):
        """
        Test case for getting the organization ID.
        """
        organization.organization_id = 1
        assert organization_base_bus_obj.get_id() == 1
    def test_organization_id(self, organization_base_bus_obj, organization):
        """
        Test case for the organization_id property.
        """
        organization.organization_id = 1
        assert organization_base_bus_obj.organization_id == 1
    def test_code(self, organization_base_bus_obj, organization):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        organization.code = test_uuid
        assert organization_base_bus_obj.code == test_uuid
    def test_code_setter(self, organization_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        organization_base_bus_obj.code = test_uuid
        assert organization_base_bus_obj.code == test_uuid
    def test_code_invalid_value(self, organization_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            organization_base_bus_obj.code = "not-a-uuid"
    def test_last_change_code(self, organization_base_bus_obj, organization):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the OrganizationBaseBusiness class.
        Args:
            organization_base_bus_obj (OrganizationBaseBusiness):
                An instance of the
                OrganizationBaseBusiness class.
            organization (Organization): An instance of the Organization class.
        Returns:
            None
        """
        organization.last_change_code = 123
        assert organization_base_bus_obj.last_change_code == 123
    def test_last_change_code_setter(self, organization_base_bus_obj):
        """
        Test case for the last_change_code setter.
        """
        organization_base_bus_obj.last_change_code = 123
        assert organization_base_bus_obj.last_change_code == 123
    def test_last_change_code_invalid_value(self, organization_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            organization_base_bus_obj.last_change_code = "not-an-int"
    def test_insert_user_id(self, organization_base_bus_obj, organization):
        """
        Test case for the insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        organization.insert_user_id = test_uuid
        assert organization_base_bus_obj.insert_user_id == test_uuid
    def test_insert_user_id_setter(self, organization_base_bus_obj):
        """
        Test case for the insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        organization_base_bus_obj.insert_user_id = test_uuid
        assert organization_base_bus_obj.insert_user_id == test_uuid
    def test_insert_user_id_invalid_value(self, organization_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            organization_base_bus_obj.insert_user_id = "not-a-uuid"
# endset
    # name,
    def test_name(self, organization_base_bus_obj, organization):
        """
        Test case for the name property.
        """
        organization.name = "Vanilla"
        assert organization_base_bus_obj.name == "Vanilla"
    def test_name_setter(self, organization_base_bus_obj):
        """
        Test case for the name setter.
        """
        organization_base_bus_obj.name = "Vanilla"
        assert organization_base_bus_obj.name == "Vanilla"
    def test_name_invalid_value(self, organization_base_bus_obj):
        """
        Test case for setting an invalid value for the
        name property.
        """
        with pytest.raises(AssertionError):
            organization_base_bus_obj.name = 123
    # TacID
# endset
    # name,
    # TacID
    def test_tac_id(self, organization_base_bus_obj, organization):
        """
        Test case for the tac_id property.
        """
        organization.tac_id = 1
        assert organization_base_bus_obj.tac_id == 1
    def test_tac_id_setter(self, organization_base_bus_obj):
        """
        Test case for the tac_id setter.
        """
        organization_base_bus_obj.tac_id = 1
        assert organization_base_bus_obj.tac_id == 1
    def test_tac_id_invalid_value(self, organization_base_bus_obj):
        """
        Test case for setting an invalid value for the
        tac_id property.
        """
        with pytest.raises(AssertionError):
            organization_base_bus_obj.tac_id = "not-an-int"
# endset
    def test_insert_utc_date_time(self, organization_base_bus_obj, organization):
        """
        Test case for the insert_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        organization.insert_utc_date_time = test_datetime
        assert organization_base_bus_obj.insert_utc_date_time == test_datetime
    def test_insert_utc_date_time_setter(self, organization_base_bus_obj):
        """
        Test case for the insert_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        organization_base_bus_obj.insert_utc_date_time = test_datetime
        assert organization_base_bus_obj.insert_utc_date_time == test_datetime
    def test_insert_utc_date_time_invalid_value(self, organization_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            organization_base_bus_obj.insert_utc_date_time = "not-a-datetime"
    def test_last_update_utc_date_time(self, organization_base_bus_obj, organization):
        """
        Test case for the last_update_utc_date_time property.
        """
        test_datetime = datetime.utcnow()
        organization.last_update_utc_date_time = test_datetime
        assert organization_base_bus_obj.last_update_utc_date_time == test_datetime
    def test_last_update_utc_date_time_setter(self, organization_base_bus_obj):
        """
        Test case for the last_update_utc_date_time setter.
        """
        test_datetime = datetime.utcnow()
        organization_base_bus_obj.last_update_utc_date_time = test_datetime
        assert organization_base_bus_obj.last_update_utc_date_time == test_datetime
    def test_last_update_utc_date_time_invalid_value(self, organization_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            organization_base_bus_obj.last_update_utc_date_time = "not-a-datetime"

