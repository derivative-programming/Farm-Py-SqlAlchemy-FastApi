# business/role.py
# pylint: disable=unused-import
"""
This module contains the
RoleBusObj class,
which represents the
business object for a
Role.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Role
import models
import managers as managers_and_enums  # noqa: F401
from .role_dyna_flows import RoleDynaFlowsBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "Role object is not initialized")


class RoleBusObj(RoleDynaFlowsBusObj):
    """
    This class represents the business object for a Role.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Role]
    ):
        """
        Convert a list of Role
        objects to a list of
        RoleBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Role]): The
                list of Role objects to convert.

        Returns:
            List[RoleBusObj]: The
                list of converted RoleBusObj
                objects.
        """
        result = list()

        for role in obj_list:
            role_bus_obj = RoleBusObj(
                session_context)

            role_bus_obj.load_from_obj_instance(
                role)

            result.append(role_bus_obj)

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
    def lookup_enum(self) -> managers_and_enums.RoleEnum:
        """
        Returns the corresponding RoleEnum
        value based on the lookup_enum_name.
        Raises:
            AttributeError: If the role
                attribute is not initialized.
        Returns:
            managers_and_enums.RoleEnum:
                The corresponding RoleEnum value.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return (
            managers_and_enums.RoleEnum[
                self.role.lookup_enum_name
            ]
        )

    async def load_from_enum(
        self,
        role_enum:
            managers_and_enums.RoleEnum
    ):
        """
        Load role data from dictionary.
        :param role_dict: Dictionary
            containing role data.
        :raises ValueError: If role_dict
            is not a dictionary or if no
            role data is found.
        """
        if not isinstance(
            role_enum,
            managers_and_enums.RoleEnum
        ):
            raise ValueError("role_enum must be a enum")
        role_manager =  \
            managers_and_enums.RoleManager(
                self._session_context
            )
        self.role = await (
            role_manager.
            from_enum(role_enum)
        )
