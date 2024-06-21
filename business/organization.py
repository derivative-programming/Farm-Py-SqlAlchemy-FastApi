# business/organization.py

"""
This module contains the OrganizationBusObj class,
which represents the business object for a Organization.
"""

from typing import List
from helpers.session_context import SessionContext
from managers import OrganizationManager
from models import Organization
import models
import managers as managers_and_enums
from .organization_fluent import OrganizationFluentBusObj

from business.org_customer import OrgCustomerBusObj

from business.org_api_key import OrgApiKeyBusObj

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

            await organization_bus_obj.load_from_obj_instance(
                organization)

            result.append(organization_bus_obj)

        return result

    async def build_org_customer(self) -> OrgCustomerBusObj:
        item = OrgCustomerBusObj(self._session_context)

        item.organization_id = self.organization_id
        item.org_customer.organization_code_peek = self.code

        return item

    async def get_all_org_customer(self) -> List[OrgCustomerBusObj]:
        results = list()
        org_customer_manager = managers_and_enums.OrgCustomerManager(self._session_context)
        obj_list = await org_customer_manager.get_by_organization_id(self.organization_id)
        for obj_item in obj_list:
            bus_obj_item = OrgCustomerBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_org_api_key(self) -> OrgApiKeyBusObj:
        item = OrgApiKeyBusObj(self._session_context)

        item.organization_id = self.organization_id
        item.org_api_key.organization_code_peek = self.code

        return item

    async def get_all_org_api_key(self) -> List[OrgApiKeyBusObj]:
        results = list()
        org_api_key_manager = managers_and_enums.OrgApiKeyManager(self._session_context)
        obj_list = await org_api_key_manager.get_by_organization_id(self.organization_id)
        for obj_item in obj_list:
            bus_obj_item = OrgApiKeyBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

