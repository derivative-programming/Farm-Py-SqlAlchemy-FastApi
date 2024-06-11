# business/date_greater_than_filter.py

"""
    #TODO add comment
"""

import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
# from business.pac import PacBusObj  # PacID
from services.db_config import db_dialect,generate_uuid
from managers import PacManager as PacIDManager  # PacID
from managers import DateGreaterThanFilterManager
import managers as managers_and_enums
from models import DateGreaterThanFilter
import models
class DateGreaterThanFilterSessionNotFoundError(Exception):
    pass
class DateGreaterThanFilterInvalidInitError(Exception):
    pass
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class DateGreaterThanFilterBusObj:
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise DateGreaterThanFilterSessionNotFoundError(f"session required")
        self._session_context = session_context
        self.date_greater_than_filter = DateGreaterThanFilter()
    @property
    def date_greater_than_filter_id(self):
        return self.date_greater_than_filter.date_greater_than_filter_id
    @date_greater_than_filter_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("date_greater_than_filter_id must be a int.")
        self.date_greater_than_filter.date_greater_than_filter_id = value
    #code
    @property
    def code(self):
        return self.date_greater_than_filter.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.date_greater_than_filter.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.date_greater_than_filter.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.date_greater_than_filter.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.date_greater_than_filter.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.date_greater_than_filter.insert_user_id = value
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.date_greater_than_filter.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.date_greater_than_filter.last_update_user_id = value

    #DayCount
    @property
    def day_count(self):
        return self.date_greater_than_filter.day_count
    @day_count.setter
    def day_count(self, value):
        assert isinstance(value, int), "day_count must be an integer"
        self.date_greater_than_filter.day_count = value
    #Description
    @property
    def description(self):
        return self.date_greater_than_filter.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.date_greater_than_filter.description = value
    #DisplayOrder
    @property
    def display_order(self):
        return self.date_greater_than_filter.display_order
    @display_order.setter
    def display_order(self, value):
        assert isinstance(value, int), "display_order must be an integer"
        self.date_greater_than_filter.display_order = value
    # isActive
    @property
    def is_active(self):
        return self.date_greater_than_filter.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.date_greater_than_filter.is_active = value
    #LookupEnumName
    @property
    def lookup_enum_name(self):
        return self.date_greater_than_filter.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.date_greater_than_filter.lookup_enum_name = value
    #Name
    @property
    def name(self):
        return self.date_greater_than_filter.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.date_greater_than_filter.name = value
     # PacID

    #dayCount,
    #description,
    #displayOrder,
    # isActive,
    #lookupEnumName,
    #name,
     # PacID
    @property
    def pac_id(self):
        return self.date_greater_than_filter.pac_id
    @pac_id.setter
    def pac_id(self, value):
        assert isinstance(value, int) or value is None, "pac_id must be an integer or None"
        self.date_greater_than_filter.pac_id = value
    @property
    def pac_code_peek(self):
        return self.date_greater_than_filter.pac_code_peek
    @pac_code_peek.setter
    def pac_code_peek(self, value):
        assert isinstance(value, UUIDType), "pac_code_peek must be a UUID"
        self.date_greater_than_filter.pac_code_peek = value

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.date_greater_than_filter.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.date_greater_than_filter.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.date_greater_than_filter.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.date_greater_than_filter.last_update_utc_date_time = value

