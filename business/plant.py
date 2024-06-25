# business/plant.py
# pylint: disable=unused-import
"""
This module contains the PlantBusObj class,
which represents the business object for a Plant.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Plant
import managers as managers_and_enums  # noqa: F401
from .plant_fluent import PlantFluentBusObj
##GENINCLUDEFILE[GENVALPascalName.top.include.*]

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Plant object is not initialized")


class PlantBusObj(PlantFluentBusObj):
    """
    This class represents the business object for a Plant.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Plant]
    ):
        """
        Convert a list of Plant
        objects to a list of
        PlantBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Plant]): The
                list of Plant objects to convert.

        Returns:
            List[PlantBusObj]: The
                list of converted PlantBusObj
                objects.
        """
        result = list()

        for plant in obj_list:
            plant_bus_obj = PlantBusObj(session_context)

            plant_bus_obj.load_from_obj_instance(
                plant)

            result.append(plant_bus_obj)

        return result
    ##GENINCLUDEFILE[GENVALPascalName.bottom.include.*]
