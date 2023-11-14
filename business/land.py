import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from business.pac import PacBusObj #PacID
from services.db_config import db_dialect,generate_uuid
# from managers import PacManager as PacIDManager #PacID
from managers import LandManager
from models import Land
import managers as managers_and_enums

class LandSessionNotFoundError(Exception):
    pass
class LandInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class LandBusObj:
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise LandSessionNotFoundError("session required")
        self.session = session
        self.land = Land()
    @property
    def land_id(self):
        return self.land.land_id
    @land_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("land_id must be a int.")
        self.land.land_id = value
    #code
    @property
    def code(self):
        return self.land.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.land.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.land.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.land.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.land.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.land.insert_user_id = value
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.land.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.land.last_update_user_id = value

    #Description
    @property
    def description(self):
        return self.land.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.land.description = value
    #DisplayOrder
    @property
    def display_order(self):
        return self.land.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.land.display_order = value
    #IsActive
    @property
    def is_active(self):
        return self.land.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.land.is_active = value
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.land.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.land.lookup_enum_name = value
    #Name
    @property
    def name(self):
        return self.land.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.land.name = value
    #PacID

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    @property
    def pac_id(self):
        return self.land.pac_id
    @pac_id.setter
    def pac_id(self, value):
        assert isinstance(value, int) or value is None, "pac_id must be an integer or None"
        self.land.pac_id = value
    @property
    def pac_code_peek(self):
        return self.land.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "pac_code_peek must be a UUID"
    #     self.land.pac_code_peek = value

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.land.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.land.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.land.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.land.last_update_utc_date_time = value

    @property
    def lookup_enum(self) -> managers_and_enums.LandEnum:
        return managers_and_enums.LandEnum[self.land.lookup_enum_name]
    async def load(self, json_data:str=None,
                   code:uuid.UUID=None,
                   land_id:int=None,
                   land_obj_instance:Land=None,
                   land_dict:dict=None,
                   land_enum:managers_and_enums.LandEnum=None):
        if land_id and self.land.land_id is None:
            land_manager = LandManager(self.session)
            land_obj = await land_manager.get_by_id(land_id)
            self.land = land_obj
        if code and self.land.land_id is None:
            land_manager = LandManager(self.session)
            land_obj = await land_manager.get_by_code(code)
            self.land = land_obj
        if land_obj_instance and self.land.land_id is None:
            land_manager = LandManager(self.session)
            land_obj = await land_manager.get_by_id(land_obj_instance.land_id)
            self.land = land_obj
        if json_data and self.land.land_id is None:
            land_manager = LandManager(self.session)
            self.land = land_manager.from_json(json_data)
        if land_dict and self.land.land_id is None:
            land_manager = LandManager(self.session)
            self.land = land_manager.from_dict(land_dict)
        if land_enum and self.land.land_id is None:
            land_manager = LandManager(self.session)
            self.land = await land_manager.from_enum(land_enum)

    async def refresh(self):
        land_manager = LandManager(self.session)
        self.land = await land_manager.refresh(self.land)
    def to_dict(self):
        land_manager = LandManager(self.session)
        return land_manager.to_dict(self.land)
    def to_json(self):
        land_manager = LandManager(self.session)
        return land_manager.to_json(self.land)
    async def save(self):
        if self.land.land_id > 0:
            land_manager = LandManager(self.session)
            self.land = await land_manager.update(self.land)
        if self.land.land_id == 0:
            land_manager = LandManager(self.session)
            self.land = await land_manager.add(self.land)
    async def delete(self):
        if self.land.land_id > 0:
            land_manager = LandManager(self.session)
            self.land = await land_manager.delete(self.land.land_id)
    def get_land_obj(self) -> Land:
        return self.land
    def is_equal(self,land:Land) -> Land:
        land_manager = LandManager(self.session)
        my_land = self.get_land_obj()
        return land_manager.is_equal(land, my_land)

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    async def get_pac_id_rel_bus_obj(self) -> PacBusObj:
        pac_bus_obj = PacBusObj(self.session)
        await pac_bus_obj.load(pac_id=self.land.pac_id)
        return pac_bus_obj

    def get_obj(self) -> Land:
        return self.land
    def get_object_name(self) -> str:
        return "land"
    def get_id(self) -> int:
        return self.land_id
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    async def get_parent_obj(self) -> PacBusObj:
        return await self.get_pac_id_rel_bus_obj()

