# business/error_log.py

"""
This module contains the ErrorLogBusObj class,
which represents the business object for a ErrorLog.
"""

from typing import List
from helpers.session_context import SessionContext
from managers import ErrorLogManager
from models import ErrorLog
import models
import managers as managers_and_enums
from .error_log_fluent import ErrorLogFluentBusObj

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

            await error_log_bus_obj.load_from_obj_instance(
                error_log)

            result.append(error_log_bus_obj)

        return result

