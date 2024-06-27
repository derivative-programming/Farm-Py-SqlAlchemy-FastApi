# business/tests/org_api_key_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
"""
Unit tests for the
OrgApiKeyBusObj class.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio

import models
from models.factory import (
    OrgApiKeyFactory)
from business.org_api_key import (
    OrgApiKeyBusObj)
from helpers.session_context import SessionContext
from models import (
    OrgApiKey)


@pytest.fixture
def session_context():
    """
    Return a mock SessionContext object.
    """
    return Mock(spec=SessionContext)


@pytest.fixture
def org_api_key():
    """
    Fixture that returns a mock
    org_api_key object.
    """
    return Mock(spec=OrgApiKey)


@pytest.fixture
def obj_list():
    """
    Return a list of mock OrgApiKey objects.
    """
    org_api_keys = []
    for _ in range(3):
        org_api_key = Mock(spec=OrgApiKey)
        org_api_keys.append(org_api_key)
    return org_api_keys


@pytest_asyncio.fixture(scope="function")
async def new_obj(session):
    """
    Fixture that returns a new instance of
    the OrgApiKey class.
    """

    return await OrgApiKeyFactory.create_async(
        session)


@pytest_asyncio.fixture(scope="function")
async def new_bus_obj(session, new_obj) -> OrgApiKeyBusObj:
    """
    Fixture that returns a new instance of
    the OrgApiKey class.
    """

    session_context = SessionContext(dict(), session)
    org_api_key_bus_obj = OrgApiKeyBusObj(session_context, new_obj)

    return org_api_key_bus_obj


class TestOrgApiKeyBusObj:
    """
    Unit tests for the
    OrgApiKeyBusObj class.
    """

    @pytest.mark.asyncio
    async def test_to_bus_obj_list(
            self, session_context, obj_list):
        """
        Test the to_bus_obj_list method.
        """
        with patch(
                "business.org_api_key"
                ".OrgApiKeyBusObj"
                ".load_from_obj_instance",
                new_callable=AsyncMock) as mock_load:
            bus_obj_list = await \
                OrgApiKeyBusObj.to_bus_obj_list(
                    session_context, obj_list)

            assert len(bus_obj_list) == len(obj_list)
            assert all(
                isinstance(bus_obj, OrgApiKeyBusObj)
                for bus_obj in bus_obj_list)
            assert all(
                bus_obj.load_from_obj_instance.called
                for bus_obj in bus_obj_list)

            for bus_obj, org_api_key in zip(bus_obj_list, obj_list):
                mock_load.assert_any_call(org_api_key)

    @pytest.mark.asyncio
    async def test_to_bus_obj_list_empty(
            self, session_context):
        """
        Test the to_bus_obj_list
        method with an empty list.
        """
        empty_obj_list = []
        bus_obj_list = await \
            OrgApiKeyBusObj.to_bus_obj_list(
                session_context,
                empty_obj_list)

        assert len(bus_obj_list) == 0
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID

    @pytest.mark.asyncio
    async def test_get_organization_id_obj(
        self, new_bus_obj: OrgApiKeyBusObj
    ):
        """
        Test the get_organization_id_obj method.
        """

        # Call the get_organization_id_bus_obj method
        fk_obj: models.Organization = await \
            new_bus_obj.get_organization_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.Organization)

        assert fk_obj.organization_id == \
            new_bus_obj.organization_id

        assert fk_obj.code == \
            new_bus_obj.organization_code_peek

    @pytest.mark.asyncio
    async def test_get_organization_id_bus_obj(
        self, new_bus_obj: OrgApiKeyBusObj
    ):
        """
        Test the get_organization_id_bus_obj method.
        """
        from ..organization import (  # OrganizationID
            OrganizationBusObj)
        # Call the get_organization_id_bus_obj method
        fk_bus_obj: OrganizationBusObj = await \
            new_bus_obj.get_organization_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, OrganizationBusObj)

        assert fk_bus_obj.organization_id == \
            new_bus_obj.organization_id

        assert fk_bus_obj.code == \
            new_bus_obj.organization_code_peek
    # OrgCustomerID

    @pytest.mark.asyncio
    async def test_get_org_customer_id_obj(
        self, new_bus_obj: OrgApiKeyBusObj
    ):
        """
        Test the get_org_customer_id_obj method.
        """

        # Call the get_org_customer_id_obj method
        fk_obj: models.OrgCustomer = \
            await new_bus_obj.get_org_customer_id_obj()

        assert fk_obj is not None

        assert isinstance(fk_obj, models.OrgCustomer)

        assert fk_obj.org_customer_id == \
            new_bus_obj.org_customer_id

        assert fk_obj.code == \
            new_bus_obj.org_customer_code_peek

    @pytest.mark.asyncio
    async def test_get_org_customer_id_bus_obj(
        self, new_bus_obj: OrgApiKeyBusObj
    ):
        """
        Test the get_org_customer_id_bus_obj
        method.
        """

        from ..org_customer import (  # OrgCustomerID
            OrgCustomerBusObj)
        # Call the get_org_customer_id_bus_obj method
        fk_bus_obj: OrgCustomerBusObj = \
            await new_bus_obj.get_org_customer_id_bus_obj()

        assert fk_bus_obj is not None

        assert isinstance(fk_bus_obj, OrgCustomerBusObj)

        assert fk_bus_obj.org_customer_id == \
            new_bus_obj.org_customer_id

        assert fk_bus_obj.code == \
            new_bus_obj.org_customer_code_peek
