# business/dyna_flow_type_schedule.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the
DynaFlowTypeScheduleBusObj class,
which represents the
business object for a
DynaFlowTypeSchedule.
"""

from typing import List

import managers as managers_and_enums  # noqa: F401
import models
from helpers.session_context import SessionContext
from models import DynaFlowTypeSchedule

from .dyna_flow_type_schedule_dyna_flows import \
    DynaFlowTypeScheduleDynaFlowsBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "DynaFlowTypeSchedule object is not initialized")


class DynaFlowTypeScheduleBusObj(DynaFlowTypeScheduleDynaFlowsBusObj):
    """
    This class represents the business object for a DynaFlowTypeSchedule.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DynaFlowTypeSchedule]
    ):
        """
        Convert a list of DynaFlowTypeSchedule
        objects to a list of
        DynaFlowTypeScheduleBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[DynaFlowTypeSchedule]): The
                list of DynaFlowTypeSchedule objects to convert.

        Returns:
            List[DynaFlowTypeScheduleBusObj]: The
                list of converted DynaFlowTypeScheduleBusObj
                objects.
        """
        result = []

        for dyna_flow_type_schedule in obj_list:
            dyna_flow_type_schedule_bus_obj = DynaFlowTypeScheduleBusObj(
                session_context)

            dyna_flow_type_schedule_bus_obj.load_from_obj_instance(
                dyna_flow_type_schedule)

            result.append(dyna_flow_type_schedule_bus_obj)

        return result
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
        from business.dyna_flow_type import \
            DynaFlowTypeBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = DynaFlowTypeBusObj(self._session_context)
        await bus_obj.load_from_id(self.dyna_flow_type_id)
        return bus_obj
    # frequencyInHours
    # isActive
    # lastUTCDateTime
    # nextUTCDateTime
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
        from business.pac import \
            PacBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = PacBusObj(self._session_context)
        await bus_obj.load_from_id(self.pac_id)
        return bus_obj
