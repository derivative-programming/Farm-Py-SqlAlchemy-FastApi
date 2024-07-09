# business/dyna_flow_task.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the
DynaFlowTaskBusObj class,
which represents the
business object for a
DynaFlowTask.
"""

from typing import List

import managers as managers_and_enums  # noqa: F401
import models
from helpers.session_context import SessionContext
from models import DynaFlowTask

from .dyna_flow_task_dyna_flows import \
    DynaFlowTaskDynaFlowsBusObj


from .dft_dependency import DFTDependencyBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "DynaFlowTask object is not initialized")


class DynaFlowTaskBusObj(DynaFlowTaskDynaFlowsBusObj):
    """
    This class represents the business object for a DynaFlowTask.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DynaFlowTask]
    ):
        """
        Convert a list of DynaFlowTask
        objects to a list of
        DynaFlowTaskBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[DynaFlowTask]): The
                list of DynaFlowTask objects to convert.

        Returns:
            List[DynaFlowTaskBusObj]: The
                list of converted DynaFlowTaskBusObj
                objects.
        """
        result = []

        for dyna_flow_task in obj_list:
            dyna_flow_task_bus_obj = DynaFlowTaskBusObj(
                session_context)

            dyna_flow_task_bus_obj.load_from_obj_instance(
                dyna_flow_task)

            result.append(dyna_flow_task_bus_obj)

        return result
    # completedUTCDateTime
    # dependencyDynaFlowTaskID
    # description
    # DynaFlowID

    async def get_dyna_flow_id_obj(self) -> models.DynaFlow:
        """
        Retrieves the related DynaFlow object based
        on the dyna_flow_id.

        Returns:
            An instance of the DynaFlow model
            representing the related dyna_flow.

        """
        dyna_flow_manager = managers_and_enums.DynaFlowManager(
            self._session_context)
        dyna_flow_obj = await dyna_flow_manager.get_by_id(
            self.dyna_flow_id)
        return dyna_flow_obj

    async def get_dyna_flow_id_bus_obj(self):
        """
        Retrieves the related DynaFlow
        business object based
        on the dyna_flow_id.

        Returns:
            An instance of the DynaFlow
            business object
            representing the related dyna_flow.

        """
        from business.dyna_flow import \
            DynaFlowBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = DynaFlowBusObj(self._session_context)
        await bus_obj.load_from_id(self.dyna_flow_id)
        return bus_obj
    # dynaFlowSubjectCode
    # DynaFlowTaskTypeID

    async def get_dyna_flow_task_type_id_obj(self) -> models.DynaFlowTaskType:
        """
        Retrieves the related DynaFlowTaskType object based on the
        dyna_flow_task_type_id.

        Returns:
            The related DynaFlowTaskType object.

        """
        dyna_flow_task_type_manager = managers_and_enums.DynaFlowTaskTypeManager(
            self._session_context)
        dyna_flow_task_type_obj = await dyna_flow_task_type_manager.get_by_id(
            self.dyna_flow_task_type_id
        )
        return dyna_flow_task_type_obj

    async def get_dyna_flow_task_type_id_bus_obj(self):
        """
        Retrieves the related DynaFlowTaskType
        business object based on the
        dyna_flow_task_type_id.

        Returns:
            The related DynaFlowTaskType
            business object.

        """
        from business.dyna_flow_task_type import \
            DynaFlowTaskTypeBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = DynaFlowTaskTypeBusObj(self._session_context)
        await bus_obj.load_from_id(self.dyna_flow_task_type_id)
        return bus_obj
    # isCanceled
    # isCancelRequested
    # isCompleted
    # isParallelRunAllowed
    # isRunTaskDebugRequired
    # isStarted
    # isSuccessful
    # maxRetryCount
    # minStartUTCDateTime
    # param1
    # param2
    # processorIdentifier
    # requestedUTCDateTime
    # resultValue
    # retryCount
    # startedUTCDateTime


    async def build_dft_dependency(
        self
    ) -> DFTDependencyBusObj:
        """
        build dft_dependency
        instance (not saved yet)
        """
        item = DFTDependencyBusObj(self._session_context)

        assert item.dft_dependency is not None


        item.dyna_flow_task_id = self.dyna_flow_task_id
        item.dft_dependency.dyna_flow_task_code_peek = self.code

        return item

    async def get_all_dft_dependency(
        self
    ) -> List[DFTDependencyBusObj]:
        """
        get all dft_dependency
        """
        results = []
        dft_dependency_manager = managers_and_enums.DFTDependencyManager(
            self._session_context)
        obj_list = await dft_dependency_manager.get_by_dyna_flow_task_id(
            self.dyna_flow_task_id)
        for obj_item in obj_list:
            bus_obj_item = DFTDependencyBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results
