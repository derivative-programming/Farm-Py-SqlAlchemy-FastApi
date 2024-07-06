# dyna_flows/dyna_flow_base.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the implementation of the
DynaFlowBase class,
which is responsible for building dynamic flow tasks.
"""

from datetime import datetime, timezone  # noqa: F401
from business.dyna_flow import DynaFlowBusObj
from managers import DynaFlowTaskTypeEnum, DynaFlowTaskTypeManager


class DynaFlowBase:
    """
    The DynaFlowBase class is responsible
    for building dynamic flow tasks
    """

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
        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            dyna_flow_bus_obj.get_session_context()
        )

        dyna_flow_task_type = await dyna_flow_task_type_manager. \
            from_enum(task_type)

        task = await dyna_flow_bus_obj.build_dyna_flow_task()
        task.dyna_flow_subject_code = dyna_flow_bus_obj.subject_code
        task.is_run_task_debug_required = \
            dyna_flow_bus_obj.is_run_task_debug_required
        task.dyna_flow_task_type_id = \
            dyna_flow_task_type.dyna_flow_task_type_id
        task.description = description
        task.requested_utc_date_time = datetime.now(timezone.utc)
        task.dependency_dyna_flow_task_id = last_task_id
        task.param_1 = param_1
        task.param_2 = param_2
        await task.save()

        return task.dyna_flow_task_id
