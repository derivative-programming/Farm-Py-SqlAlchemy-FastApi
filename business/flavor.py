# business/flavor.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the
FlavorBusObj class,
which represents the
business object for a
Flavor.
"""

from typing import List

import managers as managers_and_enums  # noqa: F401
import models
from helpers.session_context import SessionContext
from models import Flavor

from .flavor_dyna_flows import \
    FlavorDynaFlowsBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "Flavor object is not initialized")


class FlavorBusObj(FlavorDynaFlowsBusObj):
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
        result = []

        for flavor in obj_list:
            flavor_bus_obj = FlavorBusObj(
                session_context)

            flavor_bus_obj.load_from_obj_instance(
                flavor)

            result.append(flavor_bus_obj)

        return result
    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
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
        from business.pac import \
            PacBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = PacBusObj(self._session_context)
        await bus_obj.load_from_id(self.pac_id)
        return bus_obj


    @property
    def lookup_enum(self) -> managers_and_enums.FlavorEnum:
        """
        Returns the corresponding FlavorEnum
        value based on the lookup_enum_name.
        Raises:
            AttributeError: If the flavor
                attribute is not initialized.
        Returns:
            managers_and_enums.FlavorEnum:
                The corresponding FlavorEnum value.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return (
            managers_and_enums.FlavorEnum[
                self.flavor.lookup_enum_name
            ]
        )

    async def load_from_enum(
        self,
        flavor_enum:
            managers_and_enums.FlavorEnum
    ):
        """
        Load flavor data from dictionary.
        :param flavor_dict: Dictionary
            containing flavor data.
        :raises ValueError: If flavor_dict
            is not a dictionary or if no
            flavor data is found.
        """
        if not isinstance(
            flavor_enum,
            managers_and_enums.FlavorEnum
        ):
            raise ValueError("flavor_enum must be a enum")
        flavor_manager =  \
            managers_and_enums.FlavorManager(
                self._session_context
            )
        self.flavor = await (
            flavor_manager.
            from_enum(flavor_enum)
        )
