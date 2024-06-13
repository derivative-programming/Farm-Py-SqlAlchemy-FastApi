# business/role.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import RoleManager
from models import Role
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

class RoleInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass
class RoleBusObj(BaseBusObj):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.role = Role()
    @property
    def role_id(self):
        """
        #TODO add comment
        """
        return self.role.role_id
    @role_id.setter
    def code(self, value: int):
        """
        #TODO add comment
        """
        if not isinstance(value, int):
            raise ValueError("role_id must be a int.")
        self.role.role_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        return self.role.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        #if not isinstance(value, uuid.UUID):
        #raise ValueError("code must be a UUID.")
        self.role.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        return self.role.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.role.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        return self.role.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.role.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        self.insert_user_id = value
        return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        return self.role.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.role.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        self.last_update_user_id = value
        return self
# endset
    # description
    @property
    def description(self):
        """
        #TODO add comment
        """
        return self.role.description
    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, str), "description must be a string"
        self.role.description = value
    def set_prop_description(self, value):
        """
        #TODO add comment
        """
        self.description = value
        return self
    # displayOrder
    @property
    def display_order(self):
        """
        #TODO add comment
        """
        return self.role.display_order
    @display_order.setter
    def display_order(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.role.display_order = value
    def set_prop_display_order(self, value):
        """
        #TODO add comment
        """
        self.display_order = value
        return self
    # isActive
    @property
    def is_active(self):
        """
        #TODO add comment
        """
        return self.role.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.role.is_active = value
    def set_prop_is_active(self, value: bool):
        """
        #TODO add comment
        """
        self.is_active = value
        return self
    # lookupEnumName
    @property
    def lookup_enum_name(self):
        """
        #TODO add comment
        """
        return self.role.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.role.lookup_enum_name = value
    def set_prop_lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        self.lookup_enum_name = value
        return self
    # name
    @property
    def name(self):
        """
        #TODO add comment
        """
        return self.role.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, str), "name must be a string"
        self.role.name = value
    def set_prop_name(self, value):
        """
        #TODO add comment
        """
        self.name = value
        return self
    # PacID
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @property
    def pac_id(self):
        """
        #TODO add comment
        """
        return self.role.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.role.pac_id = value
    def set_prop_pac_id(self, value):
        """
        #TODO add comment
        """
        self.pac_id = value
        return self
    @property
    def pac_code_peek(self):
        """
        #TODO add comment
        """
        return self.role.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "pac_code_peek must be a UUID"
    #     self.role.pac_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        return self.role.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.role.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        return self.role.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.role.last_update_utc_date_time = value

    @property
    def lookup_enum(self) -> managers_and_enums.RoleEnum:
        return managers_and_enums.RoleEnum[self.role.lookup_enum_name]
    async def load(
        self,
        json_data: str = None,
        code: uuid.UUID = None,
        role_id: int = None,
        role_obj_instance:
            Role = None,
        role_dict: dict = None,
        role_enum:
            managers_and_enums.RoleEnum = None
    ):
        if role_id and self.role.role_id is None:
            role_manager = RoleManager(self._session_context)
            role_obj = await role_manager.get_by_id(role_id)
            self.role = role_obj
        if code and self.role.role_id is None:
            role_manager = RoleManager(self._session_context)
            role_obj = await role_manager.get_by_code(code)
            self.role = role_obj
        if role_obj_instance and self.role.role_id is None:
            role_manager = RoleManager(self._session_context)
            role_obj = await role_manager.get_by_id(role_obj_instance.role_id)
            self.role = role_obj
        if json_data and self.role.role_id is None:
            role_manager = RoleManager(self._session_context)
            self.role = role_manager.from_json(json_data)
        if role_dict and self.role.role_id is None:
            role_manager = RoleManager(self._session_context)
            self.role = role_manager.from_dict(role_dict)
        if role_enum and self.role.role_id is None:
            role_manager = RoleManager(self._session_context)
            self.role = await role_manager.from_enum(role_enum)
    @staticmethod
    async def get(
        session_context: SessionContext,
        json_data: str = None,
        code: uuid.UUID = None,
        role_id: int = None,
        role_obj_instance:
            Role = None,
        role_dict: dict = None,
        role_enum:
            managers_and_enums.RoleEnum = None
    ):
        result = RoleBusObj(session_context)
        await result.load(
            json_data,
            code,
            role_id,
            role_obj_instance,
            role_dict,
            role_enum
        )
        return result

    async def refresh(self):
        """
        #TODO add comment
        """
        role_manager = RoleManager(self._session_context)
        self.role = await role_manager.refresh(self.role)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return (self.role is not None)
    def to_dict(self):
        """
        #TODO add comment
        """
        role_manager = RoleManager(self._session_context)
        return role_manager.to_dict(self.role)
    def to_json(self):
        """
        #TODO add comment
        """
        role_manager = RoleManager(self._session_context)
        return role_manager.to_json(self.role)
    async def save(self):
        """
        #TODO add comment
        """
        if self.role.role_id is not None and self.role.role_id > 0:
            role_manager = RoleManager(self._session_context)
            self.role = await role_manager.update(self.role)
        if self.role.role_id is None or self.role.role_id == 0:
            role_manager = RoleManager(self._session_context)
            self.role = await role_manager.add(self.role)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if self.role.role_id > 0:
            role_manager = RoleManager(self._session_context)
            await role_manager.delete(self.role.role_id)
            self.role = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        self.role.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.role.display_order = random.randint(0, 100)
        self.role.is_active = random.choice([True, False])
        self.role.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.role.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.role.pac_id = random.randint(0, 100)
# endset
        return self
    def get_role_obj(self) -> Role:
        """
        #TODO add comment
        """
        return self.role
    def is_equal(self, role: Role) -> Role:
        """
        #TODO add comment
        """
        role_manager = RoleManager(self._session_context)
        my_role = self.get_role_obj()
        return role_manager.is_equal(role, my_role)
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        """
        #TODO add comment
        """
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj
# endset
    def get_obj(self) -> Role:
        """
        #TODO add comment
        """
        return self.role
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "role"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.role_id
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.pac_code_peek
    async def get_parent_obj(self) -> models.Pac:
        """
        #TODO add comment
        """
        return self.get_pac_id_rel_obj()
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Role]
    ):
        """
        #TODO add comment
        """
        result = list()
        for role in obj_list:
            role_bus_obj = RoleBusObj.get(
                session_context,
                role_obj_instance=role
            )
            result.append(role_bus_obj)
        return result

