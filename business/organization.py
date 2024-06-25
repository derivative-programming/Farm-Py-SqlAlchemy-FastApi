# business/organization.py
# pylint: disable=unused-import
"""
This module contains the
OrganizationBusObj class,
which represents the
business object for a
Organization.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Organization
import managers as managers_and_enums  # noqa: F401
from .organization_fluent import OrganizationFluentBusObj


from business.org_customer import OrgCustomerBusObj


from business.org_api_key import OrgApiKeyBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "Organization object is not initialized")


class OrganizationBusObj(OrganizationFluentBusObj):
    """
    This class represents the business object for a Organization.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Organization]
    ):
        """
        Convert a list of Organization
        objects to a list of
        OrganizationBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Organization]): The
                list of Organization objects to convert.

        Returns:
            List[OrganizationBusObj]: The
                list of converted OrganizationBusObj
                objects.
        """
        result = list()

        for organization in obj_list:
            organization_bus_obj = OrganizationBusObj(session_context)

            organization_bus_obj.load_from_obj_instance(
                organization)

            result.append(organization_bus_obj)

        return result


    async def build_org_customer(
        self) -> OrgCustomerBusObj:
        """
        build org_customer
        instance (not saved yet)
        """
        item = OrgCustomerBusObj(self._session_context)

        assert item.org_customer is not None


        item.organization_id = self.organization_id
        item.org_customer.organization_code_peek = self.code

        return item

    async def get_all_org_customer(
        self) -> List[OrgCustomerBusObj]:
        """
        get all org_customer
        """
        results = list()
        org_customer_manager = managers_and_enums.OrgCustomerManager(
            self._session_context)
        obj_list = await org_customer_manager.get_by_organization_id(
            self.organization_id)
        for obj_item in obj_list:
            bus_obj_item = OrgCustomerBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results


    async def build_org_api_key(
        self) -> OrgApiKeyBusObj:
        """
        build org_api_key
        instance (not saved yet)
        """
        item = OrgApiKeyBusObj(self._session_context)

        assert item.org_api_key is not None


        item.organization_id = self.organization_id
        item.org_api_key.organization_code_peek = self.code

        return item

    async def get_all_org_api_key(
        self) -> List[OrgApiKeyBusObj]:
        """
        get all org_api_key
        """
        results = list()
        org_api_key_manager = managers_and_enums.OrgApiKeyManager(
            self._session_context)
        obj_list = await org_api_key_manager.get_by_organization_id(
            self.organization_id)
        for obj_item in obj_list:
            bus_obj_item = OrgApiKeyBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

