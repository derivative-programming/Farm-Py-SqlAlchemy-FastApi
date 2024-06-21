# business/tri_state_filter.py

"""
This module contains the TriStateFilterBusObj class,
which represents the business object for a TriStateFilter.
"""

from typing import List
from helpers.session_context import SessionContext
from managers import TriStateFilterManager
from models import TriStateFilter
import models
import managers as managers_and_enums
from .tri_state_filter_fluent import TriStateFilterFluentBusObj

class TriStateFilterBusObj(TriStateFilterFluentBusObj):
    """
    This class represents the business object for a TriStateFilter.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[TriStateFilter]
    ):
        """
        Convert a list of TriStateFilter
        objects to a list of
        TriStateFilterBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[TriStateFilter]): The
                list of TriStateFilter objects to convert.

        Returns:
            List[TriStateFilterBusObj]: The
                list of converted TriStateFilterBusObj
                objects.
        """
        result = list()

        for tri_state_filter in obj_list:
            tri_state_filter_bus_obj = TriStateFilterBusObj(session_context)

            await tri_state_filter_bus_obj.load_from_obj_instance(
                tri_state_filter)

            result.append(tri_state_filter_bus_obj)

        return result

