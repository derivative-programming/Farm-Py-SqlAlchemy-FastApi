# business/error_log.py
# pylint: disable=unused-import
"""
This module contains the
ErrorLogBusObj class,
which represents the
business object for a
ErrorLog.
"""

from typing import List
from helpers.session_context import SessionContext
from models import ErrorLog
import models
import managers as managers_and_enums  # noqa: F401
from .error_log_fluent import ErrorLogFluentBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "ErrorLog object is not initialized")


class ErrorLogBusObj(ErrorLogFluentBusObj):
    """
    This class represents the business object for a ErrorLog.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[ErrorLog]
    ):
        """
        Convert a list of ErrorLog
        objects to a list of
        ErrorLogBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[ErrorLog]): The
                list of ErrorLog objects to convert.

        Returns:
            List[ErrorLogBusObj]: The
                list of converted ErrorLogBusObj
                objects.
        """
        result = list()

        for error_log in obj_list:
            error_log_bus_obj = ErrorLogBusObj(session_context)

            error_log_bus_obj.load_from_obj_instance(
                error_log)

            result.append(error_log_bus_obj)

        return result
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
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
    # url,
