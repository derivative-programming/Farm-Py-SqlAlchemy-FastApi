# business/org_customer.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import OrgCustomerManager
from models import OrgCustomer
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

class OrgCustomerInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass
class OrgCustomerBusObj(BaseBusObj):
    """
    This class represents the business object for a OrgCustomer.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.org_customer = OrgCustomer()
    @property
    def org_customer_id(self):
        """
        Get the org_customer ID from the OrgCustomer object.
        :return: The org_customer ID.
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.org_customer_id
    # @org_customer_id.setter
    # def org_customer_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("org_customer_id must be a int.")
    #     self.org_customer.org_customer_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.org_customer.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.org_customer.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.org_customer.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.org_customer:
    #         raise AttributeError("OrgCustomer object is not initialized")
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.org_customer.last_update_user_id = value
    # def set_prop_last_update_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     self.last_update_user_id = value
    #     return self
# endset
    # CustomerID
    # email
    @property
    def email(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        if self.org_customer.email is None:
            return ""
        return self.org_customer.email
    @email.setter
    def email(self, value):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        assert isinstance(value, str), (
            "email must be a string")
        self.org_customer.email = value
    # def set_prop_email(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.email = value
    #     return self
    # OrganizationID
# endset
    # CustomerID
    @property
    def customer_id(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.customer_id
    @customer_id.setter
    def customer_id(self, value: int):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        if not isinstance(value, int):
            raise ValueError("customer_id must be an integer.")
        self.org_customer.customer_id = value
    # def set_prop_customer_id(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.customer_id = value
    #     return self
    @property
    def customer_code_peek(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.customer_code_peek
    # @customer_code_peek.setter
    # def customer_code_peek(self, value):
    #     assert isinstance(
    #       value, uuid.UUID),
    #       "customer_code_peek must be a UUID"
    #     self.org_customer.customer_code_peek = value
    # email,
    # OrganizationID
    @property
    def organization_id(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.organization_id
    @organization_id.setter
    def organization_id(self, value):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        assert isinstance(value, int) or value is None, (
            "organization_id must be an integer or None")
        self.org_customer.organization_id = value
    # def set_prop_organization_id(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.organization_id = value
    #     return self
    @property
    def organization_code_peek(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.organization_code_peek
    # @organization_code_peek.setter
    # def organization_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "organization_code_peek must be a UUID"
    #     self.org_customer.organization_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.org_customer.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.org_customer.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load org_customer data from JSON string.
        :param json_data: JSON string containing org_customer data.
        :raises ValueError: If json_data is not a string
            or if no org_customer data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        org_customer_manager = OrgCustomerManager(self._session_context)
        self.org_customer = org_customer_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load org_customer data from UUID code.
        :param code: UUID code for loading a specific org_customer.
        :raises ValueError: If code is not a UUID or if no org_customer data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        org_customer_manager = OrgCustomerManager(self._session_context)
        org_customer_obj = await org_customer_manager.get_by_code(code)
        self.org_customer = org_customer_obj
        return self
    async def load_from_id(
        self,
        org_customer_id: int
    ):
        """
        Load org_customer data from org_customer ID.
        :param org_customer_id: Integer ID for loading a specific org_customer.
        :raises ValueError: If org_customer_id is not an integer or
            if no org_customer data is found.
        """
        if not isinstance(org_customer_id, int):
            raise ValueError("org_customer_id must be an integer")
        org_customer_manager = OrgCustomerManager(self._session_context)
        org_customer_obj = await org_customer_manager.get_by_id(org_customer_id)
        self.org_customer = org_customer_obj
        return self
    async def load_from_obj_instance(
        self,
        org_customer_obj_instance: OrgCustomer
    ):
        """
        Use the provided OrgCustomer instance.
        :param org_customer_obj_instance: Instance of the OrgCustomer class.
        :raises ValueError: If org_customer_obj_instance is not an instance of OrgCustomer.
        """
        if not isinstance(org_customer_obj_instance, OrgCustomer):
            raise ValueError("org_customer_obj_instance must be an instance of OrgCustomer")
        org_customer_manager = OrgCustomerManager(self._session_context)
        org_customer_obj_instance_org_customer_id = org_customer_obj_instance.org_customer_id
        org_customer_obj = await org_customer_manager.get_by_id(
            org_customer_obj_instance_org_customer_id
        )
        self.org_customer = org_customer_obj
        return self
    async def load_from_dict(
        self,
        org_customer_dict: dict
    ):
        """
        Load org_customer data from dictionary.
        :param org_customer_dict: Dictionary containing org_customer data.
        :raises ValueError: If org_customer_dict is not a
            dictionary or if no org_customer data is found.
        """
        if not isinstance(org_customer_dict, dict):
            raise ValueError("org_customer_dict must be a dictionary")
        org_customer_manager = OrgCustomerManager(self._session_context)
        self.org_customer = org_customer_manager.from_dict(org_customer_dict)
        return self

    def get_session_context(self):
        """
        #TODO add comment
        """
        return self._session_context
    async def refresh(self):
        """
        #TODO add comment
        """
        org_customer_manager = OrgCustomerManager(self._session_context)
        self.org_customer = await org_customer_manager.refresh(self.org_customer)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return (self.org_customer is not None)
    def to_dict(self):
        """
        #TODO add comment
        """
        org_customer_manager = OrgCustomerManager(self._session_context)
        return org_customer_manager.to_dict(self.org_customer)
    def to_json(self):
        """
        #TODO add comment
        """
        org_customer_manager = OrgCustomerManager(self._session_context)
        return org_customer_manager.to_json(self.org_customer)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError("OrgCustomer object is not initialized")
        if self.org_customer.org_customer_id is not None and self.org_customer.org_customer_id > 0:
            org_customer_manager = OrgCustomerManager(self._session_context)
            self.org_customer = await org_customer_manager.update(self.org_customer)
        if self.org_customer.org_customer_id is None or self.org_customer.org_customer_id == 0:
            org_customer_manager = OrgCustomerManager(self._session_context)
            self.org_customer = await org_customer_manager.add(self.org_customer)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        if self.org_customer.org_customer_id > 0:
            org_customer_manager = OrgCustomerManager(self._session_context)
            await org_customer_manager.delete(self.org_customer.org_customer_id)
            self.org_customer = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        self.org_customer.customer_id = random.choice(
            await managers_and_enums.CustomerManager(
                self._session_context).get_list()).customer_id
        self.org_customer.email = f"user{random.randint(1, 100)}@abc.com"
        # self.org_customer.organization_id = random.randint(0, 100)
# endset
        return self
    def get_org_customer_obj(self) -> OrgCustomer:
        """
        #TODO add comment
        """
        if not self.org_customer:
            raise AttributeError(
                "OrgCustomer object is not initialized"
            )
        return self.org_customer
    def is_equal(self, org_customer: OrgCustomer) -> bool:
        """
        #TODO add comment
        """
        org_customer_manager = OrgCustomerManager(self._session_context)
        my_org_customer = self.get_org_customer_obj()
        return org_customer_manager.is_equal(org_customer, my_org_customer)
# endset
    # CustomerID
    async def get_customer_id_rel_obj(self) -> models.Customer:
        """
        #TODO add comment
        """
        customer_manager = managers_and_enums.CustomerManager(
            self._session_context)
        customer_obj = await customer_manager.get_by_id(
            self.customer_id
        )
        return customer_obj
    # email,
    # OrganizationID
    async def get_organization_id_rel_obj(self) -> models.Organization:
        """
        #TODO add comment
        """
        organization_manager = managers_and_enums.OrganizationManager(self._session_context)
        organization_obj = await organization_manager.get_by_id(self.organization_id)
        return organization_obj
# endset
    def get_obj(self) -> OrgCustomer:
        """
        #TODO add comment
        """
        return self.org_customer
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "org_customer"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.org_customer_id
    # CustomerID
    # email,
    # OrganizationID
    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Organization'
    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.organization_code_peek
    async def get_parent_obj(self) -> models.Organization:
        """
        #TODO add comment
        """
        return self.get_organization_id_rel_obj()
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[OrgCustomer]
    ):
        """
        #TODO add comment
        """
        result = list()
        for org_customer in obj_list:
            org_customer_bus_obj = OrgCustomerBusObj(session_context)
            await org_customer_bus_obj.load_from_obj_instance(org_customer)
            result.append(org_customer_bus_obj)
        return result

