import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from managers import PacManager as PacIDManager #PacID
from managers import RoleManager
from models import Role
class RoleSessionNotFoundError(Exception):
    pass
class RoleInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class RoleBusObj:
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise RoleSessionNotFoundError("session required")
        self.session = session
        self.role = Role()
    @property
    def role_id(self):
        return self.role.role_id
    @role_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("role_id must be a int.")
        self.role.role_id = value
    #code
    @property
    def code(self):
        return self.role.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.role.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.role.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.role.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.role.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.role.insert_user_id = value
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.role.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.role.last_update_user_id = value

    #Description
    @property
    def description(self):
        return self.role.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.role.description = value
    #DisplayOrder
    @property
    def display_order(self):
        return self.role.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.role.display_order = value
    #IsActive
    @property
    def is_active(self):
        return self.role.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.role.is_active = value
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.role.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.role.lookup_enum_name = value
    #Name
    @property
    def name(self):
        return self.role.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.role.name = value
    #PacID

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @property
    def pac_id(self):
        return self.role.pac_id
    @pac_id.setter
    def pac_id(self, value):
        assert isinstance(value, int) or value is None, "pac_id must be an integer or None"
        self.role.pac_id = value
    @property
    def pac_code_peek(self):
        return self.role.pac_code_peek
    @pac_code_peek.setter
    def pac_code_peek(self, value):
        assert isinstance(value, UUIDType), "pac_code_peek must be a UUID"
        self.role.pac_code_peek = value

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.role.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.role.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.role.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.role.last_update_utc_date_time = value
    async def load(self, json_data:str=None, code:uuid.UUID=None, role_id:int=None, role_obj_instance:Role=None, role_dict:dict=None):
        if role_id and self.role.role_id is None:
            role_manager = RoleManager(self.session)
            role_obj = await role_manager.get_by_id(role_id)
            self.role = role_obj
        if code and self.role.role_id is None:
            role_manager = RoleManager(self.session)
            role_obj = await role_manager.get_by_code(code)
            self.role = role_obj
        if role_obj_instance and self.role.role_id is None:
            role_manager = RoleManager(self.session)
            role_obj = await role_manager.get_by_id(role_obj_instance.role_id)
            self.role = role_obj
        if json_data and self.role.role_id is None:
            role_manager = RoleManager(self.session)
            self.role = role_manager.from_json(json_data)
        if role_dict and self.role.role_id is None:
            role_manager = RoleManager(self.session)
            self.role = role_manager.from_dict(role_dict)
    async def refresh(self):
        role_manager = RoleManager(self.session)
        self.role = await role_manager.refresh(self.role)
    def to_dict(self):
        role_manager = RoleManager(self.session)
        return role_manager.to_dict(self.role)
    def to_json(self):
        role_manager = RoleManager(self.session)
        return role_manager.to_json(self.role)
    async def save(self):
        if self.role.role_id > 0:
            role_manager = RoleManager(self.session)
            self.role = await role_manager.update(self.role)
        if self.role.role_id == 0:
            role_manager = RoleManager(self.session)
            self.role = await role_manager.add(self.role)
    async def delete(self):
        if self.role.role_id > 0:
            role_manager = RoleManager(self.session)
            self.role = await role_manager.delete(self.role.role_id)
    def get_role_obj(self) -> Role:
        return self.role
    def is_equal(self,role:Role) -> Role:
        role_manager = RoleManager(self.session)
        my_role = self.get_role_obj()
        return role_manager.is_equal(role, my_role)

    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return await pac_manager.get_by_id(self.role.pac_id)

