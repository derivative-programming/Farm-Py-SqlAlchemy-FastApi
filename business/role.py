# business/role.py
# pylint: disable=unused-import
"""
This module contains the RoleBusObj class,
which represents the business object for a Role.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Role
import managers as managers_and_enums  # noqa: F401
from .role_fluent import RoleFluentBusObj

class RoleBusObj(RoleFluentBusObj):
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
            role_bus_obj = RoleBusObj(session_context)

            await role_bus_obj.load_from_obj_instance(
                role)

            result.append(role_bus_obj)

        return result

