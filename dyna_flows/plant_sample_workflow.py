# dyna_flows/plant_sample_workflow.py
# pylint: disable=unused-import
"""
This module contains the implementation of the
DynaFlowPlantSampleWorkflow class,
which is responsible for building dynamic flow
tasks for plant sample workflows.
"""

from datetime import datetime  # noqa: F401
from business.dyna_flow import DynaFlowBusObj
from managers import DynaFlowTaskTypeEnum


class DynaFlowPlantSampleWorkflow:
    """
    The DynaFlowPlantSampleWorkflow class is responsible
    for building dynamic flow tasks
    """

    async def build_dyna_flow_tasks(
        self,
        dyna_flow_bus_obj: DynaFlowBusObj,
    ):
        """
        Builds the dynamic flow tasks for the plant sample workflow.

        Args:
            dyna_flow_bus_obj
            (DynaFlowBusObj):
                The DynaFlowBusObj instance.

        Returns:
            None
        """
        last_task_id = 0
# endset

        # DynaFlowTaskPlantTaskOne
        last_task_id = await self._build_dyna_flow_task(
            dyna_flow_bus_obj,
            last_task_id,
            DynaFlowTaskTypeEnum.DYNAFLOWTASKPLANTTASKONE,
            "",
            str(dyna_flow_bus_obj.subject_code),
            "",
        )

        # DynaFlowTaskPlantTaskTwo
        last_task_id = await self._build_dyna_flow_task(
            dyna_flow_bus_obj,
            last_task_id,
            DynaFlowTaskTypeEnum.DYNAFLOWTASKPLANTTASKTWO,
            "",
            str(dyna_flow_bus_obj.subject_code),
            "",
        )
# endset

        await self._build_dyna_flow_task(
            dyna_flow_bus_obj,
            last_task_id,
            DynaFlowTaskTypeEnum.DYNAFLOWTASKDYNAFLOWCLEANUP,
            "Cleanup",
            str(dyna_flow_bus_obj.subject_code),
            "",
        )

    async def _build_dyna_flow_task(
        self,
        dyna_flow_bus_obj: DynaFlowBusObj,
        last_task_id: int,
        task_type: DynaFlowTaskTypeEnum,
        description: str,
        param_1: str,
        param_2: str,
    ) -> int:
        """
        Builds a dynamic flow task.

        Args:
            dyna_flow_bus_obj (DynaFlowBusObj): The DynaFlowBusObj instance.
            last_task_id (int): The ID of the last task.
            task_type (DynaFlowTaskTypeEnum): The type of the task.
            description (str): The description of the task.
            param_1 (str): The first parameter of the task.
            param_2 (str): The second parameter of the task.

        Returns:
            int: The ID of the built task.
        """
        task = await dyna_flow_bus_obj.build_dyna_flow_task()
        task.dyna_flow_subject_code = dyna_flow_bus_obj.subject_code
        task.is_run_task_debug_required = dyna_flow_bus_obj.is_run_task_debug_required
        await task.set_prop_dyna_flow_task_type_id_by_enum(task_type)
        task.description = description
        task.requested_utc_date_time = datetime.utcnow()
        task.dependency_dyna_flow_task_id = last_task_id
        task.param_1 = param_1
        task.param_2 = param_2
        await task.save()

        return task.dyna_flow_task_id
