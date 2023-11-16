import random
import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
from services.db_config import db_dialect,generate_uuid
from managers import ErrorLogManager
from models import ErrorLog
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

class ErrorLogInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class ErrorLogBusObj(BaseBusObj):
    def __init__(self, session_context:SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.error_log = ErrorLog()
    @property
    def error_log_id(self):
        return self.error_log.error_log_id
    @error_log_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("error_log_id must be a int.")
        self.error_log.error_log_id = value
    #code
    @property
    def code(self):
        return self.error_log.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.error_log.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.error_log.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.error_log.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.error_log.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.error_log.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.error_log.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.error_log.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self

    #BrowserCode
    @property
    def browser_code(self):
        return self.error_log.browser_code
    @browser_code.setter
    def browser_code(self, value):
        assert isinstance(value, UUIDType), "browser_code must be a UUID"
        self.error_log.browser_code = value
    def set_prop_browser_code(self, value):
        self.browser_code = value
        return self
    #ContextCode
    @property
    def context_code(self):
        return self.error_log.context_code
    @context_code.setter
    def context_code(self, value):
        assert isinstance(value, UUIDType), "context_code must be a UUID"
        self.error_log.context_code = value
    def set_prop_context_code(self, value):
        self.context_code = value
        return self
    #CreatedUTCDateTime
    @property
    def created_utc_date_time(self):
        return self.error_log.created_utc_date_time
    @created_utc_date_time.setter
    def created_utc_date_time(self, value):
        assert isinstance(value, datetime), "created_utc_date_time must be a datetime object"
        self.error_log.created_utc_date_time = value
    def set_prop_created_utc_date_time(self, value):
        self.created_utc_date_time = value
        return self
    #Description
    @property
    def description(self):
        return self.error_log.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.error_log.description = value
    def set_prop_description(self, value):
        self.description = value
        return self
    #IsClientSideError
    @property
    def is_client_side_error(self):
        return self.error_log.is_client_side_error
    @is_client_side_error.setter
    def is_client_side_error(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_client_side_error must be a boolean.")
        self.error_log.is_client_side_error = value
    def set_prop_is_client_side_error(self, value: bool):
        self.is_client_side_error = value
        return self
    #IsResolved
    @property
    def is_resolved(self):
        return self.error_log.is_resolved
    @is_resolved.setter
    def is_resolved(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_resolved must be a boolean.")
        self.error_log.is_resolved = value
    def set_prop_is_resolved(self, value: bool):
        self.is_resolved = value
        return self
    #PacID
    #Url
    @property
    def url(self):
        return self.error_log.url
    @url.setter
    def url(self, value):
        assert isinstance(value, str), "url must be a string"
        self.error_log.url = value
    def set_prop_url(self, value):
        self.url = value
        return self

    #browserCode,
    #contextCode,
    #createdUTCDateTime
    #description,
    #isClientSideError,
    #isResolved,
    #PacID
    @property
    def pac_id(self):
        return self.error_log.pac_id
    @pac_id.setter
    def pac_id(self, value):
        assert isinstance(value, int) or value is None, "pac_id must be an integer or None"
        self.error_log.pac_id = value
    def set_prop_pac_id(self, value):
        self.pac_id = value
        return self
    @property
    def pac_code_peek(self):
        return self.error_log.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "pac_code_peek must be a UUID"
    #     self.error_log.pac_code_peek = value
    #url,

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.error_log.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.error_log.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.error_log.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.error_log.last_update_utc_date_time = value

    async def load(self, json_data:str=None,
                   code:uuid.UUID=None,
                   error_log_id:int=None,
                   error_log_obj_instance:ErrorLog=None,
                   error_log_dict:dict=None):
        if error_log_id and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self._session_context)
            error_log_obj = await error_log_manager.get_by_id(error_log_id)
            self.error_log = error_log_obj
        if code and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self._session_context)
            error_log_obj = await error_log_manager.get_by_code(code)
            self.error_log = error_log_obj
        if error_log_obj_instance and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self._session_context)
            error_log_obj = await error_log_manager.get_by_id(error_log_obj_instance.error_log_id)
            self.error_log = error_log_obj
        if json_data and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self._session_context)
            self.error_log = error_log_manager.from_json(json_data)
        if error_log_dict and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self._session_context)
            self.error_log = error_log_manager.from_dict(error_log_dict)
        return self
    @staticmethod
    async def get(session_context:SessionContext,
                    json_data:str=None,
                   code:uuid.UUID=None,
                   error_log_id:int=None,
                   error_log_obj_instance:ErrorLog=None,
                   error_log_dict:dict=None):
        result = ErrorLogBusObj(session_context)
        await result.load(
            json_data,
            code,
            error_log_id,
            error_log_obj_instance,
            error_log_dict
        )
        return result

    async def refresh(self):
        error_log_manager = ErrorLogManager(self._session_context)
        self.error_log = await error_log_manager.refresh(self.error_log)
        return self
    def is_valid(self):
        return (self.error_log is not None)
    def to_dict(self):
        error_log_manager = ErrorLogManager(self._session_context)
        return error_log_manager.to_dict(self.error_log)
    def to_json(self):
        error_log_manager = ErrorLogManager(self._session_context)
        return error_log_manager.to_json(self.error_log)
    async def save(self):
        if self.error_log.error_log_id is not None and self.error_log.error_log_id > 0:
            error_log_manager = ErrorLogManager(self._session_context)
            self.error_log = await error_log_manager.update(self.error_log)
        if self.error_log.error_log_id is None or self.error_log.error_log_id == 0:
            error_log_manager = ErrorLogManager(self._session_context)
            self.error_log = await error_log_manager.add(self.error_log)
        return self
    async def delete(self):
        if self.error_log.error_log_id > 0:
            error_log_manager = ErrorLogManager(self._session_context)
            await error_log_manager.delete(self.error_log.error_log_id)
            self.error_log = None
    async def randomize_properties(self):
        self.error_log.browser_code = generate_uuid()
        self.error_log.context_code = generate_uuid()
        self.error_log.created_utc_date_time = datetime(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
        self.error_log.description = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.error_log.is_client_side_error = random.choice([True, False])
        self.error_log.is_resolved = random.choice([True, False])
        # self.error_log.pac_id = random.randint(0, 100)
        self.error_log.url = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))

        return self
    def get_error_log_obj(self) -> ErrorLog:
        return self.error_log
    def is_equal(self,error_log:ErrorLog) -> ErrorLog:
        error_log_manager = ErrorLogManager(self._session_context)
        my_error_log = self.get_error_log_obj()
        return error_log_manager.is_equal(error_log, my_error_log)

    #browserCode,
    #contextCode,
    #createdUTCDateTime
    #description,
    #isClientSideError,
    #isResolved,
    #PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj
    #url,

    def get_obj(self) -> ErrorLog:
        return self.error_log
    def get_object_name(self) -> str:
        return "error_log"
    def get_id(self) -> int:
        return self.error_log_id
    #browserCode,
    #contextCode,
    #createdUTCDateTime
    #description,
    #isClientSideError,
    #isResolved,
    #PacID
    async def get_parent_name(self) -> str:
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        return self.pac_code_peek
    #url,

