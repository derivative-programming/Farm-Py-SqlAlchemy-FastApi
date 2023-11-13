import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from business.pac import PacBusObj #PacID
from services.db_config import db_dialect,generate_uuid
from managers import PacManager as PacIDManager #PacID
from managers import FlavorManager
from models import Flavor
import managers as managers_and_enums
class FlavorSessionNotFoundError(Exception):
    pass
class FlavorInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class FlavorBusObj:
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise FlavorSessionNotFoundError("session required")
        self.session = session
        self.flavor = Flavor()
    @property
    def flavor_id(self):
        return self.flavor.flavor_id
    @flavor_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("flavor_id must be a int.")
        self.flavor.flavor_id = value
    #code
    @property
    def code(self):
        return self.flavor.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.flavor.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.flavor.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.flavor.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.flavor.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.flavor.insert_user_id = value
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.flavor.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.flavor.last_update_user_id = value

    #Description
    @property
    def description(self):
        return self.flavor.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.flavor.description = value
    #DisplayOrder
    @property
    def display_order(self):
        return self.flavor.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.flavor.display_order = value
    #IsActive
    @property
    def is_active(self):
        return self.flavor.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.flavor.is_active = value
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.flavor.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.flavor.lookup_enum_name = value
    #Name
    @property
    def name(self):
        return self.flavor.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.flavor.name = value
    #PacID

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @property
    def pac_id(self):
        return self.flavor.pac_id
    @pac_id.setter
    def pac_id(self, value):
        assert isinstance(value, int) or value is None, "pac_id must be an integer or None"
        self.flavor.pac_id = value
    @property
    def pac_code_peek(self):
        return self.flavor.pac_code_peek
    @pac_code_peek.setter
    def pac_code_peek(self, value):
        assert isinstance(value, UUIDType), "pac_code_peek must be a UUID"
        self.flavor.pac_code_peek = value

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.flavor.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.flavor.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.flavor.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.flavor.last_update_utc_date_time = value

    @property
    def lookup_enum(self) -> managers_and_enums.FlavorEnum:
        return managers_and_enums.FlavorEnum[self.flavor.lookup_enum_name]
    async def load(self, json_data:str=None,
                   code:uuid.UUID=None,
                   flavor_id:int=None,
                   flavor_obj_instance:Flavor=None,
                   flavor_dict:dict=None,
                   flavor_enum:managers_and_enums.FlavorEnum=None):
        if flavor_id and self.flavor.flavor_id is None:
            flavor_manager = FlavorManager(self.session)
            flavor_obj = await flavor_manager.get_by_id(flavor_id)
            self.flavor = flavor_obj
        if code and self.flavor.flavor_id is None:
            flavor_manager = FlavorManager(self.session)
            flavor_obj = await flavor_manager.get_by_code(code)
            self.flavor = flavor_obj
        if flavor_obj_instance and self.flavor.flavor_id is None:
            flavor_manager = FlavorManager(self.session)
            flavor_obj = await flavor_manager.get_by_id(flavor_obj_instance.flavor_id)
            self.flavor = flavor_obj
        if json_data and self.flavor.flavor_id is None:
            flavor_manager = FlavorManager(self.session)
            self.flavor = flavor_manager.from_json(json_data)
        if flavor_dict and self.flavor.flavor_id is None:
            flavor_manager = FlavorManager(self.session)
            self.flavor = flavor_manager.from_dict(flavor_dict)
        if flavor_enum and self.flavor.flavor_id is None:
            flavor_manager = FlavorManager(self.session)
            self.flavor = await flavor_manager.from_enum(flavor_enum)

    async def refresh(self):
        flavor_manager = FlavorManager(self.session)
        self.flavor = await flavor_manager.refresh(self.flavor)
    def to_dict(self):
        flavor_manager = FlavorManager(self.session)
        return flavor_manager.to_dict(self.flavor)
    def to_json(self):
        flavor_manager = FlavorManager(self.session)
        return flavor_manager.to_json(self.flavor)
    async def save(self):
        if self.flavor.flavor_id > 0:
            flavor_manager = FlavorManager(self.session)
            self.flavor = await flavor_manager.update(self.flavor)
        if self.flavor.flavor_id == 0:
            flavor_manager = FlavorManager(self.session)
            self.flavor = await flavor_manager.add(self.flavor)
    async def delete(self):
        if self.flavor.flavor_id > 0:
            flavor_manager = FlavorManager(self.session)
            self.flavor = await flavor_manager.delete(self.flavor.flavor_id)
    def get_flavor_obj(self) -> Flavor:
        return self.flavor
    def is_equal(self,flavor:Flavor) -> Flavor:
        flavor_manager = FlavorManager(self.session)
        my_flavor = self.get_flavor_obj()
        return flavor_manager.is_equal(flavor, my_flavor)

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    async def get_pac_id_rel_bus_obj(self) -> PacBusObj:
        pac_bus_obj = PacBusObj(self.session)
        await pac_bus_obj.load(pac_id=self.flavor.pac_id)
        return pac_bus_obj

    def get_obj(self) -> Flavor:
        return self.flavor
    def get_object_name(self) -> str:
        return "flavor"
    def get_id(self) -> int:
        return self.flavor_id
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    async def get_parent_obj(self) -> PacBusObj:
        return await self.get_pac_id_rel_bus_obj()
