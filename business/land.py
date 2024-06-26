# business/land.py
# pylint: disable=unused-import
"""
This module contains the
LandBusObj class,
which represents the
business object for a
Land.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Land
import managers as managers_and_enums  # noqa: F401
from .land_fluent import LandFluentBusObj


from business.plant import PlantBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "Land object is not initialized")


class LandBusObj(LandFluentBusObj):
    """
    This class represents the business object for a Land.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Land]
    ):
        """
        Convert a list of Land
        objects to a list of
        LandBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Land]): The
                list of Land objects to convert.

        Returns:
            List[LandBusObj]: The
                list of converted LandBusObj
                objects.
        """
        result = list()

        for land in obj_list:
            land_bus_obj = LandBusObj(session_context)

            land_bus_obj.load_from_obj_instance(
                land)

            result.append(land_bus_obj)

        return result


    async def build_plant(
        self) -> PlantBusObj:
        """
        build plant
        instance (not saved yet)
        """
        item = PlantBusObj(self._session_context)

        assert item.plant is not None
        flavor_manager = managers_and_enums.FlavorManager(
            self._session_context)
        flvr_foreign_key_id_flavor = await flavor_manager.from_enum(
            managers_and_enums.FlavorEnum.UNKNOWN)
        item.flvr_foreign_key_id = flvr_foreign_key_id_flavor.flavor_id
        item.plant.flvr_foreign_key_id_code_peek = flvr_foreign_key_id_flavor.code

        item.land_id = self.land_id
        item.plant.land_code_peek = self.code

        return item

    async def get_all_plant(
        self) -> List[PlantBusObj]:
        """
        get all plant
        """
        results = list()
        plant_manager = managers_and_enums.PlantManager(
            self._session_context)
        obj_list = await plant_manager.get_by_land_id(
            self.land_id)
        for obj_item in obj_list:
            bus_obj_item = PlantBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results
