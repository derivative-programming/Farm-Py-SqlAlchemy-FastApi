import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from managers import PacManager as PacIDManager #PacID
from managers import TriStateFilterManager
from models import TriStateFilter
class TriStateFilterSessionNotFoundError(Exception):
    pass
class TriStateFilterInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TriStateFilterBusObj:
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise TriStateFilterSessionNotFoundError("session required")
        self.session = session
        self.tri_state_filter = TriStateFilter()
    @property
    def tri_state_filter_id(self):
        return self.tri_state_filter.tri_state_filter_id
    @tri_state_filter_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("tri_state_filter_id must be a int.")
        self.tri_state_filter.tri_state_filter_id = value
    #code
    @property
    def code(self):
        return self.tri_state_filter.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.tri_state_filter.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.tri_state_filter.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.tri_state_filter.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.tri_state_filter.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.tri_state_filter.insert_user_id = value
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.tri_state_filter.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.tri_state_filter.last_update_user_id = value

    #Description
    @property
    def description(self):
        return self.tri_state_filter.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.tri_state_filter.description = value
    #DisplayOrder
    @property
    def display_order(self):
        return self.tri_state_filter.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.tri_state_filter.display_order = value
    #IsActive
    @property
    def is_active(self):
        return self.tri_state_filter.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.tri_state_filter.is_active = value
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.tri_state_filter.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.tri_state_filter.lookup_enum_name = value
    #Name
    @property
    def name(self):
        return self.tri_state_filter.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.tri_state_filter.name = value
    #PacID
    #StateIntValue
    @property
    def state_int_value(self):
        return self.tri_state_filter.state_int_value
    @state_int_value.setter
    def state_int_value(self, value):
        assert isinstance(value, int), "state_int_value must be an integer"
        self.tri_state_filter.state_int_value = value

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @property
    def pac_id(self):
        return self.tri_state_filter.pac_id
    @pac_id.setter
    def pac_id(self, value):
        assert isinstance(value, int) or value is None, "pac_id must be an integer or None"
        self.tri_state_filter.pac_id = value
    @property
    def pac_code_peek(self):
        return self.tri_state_filter.pac_code_peek
    @pac_code_peek.setter
    def pac_code_peek(self, value):
        assert isinstance(value, UUIDType), "pac_code_peek must be a UUID"
        self.tri_state_filter.pac_code_peek = value
    #stateIntValue,

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.tri_state_filter.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.tri_state_filter.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.tri_state_filter.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.tri_state_filter.last_update_utc_date_time = value
    async def load(self, json_data:str=None, code:uuid.UUID=None, tri_state_filter_id:int=None, tri_state_filter_obj_instance:TriStateFilter=None, tri_state_filter_dict:dict=None):
        if tri_state_filter_id and self.tri_state_filter.tri_state_filter_id is None:
            tri_state_filter_manager = TriStateFilterManager(self.session)
            tri_state_filter_obj = await tri_state_filter_manager.get_by_id(tri_state_filter_id)
            self.tri_state_filter = tri_state_filter_obj
        if code and self.tri_state_filter.tri_state_filter_id is None:
            tri_state_filter_manager = TriStateFilterManager(self.session)
            tri_state_filter_obj = await tri_state_filter_manager.get_by_code(code)
            self.tri_state_filter = tri_state_filter_obj
        if tri_state_filter_obj_instance and self.tri_state_filter.tri_state_filter_id is None:
            tri_state_filter_manager = TriStateFilterManager(self.session)
            tri_state_filter_obj = await tri_state_filter_manager.get_by_id(tri_state_filter_obj_instance.tri_state_filter_id)
            self.tri_state_filter = tri_state_filter_obj
        if json_data and self.tri_state_filter.tri_state_filter_id is None:
            tri_state_filter_manager = TriStateFilterManager(self.session)
            self.tri_state_filter = tri_state_filter_manager.from_json(json_data)
        if tri_state_filter_dict and self.tri_state_filter.tri_state_filter_id is None:
            tri_state_filter_manager = TriStateFilterManager(self.session)
            self.tri_state_filter = tri_state_filter_manager.from_dict(tri_state_filter_dict)
    async def refresh(self):
        tri_state_filter_manager = TriStateFilterManager(self.session)
        self.tri_state_filter = await tri_state_filter_manager.refresh(self.tri_state_filter)
    def to_dict(self):
        tri_state_filter_manager = TriStateFilterManager(self.session)
        return tri_state_filter_manager.to_dict(self.tri_state_filter)
    def to_json(self):
        tri_state_filter_manager = TriStateFilterManager(self.session)
        return tri_state_filter_manager.to_json(self.tri_state_filter)
    async def save(self):
        if self.tri_state_filter.tri_state_filter_id > 0:
            tri_state_filter_manager = TriStateFilterManager(self.session)
            self.tri_state_filter = await tri_state_filter_manager.update(self.tri_state_filter)
        if self.tri_state_filter.tri_state_filter_id == 0:
            tri_state_filter_manager = TriStateFilterManager(self.session)
            self.tri_state_filter = await tri_state_filter_manager.add(self.tri_state_filter)
    async def delete(self):
        if self.tri_state_filter.tri_state_filter_id > 0:
            tri_state_filter_manager = TriStateFilterManager(self.session)
            self.tri_state_filter = await tri_state_filter_manager.delete(self.tri_state_filter.tri_state_filter_id)
    def get_tri_state_filter_obj(self) -> TriStateFilter:
        return self.tri_state_filter
    def is_equal(self,tri_state_filter:TriStateFilter) -> TriStateFilter:
        tri_state_filter_manager = TriStateFilterManager(self.session)
        my_tri_state_filter = self.get_tri_state_filter_obj()
        return tri_state_filter_manager.is_equal(tri_state_filter, my_tri_state_filter)

    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return await pac_manager.get_by_id(self.tri_state_filter.pac_id)

