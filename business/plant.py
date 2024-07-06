# business/plant.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
PlantBusObj class,
which represents the
business object for a
Plant.
"""

from typing import List

import managers as managers_and_enums  # noqa: F401
import models
from helpers.session_context import SessionContext
from models import Plant

from .plant_dyna_flows import PlantDynaFlowsBusObj

##GENINCLUDEFILE[GENVALPascalName.top.include.*]

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Plant object is not initialized")


class PlantBusObj(PlantDynaFlowsBusObj):
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
        result = []

        for plant in obj_list:
            plant_bus_obj = PlantBusObj(
                session_context)

            plant_bus_obj.load_from_obj_instance(
                plant)

            result.append(plant_bus_obj)

        return result
# endset
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # LandID

    async def get_land_id_obj(self) -> models.Land:
        """
        Retrieves the related Land object based
        on the land_id.

        Returns:
            An instance of the Land model
            representing the related land.

        """
        land_manager = managers_and_enums.LandManager(
            self._session_context)
        land_obj = await land_manager.get_by_id(
            self.land_id)
        return land_obj

    async def get_land_id_bus_obj(self):
        """
        Retrieves the related Land
        business object based
        on the land_id.

        Returns:
            An instance of the Land
            business object
            representing the related land.

        """
        from business.land import \
            LandBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = LandBusObj(self._session_context)
        await bus_obj.load_from_id(self.land_id)
        return bus_obj
    # FlvrForeignKeyID

    async def get_flvr_foreign_key_id_obj(self) -> models.Flavor:
        """
        Retrieves the related Flavor object based on the
        flvr_foreign_key_id.

        Returns:
            The related Flavor object.

        """
        flavor_manager = managers_and_enums.FlavorManager(
            self._session_context)
        flavor_obj = await flavor_manager.get_by_id(
            self.flvr_foreign_key_id
        )
        return flavor_obj

    async def get_flvr_foreign_key_id_bus_obj(self):
        """
        Retrieves the related Flavor
        business object based on the
        flvr_foreign_key_id.

        Returns:
            The related Flavor
            business object.

        """
        from business.flavor import \
            FlavorBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = FlavorBusObj(self._session_context)
        await bus_obj.load_from_id(self.flvr_foreign_key_id)
        return bus_obj
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,
# endset

##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=false]Start
##GENLearn[isLookup=false]End
##GENTrainingBlock[caseLookupEnums]End

    ##GENINCLUDEFILE[GENVALPascalName.bottom.include.*]
