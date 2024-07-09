# business/tests/organization_fluent_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=too-few-public-methods
"""
Unit tests for the
OrganizationFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest
from business.organization_fluent import \
    OrganizationFluentBusObj
from helpers.session_context import SessionContext


class MockOrganizationBaseBusObj:
    """
    A mock base class for the
    OrganizationFluentBusObj class.
    """
    def __init__(self):
        self.name = None
        self.tac_id = None
class TestOrganizationFluentBusObj:
    """
    Unit tests for the
    OrganizationFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a OrganizationFluentBusObj
        object.
        """
        session_context = SessionContext({}, session=session)
        return OrganizationFluentBusObj(
            session_context)
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
    # TacID
    # name
    # TacID

    def test_set_prop_tac_id(self, new_fluent_bus_obj):
        """
        Test setting the tac_id property.
        """
        result = new_fluent_bus_obj.set_prop_tac_id(1)
        assert new_fluent_bus_obj.tac_id == 1
        assert result is new_fluent_bus_obj
