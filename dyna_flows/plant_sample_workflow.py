# dyna_flows/plant_sample_workflow.py
# pylint: disable=unused-import
"""
This module contains the implementation of the
DynaFlowPlantSampleWorkflow class,
which is responsible for building dynamic flow
tasks for plant sample workflows.
"""

from business.dyna_flow import DynaFlowBusObj
from managers import DynaFlowTaskTypeEnum
from dyna_flows.dyna_flow_base import DynaFlowBase


class DynaFlowPlantSampleWorkflow(DynaFlowBase):
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
