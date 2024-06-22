# business/tac.py
# pylint: disable=unused-import
"""
This module contains the TacBusObj class,
which represents the business object for a Tac.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Tac
import managers as managers_and_enums  # noqa: F401
from .tac_fluent import TacFluentBusObj

from business.organization import OrganizationBusObj

from business.customer import CustomerBusObj

class TacBusObj(TacFluentBusObj):
    """
    This class represents the business object for a Tac.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Tac]
    ):
        """
        Convert a list of Tac
        objects to a list of
        TacBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Tac]): The
                list of Tac objects to convert.

        Returns:
            List[TacBusObj]: The
                list of converted TacBusObj
                objects.
        """
        result = list()

        for tac in obj_list:
            tac_bus_obj = TacBusObj(session_context)

            await tac_bus_obj.load_from_obj_instance(
                tac)

            result.append(tac_bus_obj)

        return result

    async def build_organization(self) -> OrganizationBusObj:
        """
        build organization
        instance (not saved yet)
        """
        item = OrganizationBusObj(self._session_context)

        item.tac_id = self.tac_id
        item.organization.tac_code_peek = self.code

        return item

    async def get_all_organization(self) -> List[OrganizationBusObj]:
        """
        get all organization
        """
        results = list()
        organization_manager = managers_and_enums.OrganizationManager(self._session_context)
        obj_list = await organization_manager.get_by_tac_id(self.tac_id)
        for obj_item in obj_list:
            bus_obj_item = OrganizationBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_customer(self) -> CustomerBusObj:
        """
        build customer
        instance (not saved yet)
        """
        item = CustomerBusObj(self._session_context)

        item.tac_id = self.tac_id
        item.customer.tac_code_peek = self.code

        return item

    async def get_all_customer(self) -> List[CustomerBusObj]:
        """
        get all customer
        """
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_tac_id(self.tac_id)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results
    async def get_customer_by_email_prop(self, email) -> List[CustomerBusObj]:
        """
        get customer by email
        """
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_email_prop(email)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results
    async def get_customer_by_fs_user_code_value_prop(self, fs_user_code_value) -> List[CustomerBusObj]:
        """
        get customer by fs_user_code_value
        """
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_fs_user_code_value_prop(fs_user_code_value)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

