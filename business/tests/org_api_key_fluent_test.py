# business/tests/org_api_key_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
OrgApiKeyFluentBusObj class.
"""
import math
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
    def org_api_key(self, session):
        """
        Return a OrgApiKeyFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return OrgApiKeyFluentBusObj(session_context)
    def test_set_prop_api_key_value(self, org_api_key):
        """
        Test setting the api_key_value property.
        """
        result = org_api_key.set_prop_api_key_value("Vanilla")
        assert org_api_key.api_key_value == "Vanilla"
        assert result is org_api_key
    def test_set_prop_created_by(self, org_api_key):
        """
        Test setting the created_by property.
        """
        result = org_api_key.set_prop_created_by("Vanilla")
        assert org_api_key.created_by == "Vanilla"
        assert result is org_api_key
    def test_set_prop_created_utc_date_time(self, org_api_key):
        """
        Test setting the created_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = org_api_key.set_prop_created_utc_date_time(test_datetime)
        assert org_api_key.created_utc_date_time == test_datetime
        assert result is org_api_key
    def test_set_prop_expiration_utc_date_time(self, org_api_key):
        """
        Test setting the expiration_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = org_api_key.set_prop_expiration_utc_date_time(test_datetime)
        assert org_api_key.expiration_utc_date_time == test_datetime
        assert result is org_api_key
    def test_set_prop_is_active(self, org_api_key):
        """
        Test setting the is_active property.
        """
        result = org_api_key.set_prop_is_active(True)
        assert org_api_key.is_active is True
        assert result is org_api_key
    def test_set_prop_is_temp_user_key(self, org_api_key):
        """
        Test setting the is_temp_user_key property.
        """
        result = org_api_key.set_prop_is_temp_user_key(True)
        assert org_api_key.is_temp_user_key is True
        assert result is org_api_key
    def test_set_prop_name(self, org_api_key):
        """
        Test setting the name property.
        """
        result = org_api_key.set_prop_name("Vanilla")
        assert org_api_key.name == "Vanilla"
        assert result is org_api_key
    def test_set_prop_organization_id(self, org_api_key):
        """
        Test setting the organization_id property.
        """
        result = org_api_key.set_prop_organization_id(1)
        assert org_api_key.organization_id == 1
        assert result is org_api_key
    def test_set_prop_org_customer_id(self, org_api_key):
        """
        Test setting the org_customer_id property.
        """
        result = org_api_key.set_prop_org_customer_id(1)
        assert org_api_key.org_customer_id == 1
        assert result is org_api_key

