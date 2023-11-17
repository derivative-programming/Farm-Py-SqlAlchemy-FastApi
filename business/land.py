import random
import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
from services.db_config import db_dialect,generate_uuid
from managers import LandManager
from models import Land
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.plant import PlantBusObj

class LandInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class LandBusObj(BaseBusObj):
    def __init__(self, session_context:SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
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
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.land.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.land.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self

    #Description
    @property
    def description(self):
        return self.land.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.land.description = value
    def set_prop_description(self, value):
        self.description = value
        return self
    #DisplayOrder
    @property
    def display_order(self):
        return self.land.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.land.display_order = value
    def set_prop_display_order(self, value):
        self.display_order = value
        return self
    #IsActive
    @property
    def is_active(self):
        return self.land.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.land.is_active = value
    def set_prop_is_active(self, value: bool):
        self.is_active = value
        return self
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.land.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.land.lookup_enum_name = value
    def set_prop_lookup_enum_name(self, value):
        self.lookup_enum_name = value
        return self
    #Name
    @property
    def name(self):
        return self.land.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.land.name = value
    def set_prop_name(self, value):
        self.name = value
        return self
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
    def set_prop_pac_id(self, value):
        self.pac_id = value
        return self
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
            land_manager = LandManager(self._session_context)
            land_obj = await land_manager.get_by_id(land_id)
            self.land = land_obj
        if code and self.land.land_id is None:
            land_manager = LandManager(self._session_context)
            land_obj = await land_manager.get_by_code(code)
            self.land = land_obj
        if land_obj_instance and self.land.land_id is None:
            land_manager = LandManager(self._session_context)
            land_obj = await land_manager.get_by_id(land_obj_instance.land_id)
            self.land = land_obj
        if json_data and self.land.land_id is None:
            land_manager = LandManager(self._session_context)
            self.land = land_manager.from_json(json_data)
        if land_dict and self.land.land_id is None:
            land_manager = LandManager(self._session_context)
            self.land = land_manager.from_dict(land_dict)
        if land_enum and self.land.land_id is None:
            land_manager = LandManager(self._session_context)
            self.land = await land_manager.from_enum(land_enum)
    @staticmethod
    async def get(session_context:SessionContext,
                    json_data:str=None,
                   code:uuid.UUID=None,
                   land_id:int=None,
                   land_obj_instance:Land=None,
                   land_dict:dict=None,
                   land_enum:managers_and_enums.LandEnum=None):
        result = LandBusObj(session_context)
        await result.load(
            json_data,
            code,
            land_id,
            land_obj_instance,
            land_dict,
            land_enum
        )
        return result

    async def refresh(self):
        land_manager = LandManager(self._session_context)
        self.land = await land_manager.refresh(self.land)
        return self
    def is_valid(self):
        return (self.land is not None)
    def to_dict(self):
        land_manager = LandManager(self._session_context)
        return land_manager.to_dict(self.land)
    def to_json(self):
        land_manager = LandManager(self._session_context)
        return land_manager.to_json(self.land)
    async def save(self):
        if self.land.land_id is not None and self.land.land_id > 0:
            land_manager = LandManager(self._session_context)
            self.land = await land_manager.update(self.land)
        if self.land.land_id is None or self.land.land_id == 0:
            land_manager = LandManager(self._session_context)
            self.land = await land_manager.add(self.land)
        return self
    async def delete(self):
        if self.land.land_id > 0:
            land_manager = LandManager(self._session_context)
            await land_manager.delete(self.land.land_id)
            self.land = None
    async def randomize_properties(self):
        self.land.description = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.land.display_order = random.randint(0, 100)
        self.land.is_active = random.choice([True, False])
        self.land.lookup_enum_name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.land.name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.land.pac_id = random.randint(0, 100)

        return self
    def get_land_obj(self) -> Land:
        return self.land
    def is_equal(self,land:Land) -> Land:
        land_manager = LandManager(self._session_context)
        my_land = self.get_land_obj()
        return land_manager.is_equal(land, my_land)

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj

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
    async def get_parent_name(self) -> str:
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        return self.pac_code_peek
    async def get_parent_obj(self) -> models.Pac:
        return self.get_pac_id_rel_obj()

    @staticmethod
    async def to_bus_obj_list(session_context:SessionContext, obj_list:List[Land]):
        result = list()
        for land in obj_list:
            land_bus_obj = LandBusObj.get(session_context,land_obj_instance=land)
            result.append(land_bus_obj)
        return result

    async def build_plant(self) -> PlantBusObj:
        item = PlantBusObj(self._session_context)
        flavor_manager = managers_and_enums.FlavorManager(self._session_context)
        flvr_foreign_key_id_flavor = await flavor_manager.from_enum(
            managers_and_enums.FlavorEnum.Unknown)
        item.flvr_foreign_key_id = flvr_foreign_key_id_flavor.flavor_id
        item.plant.flvr_foreign_key_id_code_peek = flvr_foreign_key_id_flavor.code

        item.land_id = self.land_id
        item.plant.land_code_peek = self.code

        return item

    async def get_all_plant(self) -> List[PlantBusObj]:
        results = list()
        plant_manager = managers_and_enums.PlantManager(self._session_context)
        obj_list = await plant_manager.get_by_land_id(self.land_id)
        for obj_item in obj_list:
            bus_obj_item = PlantBusObj(self._session_context)
            await bus_obj_item.load(plant_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

