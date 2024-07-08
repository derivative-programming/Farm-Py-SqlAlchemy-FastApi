# business/tri_state_filter.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
TriStateFilterBusObj class,
which represents the
business object for a
TriStateFilter.
"""

from typing import List

import managers as managers_and_enums  # noqa: F401
import models
from helpers.session_context import SessionContext
from models import TriStateFilter

from .tri_state_filter_dyna_flows import TriStateFilterDynaFlowsBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "TriStateFilter object is not initialized")


class TriStateFilterBusObj(TriStateFilterDynaFlowsBusObj):
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
        result = []

        for tri_state_filter in obj_list:
            tri_state_filter_bus_obj = TriStateFilterBusObj(
                session_context)

            tri_state_filter_bus_obj.load_from_obj_instance(
                tri_state_filter)

            result.append(tri_state_filter_bus_obj)

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
    # stateIntValue


    @property
    def lookup_enum(self) -> managers_and_enums.TriStateFilterEnum:
        """
        Returns the corresponding TriStateFilterEnum
        value based on the lookup_enum_name.
        Raises:
            AttributeError: If the tri_state_filter
                attribute is not initialized.
        Returns:
            managers_and_enums.TriStateFilterEnum:
                The corresponding TriStateFilterEnum value.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return (
            managers_and_enums.TriStateFilterEnum[
                self.tri_state_filter.lookup_enum_name
            ]
        )

    async def load_from_enum(
        self,
        tri_state_filter_enum:
            managers_and_enums.TriStateFilterEnum
    ):
        """
        Load tri_state_filter data from dictionary.
        :param tri_state_filter_dict: Dictionary
            containing tri_state_filter data.
        :raises ValueError: If tri_state_filter_dict
            is not a dictionary or if no
            tri_state_filter data is found.
        """
        if not isinstance(
            tri_state_filter_enum,
            managers_and_enums.TriStateFilterEnum
        ):
            raise ValueError("tri_state_filter_enum must be a enum")
        tri_state_filter_manager =  \
            managers_and_enums.TriStateFilterManager(
                self._session_context
            )
        self.tri_state_filter = await (
            tri_state_filter_manager.
            from_enum(tri_state_filter_enum)
        )
