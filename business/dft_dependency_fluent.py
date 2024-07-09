# business/dft_dependency_fluent.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the
DFTDependencyFluentBusObj class,
which adds fluent properties
to the business object for a
DFTDependency.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .dft_dependency_base import DFTDependencyBaseBusObj


class DFTDependencyFluentBusObj(DFTDependencyBaseBusObj):
    """
    This class add fluent properties to the
    Base DFTDependency Business Object
    """

    # dependencyDFTaskID

    def set_prop_dependency_df_task_id(self, value: int):
        """
        Set the value of
        dependency_df_task_id property.

        Args:
            value (int): The value to set for
                dependency_df_task_id.

        Returns:
            self: Returns the instance of the class.

        """
        self.dependency_df_task_id = value
        return self
    # DynaFlowTaskID
    # isPlaceholder

    def set_prop_is_placeholder(self, value: bool):
        """
        Set the Is Placeholder flag for the
        DFTDependency object.

        :param value: The Is Placeholder flag value.
        :return: The updated
            DFTDependencyBusObj instance.
        """

        self.is_placeholder = value
        return self
    # dependencyDFTaskID
    # DynaFlowTaskID

    def set_prop_dyna_flow_task_id(self, value: int):
        """
        Set the dyna_flow_task ID for the
        dft_dependency.

        Args:
            value (int): The dyna_flow_task id value.

        Returns:
            DFTDependency: The updated
                DFTDependency object.
        """

        self.dyna_flow_task_id = value
        return self
    # isPlaceholder
