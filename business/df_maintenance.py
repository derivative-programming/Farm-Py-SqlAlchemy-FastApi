# business/df_maintenance.py
# pylint: disable=unused-import
"""
This module contains the
DFMaintenanceBusObj class,
which represents the
business object for a
DFMaintenance.
"""

from typing import List
from helpers.session_context import SessionContext
from models import DFMaintenance
import models
import managers as managers_and_enums  # noqa: F401
from .df_maintenance_fluent import DFMaintenanceFluentBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "DFMaintenance object is not initialized")


class DFMaintenanceBusObj(DFMaintenanceFluentBusObj):
    """
    This class represents the business object for a DFMaintenance.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DFMaintenance]
    ):
        """
        Convert a list of DFMaintenance
        objects to a list of
        DFMaintenanceBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[DFMaintenance]): The
                list of DFMaintenance objects to convert.

        Returns:
            List[DFMaintenanceBusObj]: The
                list of converted DFMaintenanceBusObj
                objects.
        """
        result = list()

        for df_maintenance in obj_list:
            df_maintenance_bus_obj = DFMaintenanceBusObj(session_context)

            df_maintenance_bus_obj.load_from_obj_instance(
                df_maintenance)

            result.append(df_maintenance_bus_obj)

        return result
    # isPaused,
    # isScheduledDFProcessRequestCompleted,
    # isScheduledDFProcessRequestStarted,
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
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
    # pausedByUsername,
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier,
