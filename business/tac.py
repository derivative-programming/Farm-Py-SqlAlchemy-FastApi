import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
# from business.pac import PacBusObj #PacID
from services.db_config import db_dialect,generate_uuid
# from managers import PacManager as PacIDManager #PacID
from managers import TacManager
from models import Tac
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.organization import OrganizationBusObj

from business.customer import CustomerBusObj

class TacSessionNotFoundError(Exception):
    pass
class TacInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TacBusObj(BaseBusObj):
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise TacSessionNotFoundError("session required")
        self.session = session
        self.tac = Tac()
    @property
    def tac_id(self):
        return self.tac.tac_id
    @tac_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("tac_id must be a int.")
        self.tac.tac_id = value
    #code
    @property
    def code(self):
        return self.tac.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.tac.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.tac.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.tac.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.tac.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.tac.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.tac.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.tac.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self

    #Description
    @property
    def description(self):
        return self.tac.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.tac.description = value
    def set_prop_description(self, value):
        self.description = value
        return self
    #DisplayOrder
    @property
    def display_order(self):
        return self.tac.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.tac.display_order = value
    def set_prop_display_order(self, value):
        self.display_order = value
        return self
    #IsActive
    @property
    def is_active(self):
        return self.tac.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.tac.is_active = value
    def set_prop_is_active(self, value: bool):
        self.is_active = value
        return self
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.tac.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.tac.lookup_enum_name = value
    def set_prop_lookup_enum_name(self, value):
        self.lookup_enum_name = value
        return self
    #Name
    @property
    def name(self):
        return self.tac.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.tac.name = value
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
        return self.tac.pac_id
    @pac_id.setter
    def pac_id(self, value):
        assert isinstance(value, int) or value is None, "pac_id must be an integer or None"
        self.tac.pac_id = value
    def set_prop_pac_id(self, value):
        self.pac_id = value
        return self
    @property
    def pac_code_peek(self):
        return self.tac.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "pac_code_peek must be a UUID"
    #     self.tac.pac_code_peek = value

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.tac.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.tac.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.tac.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.tac.last_update_utc_date_time = value

    @property
    def lookup_enum(self) -> managers_and_enums.TacEnum:
        return managers_and_enums.TacEnum[self.tac.lookup_enum_name]
    async def load(self, json_data:str=None,
                   code:uuid.UUID=None,
                   tac_id:int=None,
                   tac_obj_instance:Tac=None,
                   tac_dict:dict=None,
                   tac_enum:managers_and_enums.TacEnum=None):
        if tac_id and self.tac.tac_id is None:
            tac_manager = TacManager(self.session)
            tac_obj = await tac_manager.get_by_id(tac_id)
            self.tac = tac_obj
        if code and self.tac.tac_id is None:
            tac_manager = TacManager(self.session)
            tac_obj = await tac_manager.get_by_code(code)
            self.tac = tac_obj
        if tac_obj_instance and self.tac.tac_id is None:
            tac_manager = TacManager(self.session)
            tac_obj = await tac_manager.get_by_id(tac_obj_instance.tac_id)
            self.tac = tac_obj
        if json_data and self.tac.tac_id is None:
            tac_manager = TacManager(self.session)
            self.tac = tac_manager.from_json(json_data)
        if tac_dict and self.tac.tac_id is None:
            tac_manager = TacManager(self.session)
            self.tac = tac_manager.from_dict(tac_dict)
        if tac_enum and self.tac.tac_id is None:
            tac_manager = TacManager(self.session)
            self.tac = await tac_manager.from_enum(tac_enum)

    async def refresh(self):
        tac_manager = TacManager(self.session)
        self.tac = await tac_manager.refresh(self.tac)
    def to_dict(self):
        tac_manager = TacManager(self.session)
        return tac_manager.to_dict(self.tac)
    def to_json(self):
        tac_manager = TacManager(self.session)
        return tac_manager.to_json(self.tac)
    async def save(self):
        if self.tac.tac_id > 0:
            tac_manager = TacManager(self.session)
            self.tac = await tac_manager.update(self.tac)
        if self.tac.tac_id == 0:
            tac_manager = TacManager(self.session)
            self.tac = await tac_manager.add(self.tac)
    async def delete(self):
        if self.tac.tac_id > 0:
            tac_manager = TacManager(self.session)
            self.tac = await tac_manager.delete(self.tac.tac_id)
    def get_tac_obj(self) -> Tac:
        return self.tac
    def is_equal(self,tac:Tac) -> Tac:
        tac_manager = TacManager(self.session)
        my_tac = self.get_tac_obj()
        return tac_manager.is_equal(tac, my_tac)

    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        pac_manager = managers_and_enums.PacManager(self.session)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj

    def get_obj(self) -> Tac:
        return self.tac
    def get_object_name(self) -> str:
        return "tac"
    def get_id(self) -> int:
        return self.tac_id
    #description,
    #displayOrder,
    #isActive,
    #lookupEnumName,
    #name,
    #PacID
    # async def get_parent_obj(self) -> PacBusObj:
    #     return await self.get_pac_id_rel_bus_obj()
    async def get_parent_name(self) -> str:
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        return self.pac_code_peek

    async def build_organization(self) -> OrganizationBusObj:
        item = OrganizationBusObj(self.session)

        item.tac_id = self.tac_id
        item.tac_code_peek = self.code

        return item

    async def get_all_organization(self) -> List[OrganizationBusObj]:
        results = list()
        organization_manager = managers_and_enums.OrganizationManager(self.session)
        obj_list = organization_manager.get_by_tac_id(self.tac_id)
        for obj_item in obj_list:
            bus_obj_item = await OrganizationBusObj(self.session).load(organization_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_customer(self) -> CustomerBusObj:
        item = CustomerBusObj(self.session)

        item.tac_id = self.tac_id
        item.tac_code_peek = self.code

        return item

    async def get_all_customer(self) -> List[CustomerBusObj]:
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self.session)
        obj_list = customer_manager.get_by_tac_id(self.tac_id)
        for obj_item in obj_list:
            bus_obj_item = await CustomerBusObj(self.session).load(customer_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

