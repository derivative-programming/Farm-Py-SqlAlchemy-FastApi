# business/tests/dft_dependency_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
DFTDependencyFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.dft_dependency_fluent import (
    DFTDependencyFluentBusObj)
from helpers.session_context import SessionContext


class MockDFTDependencyBaseBusObj:
    """
    A mock base class for the
    DFTDependencyFluentBusObj class.
    """
    def __init__(self):
        self.dependency_df_task_id = None
        self.dyna_flow_task_id = None
        self.is_placeholder = None
class TestDFTDependencyFluentBusObj:
    """
    Unit tests for the
    DFTDependencyFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a DFTDependencyFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return DFTDependencyFluentBusObj(session_context)
    # dependencyDFTaskID

    def test_set_prop_dependency_df_task_id(self, new_fluent_bus_obj):
        """
        Test setting the dependency_df_task_id property.
        """
        result = new_fluent_bus_obj.set_prop_dependency_df_task_id(42)
        assert new_fluent_bus_obj.dependency_df_task_id == 42
        assert result is new_fluent_bus_obj
    # DynaFlowTaskID
    # isPlaceholder

    def test_set_prop_is_placeholder(self, new_fluent_bus_obj):
        """
        Test setting the is_placeholder property.
        """
        result = new_fluent_bus_obj.set_prop_is_placeholder(True)
        assert new_fluent_bus_obj.is_placeholder is True
        assert result is new_fluent_bus_obj
    # dependencyDFTaskID,
    # DynaFlowTaskID

    def test_set_prop_dyna_flow_task_id(self, new_fluent_bus_obj):
        """
        Test setting the dyna_flow_task_id property.
        """
        result = new_fluent_bus_obj.set_prop_dyna_flow_task_id(1)
        assert new_fluent_bus_obj.dyna_flow_task_id == 1
        assert result is new_fluent_bus_obj
    # isPlaceholder,
