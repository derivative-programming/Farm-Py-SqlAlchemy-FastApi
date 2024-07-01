# business/df_maintenance_base.py
# pylint: disable=unused-import

"""
This module contains the
DFMaintenanceBaseBusObj class,
which represents the base
business object for a
DFMaintenance.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import DFMaintenanceManager
from models import DFMaintenance
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DFMaintenance object is not initialized")


class DFMaintenanceInvalidInitError(Exception):
    """
    Exception raised when the
    DFMaintenance object
    is not initialized properly.
    """


class DFMaintenanceBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a DFMaintenance.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        df_maintenance: Optional[DFMaintenance] = None
    ):
        """
        Initializes a new instance of the
        DFMaintenanceBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if df_maintenance is None:
            df_maintenance = DFMaintenance()

        self._session_context = session_context

        self.df_maintenance = df_maintenance

    @property
    def df_maintenance_id(self) -> int:
        """
        Get the df_maintenance ID from the
        DFMaintenance object.

        :return: The df_maintenance ID.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.df_maintenance_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        DFMaintenance object.

        :return: The code.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the DFMaintenance object.

        :param value: The code value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.df_maintenance.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        DFMaintenance object.

        :return: The last change code.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        DFMaintenance object.

        :param value: The last change code value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.df_maintenance.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        DFMaintenance object.

        :return: The insert user ID.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        DFMaintenance object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.df_maintenance.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        DFMaintenance object.

        :return: The last update user ID.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        DFMaintenance object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.df_maintenance.last_update_user_id = value

    # isPaused

    @property
    def is_paused(self):
        """
        Get the Is Paused flag from the
        DFMaintenance object.

        :return: The Is Paused flag.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.is_paused

    @is_paused.setter
    def is_paused(self, value: bool):
        """
        Set the Is Paused flag for the
        DFMaintenance object.

        :param value: The Is Paused flag value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises ValueError: If the Is Paused flag is not a boolean.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_paused must be a boolean.")

        self.df_maintenance.is_paused = value
    # isScheduledDFProcessRequestCompleted

    @property
    def is_scheduled_df_process_request_completed(self):
        """
        Get the Is Scheduled DF Process Request Completed flag from the
        DFMaintenance object.

        :return: The Is Scheduled DF Process Request Completed flag.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.is_scheduled_df_process_request_completed

    @is_scheduled_df_process_request_completed.setter
    def is_scheduled_df_process_request_completed(self, value: bool):
        """
        Set the Is Scheduled DF Process Request Completed flag for the
        DFMaintenance object.

        :param value: The Is Scheduled DF Process Request Completed flag value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises ValueError: If the Is Scheduled DF Process Request Completed flag is not a boolean.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_scheduled_df_process_request_completed must be a boolean.")

        self.df_maintenance.is_scheduled_df_process_request_completed = value
    # isScheduledDFProcessRequestStarted

    @property
    def is_scheduled_df_process_request_started(self):
        """
        Get the Is Scheduled DF Process Request Started flag from the
        DFMaintenance object.

        :return: The Is Scheduled DF Process Request Started flag.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.is_scheduled_df_process_request_started

    @is_scheduled_df_process_request_started.setter
    def is_scheduled_df_process_request_started(self, value: bool):
        """
        Set the Is Scheduled DF Process Request Started flag for the
        DFMaintenance object.

        :param value: The Is Scheduled DF Process Request Started flag value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises ValueError: If the Is Scheduled DF Process Request Started flag is not a boolean.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_scheduled_df_process_request_started must be a boolean.")

        self.df_maintenance.is_scheduled_df_process_request_started = value
    # lastScheduledDFProcessRequestUTCDateTime

    @property
    def last_scheduled_df_process_request_utc_date_time(self):
        """
        Returns the value of
        last_scheduled_df_process_request_utc_date_time attribute of the
        df_maintenance.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        Returns:
            The value of
            last_scheduled_df_process_request_utc_date_time
            attribute.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.last_scheduled_df_process_request_utc_date_time

    @last_scheduled_df_process_request_utc_date_time.setter
    def last_scheduled_df_process_request_utc_date_time(self, value):
        """
        Sets the value of
        last_scheduled_df_process_request_utc_date_time attribute
        for the df_maintenance.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "last_scheduled_df_process_request_utc_date_time "
            "must be a datetime object")
        self.df_maintenance.last_scheduled_df_process_request_utc_date_time = value
    # nextScheduledDFProcessRequestUTCDateTime

    @property
    def next_scheduled_df_process_request_utc_date_time(self):
        """
        Returns the value of
        next_scheduled_df_process_request_utc_date_time attribute of the
        df_maintenance.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        Returns:
            The value of
            next_scheduled_df_process_request_utc_date_time
            attribute.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.next_scheduled_df_process_request_utc_date_time

    @next_scheduled_df_process_request_utc_date_time.setter
    def next_scheduled_df_process_request_utc_date_time(self, value):
        """
        Sets the value of
        next_scheduled_df_process_request_utc_date_time attribute
        for the df_maintenance.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "next_scheduled_df_process_request_utc_date_time "
            "must be a datetime object")
        self.df_maintenance.next_scheduled_df_process_request_utc_date_time = value
    # PacID
    # pausedByUsername

    @property
    def paused_by_username(self):
        """
        Get the Paused By Username from the
        DFMaintenance object.

        :return: The Paused By Username.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.df_maintenance.paused_by_username is None:
            return ""

        return self.df_maintenance.paused_by_username

    @paused_by_username.setter
    def paused_by_username(self, value):
        """
        Set the Paused By Username for the
        DFMaintenance object.

        :param value: The Paused By Username value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises AssertionError: If the Paused By Username is not a string.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "paused_by_username must be a string"
        self.df_maintenance.paused_by_username = value
    # pausedUTCDateTime

    @property
    def paused_utc_date_time(self):
        """
        Returns the value of
        paused_utc_date_time attribute of the
        df_maintenance.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        Returns:
            The value of
            paused_utc_date_time
            attribute.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.paused_utc_date_time

    @paused_utc_date_time.setter
    def paused_utc_date_time(self, value):
        """
        Sets the value of
        paused_utc_date_time attribute
        for the df_maintenance.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "paused_utc_date_time "
            "must be a datetime object")
        self.df_maintenance.paused_utc_date_time = value
    # scheduledDFProcessRequestProcessorIdentifier

    @property
    def scheduled_df_process_request_processor_identifier(self):
        """
        Get the Scheduled DF Process Request Processor Identifier from the
        DFMaintenance object.

        :return: The Scheduled DF Process Request Processor Identifier.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.df_maintenance.scheduled_df_process_request_processor_identifier is None:
            return ""

        return self.df_maintenance.scheduled_df_process_request_processor_identifier

    @scheduled_df_process_request_processor_identifier.setter
    def scheduled_df_process_request_processor_identifier(self, value):
        """
        Set the Scheduled DF Process Request Processor Identifier for the
        DFMaintenance object.

        :param value: The Scheduled DF Process Request Processor Identifier value.
        :raises AttributeError: If the
            DFMaintenance object is not initialized.
        :raises AssertionError: If the Scheduled DF Process Request Processor Identifier is not a string.
        """

        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "scheduled_df_process_request_processor_identifier must be a string"
        self.df_maintenance.scheduled_df_process_request_processor_identifier = value
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # PacID
    @property
    def pac_id(self):
        """
        Returns the pac ID
        associated with the
        df_maintenance.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        Returns:
            int: The pac ID of the df_maintenance.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the df_maintenance.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.df_maintenance.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the df_maintenance.

        Raises:
            AttributeError: If the
            df_maintenance is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the df_maintenance.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.pac_code_peek
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal

    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the df_maintenance object.

        Raises:
            AttributeError: If the
                df_maintenance object is not initialized.

        Returns:
            The UTC date and time inserted into the
            df_maintenance object.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        df_maintenance.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.df_maintenance.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the df_maintenance.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the df_maintenance.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the df_maintenance.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                df_maintenance is not initialized.

        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.df_maintenance.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load df_maintenance data
        from JSON string.

        :param json_data: JSON string containing
            df_maintenance data.
        :raises ValueError: If json_data is not a string
            or if no df_maintenance
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        df_maintenance_manager = DFMaintenanceManager(
            self._session_context)
        self.df_maintenance = await \
            df_maintenance_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load df_maintenance
        data from UUID code.

        :param code: UUID code for loading a specific
            df_maintenance.
        :raises ValueError: If code is not a UUID or if no
            df_maintenance data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        df_maintenance_manager = DFMaintenanceManager(
            self._session_context)
        df_maintenance_obj = await df_maintenance_manager.get_by_code(
            code)
        self.df_maintenance = df_maintenance_obj

        return self

    async def load_from_id(
        self,
        df_maintenance_id: int
    ):
        """
        Load df_maintenance data from
        df_maintenance ID.

        :param df_maintenance_id: Integer ID for loading a specific
            df_maintenance.
        :raises ValueError: If df_maintenance_id
            is not an integer or
            if no df_maintenance
            data is found.
        """

        if not isinstance(df_maintenance_id, int):
            raise ValueError(
                "df_maintenance_id must be an integer")

        df_maintenance_manager = DFMaintenanceManager(
            self._session_context)
        df_maintenance_obj = await df_maintenance_manager.get_by_id(
            df_maintenance_id)
        self.df_maintenance = df_maintenance_obj

        return self

    def load_from_obj_instance(
        self,
        df_maintenance_obj_instance: DFMaintenance
    ):
        """
        Use the provided
        DFMaintenance instance.

        :param df_maintenance_obj_instance: Instance of the
            DFMaintenance class.
        :raises ValueError: If df_maintenance_obj_instance
            is not an instance of
            DFMaintenance.
        """

        if not isinstance(df_maintenance_obj_instance,
                          DFMaintenance):
            raise ValueError(
                "df_maintenance_obj_instance must be an "
                "instance of DFMaintenance")

        self.df_maintenance = df_maintenance_obj_instance

        return self

    async def load_from_dict(
        self,
        df_maintenance_dict: dict
    ):
        """
        Load df_maintenance data
        from dictionary.

        :param df_maintenance_dict: Dictionary containing
            df_maintenance data.
        :raises ValueError: If df_maintenance_dict
            is not a
            dictionary or if no
            df_maintenance data is found.
        """
        if not isinstance(df_maintenance_dict, dict):
            raise ValueError(
                "df_maintenance_dict must be a dictionary")

        df_maintenance_manager = DFMaintenanceManager(
            self._session_context)

        self.df_maintenance = await \
            df_maintenance_manager.from_dict(
                df_maintenance_dict)

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
        Refreshes the df_maintenance
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            df_maintenance object.
        """
        df_maintenance_manager = DFMaintenanceManager(
            self._session_context)
        self.df_maintenance = await \
            df_maintenance_manager.refresh(
                self.df_maintenance)

        return self

    def is_valid(self):
        """
        Check if the df_maintenance
        is valid.

        Returns:
            bool: True if the df_maintenance
                is valid, False otherwise.
        """
        return self.df_maintenance is not None

    def to_dict(self):
        """
        Converts the DFMaintenance
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                DFMaintenance object.
        """
        df_maintenance_manager = DFMaintenanceManager(
            self._session_context)
        return df_maintenance_manager.to_dict(
            self.df_maintenance)

    def to_json(self):
        """
        Converts the df_maintenance
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                df_maintenance object.
        """
        df_maintenance_manager = DFMaintenanceManager(
            self._session_context)
        return df_maintenance_manager.to_json(
            self.df_maintenance)

    async def save(self):
        """
        Saves the df_maintenance object
        to the database.

        If the df_maintenance object
        is not initialized, an AttributeError is raised.
        If the df_maintenance_id
        is greater than 0, the
        df_maintenance is
        updated in the database.
        If the df_maintenance_id is 0,
        the df_maintenance is
        added to the database.

        Returns:
            The updated or added
            df_maintenance object.

        Raises:
            AttributeError: If the df_maintenance
            object is not initialized.
        """
        if not self.df_maintenance:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        df_maintenance_id = self.df_maintenance.df_maintenance_id

        if df_maintenance_id > 0:
            df_maintenance_manager = DFMaintenanceManager(
                self._session_context)
            self.df_maintenance = await \
                df_maintenance_manager.update(
                    self.df_maintenance)

        if df_maintenance_id == 0:
            df_maintenance_manager = DFMaintenanceManager(
                self._session_context)
            self.df_maintenance = await \
                df_maintenance_manager.add(
                    self.df_maintenance)

        return self

    async def delete(self):
        """
        Deletes the df_maintenance
        from the database.

        Raises:
            AttributeError: If the df_maintenance
                is not initialized.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.df_maintenance.df_maintenance_id > 0:
            df_maintenance_manager = DFMaintenanceManager(
                self._session_context)
            await df_maintenance_manager.delete(
                self.df_maintenance.df_maintenance_id)
            self.df_maintenance = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        df_maintenance object.

        This method generates random values for various
        properties of the df_maintenance
        object

        Returns:
            self: The current instance of the
                DFMaintenance class.

        Raises:
            AttributeError: If the df_maintenance
                object is not initialized.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.df_maintenance.is_paused = (
            random.choice([True, False]))
        self.df_maintenance.is_scheduled_df_process_request_completed = (
            random.choice([True, False]))
        self.df_maintenance.is_scheduled_df_process_request_started = (
            random.choice([True, False]))
        self.df_maintenance.last_scheduled_df_process_request_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.df_maintenance.next_scheduled_df_process_request_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        # self.df_maintenance.pac_id = random.randint(0, 100)
        self.df_maintenance.paused_by_username = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.df_maintenance.paused_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.df_maintenance.scheduled_df_process_request_processor_identifier = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))

        return self

    def get_df_maintenance_obj(self) -> DFMaintenance:
        """
        Returns the df_maintenance
        object.

        Raises:
            AttributeError: If the df_maintenance
                object is not initialized.

        Returns:
            DFMaintenance: The df_maintenance
                object.
        """
        if not self.df_maintenance:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.df_maintenance

    def is_equal(
        self,
        df_maintenance: DFMaintenance
    ) -> bool:
        """
        Checks if the current df_maintenance
        is equal to the given df_maintenance.

        Args:
            df_maintenance (DFMaintenance): The
                df_maintenance to compare with.

        Returns:
            bool: True if the df_maintenances
                are equal, False otherwise.
        """
        df_maintenance_manager = DFMaintenanceManager(
            self._session_context)
        my_df_maintenance = self.get_df_maintenance_obj()
        return df_maintenance_manager.is_equal(
            df_maintenance, my_df_maintenance)

    def get_obj(self) -> DFMaintenance:
        """
        Returns the DFMaintenance object.

        :return: The DFMaintenance object.
        :rtype: DFMaintenance
        """

        return self.df_maintenance

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "df_maintenance"

    def get_id(self) -> int:
        """
        Returns the ID of the df_maintenance.

        :return: The ID of the df_maintenance.
        :rtype: int
        """
        return self.df_maintenance_id
    # isPaused,
    # isScheduledDFProcessRequestCompleted,
    # isScheduledDFProcessRequestStarted,
    # lastScheduledDFProcessRequestUTCDateTime
    # nextScheduledDFProcessRequestUTCDateTime
    # PacID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent df_maintenance.

        Returns:
            str: The name of the parent df_maintenance.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the df_maintenance.

        Returns:
            The parent code of the df_maintenance
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        df_maintenance.

        Returns:
            The parent object of the current
            df_maintenance,
            which is an instance of the
            Pac model.
        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj
    # pausedByUsername,
    # pausedUTCDateTime
    # scheduledDFProcessRequestProcessorIdentifier,
