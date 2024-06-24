# business/tests/organization_fluent_test.py
"""
Unit tests for the OrganizationFluentBusObj class.
"""
import math
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4
import pytest
from business.organization_fluent import OrganizationFluentBusObj
from helpers.session_context import SessionContext
class MockOrganizationBaseBusObj:
    """
    A mock base class for the OrganizationFluentBusObj class.
    """
    def __init__(self):
        self.name = None
        self.tac_id = None
class TestOrganizationFluentBusObj:
    """
    Unit tests for the OrganizationFluentBusObj class.
    """
    @pytest.fixture
    def organization(self, session):
        """
        Return a OrganizationFluentBusObj object.
        """
        session_context = SessionContext(dict(), session=session)
        return OrganizationFluentBusObj(session_context)
    def test_set_prop_name(self, organization):
        """
        Test setting the name property.
        """
        result = organization.set_prop_name("Vanilla")
        assert organization.name == "Vanilla"
        assert result is organization
    def test_set_prop_tac_id(self, organization):
        """
        Test setting the tac_id property.
        """
        result = organization.set_prop_tac_id(1)
        assert organization.tac_id == 1
        assert result is organization
