# business/flavor.py
# pylint: disable=unused-import
"""
This module contains the
FlavorBusObj class,
which represents the
business object for a
Flavor.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Flavor
import models
import managers as managers_and_enums  # noqa: F401
from .flavor_fluent import FlavorFluentBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "Flavor object is not initialized")


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

            flavor_bus_obj.load_from_obj_instance(
                flavor)

            result.append(flavor_bus_obj)

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
