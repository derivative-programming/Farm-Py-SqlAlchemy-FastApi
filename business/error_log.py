# business/error_log.py
"""
    #TODO add comment
"""
from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import ErrorLogManager
from models import ErrorLog
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "ErrorLog object is not initialized")
class ErrorLogInvalidInitError(Exception):
    """
    #TODO add comment
    """
class ErrorLogBusObj(BaseBusObj):
    """
    This class represents the business object for a ErrorLog.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.error_log = ErrorLog()
    @property
    def error_log_id(self) -> int:
        """
        Get the error_log ID from the ErrorLog object.
        :return: The error_log ID.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.error_log_id
    # @error_log_id.setter
    # def error_log_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("error_log_id must be a int.")
    #     self.error_log.error_log_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.error_log.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.error_log.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.error_log.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.error_log:
    #         raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.error_log.last_update_user_id = value
    # def set_prop_last_update_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     self.last_update_user_id = value
    #     return self
# endset
    # browserCode
    @property
    def browser_code(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.browser_code
    @browser_code.setter
    def browser_code(self, value):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, uuid.UUID), (
            "browser_code must be a UUID")
        self.error_log.browser_code = value
    def set_prop_browser_code(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        self.browser_code = value
        return self
    # contextCode
    @property
    def context_code(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.context_code
    @context_code.setter
    def context_code(self, value):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, uuid.UUID), (
            "context_code must be a UUID")
        self.error_log.context_code = value
    def set_prop_context_code(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        self.context_code = value
        return self
    # createdUTCDateTime
    @property
    def created_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.created_utc_date_time
    @created_utc_date_time.setter
    def created_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime), (
            "created_utc_date_time must be a datetime object")
        self.error_log.created_utc_date_time = value
    def set_prop_created_utc_date_time(self, value: datetime):
        """
        #TODO add comment
        """
        self.created_utc_date_time = value
        return self
    # description
    @property
    def description(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.error_log.description is None:
            return ""
        return self.error_log.description
    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "description must be a string"
        self.error_log.description = value
    def set_prop_description(self, value: str):
        """
        #TODO add comment
        """
        self.description = value
        return self
    # isClientSideError
    @property
    def is_client_side_error(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.is_client_side_error
    @is_client_side_error.setter
    def is_client_side_error(self, value: bool):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_client_side_error must be a boolean.")
        self.error_log.is_client_side_error = value
    def set_prop_is_client_side_error(self, value: bool):
        """
        #TODO add comment
        """
        self.is_client_side_error = value
        return self
    # isResolved
    @property
    def is_resolved(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.is_resolved
    @is_resolved.setter
    def is_resolved(self, value: bool):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_resolved must be a boolean.")
        self.error_log.is_resolved = value
    def set_prop_is_resolved(self, value: bool):
        """
        #TODO add comment
        """
        self.is_resolved = value
        return self
    # PacID
    # url
    @property
    def url(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.error_log.url is None:
            return ""
        return self.error_log.url
    @url.setter
    def url(self, value):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "url must be a string"
        self.error_log.url = value
    def set_prop_url(self, value: str):
        """
        #TODO add comment
        """
        self.url = value
        return self
# endset
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID
    @property
    def pac_id(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.error_log.pac_id = value
    def set_prop_pac_id(self, value: int):
        """
        #TODO add comment
        """
        self.pac_id = value
        return self
    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "pac_code_peek must be a UUID"
    #     self.error_log.pac_code_peek = value
    # url,
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.error_log.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.error_log.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load error_log data from JSON string.
        :param json_data: JSON string containing error_log data.
        :raises ValueError: If json_data is not a string
            or if no error_log data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        error_log_manager = ErrorLogManager(self._session_context)
        self.error_log = error_log_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load error_log data from UUID code.
        :param code: UUID code for loading a specific error_log.
        :raises ValueError: If code is not a UUID or if no error_log data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        error_log_manager = ErrorLogManager(self._session_context)
        error_log_obj = await error_log_manager.get_by_code(code)
        self.error_log = error_log_obj
        return self
    async def load_from_id(
        self,
        error_log_id: int
    ):
        """
        Load error_log data from error_log ID.
        :param error_log_id: Integer ID for loading a specific error_log.
        :raises ValueError: If error_log_id is not an integer or
            if no error_log data is found.
        """
        if not isinstance(error_log_id, int):
            raise ValueError("error_log_id must be an integer")
        error_log_manager = ErrorLogManager(self._session_context)
        error_log_obj = await error_log_manager.get_by_id(error_log_id)
        self.error_log = error_log_obj
        return self
    async def load_from_obj_instance(
        self,
        error_log_obj_instance: ErrorLog
    ):
        """
        Use the provided ErrorLog instance.
        :param error_log_obj_instance: Instance of the ErrorLog class.
        :raises ValueError: If error_log_obj_instance is not an instance of ErrorLog.
        """
        if not isinstance(error_log_obj_instance, ErrorLog):
            raise ValueError("error_log_obj_instance must be an instance of ErrorLog")
        error_log_manager = ErrorLogManager(self._session_context)
        error_log_obj_instance_error_log_id = error_log_obj_instance.error_log_id
        error_log_obj = await error_log_manager.get_by_id(
            error_log_obj_instance_error_log_id
        )
        self.error_log = error_log_obj
        return self
    async def load_from_dict(
        self,
        error_log_dict: dict
    ):
        """
        Load error_log data from dictionary.
        :param error_log_dict: Dictionary containing error_log data.
        :raises ValueError: If error_log_dict is not a
            dictionary or if no error_log data is found.
        """
        if not isinstance(error_log_dict, dict):
            raise ValueError("error_log_dict must be a dictionary")
        error_log_manager = ErrorLogManager(self._session_context)
        self.error_log = error_log_manager.from_dict(error_log_dict)
        return self

    def get_session_context(self):
        """
        #TODO add comment
        """
        return self._session_context
    async def refresh(self):
        """
        #TODO add comment
        """
        error_log_manager = ErrorLogManager(self._session_context)
        self.error_log = await error_log_manager.refresh(self.error_log)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return self.error_log is not None
    def to_dict(self):
        """
        #TODO add comment
        """
        error_log_manager = ErrorLogManager(self._session_context)
        return error_log_manager.to_dict(self.error_log)
    def to_json(self):
        """
        #TODO add comment
        """
        error_log_manager = ErrorLogManager(self._session_context)
        return error_log_manager.to_json(self.error_log)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        if self.error_log.error_log_id > 0:
            error_log_manager = ErrorLogManager(self._session_context)
            self.error_log = await error_log_manager.update(self.error_log)
        if self.error_log.error_log_id == 0:
            error_log_manager = ErrorLogManager(self._session_context)
            self.error_log = await error_log_manager.add(self.error_log)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.error_log.error_log_id > 0:
            error_log_manager = ErrorLogManager(self._session_context)
            await error_log_manager.delete(self.error_log.error_log_id)
            self.error_log = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.error_log.browser_code = uuid.uuid4()
        self.error_log.context_code = uuid.uuid4()
        self.error_log.created_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.error_log.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.error_log.is_client_side_error = random.choice([True, False])
        self.error_log.is_resolved = random.choice([True, False])
        # self.error_log.pac_id = random.randint(0, 100)
        self.error_log.url = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
# endset
        return self
    def get_error_log_obj(self) -> ErrorLog:
        """
        #TODO add comment
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.error_log
    def is_equal(self, error_log: ErrorLog) -> bool:
        """
        #TODO add comment
        """
        error_log_manager = ErrorLogManager(self._session_context)
        my_error_log = self.get_error_log_obj()
        return error_log_manager.is_equal(error_log, my_error_log)
# endset
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        """
        #TODO add comment
        """
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj
    # url,
# endset
    def get_obj(self) -> ErrorLog:
        """
        #TODO add comment
        """
        return self.error_log
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "error_log"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.error_log_id
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID
    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.pac_code_peek
    async def get_parent_obj(self) -> models.Pac:
        """
        #TODO add comment
        """
        return self.get_pac_id_rel_obj()
    # url,
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[ErrorLog]
    ):
        """
        #TODO add comment
        """
        result = list()
        for error_log in obj_list:
            error_log_bus_obj = ErrorLogBusObj(session_context)
            await error_log_bus_obj.load_from_obj_instance(error_log)
            result.append(error_log_bus_obj)
        return result

