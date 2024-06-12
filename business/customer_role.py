# business/customer_role.py
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
from managers import CustomerRoleManager
from models import CustomerRole
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

class CustomerRoleInvalidInitError(Exception):
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
class CustomerRoleBusObj(BaseBusObj):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.customer_role = CustomerRole()
    @property
    def customer_role_id(self):
        return self.customer_role.customer_role_id
    @customer_role_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("customer_role_id must be a int.")
        self.customer_role.customer_role_id = value
    # code
    @property
    def code(self):
        return self.customer_role.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.customer_role.code = value
    # last_change_code
    @property
    def last_change_code(self):
        return self.customer_role.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.customer_role.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        return self.customer_role.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.customer_role.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        return self.customer_role.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.customer_role.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self
# endset
    # CustomerID
    # isPlaceholder
    @property
    def is_placeholder(self):
        return self.customer_role.is_placeholder
    @is_placeholder.setter
    def is_placeholder(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_placeholder must be a boolean.")
        self.customer_role.is_placeholder = value
    def set_prop_is_placeholder(self, value: bool):
        self.is_placeholder = value
        return self
    # placeholder
    @property
    def placeholder(self):
        return self.customer_role.placeholder
    @placeholder.setter
    def placeholder(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("placeholder must be a boolean.")
        self.customer_role.placeholder = value
    def set_prop_placeholder(self, value: bool):
        self.placeholder = value
        return self
    # RoleID
# endset
    # CustomerID
    @property
    def customer_id(self):
        return self.customer_role.customer_id
    @customer_id.setter
    def customer_id(self, value):
        assert isinstance(value, int) or value is None, (
            "customer_id must be an integer or None")
        self.customer_role.customer_id = value
    def set_prop_customer_id(self, value):
        self.customer_id = value
        return self
    @property
    def customer_code_peek(self):
        return self.customer_role.customer_code_peek
    # @customer_code_peek.setter
    # def customer_code_peek(self, value):
    #     assert isinstance(value, UUIDType),
    #           "customer_code_peek must be a UUID"
    #     self.customer_role.customer_code_peek = value
    # isPlaceholder,
    # placeholder,
    # RoleID
    @property
    def role_id(self):
        return self.customer_role.role_id
    @role_id.setter
    def role_id(self, value: int):
        if not isinstance(value, int):
            raise ValueError("role_id must be an integer.")
        self.customer_role.role_id = value
    def set_prop_role_id(self, value):
        self.role_id = value
        return self
    @property
    def role_code_peek(self):
        return self.customer_role.role_code_peek
    # @role_code_peek.setter
    # def role_code_peek(self, value):
    #     assert isinstance(
    #       value, UUIDType),
    #       "role_code_peek must be a UUID"
    #     self.customer_role.role_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.customer_role.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.customer_role.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.customer_role.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.customer_role.last_update_utc_date_time = value

    async def load(self, json_data: str = None,
                   code: uuid.UUID = None,
                   customer_role_id: int = None,
                   customer_role_obj_instance: CustomerRole = None,
                   customer_role_dict: dict = None):
        if customer_role_id and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self._session_context)
            customer_role_obj = await customer_role_manager.get_by_id(customer_role_id)
            self.customer_role = customer_role_obj
        if code and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self._session_context)
            customer_role_obj = await customer_role_manager.get_by_code(code)
            self.customer_role = customer_role_obj
        if customer_role_obj_instance and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self._session_context)
            customer_role_obj = await customer_role_manager.get_by_id(
                customer_role_obj_instance.customer_role_id
                )
            self.customer_role = customer_role_obj
        if json_data and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self._session_context)
            self.customer_role = customer_role_manager.from_json(json_data)
        if customer_role_dict and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self._session_context)
            self.customer_role = customer_role_manager.from_dict(customer_role_dict)
        return self
    @staticmethod
    async def get(
        session_context: SessionContext,
        json_data: str = None,
        code: uuid.UUID = None,
        customer_role_id: int = None,
        customer_role_obj_instance: CustomerRole = None,
        customer_role_dict: dict = None
    ):
        result = CustomerRoleBusObj(session_context)
        await result.load(
            json_data,
            code,
            customer_role_id,
            customer_role_obj_instance,
            customer_role_dict
        )
        return result

    async def refresh(self):
        customer_role_manager = CustomerRoleManager(self._session_context)
        self.customer_role = await customer_role_manager.refresh(self.customer_role)
        return self
    def is_valid(self):
        return (self.customer_role is not None)
    def to_dict(self):
        customer_role_manager = CustomerRoleManager(self._session_context)
        return customer_role_manager.to_dict(self.customer_role)
    def to_json(self):
        customer_role_manager = CustomerRoleManager(self._session_context)
        return customer_role_manager.to_json(self.customer_role)
    async def save(self):
        if self.customer_role.customer_role_id is not None and self.customer_role.customer_role_id > 0:
            customer_role_manager = CustomerRoleManager(self._session_context)
            self.customer_role = await customer_role_manager.update(self.customer_role)
        if self.customer_role.customer_role_id is None or self.customer_role.customer_role_id == 0:
            customer_role_manager = CustomerRoleManager(self._session_context)
            self.customer_role = await customer_role_manager.add(self.customer_role)
        return self
    async def delete(self):
        if self.customer_role.customer_role_id > 0:
            customer_role_manager = CustomerRoleManager(self._session_context)
            await customer_role_manager.delete(self.customer_role.customer_role_id)
            self.customer_role = None
    async def randomize_properties(self):
        # self.customer_role.customer_id = random.randint(0, 100)
        self.customer_role.is_placeholder = random.choice([True, False])
        self.customer_role.placeholder = random.choice([True, False])
        self.customer_role.role_id = random.choice(
            await managers_and_enums.RoleManager(
                self._session_context).get_list()).role_id
# endset
        return self
    def get_customer_role_obj(self) -> CustomerRole:
        return self.customer_role
    def is_equal(self, customer_role: CustomerRole) -> CustomerRole:
        customer_role_manager = CustomerRoleManager(self._session_context)
        my_customer_role = self.get_customer_role_obj()
        return customer_role_manager.is_equal(customer_role, my_customer_role)
# endset
    # CustomerID
    async def get_customer_id_rel_obj(self) -> models.Customer:
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        customer_obj = await customer_manager.get_by_id(self.customer_id)
        return customer_obj
    # isPlaceholder,
    # placeholder,
    # RoleID
    async def get_role_id_rel_obj(self) -> models.Role:
        role_manager = managers_and_enums.RoleManager(
            self._session_context)
        role_obj = await role_manager.get_by_id(
            self.role_id)
        return role_obj
# endset
    def get_obj(self) -> CustomerRole:
        return self.customer_role
    def get_object_name(self) -> str:
        return "customer_role"
    def get_id(self) -> int:
        return self.customer_role_id
    # CustomerID
    async def get_parent_name(self) -> str:
        return 'Customer'
    async def get_parent_code(self) -> uuid.UUID:
        return self.customer_code_peek
    async def get_parent_obj(self) -> models.Customer:
        return self.get_customer_id_rel_obj()
    # isPlaceholder,
    # placeholder,
    # RoleID
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[CustomerRole]
    ):
        result = list()
        for customer_role in obj_list:
            customer_role_bus_obj = CustomerRoleBusObj.get(
                session_context,
                customer_role_obj_instance=customer_role
            )
            result.append(customer_role_bus_obj)
        return result

