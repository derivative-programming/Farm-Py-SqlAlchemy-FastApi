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
    This class represents the business object for a Role.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.role = Role()
    @property
    def role_id(self):
        """
        Get the role ID from the Role object.
        :return: The role ID.
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.role_id
    # @role_id.setter
    # def role_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("role_id must be a int.")
    #     self.role.role_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.role.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.role.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.role.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.role:
    #         raise AttributeError("Role object is not initialized")
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.role.last_update_user_id = value
    # def set_prop_last_update_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     self.last_update_user_id = value
    #     return self
# endset
    # description
    @property
    def description(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if self.role.description is None:
            return ""
        return self.role.description
    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        assert isinstance(value, str), "description must be a string"
        self.role.description = value
    # def set_prop_description(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.description = value
    #     return self
    # displayOrder
    @property
    def display_order(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.display_order
    @display_order.setter
    def display_order(self, value):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.role.display_order = value
    # def set_prop_display_order(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.display_order = value
    #     return self
    # isActive
    @property
    def is_active(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.role.is_active = value
    # def set_prop_is_active(self, value: bool):
    #     """
    #     #TODO add comment
    #     """
    #     self.is_active = value
    #     return self
    # lookupEnumName
    @property
    def lookup_enum_name(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if self.role.lookup_enum_name is None:
            return ""
        return self.role.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.role.lookup_enum_name = value
    # def set_prop_lookup_enum_name(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.lookup_enum_name = value
    #     return self
    # name
    @property
    def name(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if self.role.name is None:
            return ""
        return self.role.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        assert isinstance(value, str), "name must be a string"
        self.role.name = value
    # def set_prop_name(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.name = value
    #     return self
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
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.role.pac_id = value
    # def set_prop_pac_id(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.pac_id = value
    #     return self
    @property
    def pac_code_peek(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
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
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.role.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.role.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load role data from JSON string.
        :param json_data: JSON string containing role data.
        :raises ValueError: If json_data is not a string or if no role data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        role_manager = RoleManager(self._session_context)
        self.role = role_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load role data from UUID code.
        :param code: UUID code for loading a specific role.
        :raises ValueError: If code is not a UUID or if no role data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        role_manager = RoleManager(self._session_context)
        role_obj = await role_manager.get_by_code(code)
        self.role = role_obj
        return self
    async def load_from_id(
        self,
        role_id: int
    ):
        """
        Load role data from role ID.
        :param role_id: Integer ID for loading a specific role.
        :raises ValueError: If role_id is not an integer or if no role data is found.
        """
        if not isinstance(role_id, int):
            raise ValueError("role_id must be an integer")
        role_manager = RoleManager(self._session_context)
        role_obj = await role_manager.get_by_id(role_id)
        self.role = role_obj
        return self
    async def load_from_obj_instance(
        self,
        role_obj_instance: Role
    ):
        """
        Use the provided Role instance.
        :param role_obj_instance: Instance of the Role class.
        :raises ValueError: If role_obj_instance is not an instance of Role.
        """
        if not isinstance(role_obj_instance, Role):
            raise ValueError("role_obj_instance must be an instance of Role")
        role_manager = RoleManager(self._session_context)
        role_obj_instance_role_id = role_obj_instance.role_id
        role_obj = await role_manager.get_by_id(
            role_obj_instance_role_id
        )
        self.role = role_obj
        return self
    async def load_from_dict(
        self,
        role_dict: dict
    ):
        """
        Load role data from dictionary.
        :param role_dict: Dictionary containing role data.
        :raises ValueError: If role_dict is not a dictionary or if no role data is found.
        """
        if not isinstance(role_dict, dict):
            raise ValueError("role_dict must be a dictionary")
        role_manager = RoleManager(self._session_context)
        self.role = role_manager.from_dict(role_dict)
        return self

    @property
    def lookup_enum(self) -> managers_and_enums.RoleEnum:
        return managers_and_enums.RoleEnum[self.role.lookup_enum_name]
    async def load_from_enum(
        self,
        role_enum:
            managers_and_enums.RoleEnum
    ):
        """
        Load plant data from dictionary.
        :param plant_dict: Dictionary containing plant data.
        :raises ValueError: If plant_dict is not a dictionary or if no plant data is found.
        """
        if not isinstance(role_enum, managers_and_enums.RoleEnum):
            raise ValueError("role_enum must be a enum")
        role_manager = RoleManager(self._session_context)
        self.role = await role_manager.from_enum(role_enum)

    def get_session_context(self):
        """
        #TODO add comment
        """
        return self._session_context
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
        if not self.role:
            raise AttributeError("Role object is not initialized")
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
        if not self.role:
            raise AttributeError("Role object is not initialized")
        if self.role.role_id > 0:
            role_manager = RoleManager(self._session_context)
            await role_manager.delete(self.role.role_id)
            self.role = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.role:
            raise AttributeError("Role object is not initialized")
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
        if not self.role:
            raise AttributeError("Role object is not initialized")
        return self.role
    def is_equal(self, role: Role) -> bool:
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
            role_bus_obj = RoleBusObj(session_context)
            await role_bus_obj.load_from_obj_instance(role)
            result.append(role_bus_obj)
        return result

