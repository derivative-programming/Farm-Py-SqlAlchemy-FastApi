# business/customer_role.py
"""
    #TODO add comment
"""
from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import CustomerRoleManager
from models import CustomerRole
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "CustomerRole object is not initialized")
class CustomerRoleInvalidInitError(Exception):
    """
    #TODO add comment
    """
class CustomerRoleBusObj(BaseBusObj):
    """
    This class represents the business object for a CustomerRole.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.customer_role = CustomerRole()
    @property
    def customer_role_id(self) -> int:
        """
        Get the customer_role ID from the CustomerRole object.
        :return: The customer_role ID.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.customer_role_id
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.customer_role.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.customer_role.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.customer_role.insert_user_id = value
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.customer_role.last_update_user_id = value
# endset
    # CustomerID
    # isPlaceholder
    @property
    def is_placeholder(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.is_placeholder
    @is_placeholder.setter
    def is_placeholder(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_placeholder must be a boolean.")
        self.customer_role.is_placeholder = value
    def set_prop_is_placeholder(self, value: bool):
        """
        #TODO add comment
        """
        self.is_placeholder = value
        return self
    # placeholder
    @property
    def placeholder(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.placeholder
    @placeholder.setter
    def placeholder(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("placeholder must be a boolean.")
        self.customer_role.placeholder = value
    def set_prop_placeholder(self, value: bool):
        """
        #TODO add comment
        """
        self.placeholder = value
        return self
    # RoleID
# endset
    # CustomerID
    @property
    def customer_id(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.customer_id
    @customer_id.setter
    def customer_id(self, value):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "customer_id must be an integer or None")
        self.customer_role.customer_id = value
    def set_prop_customer_id(self, value: int):
        """
        #TODO add comment
        """
        self.customer_id = value
        return self
    @property
    def customer_code_peek(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.customer_code_peek
    # @customer_code_peek.setter
    # def customer_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "customer_code_peek must be a UUID"
    #     self.customer_role.customer_code_peek = value
    # isPlaceholder,
    # placeholder,
    # RoleID
    @property
    def role_id(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.role_id
    @role_id.setter
    def role_id(self, value: int):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("role_id must be an integer.")
        self.customer_role.role_id = value
    def set_prop_role_id(self, value: int):
        """
        #TODO add comment
        """
        self.role_id = value
        return self
    @property
    def role_code_peek(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.role_code_peek
    # @role_code_peek.setter
    # def role_code_peek(self, value):
    #     assert isinstance(
    #       value, uuid.UUID),
    #       "role_code_peek must be a UUID"
    #     self.customer_role.role_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.customer_role.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.customer_role.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load customer_role data from JSON string.
        :param json_data: JSON string containing customer_role data.
        :raises ValueError: If json_data is not a string
            or if no customer_role data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        customer_role_manager = CustomerRoleManager(self._session_context)
        self.customer_role = customer_role_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load customer_role data from UUID code.
        :param code: UUID code for loading a specific customer_role.
        :raises ValueError: If code is not a UUID or if no customer_role data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        customer_role_manager = CustomerRoleManager(self._session_context)
        customer_role_obj = await customer_role_manager.get_by_code(code)
        self.customer_role = customer_role_obj
        return self
    async def load_from_id(
        self,
        customer_role_id: int
    ):
        """
        Load customer_role data from customer_role ID.
        :param customer_role_id: Integer ID for loading a specific customer_role.
        :raises ValueError: If customer_role_id is not an integer or
            if no customer_role data is found.
        """
        if not isinstance(customer_role_id, int):
            raise ValueError("customer_role_id must be an integer")
        customer_role_manager = CustomerRoleManager(self._session_context)
        customer_role_obj = await customer_role_manager.get_by_id(customer_role_id)
        self.customer_role = customer_role_obj
        return self
    async def load_from_obj_instance(
        self,
        customer_role_obj_instance: CustomerRole
    ):
        """
        Use the provided CustomerRole instance.
        :param customer_role_obj_instance: Instance of the CustomerRole class.
        :raises ValueError: If customer_role_obj_instance is not an instance of CustomerRole.
        """
        if not isinstance(customer_role_obj_instance, CustomerRole):
            raise ValueError("customer_role_obj_instance must be an instance of CustomerRole")
        customer_role_manager = CustomerRoleManager(self._session_context)
        customer_role_obj_instance_customer_role_id = customer_role_obj_instance.customer_role_id
        customer_role_obj = await customer_role_manager.get_by_id(
            customer_role_obj_instance_customer_role_id
        )
        self.customer_role = customer_role_obj
        return self
    async def load_from_dict(
        self,
        customer_role_dict: dict
    ):
        """
        Load customer_role data from dictionary.
        :param customer_role_dict: Dictionary containing customer_role data.
        :raises ValueError: If customer_role_dict is not a
            dictionary or if no customer_role data is found.
        """
        if not isinstance(customer_role_dict, dict):
            raise ValueError("customer_role_dict must be a dictionary")
        customer_role_manager = CustomerRoleManager(self._session_context)
        self.customer_role = customer_role_manager.from_dict(customer_role_dict)
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
        customer_role_manager = CustomerRoleManager(self._session_context)
        self.customer_role = await customer_role_manager.refresh(self.customer_role)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return self.customer_role is not None
    def to_dict(self):
        """
        #TODO add comment
        """
        customer_role_manager = CustomerRoleManager(self._session_context)
        return customer_role_manager.to_dict(self.customer_role)
    def to_json(self):
        """
        #TODO add comment
        """
        customer_role_manager = CustomerRoleManager(self._session_context)
        return customer_role_manager.to_json(self.customer_role)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        customer_role_id = self.customer_role.customer_role_id
        if customer_role_id > 0:
            customer_role_manager = CustomerRoleManager(self._session_context)
            self.customer_role = await customer_role_manager.update(self.customer_role)
        if customer_role_id == 0:
            customer_role_manager = CustomerRoleManager(self._session_context)
            self.customer_role = await customer_role_manager.add(self.customer_role)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer_role.customer_role_id > 0:
            customer_role_manager = CustomerRoleManager(self._session_context)
            await customer_role_manager.delete(self.customer_role.customer_role_id)
            self.customer_role = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        # self.customer_role.customer_id = random.randint(0, 100)
        self.customer_role.is_placeholder = (
            random.choice([True, False]))
        self.customer_role.placeholder = (
            random.choice([True, False]))
        self.customer_role.role_id = random.choice(
            await managers_and_enums.RoleManager(
                self._session_context).get_list()).role_id
# endset
        return self
    def get_customer_role_obj(self) -> CustomerRole:
        """
        #TODO add comment
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role
    def is_equal(self, customer_role: CustomerRole) -> bool:
        """
        #TODO add comment
        """
        customer_role_manager = CustomerRoleManager(self._session_context)
        my_customer_role = self.get_customer_role_obj()
        return customer_role_manager.is_equal(customer_role, my_customer_role)
# endset
    # CustomerID
    async def get_customer_id_rel_obj(self) -> models.Customer:
        """
        #TODO add comment
        """
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        customer_obj = await customer_manager.get_by_id(self.customer_id)
        return customer_obj
    # isPlaceholder,
    # placeholder,
    # RoleID
    async def get_role_id_rel_obj(self) -> models.Role:
        """
        #TODO add comment
        """
        role_manager = managers_and_enums.RoleManager(
            self._session_context)
        role_obj = await role_manager.get_by_id(
            self.role_id
        )
        return role_obj
# endset
    def get_obj(self) -> CustomerRole:
        """
        #TODO add comment
        """
        return self.customer_role
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "customer_role"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.customer_role_id
    # CustomerID
    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Customer'
    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.customer_code_peek
    async def get_parent_obj(self) -> models.Customer:
        """
        #TODO add comment
        """
        customer = await self.get_customer_id_rel_obj()
        return customer
    # isPlaceholder,
    # placeholder,
    # RoleID
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[CustomerRole]
    ):
        """
        #TODO add comment
        """
        result = list()
        for customer_role in obj_list:
            customer_role_bus_obj = CustomerRoleBusObj(session_context)
            await customer_role_bus_obj.load_from_obj_instance(customer_role)
            result.append(customer_role_bus_obj)
        return result

