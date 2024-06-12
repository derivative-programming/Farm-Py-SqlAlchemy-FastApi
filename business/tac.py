# business/tac.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
from services.db_config import DB_DIALECT, generate_uuid
from managers import TacManager
from models import Tac
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.organization import OrganizationBusObj

from business.customer import CustomerBusObj

class TacInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TacBusObj(BaseBusObj):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.tac = Tac()
    @property
    def tac_id(self):
        return self.tac.tac_id
    @tac_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("tac_id must be a int.")
        self.tac.tac_id = value
    # code
    @property
    def code(self):
        return self.tac.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.tac.code = value
    # last_change_code
    @property
    def last_change_code(self):
        return self.tac.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.tac.last_change_code = value
    # insert_user_id
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
    # last_update_user_id
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
# endset
    # description
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
    # displayOrder
    @property
    def display_order(self):
        return self.tac.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.tac.display_order = value
    def set_prop_display_order(self, value):
        self.display_order = value
        return self
    # isActive
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
    # lookupEnumName
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
    # name
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
        return self.tac.pac_id
    @pac_id.setter
    def pac_id(self, value):
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.tac.pac_id = value
    def set_prop_pac_id(self, value):
        self.pac_id = value
        return self
    @property
    def pac_code_peek(self):
        return self.tac.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, UUIDType),
    #           "pac_code_peek must be a UUID"
    #     self.tac.pac_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.tac.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.tac.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.tac.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.tac.last_update_utc_date_time = value

    @property
    def lookup_enum(self) -> managers_and_enums.TacEnum:
        return managers_and_enums.TacEnum[self.tac.lookup_enum_name]
    async def load(
        self,
        json_data: str = None,
        code: uuid.UUID = None,
        tac_id: int = None,
        tac_obj_instance:
            Tac = None,
        tac_dict: dict = None,
        tac_enum:
            managers_and_enums.TacEnum = None
    ):
        if tac_id and self.tac.tac_id is None:
            tac_manager = TacManager(self._session_context)
            tac_obj = await tac_manager.get_by_id(tac_id)
            self.tac = tac_obj
        if code and self.tac.tac_id is None:
            tac_manager = TacManager(self._session_context)
            tac_obj = await tac_manager.get_by_code(code)
            self.tac = tac_obj
        if tac_obj_instance and self.tac.tac_id is None:
            tac_manager = TacManager(self._session_context)
            tac_obj = await tac_manager.get_by_id(tac_obj_instance.tac_id)
            self.tac = tac_obj
        if json_data and self.tac.tac_id is None:
            tac_manager = TacManager(self._session_context)
            self.tac = tac_manager.from_json(json_data)
        if tac_dict and self.tac.tac_id is None:
            tac_manager = TacManager(self._session_context)
            self.tac = tac_manager.from_dict(tac_dict)
        if tac_enum and self.tac.tac_id is None:
            tac_manager = TacManager(self._session_context)
            self.tac = await tac_manager.from_enum(tac_enum)
    @staticmethod
    async def get(
        session_context: SessionContext,
        json_data: str = None,
        code: uuid.UUID = None,
        tac_id: int = None,
        tac_obj_instance:
            Tac = None,
        tac_dict: dict = None,
        tac_enum:
            managers_and_enums.TacEnum = None
    ):
        result = TacBusObj(session_context)
        await result.load(
            json_data,
            code,
            tac_id,
            tac_obj_instance,
            tac_dict,
            tac_enum
        )
        return result

    async def refresh(self):
        tac_manager = TacManager(self._session_context)
        self.tac = await tac_manager.refresh(self.tac)
        return self
    def is_valid(self):
        return (self.tac is not None)
    def to_dict(self):
        tac_manager = TacManager(self._session_context)
        return tac_manager.to_dict(self.tac)
    def to_json(self):
        tac_manager = TacManager(self._session_context)
        return tac_manager.to_json(self.tac)
    async def save(self):
        if self.tac.tac_id is not None and self.tac.tac_id > 0:
            tac_manager = TacManager(self._session_context)
            self.tac = await tac_manager.update(self.tac)
        if self.tac.tac_id is None or self.tac.tac_id == 0:
            tac_manager = TacManager(self._session_context)
            self.tac = await tac_manager.add(self.tac)
        return self
    async def delete(self):
        if self.tac.tac_id > 0:
            tac_manager = TacManager(self._session_context)
            await tac_manager.delete(self.tac.tac_id)
            self.tac = None
    async def randomize_properties(self):
        self.tac.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tac.display_order = random.randint(0, 100)
        self.tac.is_active = random.choice([True, False])
        self.tac.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tac.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.tac.pac_id = random.randint(0, 100)
# endset
        return self
    def get_tac_obj(self) -> Tac:
        return self.tac
    def is_equal(self, tac: Tac) -> Tac:
        tac_manager = TacManager(self._session_context)
        my_tac = self.get_tac_obj()
        return tac_manager.is_equal(tac, my_tac)
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj
# endset
    def get_obj(self) -> Tac:
        return self.tac
    def get_object_name(self) -> str:
        return "tac"
    def get_id(self) -> int:
        return self.tac_id
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_parent_name(self) -> str:
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        return self.pac_code_peek
    async def get_parent_obj(self) -> models.Pac:
        return self.get_pac_id_rel_obj()
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Tac]
    ):
        result = list()
        for tac in obj_list:
            tac_bus_obj = TacBusObj.get(
                session_context,
                tac_obj_instance=tac
            )
            result.append(tac_bus_obj)
        return result

    async def build_organization(self) -> OrganizationBusObj:
        item = OrganizationBusObj(self._session_context)

        item.tac_id = self.tac_id
        item.organization.tac_code_peek = self.code

        return item

    async def get_all_organization(self) -> List[OrganizationBusObj]:
        results = list()
        organization_manager = managers_and_enums.OrganizationManager(self._session_context)
        obj_list = await organization_manager.get_by_tac_id(self.tac_id)
        for obj_item in obj_list:
            bus_obj_item = OrganizationBusObj(self._session_context)
            await bus_obj_item.load(organization_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_customer(self) -> CustomerBusObj:
        item = CustomerBusObj(self._session_context)

        item.tac_id = self.tac_id
        item.customer.tac_code_peek = self.code

        return item

    async def get_all_customer(self) -> List[CustomerBusObj]:
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_tac_id(self.tac_id)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load(customer_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results
    async def get_customer_by_email_prop(self, email) -> List[CustomerBusObj]:
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_email_prop(email)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load(customer_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results
    async def get_customer_by_fs_user_code_value_prop(self, fs_user_code_value) -> List[CustomerBusObj]:
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_fs_user_code_value_prop(fs_user_code_value)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load(customer_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

