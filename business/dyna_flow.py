# business/dyna_flow.py
# pylint: disable=unused-import
"""
This module contains the
DynaFlowBusObj class,
which represents the
business object for a
DynaFlow.
"""

from typing import List
from helpers.session_context import SessionContext
from models import DynaFlow
import models
import managers as managers_and_enums  # noqa: F401
from .dyna_flow_fluent import DynaFlowFluentBusObj


from .dyna_flow_task import DynaFlowTaskBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "DynaFlow object is not initialized")


class DynaFlowBusObj(DynaFlowFluentBusObj):
    """
    This class represents the business object for a DynaFlow.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DynaFlow]
    ):
        """
        Convert a list of DynaFlow
        objects to a list of
        DynaFlowBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[DynaFlow]): The
                list of DynaFlow objects to convert.

        Returns:
            List[DynaFlowBusObj]: The
                list of converted DynaFlowBusObj
                objects.
        """
        result = list()

        for dyna_flow in obj_list:
            dyna_flow_bus_obj = DynaFlowBusObj(
                session_context)

            dyna_flow_bus_obj.load_from_obj_instance(
                dyna_flow)

            result.append(dyna_flow_bus_obj)

        return result
    # completedUTCDateTime
    # dependencyDynaFlowID,
    # description,
    # DynaFlowTypeID

    async def get_dyna_flow_type_id_obj(self) -> models.DynaFlowType:
        """
        Retrieves the related DynaFlowType object based on the
        dyna_flow_type_id.

        Returns:
            The related DynaFlowType object.

        """
        dyna_flow_type_manager = managers_and_enums.DynaFlowTypeManager(
            self._session_context)
        dyna_flow_type_obj = await dyna_flow_type_manager.get_by_id(
            self.dyna_flow_type_id
        )
        return dyna_flow_type_obj

    async def get_dyna_flow_type_id_bus_obj(self):
        """
        Retrieves the related DynaFlowType
        business object based on the
        dyna_flow_type_id.

        Returns:
            The related DynaFlowType
            business object.

        """
        from .dyna_flow_type import DynaFlowTypeBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = DynaFlowTypeBusObj(self._session_context)
        await bus_obj.load_from_id(self.dyna_flow_type_id)
        return bus_obj
    # isBuildTaskDebugRequired,
    # isCanceled,
    # isCancelRequested,
    # isCompleted,
    # isPaused,
    # isResubmitted,
    # isRunTaskDebugRequired,
    # isStarted,
    # isSuccessful,
    # isTaskCreationStarted,
    # isTasksCreated,
    # minStartUTCDateTime
    # PacID

    async def get_pac_id_obj(self) -> models.Pac:
        """
        Retrieves the related Pac object based
        on the pac_id.

        Returns:
            An instance of the Pac model
            representing the related pac.

        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj

    async def get_pac_id_bus_obj(self):
        """
        Retrieves the related Pac
        business object based
        on the pac_id.

        Returns:
            An instance of the Pac
            business object
            representing the related pac.

        """
        from .pac import PacBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = PacBusObj(self._session_context)
        await bus_obj.load_from_id(self.pac_id)
        return bus_obj
    # param1,
    # parentDynaFlowID,
    # priorityLevel,
    # requestedUTCDateTime
    # resultValue,
    # rootDynaFlowID,
    # startedUTCDateTime
    # subjectCode,
    # taskCreationProcessorIdentifier,


    async def build_dyna_flow_task(
        self
    ) -> DynaFlowTaskBusObj:
        """
        build dyna_flow_task
        instance (not saved yet)
        """
        item = DynaFlowTaskBusObj(self._session_context)

        assert item.dyna_flow_task is not None
        dyna_flow_task_type_manager = managers_and_enums.DynaFlowTaskTypeManager(
            self._session_context)
        dyna_flow_task_type_id_dyna_flow_task_type = await dyna_flow_task_type_manager.from_enum(
            managers_and_enums.DynaFlowTaskTypeEnum.UNKNOWN)
        item.dyna_flow_task_type_id = dyna_flow_task_type_id_dyna_flow_task_type.dyna_flow_task_type_id
        item.dyna_flow_task.dyna_flow_task_type_id_code_peek = dyna_flow_task_type_id_dyna_flow_task_type.code

        item.dyna_flow_id = self.dyna_flow_id
        item.dyna_flow_task.dyna_flow_code_peek = self.code

        return item

    async def get_all_dyna_flow_task(
        self
    ) -> List[DynaFlowTaskBusObj]:
        """
        get all dyna_flow_task
        """
        results = list()
        dyna_flow_task_manager = managers_and_enums.DynaFlowTaskManager(
            self._session_context)
        obj_list = await dyna_flow_task_manager.get_by_dyna_flow_id(
            self.dyna_flow_id)
        for obj_item in obj_list:
            bus_obj_item = DynaFlowTaskBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results
