# business/org_customer.py
# pylint: disable=unused-import
"""
This module contains the
OrgCustomerBusObj class,
which represents the
business object for a
OrgCustomer.
"""

from typing import List
from helpers.session_context import SessionContext
from models import OrgCustomer
import models
import managers as managers_and_enums  # noqa: F401
from .org_customer_fluent import OrgCustomerFluentBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "OrgCustomer object is not initialized")


class OrgCustomerBusObj(OrgCustomerFluentBusObj):
    """
    This class represents the business object for a OrgCustomer.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[OrgCustomer]
    ):
        """
        Convert a list of OrgCustomer
        objects to a list of
        OrgCustomerBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[OrgCustomer]): The
                list of OrgCustomer objects to convert.

        Returns:
            List[OrgCustomerBusObj]: The
                list of converted OrgCustomerBusObj
                objects.
        """
        result = list()

        for org_customer in obj_list:
            org_customer_bus_obj = OrgCustomerBusObj(
                session_context)

            org_customer_bus_obj.load_from_obj_instance(
                org_customer)

            result.append(org_customer_bus_obj)

        return result
    # CustomerID

    async def get_customer_id_obj(self) -> models.Customer:
        """
        Retrieves the related Customer object based on the
        customer_id.

        Returns:
            The related Customer object.

        """
        customer_manager = managers_and_enums.CustomerManager(
            self._session_context)
        customer_obj = await customer_manager.get_by_id(
            self.customer_id
        )
        return customer_obj

    async def get_customer_id_bus_obj(self):
        """
        Retrieves the related Customer
        business object based on the
        customer_id.

        Returns:
            The related Customer
            business object.

        """
        from .customer import CustomerBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = CustomerBusObj(self._session_context)
        await bus_obj.load_from_id(self.customer_id)
        return bus_obj
    # email,
    # OrganizationID

    async def get_organization_id_obj(self) -> models.Organization:
        """
        Retrieves the related Organization object based
        on the organization_id.

        Returns:
            An instance of the Organization model
            representing the related organization.

        """
        organization_manager = managers_and_enums.OrganizationManager(
            self._session_context)
        organization_obj = await organization_manager.get_by_id(
            self.organization_id)
        return organization_obj

    async def get_organization_id_bus_obj(self):
        """
        Retrieves the related Organization
        business object based
        on the organization_id.

        Returns:
            An instance of the Organization
            business object
            representing the related organization.

        """
        from .organization import OrganizationBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = OrganizationBusObj(self._session_context)
        await bus_obj.load_from_id(self.organization_id)
        return bus_obj
