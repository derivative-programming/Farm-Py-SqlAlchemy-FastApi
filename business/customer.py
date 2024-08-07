# business/customer.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the
CustomerBusObj class,
which represents the
business object for a
Customer.
"""

from typing import List

import managers as managers_and_enums  # noqa: F401
import models
from helpers.session_context import SessionContext
from models import Customer

from .customer_dyna_flows import \
    CustomerDynaFlowsBusObj


from .customer_role import CustomerRoleBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "Customer object is not initialized")


class CustomerBusObj(CustomerDynaFlowsBusObj):
    """
    This class represents the business object for a Customer.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Customer]
    ):
        """
        Convert a list of Customer
        objects to a list of
        CustomerBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Customer]): The
                list of Customer objects to convert.

        Returns:
            List[CustomerBusObj]: The
                list of converted CustomerBusObj
                objects.
        """
        result = []

        for customer in obj_list:
            customer_bus_obj = CustomerBusObj(
                session_context)

            customer_bus_obj.load_from_obj_instance(
                customer)

            result.append(customer_bus_obj)

        return result
    # activeOrganizationID
    # email
    # emailConfirmedUTCDateTime
    # firstName
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue
    # fSUserCodeValue
    # isActive
    # isEmailAllowed
    # isEmailConfirmed
    # isEmailMarketingAllowed
    # isLocked
    # isMultipleOrganizationsAllowed
    # isVerboseLoggingForced
    # lastLoginUTCDateTime
    # lastName
    # password
    # phone
    # province
    # registrationUTCDateTime
    # TacID

    async def get_tac_id_obj(self) -> models.Tac:
        """
        Retrieves the related Tac object based
        on the tac_id.

        Returns:
            An instance of the Tac model
            representing the related tac.

        """
        tac_manager = managers_and_enums.TacManager(
            self._session_context)
        tac_obj = await tac_manager.get_by_id(
            self.tac_id)
        return tac_obj

    async def get_tac_id_bus_obj(self):
        """
        Retrieves the related Tac
        business object based
        on the tac_id.

        Returns:
            An instance of the Tac
            business object
            representing the related tac.

        """
        from business.tac import \
            TacBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = TacBusObj(self._session_context)
        await bus_obj.load_from_id(self.tac_id)
        return bus_obj
    # uTCOffsetInMinutes
    # zip


    async def build_customer_role(
        self
    ) -> CustomerRoleBusObj:
        """
        build customer_role
        instance (not saved yet)
        """
        item = CustomerRoleBusObj(self._session_context)

        assert item.customer_role is not None
        role_manager = \
            managers_and_enums.RoleManager(
                self._session_context)
        role_id_role = await \
            role_manager.from_enum(
                managers_and_enums.RoleEnum.UNKNOWN)
        item.role_id = \
            role_id_role.role_id
        item.customer_role.role_id_code_peek = \
            role_id_role.code

        item.customer_id = self.customer_id
        item.customer_role.customer_code_peek = self.code

        return item

    async def get_all_customer_role(
        self
    ) -> List[CustomerRoleBusObj]:
        """
        get all customer_role
        """
        results = []
        customer_role_manager = managers_and_enums.CustomerRoleManager(
            self._session_context)
        obj_list = await customer_role_manager.get_by_customer_id(
            self.customer_id)
        for obj_item in obj_list:
            bus_obj_item = CustomerRoleBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results
