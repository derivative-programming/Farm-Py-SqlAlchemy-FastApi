# business/pac.py
# pylint: disable=unused-import
"""
"""
import uuid
from decimal import Decimal  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from typing import List
from helpers import SessionContext, TypeConversion  # noqa: F401
from models import Pac, DynaFlow
from models import pac
import managers as managers_and_enums  # noqa: F401
from .pac_reports import PacReportsBusObj


class PacDynaFlowsBusObj(PacReportsBusObj):
    """
    """
# PacProcessAllDynaFlowTypeScheduleFlow
    async def request_dyna_flow_pac_process_all_dyna_flow_type_schedule_flow(
        self,
        description="Pac Process All Dyna Flow Type Schedule Flow",
        dependency_dyna_flow_id=0,
        parent_dyna_flow_id=0,
        param_1=""
    ) -> int:
        """
        Request the pac sample workflow dynamic flow.

        Returns:
            None
        """

        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        dyna_flow_manager = managers_and_enums.DynaFlowManager(
            self._session_context)
        dyna_flow_type_manager = managers_and_enums.DynaFlowTypeManager(
            self._session_context)

        pac_list = await pac_manager.get_list()

        pac_obj = pac_list[0]

        dyna_flow = await dyna_flow_manager.build(
            pac_id=pac_obj.pac_id,
            description=description,
            requested_utc_date_time=datetime.now(timezone.utc),
            subject_code=self.code,
            dependency_dyna_flow_id=dependency_dyna_flow_id,
            parent_dyna_flow_id=parent_dyna_flow_id,
            param_1=param_1,
        )

        dyna_flow_type = await dyna_flow_type_manager.from_enum(
            managers_and_enums.DynaFlowTypeEnum.PACPROCESSALLDYNAFLOWTYPESCHEDULEFLOW
        )

        dyna_flow.dyna_flow_type_id = dyna_flow_type.dyna_flow_type_id

        dyna_flow = await dyna_flow_manager.add(dyna_flow)

        if dyna_flow.parent_dyna_flow_id > 0:

            parent_dyna_flow = await dyna_flow_manager.get_by_id(
                dyna_flow.parent_dyna_flow_id)

            dyna_flow.root_dyna_flow_id = parent_dyna_flow.root_dyna_flow_id

        else:
            dyna_flow.root_dyna_flow_id = dyna_flow.dyna_flow_id

        dyna_flow = await dyna_flow_manager.update(dyna_flow)

        return dyna_flow.dyna_flow_id
