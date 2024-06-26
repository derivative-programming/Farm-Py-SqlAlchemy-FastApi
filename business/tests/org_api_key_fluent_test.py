# business/tests/org_api_key_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
OrgApiKeyFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.org_api_key_fluent import (
    OrgApiKeyFluentBusObj)
from helpers.session_context import SessionContext


class MockOrgApiKeyBaseBusObj:
    """
    A mock base class for the
    OrgApiKeyFluentBusObj class.
    """
    def __init__(self):
        self.api_key_value = None
        self.created_by = None
        self.created_utc_date_time = None
        self.expiration_utc_date_time = None
        self.is_active = None
        self.is_temp_user_key = None
        self.name = None
        self.organization_id = None
        self.org_customer_id = None
class TestOrgApiKeyFluentBusObj:
    """
    Unit tests for the
    OrgApiKeyFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a OrgApiKeyFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return OrgApiKeyFluentBusObj(session_context)
    # apiKeyValue

    def test_set_prop_api_key_value(self, new_fluent_bus_obj):
        """
        Test setting the api_key_value property.
        """
        result = new_fluent_bus_obj.set_prop_api_key_value(
            "Vanilla")
        assert new_fluent_bus_obj.api_key_value == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # createdBy

    def test_set_prop_created_by(self, new_fluent_bus_obj):
        """
        Test setting the created_by property.
        """
        result = new_fluent_bus_obj.set_prop_created_by(
            "Vanilla")
        assert new_fluent_bus_obj.created_by == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # createdUTCDateTime

    def test_set_prop_created_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the created_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_created_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.created_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # expirationUTCDateTime

    def test_set_prop_expiration_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the expiration_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_expiration_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.expiration_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # isActive

    def test_set_prop_is_active(self, new_fluent_bus_obj):
        """
        Test setting the is_active property.
        """
        result = new_fluent_bus_obj.set_prop_is_active(True)
        assert new_fluent_bus_obj.is_active is True
        assert result is new_fluent_bus_obj
    # isTempUserKey

    def test_set_prop_is_temp_user_key(self, new_fluent_bus_obj):
        """
        Test setting the is_temp_user_key property.
        """
        result = new_fluent_bus_obj.set_prop_is_temp_user_key(True)
        assert new_fluent_bus_obj.is_temp_user_key is True
        assert result is new_fluent_bus_obj
    # name

    def test_set_prop_name(self, new_fluent_bus_obj):
        """
        Test setting the name property.
        """
        result = new_fluent_bus_obj.set_prop_name(
            "Vanilla")
        assert new_fluent_bus_obj.name == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # OrganizationID
    # OrgCustomerID
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID

    def test_set_prop_organization_id(self, new_fluent_bus_obj):
        """
        Test setting the organization_id property.
        """
        result = new_fluent_bus_obj.set_prop_organization_id(1)
        assert new_fluent_bus_obj.organization_id == 1
        assert result is new_fluent_bus_obj
    # OrgCustomerID

    def test_set_prop_org_customer_id(self, new_fluent_bus_obj):
        """
        Test setting the org_customer_id property.
        """
        result = new_fluent_bus_obj.set_prop_org_customer_id(1)
        assert new_fluent_bus_obj.org_customer_id == 1
        assert result is new_fluent_bus_obj
