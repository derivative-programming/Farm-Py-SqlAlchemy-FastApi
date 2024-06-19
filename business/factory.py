# business/factory.py

"""
This module contains the BusObjFactory class which is responsible for creating business objects based on the object type.
"""

import uuid

from helpers.session_context import SessionContext
from .customer import CustomerBusObj
from .customer_role import CustomerRoleBusObj
from .date_greater_than_filter import DateGreaterThanFilterBusObj
from .error_log import ErrorLogBusObj
from .flavor import FlavorBusObj
from .land import LandBusObj
from .organization import OrganizationBusObj
from .org_api_key import OrgApiKeyBusObj
from .org_customer import OrgCustomerBusObj
from .pac import PacBusObj
from .plant import PlantBusObj
from .role import RoleBusObj
from .tac import TacBusObj
from .tri_state_filter import TriStateFilterBusObj


class BusObjFactory:
    """
    The BusObjFactory class is responsible for creating business objects based on the object type.
    """

    @staticmethod
    async def create_from_code(
        session_context: SessionContext,
        name,
        code: uuid.UUID
    ):
        """
        Create a business object based on the object type and code.

        Args:
            session_context (SessionContext): The session context.
            name (str): The object type.
            code (uuid.UUID): The object code.

        Returns:
            The created business object.

        Raises:
            ValueError: If the object type is unknown.
        """

        if name == '':
            raise ValueError(f"Unknown object type: {name}")

        elif name == 'Customer':
            return await (
                CustomerBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'CustomerRole':
            return await (
                CustomerRoleBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'DateGreaterThanFilter':
            return await (
                DateGreaterThanFilterBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'ErrorLog':
            return await (
                ErrorLogBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'Flavor':
            return await (
                FlavorBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'Land':
            return await (
                LandBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'Organization':
            return await (
                OrganizationBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'OrgApiKey':
            return await (
                OrgApiKeyBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'OrgCustomer':
            return await (
                OrgCustomerBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'Pac':
            return await (
                PacBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'Plant':
            return await (
                PlantBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'Role':
            return await (
                RoleBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'Tac':
            return await (
                TacBusObj(session_context)
                .load_from_code(code)
            )
        elif name == 'TriStateFilter':
            return await (
                TriStateFilterBusObj(session_context)
                .load_from_code(code)
            )

        else:
            raise ValueError(f"Unknown object type: {name}")

    @staticmethod
    async def create_from_id(
        session_context: SessionContext,
        name,
        obj_id: int
    ):
        """
        Create a business object based on the object type and ID.

        Args:
            session_context (SessionContext): The session context.
            name (str): The object type.
            obj_id (int): The object ID.

        Returns:
            The created business object.

        Raises:
            ValueError: If the object type is unknown.
        """

        if name == '':
            raise ValueError(f"Unknown object type: {name}")
        elif name == 'Customer':
            return await (
                CustomerBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'CustomerRole':
            return await (
                CustomerRoleBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'DateGreaterThanFilter':
            return await (
                DateGreaterThanFilterBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'ErrorLog':
            return await (
                ErrorLogBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'Flavor':
            return await (
                FlavorBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'Land':
            return await (
                LandBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'Organization':
            return await (
                OrganizationBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'OrgApiKey':
            return await (
                OrgApiKeyBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'OrgCustomer':
            return await (
                OrgCustomerBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'Pac':
            return await (
                PacBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'Plant':
            return await (
                PlantBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'Role':
            return await (
                RoleBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'Tac':
            return await (
                TacBusObj(session_context)
                .load_from_id(obj_id)
            )
        elif name == 'TriStateFilter':
            return await (
                TriStateFilterBusObj(session_context)
                .load_from_id(obj_id)
            )

        else:
            raise ValueError(f"Unknown object type: {name}")