##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=true]Start

    @property
    def lookup_enum(self) -> managers_and_enums.DateGreaterThanFilterEnum:
        return managers_and_enums.DateGreaterThanFilterEnum[self.date_greater_than_filter.lookup_enum_name]

    async def load(self, json_data: str = None,
                   code: uuid.UUID = None,
                   date_greater_than_filter_id: int = None,
                   date_greater_than_filter_obj_instance: DateGreaterThanFilter = None,
                   date_greater_than_filter_dict: dict = None,
                   date_greater_than_filter_enum:managers_and_enums.DateGreaterThanFilterEnum = None):
        if date_greater_than_filter_id and self.date_greater_than_filter.date_greater_than_filter_id is None:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            date_greater_than_filter_obj = await date_greater_than_filter_manager.get_by_id(date_greater_than_filter_id)
            self.date_greater_than_filter = date_greater_than_filter_obj
        if code and self.date_greater_than_filter.date_greater_than_filter_id is None:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            date_greater_than_filter_obj = await date_greater_than_filter_manager.get_by_code(code)
            self.date_greater_than_filter = date_greater_than_filter_obj
        if date_greater_than_filter_obj_instance and self.date_greater_than_filter.date_greater_than_filter_id is None:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            date_greater_than_filter_obj = await date_greater_than_filter_manager.get_by_id(date_greater_than_filter_obj_instance.date_greater_than_filter_id)
            self.date_greater_than_filter = date_greater_than_filter_obj
        if json_data and self.date_greater_than_filter.date_greater_than_filter_id is None:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            self.date_greater_than_filter = date_greater_than_filter_manager.from_json(json_data)
        if date_greater_than_filter_dict and self.date_greater_than_filter.date_greater_than_filter_id is None:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            self.date_greater_than_filter = date_greater_than_filter_manager.from_dict(date_greater_than_filter_dict)
        if date_greater_than_filter_enum and self.date_greater_than_filter.date_greater_than_filter_id is None:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            self.date_greater_than_filter = await date_greater_than_filter_manager.from_enum(date_greater_than_filter_enum)

    @staticmethod
    async def get(session_context: SessionContext,
                    json_data: str = None,
                   code: uuid.UUID = None,
                   date_greater_than_filter_id: int = None,
                   date_greater_than_filter_obj_instance: DateGreaterThanFilter = None,
                   date_greater_than_filter_dict: dict = None,
                   date_greater_than_filter_enum:managers_and_enums.DateGreaterThanFilterEnum = None):
        result = DateGreaterThanFilterBusObj(session_context)

        await result.load(
            json_data,
            code,
            date_greater_than_filter_id,
            date_greater_than_filter_obj_instance,
            date_greater_than_filter_dict,
            date_greater_than_filter_enum
        )

        return result
##GENLearn[isLookup=true]End
##GENTrainingBlock[caseLookupEnums]End
    def is_valid(self):
        return (self.date_greater_than_filter is not None)
    async def refresh(self):
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        self.date_greater_than_filter = await date_greater_than_filter_manager.refresh(self.date_greater_than_filter)
    def to_dict(self):
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        return date_greater_than_filter_manager.to_dict(self.date_greater_than_filter)
    def to_json(self):
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        return date_greater_than_filter_manager.to_json(self.date_greater_than_filter)
    async def save(self):
        if self.date_greater_than_filter.date_greater_than_filter_id is not None and self.date_greater_than_filter.date_greater_than_filter_id > 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            self.date_greater_than_filter = await date_greater_than_filter_manager.update(self.date_greater_than_filter)
        if self.date_greater_than_filter.date_greater_than_filter_id is None or self.date_greater_than_filter.date_greater_than_filter_id == 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            self.date_greater_than_filter = await date_greater_than_filter_manager.add(self.date_greater_than_filter)
    async def delete(self):
        if self.date_greater_than_filter.date_greater_than_filter_id > 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            self.date_greater_than_filter = await date_greater_than_filter_manager.delete(self.date_greater_than_filter.date_greater_than_filter_id)
    def get_date_greater_than_filter_obj(self) -> DateGreaterThanFilter:
        return self.date_greater_than_filter
    def is_equal(self, date_greater_than_filter: DateGreaterThanFilter) -> DateGreaterThanFilter:
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        my_date_greater_than_filter = self.get_date_greater_than_filter_obj()
        return date_greater_than_filter_manager.is_equal(date_greater_than_filter, my_date_greater_than_filter)

    #dayCount,
    #description,
    #displayOrder,
    # isActive,
    #lookupEnumName,
    #name,
     # PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj

    def get_obj(self) -> DateGreaterThanFilter:
        return self.date_greater_than_filter
    def get_object_name(self) -> str:
        return "date_greater_than_filter"
    def get_id(self) -> int:
        return self.date_greater_than_filter_id
    #dayCount,
    #description,
    #displayOrder,
    # isActive,
    #lookupEnumName,
    #name,
     # PacID
    # async def get_parent_obj(self) -> PacBusObj:
    #     return await self.get_pac_id_rel_bus_obj()
    async def get_parent_name(self) -> str:
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        return self.pac_code_peek
