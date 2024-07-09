# dyna_flows/pac_process_all_dyna_flow_type_schedule_flow.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the implementation of the
DynaFlowPacProcessAllDynaFlowTypeScheduleFlow class,
which is responsible for building dynamic flow
tasks for pac sample workflows.
"""

from business.dyna_flow import DynaFlowBusObj
from managers import DynaFlowTaskTypeEnum
from dyna_flows.dyna_flow_base import DynaFlowBase


class DynaFlowPacProcessAllDynaFlowTypeScheduleFlow(DynaFlowBase):  # pylint: disable=too-few-public-methods
    """
    The DynaFlowPacProcessAllDynaFlowTypeScheduleFlow class is responsible
    for building dynamic flow tasks
    """

    async def build_dyna_flow_tasks(
        self,
        dyna_flow_bus_obj: DynaFlowBusObj,
    ):
        """
        Builds the dynamic flow tasks for the pac sample workflow.

        Args:
            dyna_flow_bus_obj
            (DynaFlowBusObj):
                The DynaFlowBusObj instance.

        Returns:
            None
        """
        last_task_id = 0
        # ProcessAllDynaFlowTypeScheduleTask
        last_task_id = await self._build_dyna_flow_task(
            dyna_flow_bus_obj,
            last_task_id,
            DynaFlowTaskTypeEnum.PROCESSALLDYNAFLOWTYPESCHEDULETASK,
            "",
            str(dyna_flow_bus_obj.subject_code),
            "",
        )

        await self._build_dyna_flow_task(
            dyna_flow_bus_obj,
            last_task_id,
            DynaFlowTaskTypeEnum.DYNAFLOWTASKDYNAFLOWCLEANUP,
            "Cleanup",
            str(dyna_flow_bus_obj.subject_code),
            "",
        )
