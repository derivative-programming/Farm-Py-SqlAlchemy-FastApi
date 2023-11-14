import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from business.pac import PacBusObj #PacID
from services.db_config import db_dialect,generate_uuid
# from managers import PacManager as PacIDManager #PacID
from managers import ErrorLogManager
from models import ErrorLog
import managers as managers_and_enums

class ErrorLogSessionNotFoundError(Exception):
    pass
class ErrorLogInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class ErrorLogBusObj:
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise ErrorLogSessionNotFoundError("session required")
        self.session = session
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
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.error_log.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.error_log.last_update_user_id = value

    #BrowserCode
    @property
    def browser_code(self):
        return self.error_log.browser_code
    @browser_code.setter
    def browser_code(self, value):
        assert isinstance(value, UUIDType), "browser_code must be a UUID"
        self.error_log.browser_code = value
    #ContextCode
    @property
    def context_code(self):
        return self.error_log.context_code
    @context_code.setter
    def context_code(self, value):
        assert isinstance(value, UUIDType), "context_code must be a UUID"
        self.error_log.context_code = value
    #CreatedUTCDateTime
    @property
    def created_utc_date_time(self):
        return self.error_log.created_utc_date_time
    @created_utc_date_time.setter
    def created_utc_date_time(self, value):
        assert isinstance(value, datetime), "created_utc_date_time must be a datetime object"
        self.error_log.created_utc_date_time = value
    #Description
    @property
    def description(self):
        return self.error_log.description
    @description.setter
    def description(self, value):
        assert isinstance(value, str), "description must be a string"
        self.error_log.description = value
    #IsClientSideError
    @property
    def is_client_side_error(self):
        return self.error_log.is_client_side_error
    @is_client_side_error.setter
    def is_client_side_error(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_client_side_error must be a boolean.")
        self.error_log.is_client_side_error = value
    #IsResolved
    @property
    def is_resolved(self):
        return self.error_log.is_resolved
    @is_resolved.setter
    def is_resolved(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_resolved must be a boolean.")
        self.error_log.is_resolved = value
    #PacID
    #Url
    @property
    def url(self):
        return self.error_log.url
    @url.setter
    def url(self, value):
        assert isinstance(value, str), "url must be a string"
        self.error_log.url = value

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
            error_log_manager = ErrorLogManager(self.session)
            error_log_obj = await error_log_manager.get_by_id(error_log_id)
            self.error_log = error_log_obj
        if code and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self.session)
            error_log_obj = await error_log_manager.get_by_code(code)
            self.error_log = error_log_obj
        if error_log_obj_instance and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self.session)
            error_log_obj = await error_log_manager.get_by_id(error_log_obj_instance.error_log_id)
            self.error_log = error_log_obj
        if json_data and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self.session)
            self.error_log = error_log_manager.from_json(json_data)
        if error_log_dict and self.error_log.error_log_id is None:
            error_log_manager = ErrorLogManager(self.session)
            self.error_log = error_log_manager.from_dict(error_log_dict)

    async def refresh(self):
        error_log_manager = ErrorLogManager(self.session)
        self.error_log = await error_log_manager.refresh(self.error_log)
    def to_dict(self):
        error_log_manager = ErrorLogManager(self.session)
        return error_log_manager.to_dict(self.error_log)
    def to_json(self):
        error_log_manager = ErrorLogManager(self.session)
        return error_log_manager.to_json(self.error_log)
    async def save(self):
        if self.error_log.error_log_id > 0:
            error_log_manager = ErrorLogManager(self.session)
            self.error_log = await error_log_manager.update(self.error_log)
        if self.error_log.error_log_id == 0:
            error_log_manager = ErrorLogManager(self.session)
            self.error_log = await error_log_manager.add(self.error_log)
    async def delete(self):
        if self.error_log.error_log_id > 0:
            error_log_manager = ErrorLogManager(self.session)
            self.error_log = await error_log_manager.delete(self.error_log.error_log_id)
    def get_error_log_obj(self) -> ErrorLog:
        return self.error_log
    def is_equal(self,error_log:ErrorLog) -> ErrorLog:
        error_log_manager = ErrorLogManager(self.session)
        my_error_log = self.get_error_log_obj()
        return error_log_manager.is_equal(error_log, my_error_log)

    #browserCode,
    #contextCode,
    #createdUTCDateTime
    #description,
    #isClientSideError,
    #isResolved,
    #PacID
    async def get_pac_id_rel_bus_obj(self) -> PacBusObj:
        pac_bus_obj = PacBusObj(self.session)
        await pac_bus_obj.load(pac_id=self.error_log.pac_id)
        return pac_bus_obj
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
    async def get_parent_obj(self) -> PacBusObj:
        return await self.get_pac_id_rel_bus_obj()
    #url,

