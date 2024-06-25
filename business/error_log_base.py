# business/error_log_base.py

"""
This module contains the ErrorLogBaseBusObj class,
which represents the base business object for a ErrorLog.
"""

from decimal import Decimal
import random
from typing import Optional
import uuid
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
    Exception raised when the
    ErrorLog object
    is not initialized properly.
    """


class ErrorLogBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a ErrorLog.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        error_log: Optional[ErrorLog] = None
    ):
        """
        Initializes a new instance of the
        ErrorLogBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if error_log is None:
            error_log = ErrorLog()

        self._session_context = session_context

        self.error_log = error_log

    @property
    def error_log_id(self) -> int:
        """
        Get the error_log ID from the
        ErrorLog object.

        :return: The error_log ID.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.error_log_id

    # code
    @property
    def code(self):
        """
        Get the code from the
        ErrorLog object.

        :return: The code.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the ErrorLog object.

        :param value: The code value.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        :raises ValueError: If the code is not a UUID.
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
        Get the last change code from the
        ErrorLog object.

        :return: The last change code.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        ErrorLog object.

        :param value: The last change code value.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        :raises ValueError: If the last change code is not an integer.
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
        Get the insert user ID from the
        ErrorLog object.

        :return: The insert user ID.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        ErrorLog object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.error_log.insert_user_id = value

    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        ErrorLog object.

        :return: The last update user ID.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        ErrorLog object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.error_log.last_update_user_id = value

    # browserCode

    @property
    def browser_code(self):
        """
        Returns the value of the
        some unique identifier for the
        error_log.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        Returns:
            The value of the some unique identifier for the
            error_log.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.browser_code

    @browser_code.setter
    def browser_code(self, value):
        """
        Sets the value of the
        'browser_code'
        attribute for the
        error_log.

        Args:
            value (uuid.UUID): The UUID value to set for
                'browser_code'.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, uuid.UUID), (
            "browser_code must be a UUID")
        self.error_log.browser_code = value
    # contextCode

    @property
    def context_code(self):
        """
        Returns the value of the
        some unique identifier for the
        error_log.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        Returns:
            The value of the some unique identifier for the
            error_log.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.context_code

    @context_code.setter
    def context_code(self, value):
        """
        Sets the value of the
        'context_code'
        attribute for the
        error_log.

        Args:
            value (uuid.UUID): The UUID value to set for
                'context_code'.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, uuid.UUID), (
            "context_code must be a UUID")
        self.error_log.context_code = value
    # createdUTCDateTime

    @property
    def created_utc_date_time(self):
        """
        Returns the value of
        created_utc_date_time attribute of the
        error_log.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        Returns:
            The value of
            created_utc_date_time
            attribute.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.created_utc_date_time

    @created_utc_date_time.setter
    def created_utc_date_time(self, value):
        """
        Sets the value of
        created_utc_date_time attribute
        for the error_log.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "created_utc_date_time "
            "must be a datetime object")
        self.error_log.created_utc_date_time = value
    # description

    @property
    def description(self):
        """
        Get the Description from the
        ErrorLog object.

        :return: The Description.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
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
        Set the Description for the
        ErrorLog object.

        :param value: The Description value.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "description must be a string"
        self.error_log.description = value
    # isClientSideError

    @property
    def is_client_side_error(self):
        """
        Get the Is Client Side Error flag from the
        ErrorLog object.

        :return: The Is Client Side Error flag.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.is_client_side_error

    @is_client_side_error.setter
    def is_client_side_error(self, value: bool):
        """
        Set the Is Client Side Error flag for the
        ErrorLog object.

        :param value: The Is Client Side Error flag value.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        :raises ValueError: If the Is Client Side Error flag is not a boolean.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_client_side_error must be a boolean.")

        self.error_log.is_client_side_error = value
    # isResolved

    @property
    def is_resolved(self):
        """
        Get the Is Resolved flag from the
        ErrorLog object.

        :return: The Is Resolved flag.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.is_resolved

    @is_resolved.setter
    def is_resolved(self, value: bool):
        """
        Set the Is Resolved flag for the
        ErrorLog object.

        :param value: The Is Resolved flag value.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        :raises ValueError: If the Is Resolved flag is not a boolean.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_resolved must be a boolean.")

        self.error_log.is_resolved = value
    # PacID
    # url

    @property
    def url(self):
        """
        Get the Url from the
        ErrorLog object.

        :return: The Url.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
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
        Set the Url for the
        ErrorLog object.

        :param value: The Url value.
        :raises AttributeError: If the
            ErrorLog object is not initialized.
        :raises AssertionError: If the Url is not a string.
        """

        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "url must be a string"
        self.error_log.url = value
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # PacID
    @property
    def pac_id(self):
        """
        Returns the pac ID
        associated with the
        error_log.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        Returns:
            int: The pac ID of the error_log.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the error_log.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.error_log.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the error_log.

        Raises:
            AttributeError: If the
            error_log is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the error_log.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.pac_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the error_log object.

        Raises:
            AttributeError: If the
                error_log object is not initialized.

        Returns:
            The UTC date and time inserted into the
            error_log object.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        error_log.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.error_log.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the error_log.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the error_log.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the error_log.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                error_log is not initialized.

        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.error_log.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load error_log data
        from JSON string.

        :param json_data: JSON string containing
            error_log data.
        :raises ValueError: If json_data is not a string
            or if no error_log
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        error_log_manager = ErrorLogManager(
            self._session_context)
        self.error_log = await error_log_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load error_log
        data from UUID code.

        :param code: UUID code for loading a specific
            error_log.
        :raises ValueError: If code is not a UUID or if no
            error_log data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        error_log_manager = ErrorLogManager(
            self._session_context)
        error_log_obj = await error_log_manager.get_by_code(
            code)
        self.error_log = error_log_obj

        return self

    async def load_from_id(
        self,
        error_log_id: int
    ):
        """
        Load error_log data from
        error_log ID.

        :param error_log_id: Integer ID for loading a specific
            error_log.
        :raises ValueError: If error_log_id
            is not an integer or
            if no error_log
            data is found.
        """

        if not isinstance(error_log_id, int):
            raise ValueError(
                "error_log_id must be an integer")

        error_log_manager = ErrorLogManager(
            self._session_context)
        error_log_obj = await error_log_manager.get_by_id(
            error_log_id)
        self.error_log = error_log_obj

        return self

    def load_from_obj_instance(
        self,
        error_log_obj_instance: ErrorLog
    ):
        """
        Use the provided
        ErrorLog instance.

        :param error_log_obj_instance: Instance of the
            ErrorLog class.
        :raises ValueError: If error_log_obj_instance
            is not an instance of
            ErrorLog.
        """

        if not isinstance(error_log_obj_instance,
                          ErrorLog):
            raise ValueError(
                "error_log_obj_instance must be an instance of ErrorLog")

        # error_log_manager = ErrorLogManager(
        #     self._session_context)

        # error_log_dict = error_log_manager.to_dict(error_log_obj_instance)

        # self.error_log = error_log_manager.from_dict(error_log_dict)

        self.error_log = error_log_obj_instance

        return self

    async def load_from_dict(
        self,
        error_log_dict: dict
    ):
        """
        Load error_log data
        from dictionary.

        :param error_log_dict: Dictionary containing
            error_log data.
        :raises ValueError: If error_log_dict
            is not a
            dictionary or if no
            error_log data is found.
        """
        if not isinstance(error_log_dict, dict):
            raise ValueError(
                "error_log_dict must be a dictionary")

        error_log_manager = ErrorLogManager(
            self._session_context)

        self.error_log = await error_log_manager.from_dict(
            error_log_dict)

        return self


    def get_session_context(self):
        """
        Returns the session context.

        :return: The session context.
        :rtype: SessionContext
        """
        return self._session_context

    async def refresh(self):
        """
        Refreshes the error_log
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            error_log object.
        """
        error_log_manager = ErrorLogManager(
            self._session_context)
        self.error_log = await error_log_manager.refresh(
            self.error_log)

        return self

    def is_valid(self):
        """
        Check if the error_log
        is valid.

        Returns:
            bool: True if the error_log
                is valid, False otherwise.
        """
        return self.error_log is not None

    def to_dict(self):
        """
        Converts the ErrorLog
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                ErrorLog object.
        """
        error_log_manager = ErrorLogManager(
            self._session_context)
        return error_log_manager.to_dict(
            self.error_log)

    def to_json(self):
        """
        Converts the error_log
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                error_log object.
        """
        error_log_manager = ErrorLogManager(
            self._session_context)
        return error_log_manager.to_json(
            self.error_log)

    async def save(self):
        """
        Saves the error_log object
        to the database.

        If the error_log object
        is not initialized, an AttributeError is raised.
        If the error_log_id
        is greater than 0, the
        error_log is
        updated in the database.
        If the error_log_id is 0,
        the error_log is
        added to the database.

        Returns:
            The updated or added
            error_log object.

        Raises:
            AttributeError: If the error_log
            object is not initialized.
        """
        if not self.error_log:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        error_log_id = self.error_log.error_log_id

        if error_log_id > 0:
            error_log_manager = ErrorLogManager(
                self._session_context)
            self.error_log = await error_log_manager.update(
                self.error_log)

        if error_log_id == 0:
            error_log_manager = ErrorLogManager(
                self._session_context)
            self.error_log = await error_log_manager.add(
                self.error_log)

        return self

    async def delete(self):
        """
        Deletes the error_log
        from the database.

        Raises:
            AttributeError: If the error_log
                is not initialized.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.error_log.error_log_id > 0:
            error_log_manager = ErrorLogManager(
                self._session_context)
            await error_log_manager.delete(
                self.error_log.error_log_id)
            self.error_log = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        error_log object.

        This method generates random values for various
        properties of the error_log
        object

        Returns:
            self: The current instance of the
                ErrorLog class.

        Raises:
            AttributeError: If the error_log
                object is not initialized.
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
        self.error_log.is_client_side_error = (
            random.choice([True, False]))
        self.error_log.is_resolved = (
            random.choice([True, False]))
        # self.error_log.pac_id = random.randint(0, 100)
        self.error_log.url = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))

        return self

    def get_error_log_obj(self) -> ErrorLog:
        """
        Returns the error_log
        object.

        Raises:
            AttributeError: If the error_log
                object is not initialized.

        Returns:
            ErrorLog: The error_log
                object.
        """
        if not self.error_log:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.error_log

    def is_equal(
        self,
        error_log: ErrorLog
    ) -> bool:
        """
        Checks if the current error_log
        is equal to the given error_log.

        Args:
            error_log (ErrorLog): The
                error_log to compare with.

        Returns:
            bool: True if the error_logs
                are equal, False otherwise.
        """
        error_log_manager = ErrorLogManager(
            self._session_context)
        my_error_log = self.get_error_log_obj()
        return error_log_manager.is_equal(
            error_log, my_error_log)
    # browserCode,
    # contextCode,
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID

    async def get_pac_id_rel_obj(self) -> models.Pac:
        """
        Retrieves the related Pac object based
        on the pac_id.

        Returns:
            An instance of the Pac model
            representing the related pac.

        """
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj
    # url,

    def get_obj(self) -> ErrorLog:
        """
        Returns the ErrorLog object.

        :return: The ErrorLog object.
        :rtype: ErrorLog
        """

        return self.error_log

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "error_log"

    def get_id(self) -> int:
        """
        Returns the ID of the error_log.

        :return: The ID of the error_log.
        :rtype: int
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
        Get the name of the parent error_log.

        Returns:
            str: The name of the parent error_log.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the error_log.

        Returns:
            The parent code of the error_log
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        error_log.

        Returns:
            The parent object of the current
            error_log,
            which is an instance of the
            Pac model.
        """
        pac = await self.get_pac_id_rel_obj()

        return pac
    # url,

