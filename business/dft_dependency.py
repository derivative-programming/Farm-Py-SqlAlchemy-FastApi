# business/dft_dependency.py
# pylint: disable=unused-import
"""
This module contains the
DFTDependencyBusObj class,
which represents the
business object for a
DFTDependency.
"""

from typing import List
from helpers.session_context import SessionContext
from models import DFTDependency
import models
import managers as managers_and_enums  # noqa: F401
from .dft_dependency_fluent import DFTDependencyFluentBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "DFTDependency object is not initialized")


class DFTDependencyBusObj(DFTDependencyFluentBusObj):
    """
    This class represents the business object for a DFTDependency.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DFTDependency]
    ):
        """
        Convert a list of DFTDependency
        objects to a list of
        DFTDependencyBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[DFTDependency]): The
                list of DFTDependency objects to convert.

        Returns:
            List[DFTDependencyBusObj]: The
                list of converted DFTDependencyBusObj
                objects.
        """
        result = list()

        for dft_dependency in obj_list:
            dft_dependency_bus_obj = DFTDependencyBusObj(session_context)

            dft_dependency_bus_obj.load_from_obj_instance(
                dft_dependency)

            result.append(dft_dependency_bus_obj)

        return result
    # dependencyDFTaskID,
    # DynaFlowTaskID

    async def get_dyna_flow_task_id_obj(self) -> models.DynaFlowTask:
        """
        Retrieves the related DynaFlowTask object based
        on the dyna_flow_task_id.

        Returns:
            An instance of the DynaFlowTask model
            representing the related dyna_flow_task.

        """
        dyna_flow_task_manager = managers_and_enums.DynaFlowTaskManager(
            self._session_context)
        dyna_flow_task_obj = await dyna_flow_task_manager.get_by_id(
            self.dyna_flow_task_id)
        return dyna_flow_task_obj

    async def get_dyna_flow_task_id_bus_obj(self):
        """
        Retrieves the related DynaFlowTask
        business object based
        on the dyna_flow_task_id.

        Returns:
            An instance of the DynaFlowTask
            business object
            representing the related dyna_flow_task.

        """
        from .dyna_flow_task import DynaFlowTaskBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = DynaFlowTaskBusObj(self._session_context)
        await bus_obj.load_from_id(self.dyna_flow_task_id)
        return bus_obj
    # isPlaceholder,
