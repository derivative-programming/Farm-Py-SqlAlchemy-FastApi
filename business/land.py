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
import models
import managers as managers_and_enums  # noqa: F401
from .land_fluent import LandFluentBusObj


from .plant import PlantBusObj


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
            land_bus_obj = LandBusObj(
                session_context)

            land_bus_obj.load_from_obj_instance(
                land)

            result.append(land_bus_obj)

        return result
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
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


    @property
    def lookup_enum(self) -> managers_and_enums.LandEnum:
        """
        Returns the corresponding LandEnum
        value based on the lookup_enum_name.
        Raises:
            AttributeError: If the land
                attribute is not initialized.
        Returns:
            managers_and_enums.LandEnum:
                The corresponding LandEnum value.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return (
            managers_and_enums.LandEnum[
                self.land.lookup_enum_name
            ]
        )

    async def load_from_enum(
        self,
        land_enum:
            managers_and_enums.LandEnum
    ):
        """
        Load land data from dictionary.
        :param land_dict: Dictionary
            containing land data.
        :raises ValueError: If land_dict
            is not a dictionary or if no
            land data is found.
        """
        if not isinstance(
            land_enum,
            managers_and_enums.LandEnum
        ):
            raise ValueError("land_enum must be a enum")
        land_manager =  \
            managers_and_enums.LandManager(
                self._session_context
            )
        self.land = await (
            land_manager.
            from_enum(land_enum)
        )


    async def build_plant(
        self
    ) -> PlantBusObj:
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
        self
    ) -> List[PlantBusObj]:
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
