# business/flavor.py
# pylint: disable=unused-import
"""
This module contains the FlavorBusObj class,
which represents the business object for a Flavor.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Flavor
import managers as managers_and_enums  # noqa: F401
from .flavor_fluent import FlavorFluentBusObj

class FlavorBusObj(FlavorFluentBusObj):
    """
    This class represents the business object for a Flavor.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Flavor]
    ):
        """
        Convert a list of Flavor
        objects to a list of
        FlavorBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Flavor]): The
                list of Flavor objects to convert.

        Returns:
            List[FlavorBusObj]: The
                list of converted FlavorBusObj
                objects.
        """
        result = list()

        for flavor in obj_list:
            flavor_bus_obj = FlavorBusObj(session_context)

            await flavor_bus_obj.load_from_obj_instance(
                flavor)

            result.append(flavor_bus_obj)

        return result

