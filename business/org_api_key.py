# business/org_api_key.py
# pylint: disable=unused-import
"""
This module contains the
OrgApiKeyBusObj class,
which represents the
business object for a
OrgApiKey.
"""

from typing import List
from helpers.session_context import SessionContext
from models import OrgApiKey
import models
import managers as managers_and_enums  # noqa: F401
from .org_api_key_fluent import OrgApiKeyFluentBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "OrgApiKey object is not initialized")


class OrgApiKeyBusObj(OrgApiKeyFluentBusObj):
    """
    This class represents the business object for a OrgApiKey.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[OrgApiKey]
    ):
        """
        Convert a list of OrgApiKey
        objects to a list of
        OrgApiKeyBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[OrgApiKey]): The
                list of OrgApiKey objects to convert.

        Returns:
            List[OrgApiKeyBusObj]: The
                list of converted OrgApiKeyBusObj
                objects.
        """
        result = list()

        for org_api_key in obj_list:
            org_api_key_bus_obj = OrgApiKeyBusObj(session_context)

            org_api_key_bus_obj.load_from_obj_instance(
                org_api_key)

            result.append(org_api_key_bus_obj)

        return result
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
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
    # OrgCustomerID

    async def get_org_customer_id_obj(self) -> models.OrgCustomer:
        """
        Retrieves the related OrgCustomer object based on the
        org_customer_id.

        Returns:
            The related OrgCustomer object.

        """
        org_customer_manager = managers_and_enums.OrgCustomerManager(
            self._session_context)
        org_customer_obj = await org_customer_manager.get_by_id(
            self.org_customer_id
        )
        return org_customer_obj

    async def get_org_customer_id_bus_obj(self):
        """
        Retrieves the related OrgCustomer
        business object based on the
        org_customer_id.

        Returns:
            The related OrgCustomer
            business object.

        """
        from .org_customer import OrgCustomerBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = OrgCustomerBusObj(self._session_context)
        await bus_obj.load_from_id(self.org_customer_id)
        return bus_obj
