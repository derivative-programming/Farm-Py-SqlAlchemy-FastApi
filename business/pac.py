import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid

from managers import PacManager
from models import Pac
class PacSessionNotFoundError(Exception):
    pass
class PacInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class PacBusObj:
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise PacSessionNotFoundError("session required")
        self.session = session
        self.pac = Pac()
    @property
    def pac_id(self):
        return self.pac.pac_id
    @pac_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("pac_id must be a int.")
        self.pac.pac_id = value
    #code
    @property
    def code(self):
        return self.pac.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.pac.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.pac.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.pac.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.pac.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.pac.insert_user_id = value
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.pac.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.pac.last_update_user_id = value

    #Description
    @property
    def description(self):
        return self.pac.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.pac.description = value
    #DisplayOrder
    @property
    def display_order(self):
        return self.pac.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.pac.display_order = value
    #IsActive
    @property
    def is_active(self):
        return self.pac.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.pac.is_active = value
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.pac.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.pac.lookup_enum_name = value
    #Name
    @property
    def name(self):
        return self.pac.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.pac.name = value

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.pac.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.pac.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.pac.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.pac.last_update_utc_date_time = value
    async def load(self, json_data:str=None, code:uuid.UUID=None, pac_id:int=None, pac_obj_instance:Pac=None, pac_dict:dict=None):
        if pac_id and self.pac.pac_id is None:
            pac_manager = PacManager(self.session)
            pac_obj = await pac_manager.get_by_id(pac_id)
            self.pac = pac_obj
        if code and self.pac.pac_id is None:
            pac_manager = PacManager(self.session)
            pac_obj = await pac_manager.get_by_code(code)
            self.pac = pac_obj
        if pac_obj_instance and self.pac.pac_id is None:
            pac_manager = PacManager(self.session)
            pac_obj = await pac_manager.get_by_id(pac_obj_instance.pac_id)
            self.pac = pac_obj
        if json_data and self.pac.pac_id is None:
            pac_manager = PacManager(self.session)
            self.pac = pac_manager.from_json(json_data)
        if pac_dict and self.pac.pac_id is None:
            pac_manager = PacManager(self.session)
            self.pac = pac_manager.from_dict(pac_dict)
    async def refresh(self):
        pac_manager = PacManager(self.session)
        self.pac = await pac_manager.refresh(self.pac)
    def to_dict(self):
        pac_manager = PacManager(self.session)
        return pac_manager.to_dict(self.pac)
    def to_json(self):
        pac_manager = PacManager(self.session)
        return pac_manager.to_json(self.pac)
    async def save(self):
        if self.pac.pac_id > 0:
            pac_manager = PacManager(self.session)
            self.pac = await pac_manager.update(self.pac)
        if self.pac.pac_id == 0:
            pac_manager = PacManager(self.session)
            self.pac = await pac_manager.add(self.pac)
    async def delete(self):
        if self.pac.pac_id > 0:
            pac_manager = PacManager(self.session)
            self.pac = await pac_manager.delete(self.pac.pac_id)
    def get_pac_obj(self) -> Pac:
        return self.pac
    def is_equal(self,pac:Pac) -> Pac:
        pac_manager = PacManager(self.session)
        my_pac = self.get_pac_obj()
        return pac_manager.is_equal(pac, my_pac)

