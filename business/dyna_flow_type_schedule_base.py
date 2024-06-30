# business/dyna_flow_type_schedule_base.py
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTypeScheduleBaseBusObj class,
which represents the base
business object for a
DynaFlowTypeSchedule.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import DynaFlowTypeScheduleManager
from models import DynaFlowTypeSchedule
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DynaFlowTypeSchedule object is not initialized")


class DynaFlowTypeScheduleInvalidInitError(Exception):
    """
    Exception raised when the
    DynaFlowTypeSchedule object
    is not initialized properly.
    """


class DynaFlowTypeScheduleBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a DynaFlowTypeSchedule.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        dyna_flow_type_schedule: Optional[DynaFlowTypeSchedule] = None
    ):
        """
        Initializes a new instance of the
        DynaFlowTypeScheduleBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if dyna_flow_type_schedule is None:
            dyna_flow_type_schedule = DynaFlowTypeSchedule()

        self._session_context = session_context

        self.dyna_flow_type_schedule = dyna_flow_type_schedule

    @property
    def dyna_flow_type_schedule_id(self) -> int:
        """
        Get the dyna_flow_type_schedule ID from the
        DynaFlowTypeSchedule object.

        :return: The dyna_flow_type_schedule ID.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.dyna_flow_type_schedule_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        DynaFlowTypeSchedule object.

        :return: The code.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the DynaFlowTypeSchedule object.

        :param value: The code value.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.dyna_flow_type_schedule.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        DynaFlowTypeSchedule object.

        :return: The last change code.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        DynaFlowTypeSchedule object.

        :param value: The last change code value.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.dyna_flow_type_schedule.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        DynaFlowTypeSchedule object.

        :return: The insert user ID.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        DynaFlowTypeSchedule object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.dyna_flow_type_schedule.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        DynaFlowTypeSchedule object.

        :return: The last update user ID.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        DynaFlowTypeSchedule object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.dyna_flow_type_schedule.last_update_user_id = value

    # DynaFlowTypeID
    # frequencyInHours

    @property
    def frequency_in_hours(self):
        """
        Returns the value of
        frequency_in_hours attribute of the
        dyna_flow_type_schedule.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        Returns:
            int: The value of
                frequency_in_hours attribute.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.frequency_in_hours

    @frequency_in_hours.setter
    def frequency_in_hours(self, value):
        """
        Sets the value of
        frequency_in_hours for the
        dyna_flow_type_schedule.

        Args:
            value (int): The integer value to set for
                frequency_in_hours.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "frequency_in_hours must be an integer")
        self.dyna_flow_type_schedule.frequency_in_hours = value
    # isActive

    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        DynaFlowTypeSchedule object.

        :return: The Is Active flag.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        DynaFlowTypeSchedule object.

        :param value: The Is Active flag value.
        :raises AttributeError: If the
            DynaFlowTypeSchedule object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_active must be a boolean.")

        self.dyna_flow_type_schedule.is_active = value
    # lastUTCDateTime

    @property
    def last_utc_date_time(self):
        """
        Returns the value of
        last_utc_date_time attribute of the
        dyna_flow_type_schedule.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        Returns:
            The value of
            last_utc_date_time
            attribute.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.last_utc_date_time

    @last_utc_date_time.setter
    def last_utc_date_time(self, value):
        """
        Sets the value of
        last_utc_date_time attribute
        for the dyna_flow_type_schedule.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "last_utc_date_time "
            "must be a datetime object")
        self.dyna_flow_type_schedule.last_utc_date_time = value
    # nextUTCDateTime

    @property
    def next_utc_date_time(self):
        """
        Returns the value of
        next_utc_date_time attribute of the
        dyna_flow_type_schedule.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        Returns:
            The value of
            next_utc_date_time
            attribute.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.next_utc_date_time

    @next_utc_date_time.setter
    def next_utc_date_time(self, value):
        """
        Sets the value of
        next_utc_date_time attribute
        for the dyna_flow_type_schedule.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "next_utc_date_time "
            "must be a datetime object")
        self.dyna_flow_type_schedule.next_utc_date_time = value
    # PacID
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
    # DynaFlowTypeID

    @property
    def dyna_flow_type_id(self):
        """
        Returns the dyna_flow_type_id
        of the dyna_flow_type
        associated with the
        dyna_flow_type_schedule.

        Raises:
            AttributeError: If the
            dyna_flow_type_schedule is not initialized.

        Returns:
            int: The foreign key ID of the dyna_flow_type.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.dyna_flow_type_id

    @dyna_flow_type_id.setter
    def dyna_flow_type_id(self, value: int):
        """
        Sets the foreign key ID for the
        dyna_flow_type of the
        dyna_flow_type_schedule.

        Args:
            value (int): The foreign key ID to set.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.
            ValueError: If the value is not an integer.
        """

        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("dyna_flow_type_id must be an integer.")

        self.dyna_flow_type_schedule.dyna_flow_type_id = value

    @property
    def dyna_flow_type_code_peek(self) -> uuid.UUID:
        """
        Returns the dyna_flow_type_id code peek
        of the dyna_flow_type_schedule.

        Raises:
            AttributeError: If the dyna_flow_type_schedule
                is not initialized.

        Returns:
            uuid.UUID: The flvr foreign key code peek
            of the dyna_flow_type_schedule.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.dyna_flow_type_code_peek
    # PacID
    @property
    def pac_id(self):
        """
        Returns the pac ID
        associated with the
        dyna_flow_type_schedule.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        Returns:
            int: The pac ID of the dyna_flow_type_schedule.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the dyna_flow_type_schedule.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.dyna_flow_type_schedule.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the dyna_flow_type_schedule.

        Raises:
            AttributeError: If the
            dyna_flow_type_schedule is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the dyna_flow_type_schedule.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.pac_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the dyna_flow_type_schedule object.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule object is not initialized.

        Returns:
            The UTC date and time inserted into the
            dyna_flow_type_schedule object.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        dyna_flow_type_schedule.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.dyna_flow_type_schedule.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the dyna_flow_type_schedule.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the dyna_flow_type_schedule.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the dyna_flow_type_schedule.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                dyna_flow_type_schedule is not initialized.

        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.dyna_flow_type_schedule.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load dyna_flow_type_schedule data
        from JSON string.

        :param json_data: JSON string containing
            dyna_flow_type_schedule data.
        :raises ValueError: If json_data is not a string
            or if no dyna_flow_type_schedule
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
            self._session_context)
        self.dyna_flow_type_schedule = await \
            dyna_flow_type_schedule_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load dyna_flow_type_schedule
        data from UUID code.

        :param code: UUID code for loading a specific
            dyna_flow_type_schedule.
        :raises ValueError: If code is not a UUID or if no
            dyna_flow_type_schedule data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
            self._session_context)
        dyna_flow_type_schedule_obj = await dyna_flow_type_schedule_manager.get_by_code(
            code)
        self.dyna_flow_type_schedule = dyna_flow_type_schedule_obj

        return self

    async def load_from_id(
        self,
        dyna_flow_type_schedule_id: int
    ):
        """
        Load dyna_flow_type_schedule data from
        dyna_flow_type_schedule ID.

        :param dyna_flow_type_schedule_id: Integer ID for loading a specific
            dyna_flow_type_schedule.
        :raises ValueError: If dyna_flow_type_schedule_id
            is not an integer or
            if no dyna_flow_type_schedule
            data is found.
        """

        if not isinstance(dyna_flow_type_schedule_id, int):
            raise ValueError(
                "dyna_flow_type_schedule_id must be an integer")

        dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
            self._session_context)
        dyna_flow_type_schedule_obj = await dyna_flow_type_schedule_manager.get_by_id(
            dyna_flow_type_schedule_id)
        self.dyna_flow_type_schedule = dyna_flow_type_schedule_obj

        return self

    def load_from_obj_instance(
        self,
        dyna_flow_type_schedule_obj_instance: DynaFlowTypeSchedule
    ):
        """
        Use the provided
        DynaFlowTypeSchedule instance.

        :param dyna_flow_type_schedule_obj_instance: Instance of the
            DynaFlowTypeSchedule class.
        :raises ValueError: If dyna_flow_type_schedule_obj_instance
            is not an instance of
            DynaFlowTypeSchedule.
        """

        if not isinstance(dyna_flow_type_schedule_obj_instance,
                          DynaFlowTypeSchedule):
            raise ValueError(
                "dyna_flow_type_schedule_obj_instance must be an "
                "instance of DynaFlowTypeSchedule")

        self.dyna_flow_type_schedule = dyna_flow_type_schedule_obj_instance

        return self

    async def load_from_dict(
        self,
        dyna_flow_type_schedule_dict: dict
    ):
        """
        Load dyna_flow_type_schedule data
        from dictionary.

        :param dyna_flow_type_schedule_dict: Dictionary containing
            dyna_flow_type_schedule data.
        :raises ValueError: If dyna_flow_type_schedule_dict
            is not a
            dictionary or if no
            dyna_flow_type_schedule data is found.
        """
        if not isinstance(dyna_flow_type_schedule_dict, dict):
            raise ValueError(
                "dyna_flow_type_schedule_dict must be a dictionary")

        dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
            self._session_context)

        self.dyna_flow_type_schedule = await \
            dyna_flow_type_schedule_manager.from_dict(
                dyna_flow_type_schedule_dict)

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
        Refreshes the dyna_flow_type_schedule
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            dyna_flow_type_schedule object.
        """
        dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
            self._session_context)
        self.dyna_flow_type_schedule = await \
            dyna_flow_type_schedule_manager.refresh(
                self.dyna_flow_type_schedule)

        return self

    def is_valid(self):
        """
        Check if the dyna_flow_type_schedule
        is valid.

        Returns:
            bool: True if the dyna_flow_type_schedule
                is valid, False otherwise.
        """
        return self.dyna_flow_type_schedule is not None

    def to_dict(self):
        """
        Converts the DynaFlowTypeSchedule
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                DynaFlowTypeSchedule object.
        """
        dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
            self._session_context)
        return dyna_flow_type_schedule_manager.to_dict(
            self.dyna_flow_type_schedule)

    def to_json(self):
        """
        Converts the dyna_flow_type_schedule
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                dyna_flow_type_schedule object.
        """
        dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
            self._session_context)
        return dyna_flow_type_schedule_manager.to_json(
            self.dyna_flow_type_schedule)

    async def save(self):
        """
        Saves the dyna_flow_type_schedule object
        to the database.

        If the dyna_flow_type_schedule object
        is not initialized, an AttributeError is raised.
        If the dyna_flow_type_schedule_id
        is greater than 0, the
        dyna_flow_type_schedule is
        updated in the database.
        If the dyna_flow_type_schedule_id is 0,
        the dyna_flow_type_schedule is
        added to the database.

        Returns:
            The updated or added
            dyna_flow_type_schedule object.

        Raises:
            AttributeError: If the dyna_flow_type_schedule
            object is not initialized.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        dyna_flow_type_schedule_id = self.dyna_flow_type_schedule.dyna_flow_type_schedule_id

        if dyna_flow_type_schedule_id > 0:
            dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
                self._session_context)
            self.dyna_flow_type_schedule = await \
                dyna_flow_type_schedule_manager.update(
                    self.dyna_flow_type_schedule)

        if dyna_flow_type_schedule_id == 0:
            dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
                self._session_context)
            self.dyna_flow_type_schedule = await \
                dyna_flow_type_schedule_manager.add(
                    self.dyna_flow_type_schedule)

        return self

    async def delete(self):
        """
        Deletes the dyna_flow_type_schedule
        from the database.

        Raises:
            AttributeError: If the dyna_flow_type_schedule
                is not initialized.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_type_schedule.dyna_flow_type_schedule_id > 0:
            dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
                self._session_context)
            await dyna_flow_type_schedule_manager.delete(
                self.dyna_flow_type_schedule.dyna_flow_type_schedule_id)
            self.dyna_flow_type_schedule = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        dyna_flow_type_schedule object.

        This method generates random values for various
        properties of the dyna_flow_type_schedule
        object

        Returns:
            self: The current instance of the
                DynaFlowTypeSchedule class.

        Raises:
            AttributeError: If the dyna_flow_type_schedule
                object is not initialized.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.dyna_flow_type_schedule.dyna_flow_type_id = random.choice(
            await managers_and_enums.DynaFlowTypeManager(
                self._session_context).get_list()).dyna_flow_type_id
        self.dyna_flow_type_schedule.frequency_in_hours = (
            random.randint(0, 100))
        self.dyna_flow_type_schedule.is_active = (
            random.choice([True, False]))
        self.dyna_flow_type_schedule.last_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.dyna_flow_type_schedule.next_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        # self.dyna_flow_type_schedule.pac_id = random.randint(0, 100)

        return self

    def get_dyna_flow_type_schedule_obj(self) -> DynaFlowTypeSchedule:
        """
        Returns the dyna_flow_type_schedule
        object.

        Raises:
            AttributeError: If the dyna_flow_type_schedule
                object is not initialized.

        Returns:
            DynaFlowTypeSchedule: The dyna_flow_type_schedule
                object.
        """
        if not self.dyna_flow_type_schedule:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_type_schedule

    def is_equal(
        self,
        dyna_flow_type_schedule: DynaFlowTypeSchedule
    ) -> bool:
        """
        Checks if the current dyna_flow_type_schedule
        is equal to the given dyna_flow_type_schedule.

        Args:
            dyna_flow_type_schedule (DynaFlowTypeSchedule): The
                dyna_flow_type_schedule to compare with.

        Returns:
            bool: True if the dyna_flow_type_schedules
                are equal, False otherwise.
        """
        dyna_flow_type_schedule_manager = DynaFlowTypeScheduleManager(
            self._session_context)
        my_dyna_flow_type_schedule = self.get_dyna_flow_type_schedule_obj()
        return dyna_flow_type_schedule_manager.is_equal(
            dyna_flow_type_schedule, my_dyna_flow_type_schedule)

    def get_obj(self) -> DynaFlowTypeSchedule:
        """
        Returns the DynaFlowTypeSchedule object.

        :return: The DynaFlowTypeSchedule object.
        :rtype: DynaFlowTypeSchedule
        """

        return self.dyna_flow_type_schedule

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "dyna_flow_type_schedule"

    def get_id(self) -> int:
        """
        Returns the ID of the dyna_flow_type_schedule.

        :return: The ID of the dyna_flow_type_schedule.
        :rtype: int
        """
        return self.dyna_flow_type_schedule_id
    # DynaFlowTypeID
    # frequencyInHours,
    # isActive,
    # lastUTCDateTime
    # nextUTCDateTime
    # PacID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent dyna_flow_type_schedule.

        Returns:
            str: The name of the parent dyna_flow_type_schedule.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the dyna_flow_type_schedule.

        Returns:
            The parent code of the dyna_flow_type_schedule
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        dyna_flow_type_schedule.

        Returns:
            The parent object of the current
            dyna_flow_type_schedule,
            which is an instance of the
            Pac model.
        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj
