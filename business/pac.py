import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from services.db_config import db_dialect,generate_uuid

from managers import PacManager
from models import Pac
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.tri_state_filter import TriStateFilterBusObj

from business.tac import TacBusObj

from business.role import RoleBusObj

from business.land import LandBusObj

from business.flavor import FlavorBusObj

from business.error_log import ErrorLogBusObj

from business.date_greater_than_filter import DateGreaterThanFilterBusObj

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
class PacBusObj(BaseBusObj):
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
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.pac.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.pac.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self

    #Description
    @property
    def description(self):
        return self.pac.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.pac.description = value
    def set_prop_description(self, value):
        self.description = value
        return self
    #DisplayOrder
    @property
    def display_order(self):
        return self.pac.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.pac.display_order = value
    def set_prop_display_order(self, value):
        self.display_order = value
        return self
    #IsActive
    @property
    def is_active(self):
        return self.pac.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.pac.is_active = value
    def set_prop_is_active(self, value: bool):
        self.is_active = value
        return self
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.pac.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.pac.lookup_enum_name = value
    def set_prop_lookup_enum_name(self, value):
        self.lookup_enum_name = value
        return self
    #Name
    @property
    def name(self):
        return self.pac.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.pac.name = value
    def set_prop_name(self, value):
        self.name = value
        return self

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

    @property
    def lookup_enum(self) -> managers_and_enums.PacEnum:
        return managers_and_enums.PacEnum[self.pac.lookup_enum_name]
    async def load(self, json_data:str=None,
                   code:uuid.UUID=None,
                   pac_id:int=None,
                   pac_obj_instance:Pac=None,
                   pac_dict:dict=None,
                   pac_enum:managers_and_enums.PacEnum=None):
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
        if pac_enum and self.pac.pac_id is None:
            pac_manager = PacManager(self.session)
            self.pac = await pac_manager.from_enum(pac_enum)

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
        if self.pac.pac_id is not None and self.pac.pac_id > 0:
            pac_manager = PacManager(self.session)
            self.pac = await pac_manager.update(self.pac)
        if self.pac.pac_id is None or self.pac.pac_id == 0:
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

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,

    def get_obj(self) -> Pac:
        return self.pac
    def get_object_name(self) -> str:
        return "pac"
    def get_id(self) -> int:
        return self.pac_id
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,

    async def build_tri_state_filter(self) -> TriStateFilterBusObj:
        item = TriStateFilterBusObj(self.session)

        item.pac_id = self.pac_id
        item.tri_state_filter.pac_code_peek = self.code

        return item

    async def get_all_tri_state_filter(self) -> List[TriStateFilterBusObj]:
        results = list()
        tri_state_filter_manager = managers_and_enums.TriStateFilterManager(self.session)
        obj_list = await tri_state_filter_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = TriStateFilterBusObj(self.session)
            await bus_obj_item.load(tri_state_filter_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_tac(self) -> TacBusObj:
        item = TacBusObj(self.session)

        item.pac_id = self.pac_id
        item.tac.pac_code_peek = self.code

        return item

    async def get_all_tac(self) -> List[TacBusObj]:
        results = list()
        tac_manager = managers_and_enums.TacManager(self.session)
        obj_list = await tac_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = TacBusObj(self.session)
            await bus_obj_item.load(tac_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_role(self) -> RoleBusObj:
        item = RoleBusObj(self.session)

        item.pac_id = self.pac_id
        item.role.pac_code_peek = self.code

        return item

    async def get_all_role(self) -> List[RoleBusObj]:
        results = list()
        role_manager = managers_and_enums.RoleManager(self.session)
        obj_list = await role_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = RoleBusObj(self.session)
            await bus_obj_item.load(role_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_land(self) -> LandBusObj:
        item = LandBusObj(self.session)

        item.pac_id = self.pac_id
        item.land.pac_code_peek = self.code

        return item

    async def get_all_land(self) -> List[LandBusObj]:
        results = list()
        land_manager = managers_and_enums.LandManager(self.session)
        obj_list = await land_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = LandBusObj(self.session)
            await bus_obj_item.load(land_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_flavor(self) -> FlavorBusObj:
        item = FlavorBusObj(self.session)

        item.pac_id = self.pac_id
        item.flavor.pac_code_peek = self.code

        return item

    async def get_all_flavor(self) -> List[FlavorBusObj]:
        results = list()
        flavor_manager = managers_and_enums.FlavorManager(self.session)
        obj_list = await flavor_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = FlavorBusObj(self.session)
            await bus_obj_item.load(flavor_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_error_log(self) -> ErrorLogBusObj:
        item = ErrorLogBusObj(self.session)

        item.pac_id = self.pac_id
        item.error_log.pac_code_peek = self.code

        return item

    async def get_all_error_log(self) -> List[ErrorLogBusObj]:
        results = list()
        error_log_manager = managers_and_enums.ErrorLogManager(self.session)
        obj_list = await error_log_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = ErrorLogBusObj(self.session)
            await bus_obj_item.load(error_log_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_date_greater_than_filter(self) -> DateGreaterThanFilterBusObj:
        item = DateGreaterThanFilterBusObj(self.session)

        item.pac_id = self.pac_id
        item.date_greater_than_filter.pac_code_peek = self.code

        return item

    async def get_all_date_greater_than_filter(self) -> List[DateGreaterThanFilterBusObj]:
        results = list()
        date_greater_than_filter_manager = managers_and_enums.DateGreaterThanFilterManager(self.session)
        obj_list = await date_greater_than_filter_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = DateGreaterThanFilterBusObj(self.session)
            await bus_obj_item.load(date_greater_than_filter_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

