# business/org_customer.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
from services.db_config import DB_DIALECT, generate_uuid
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
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class OrgCustomerBusObj(BaseBusObj):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.org_customer = OrgCustomer()
    @property
    def org_customer_id(self):
        return self.org_customer.org_customer_id
    @org_customer_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("org_customer_id must be a int.")
        self.org_customer.org_customer_id = value
    # code
    @property
    def code(self):
        return self.org_customer.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.org_customer.code = value
    # last_change_code
    @property
    def last_change_code(self):
        return self.org_customer.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.org_customer.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        return self.org_customer.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.org_customer.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        return self.org_customer.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.org_customer.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self
# endset
    # CustomerID
    # email
    @property
    def email(self):
        return self.org_customer.email
    @email.setter
    def email(self, value):
        assert isinstance(value, str), (
            "email must be a string")
        self.org_customer.email = value
    def set_prop_email(self, value):
        self.email = value
        return self
    # OrganizationID
# endset
    # CustomerID
    @property
    def customer_id(self):
        return self.org_customer.customer_id
    @customer_id.setter
    def customer_id(self, value: int):
        if not isinstance(value, int):
            raise ValueError("customer_id must be an integer.")
        self.org_customer.customer_id = value
    def set_prop_customer_id(self, value):
        self.customer_id = value
        return self
    @property
    def customer_code_peek(self):
        return self.org_customer.customer_code_peek
    # @customer_code_peek.setter
    # def customer_code_peek(self, value):
    #     assert isinstance(
    #       value, UUIDType),
    #       "customer_code_peek must be a UUID"
    #     self.org_customer.customer_code_peek = value
    # email,
    # OrganizationID
    @property
    def organization_id(self):
        return self.org_customer.organization_id
    @organization_id.setter
    def organization_id(self, value):
        assert isinstance(value, int) or value is None, (
            "organization_id must be an integer or None")
        self.org_customer.organization_id = value
    def set_prop_organization_id(self, value):
        self.organization_id = value
        return self
    @property
    def organization_code_peek(self):
        return self.org_customer.organization_code_peek
    # @organization_code_peek.setter
    # def organization_code_peek(self, value):
    #     assert isinstance(value, UUIDType),
    #           "organization_code_peek must be a UUID"
    #     self.org_customer.organization_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.org_customer.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.org_customer.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.org_customer.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.org_customer.last_update_utc_date_time = value

    async def load(self, json_data: str = None,
                   code: uuid.UUID = None,
                   org_customer_id: int = None,
                   org_customer_obj_instance: OrgCustomer = None,
                   org_customer_dict: dict = None):
        if org_customer_id and self.org_customer.org_customer_id is None:
            org_customer_manager = OrgCustomerManager(self._session_context)
            org_customer_obj = await org_customer_manager.get_by_id(org_customer_id)
            self.org_customer = org_customer_obj
        if code and self.org_customer.org_customer_id is None:
            org_customer_manager = OrgCustomerManager(self._session_context)
            org_customer_obj = await org_customer_manager.get_by_code(code)
            self.org_customer = org_customer_obj
        if org_customer_obj_instance and self.org_customer.org_customer_id is None:
            org_customer_manager = OrgCustomerManager(self._session_context)
            org_customer_obj = await org_customer_manager.get_by_id(
                org_customer_obj_instance.org_customer_id
                )
            self.org_customer = org_customer_obj
        if json_data and self.org_customer.org_customer_id is None:
            org_customer_manager = OrgCustomerManager(self._session_context)
            self.org_customer = org_customer_manager.from_json(json_data)
        if org_customer_dict and self.org_customer.org_customer_id is None:
            org_customer_manager = OrgCustomerManager(self._session_context)
            self.org_customer = org_customer_manager.from_dict(org_customer_dict)
        return self
    @staticmethod
    async def get(
        session_context: SessionContext,
        json_data: str = None,
        code: uuid.UUID = None,
        org_customer_id: int = None,
        org_customer_obj_instance: OrgCustomer = None,
        org_customer_dict: dict = None
    ):
        result = OrgCustomerBusObj(session_context)
        await result.load(
            json_data,
            code,
            org_customer_id,
            org_customer_obj_instance,
            org_customer_dict
        )
        return result

    async def refresh(self):
        org_customer_manager = OrgCustomerManager(self._session_context)
        self.org_customer = await org_customer_manager.refresh(self.org_customer)
        return self
    def is_valid(self):
        return (self.org_customer is not None)
    def to_dict(self):
        org_customer_manager = OrgCustomerManager(self._session_context)
        return org_customer_manager.to_dict(self.org_customer)
    def to_json(self):
        org_customer_manager = OrgCustomerManager(self._session_context)
        return org_customer_manager.to_json(self.org_customer)
    async def save(self):
        if self.org_customer.org_customer_id is not None and self.org_customer.org_customer_id > 0:
            org_customer_manager = OrgCustomerManager(self._session_context)
            self.org_customer = await org_customer_manager.update(self.org_customer)
        if self.org_customer.org_customer_id is None or self.org_customer.org_customer_id == 0:
            org_customer_manager = OrgCustomerManager(self._session_context)
            self.org_customer = await org_customer_manager.add(self.org_customer)
        return self
    async def delete(self):
        if self.org_customer.org_customer_id > 0:
            org_customer_manager = OrgCustomerManager(self._session_context)
            await org_customer_manager.delete(self.org_customer.org_customer_id)
            self.org_customer = None
    async def randomize_properties(self):
        self.org_customer.customer_id = random.choice(
            await managers_and_enums.CustomerManager(
                self._session_context).get_list()).customer_id
        self.org_customer.email = f"user{random.randint(1, 100)}@abc.com"
        # self.org_customer.organization_id = random.randint(0, 100)
# endset
        return self
    def get_org_customer_obj(self) -> OrgCustomer:
        return self.org_customer
    def is_equal(self, org_customer: OrgCustomer) -> OrgCustomer:
        org_customer_manager = OrgCustomerManager(self._session_context)
        my_org_customer = self.get_org_customer_obj()
        return org_customer_manager.is_equal(org_customer, my_org_customer)
# endset
    # CustomerID
    async def get_customer_id_rel_obj(self) -> models.Customer:
        customer_manager = managers_and_enums.CustomerManager(
            self._session_context)
        customer_obj = await customer_manager.get_by_id(
            self.customer_id)
        return customer_obj
    # email,
    # OrganizationID
    async def get_organization_id_rel_obj(self) -> models.Organization:
        organization_manager = managers_and_enums.OrganizationManager(self._session_context)
        organization_obj = await organization_manager.get_by_id(self.organization_id)
        return organization_obj
# endset
    def get_obj(self) -> OrgCustomer:
        return self.org_customer
    def get_object_name(self) -> str:
        return "org_customer"
    def get_id(self) -> int:
        return self.org_customer_id
    # CustomerID
    # email,
    # OrganizationID
    async def get_parent_name(self) -> str:
        return 'Organization'
    async def get_parent_code(self) -> uuid.UUID:
        return self.organization_code_peek
    async def get_parent_obj(self) -> models.Organization:
        return self.get_organization_id_rel_obj()
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[OrgCustomer]
    ):
        result = list()
        for org_customer in obj_list:
            org_customer_bus_obj = OrgCustomerBusObj.get(
                session_context,
                org_customer_obj_instance=org_customer
            )
            result.append(org_customer_bus_obj)
        return result

